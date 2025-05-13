# backend/inventario/serializers.py

from rest_framework import serializers
from .models import (
    Country, Temporada,
    Equipo, Proveedor,
    ModeloCamiseta, VarianteCamiseta,
    Compra, CompraLinea,
    Venta, VentaLinea,
    StockMovimiento,
)

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class TemporadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temporada
        fields = '__all__'

class ModeloCamisetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeloCamiseta
        fields = '__all__'

class VarianteCamisetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = VarianteCamiseta
        fields = '__all__'

class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = '__all__'

class CompraLineaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompraLinea
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'

class VentaLineaSerializer(serializers.ModelSerializer):
    class Meta:
        model = VentaLinea
        fields = '__all__'

class StockMovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovimiento
        fields = '__all__'

class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'