from django.db import models

class Equipo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    pais   = models.CharField(max_length=100)
    tipo   = models.CharField(
        max_length=10,
        choices=[('CLUB','Club'), ('SELECCION','SelecciÃ³n')],
        default='CLUB'
    )
    def __str__(self):
        return f\"{self.nombre} ({self.pais})\"

class Proveedor(models.Model):
    nombre   = models.CharField(max_length=150)
    telefono = models.CharField(max_length=30)
    def __str__(self):
        return self.nombre

class CamisetaModel(models.Model):
    VERSION_CHOICES = [
        ('FAN','Fan'), ('PLAYER','Player'),
        ('RETRO','Retro'), ('INFANTIL','Infantil'), ('KIT','Kit'),
    ]
    TALLA_CHOICES = [
        ('S','S'),('M','M'),('L','L'),('XL','XL'),
        ('XXL','XXL'),('XXXL','XXXL'),
        ('XXXXL','XXXXXL'),('XXXXXL','XXXXXXL'),
    ] + [(f'{i}A', f'{i} aÃ±os') for i in range(2,15)]
    equipo     = models.ForeignKey(Equipo, on_delete=models.PROTECT)
    version    = models.CharField(max_length=10, choices=VERSION_CHOICES)
    temporada  = models.CharField(max_length=9)
    talla      = models.CharField(max_length=6, choices=TALLA_CHOICES)
    imagen_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f\"{self.equipo.nombre} {self.temporada} {self.version} {self.talla}\"
