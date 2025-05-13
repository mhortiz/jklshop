from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Country(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name

class Temporada(models.Model):
    start_year = models.PositiveIntegerField()
    end_year   = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = (('start_year','end_year'),)

    def __str__(self):
        if self.end_year:
            return f"{str(self.start_year)[-2:]}-{str(self.end_year)[-2:]}"
        return str(self.start_year)

class Equipo(models.Model):
    nombre  = models.CharField(max_length=100, unique=True)
    country = models.ForeignKey(
        Country, on_delete=models.PROTECT, related_name='equipos'
    )
    tipo    = models.CharField(
        max_length=10,
        choices=[('CLUB','Club'),('SELECCION','Selección')],
        default='CLUB'
    )

    def __str__(self):
        return f"{self.nombre} ({self.country.name})"

class Proveedor(models.Model):
    nombre   = models.CharField(max_length=150)
    telefono = models.CharField(max_length=30)
    def __str__(self):
        return self.nombre

class ModeloCamiseta(models.Model):
    VERSION_CHOICES = [
        ('FAN','Fan'),('PLAYER','Player'),
        ('RETRO','Retro'),('INFANTIL','Infantil'),('KIT','Kit'),
    ]

    KIT_TYPE_CHOICES = [
        ('LOCAL',      'Local'),
        ('VISITANTE',  'Visitante'),
        ('TERCERA',    'Tercera equipación'),
        ('ALTERNATIVA','Alternativa'),
    ]

    equipo     = models.ForeignKey(Equipo, on_delete=models.PROTECT)
    version    = models.CharField(max_length=10, choices=VERSION_CHOICES)
    temporada  = models.ForeignKey(
        Temporada, on_delete=models.PROTECT, related_name='modelos'
    )
    tipo_kit   = models.CharField(
        max_length=12,
        choices=KIT_TYPE_CHOICES,
        default='LOCAL',
        help_text="Local/Visitante/Tercera/Alternativa"
    )
    imagen_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('equipo','version','temporada','tipo_kit')

    def __str__(self):
        return f"{self.equipo.nombre} {self.temporada} {self.get_tipo_kit_display()}"

# 2) Variante por talla de cada diseño
class VarianteCamiseta(models.Model):
    TALLA_CHOICES = [
        ('S','S'),('M','M'),('L','L'),('XL','XL'),
        ('XXL','XXL'),('XXXL','XXXL'),
        ('XXXXL','XXXXXL'),('XXXXXL','XXXXXXL'),
    ] + [(f'{i}A', f'{i} años') for i in range(2,15)]

    modelo = models.ForeignKey(
        ModeloCamiseta, on_delete=models.CASCADE, related_name='variantes'
    )
    talla  = models.CharField(max_length=6, choices=TALLA_CHOICES)

    class Meta:
        unique_together = ('modelo','talla')

    def __str__(self):
        return f"{self.modelo} – {self.talla}"

class Compra(models.Model):
    proveedor     = models.ForeignKey('Proveedor', on_delete=models.PROTECT)
    fecha         = models.DateTimeField(default=timezone.now)
    total_coste   = models.DecimalField(max_digits=10, decimal_places=2)

class CompraLinea(models.Model):
    compra   = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='lineas')
    variante = models.ForeignKey(VarianteCamiseta, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    coste_unitario = models.DecimalField(max_digits=10, decimal_places=2)

class Venta(models.Model):
    fecha         = models.DateTimeField(default=timezone.now)
    total_ingreso = models.DecimalField(max_digits=10, decimal_places=2)

class VentaLinea(models.Model):
    venta    = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='lineas')
    variante = models.ForeignKey(VarianteCamiseta, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

class StockMovimiento(models.Model):
    TIPO_CHOICES = [('IN','IN'),('OUT','OUT')]
    variante  = models.ForeignKey(VarianteCamiseta, on_delete=models.CASCADE)
    tipo      = models.CharField(max_length=3, choices=TIPO_CHOICES)
    cantidad  = models.PositiveIntegerField()
    fecha_mov = models.DateTimeField(default=timezone.now)


class StockMovimiento(models.Model):
    TIPO_CHOICES = [('IN','IN'),('OUT','OUT')]

    variante   = models.ForeignKey(VarianteCamiseta, on_delete=models.CASCADE)
    tipo       = models.CharField(max_length=3, choices=TIPO_CHOICES)
    cantidad   = models.PositiveIntegerField()
    fecha_mov  = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.tipo} {self.cantidad}×{self.camiseta} @ {self.fecha_mov.date()}"


# — Señales para generar movimientos de stock automáticamente — #

@receiver(post_save, sender=CompraLinea)
def entrada_stock(sender, instance, created, **kwargs):
    if created:
        StockMovimiento.objects.create(
            variante=instance.variante,
            tipo='IN',
            cantidad=instance.cantidad,
            fecha_mov=instance.compra.fecha
        )

@receiver(post_save, sender=VentaLinea)
def salida_stock(sender, instance, created, **kwargs):
    if created:
        StockMovimiento.objects.create(
            variante=instance.variante,
            tipo='OUT',
            cantidad=instance.cantidad,
            fecha_mov=instance.venta.fecha
        )