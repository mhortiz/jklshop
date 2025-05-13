from django.contrib import admin
from .models import (
    Country,
    Temporada,
    Equipo,
    Proveedor,
    ModeloCamiseta,
    VarianteCamiseta,
    Compra,
    CompraLinea,
    Venta,
    VentaLinea,
    StockMovimiento,
)

# Registra Country y Temporada primero
admin.site.register(Country)
admin.site.register(Temporada)

# Resto de registros
admin.site.register(Equipo)
admin.site.register(Proveedor)

class ModeloCamisetaAdmin(admin.ModelAdmin):
    list_display = ('equipo', 'version', 'temporada', 'tipo_kit')
    list_filter  = ('version', 'temporada', 'tipo_kit')
    search_fields = ('equipo__nombre',)

admin.site.register(ModeloCamiseta, ModeloCamisetaAdmin)
admin.site.register(VarianteCamiseta)
admin.site.register(Compra)
admin.site.register(CompraLinea)
admin.site.register(Venta)
admin.site.register(VentaLinea)
admin.site.register(StockMovimiento)
