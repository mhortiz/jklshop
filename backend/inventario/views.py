# backend/inventario/views.py

from rest_framework import viewsets
from .models import (
    Country, Temporada,
    Equipo, Proveedor,
    ModeloCamiseta, VarianteCamiseta,
    Compra, CompraLinea,
    Venta, VentaLinea,
    StockMovimiento,
)
from .serializers import (
    CountrySerializer, TemporadaSerializer,
    EquipoSerializer, ProveedorSerializer,
    ModeloCamisetaSerializer, VarianteCamisetaSerializer,
    CompraSerializer, CompraLineaSerializer,
    VentaSerializer, VentaLineaSerializer,
    StockMovimientoSerializer,
)

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class TemporadaViewSet(viewsets.ModelViewSet):
    queryset = Temporada.objects.all()
    serializer_class = TemporadaSerializer

class ModeloCamisetaViewSet(viewsets.ModelViewSet):
    queryset = ModeloCamiseta.objects.all()
    serializer_class = ModeloCamisetaSerializer

class VarianteCamisetaViewSet(viewsets.ModelViewSet):
    queryset = VarianteCamiseta.objects.all()
    serializer_class = VarianteCamisetaSerializer

class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer

class CompraLineaViewSet(viewsets.ModelViewSet):
    queryset = CompraLinea.objects.all()
    serializer_class = CompraLineaSerializer

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

class VentaLineaViewSet(viewsets.ModelViewSet):
    queryset = VentaLinea.objects.all()
    serializer_class = VentaLineaSerializer

class StockMovimientoViewSet(viewsets.ModelViewSet):
    queryset = StockMovimiento.objects.all()
    serializer_class = StockMovimientoSerializer

class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

from django.db.models import Sum, F, Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import VentaLinea, VarianteCamiseta, StockMovimiento
from django.db.models import Sum, F, Q, Value
from django.db.models.functions import Coalesce

@api_view(['GET'])
def ventas_por_periodo(request):
    start = request.query_params.get('start')  # YYYY-MM-DD
    end   = request.query_params.get('end')
    qs = VentaLinea.objects.filter(
            venta__fecha__date__gte=start,
            venta__fecha__date__lte=end
         ).annotate(
            day=F('venta__fecha__date'),
            ingreso=F('cantidad') * F('precio_unitario')
         ).values('day').annotate(
            total_ingreso=Sum('ingreso')
         ).order_by('day')
    return Response(qs)

@api_view(['GET'])
def modelos_mas_vendidos(request):
    qs = VentaLinea.objects.values(
            modelo_id=F('variante__modelo__id'),
            equipo=F('variante__modelo__equipo__nombre'),
            version=F('variante__modelo__version'),
            tipo_kit=F('variante__modelo__tipo_kit')
         ).annotate(
            total_vendido=Sum('cantidad')
         ).order_by('-total_vendido')
    return Response(qs)

@api_view(['GET'])
def stock_actual(request):
    qs = VarianteCamiseta.objects.annotate(
        stock_in=Coalesce(
            Sum('stockmovimiento__cantidad', filter=Q(stockmovimiento__tipo='IN')),
            Value(0)
        ),
        stock_out=Coalesce(
            Sum('stockmovimiento__cantidad', filter=Q(stockmovimiento__tipo='OUT')),
            Value(0)
        )
    ).annotate(
        stock=F('stock_in') - F('stock_out')
    ).values(
        'id',
        'modelo',
        'talla',
        'stock'
    )
    return Response(qs)

@api_view(['GET'])
def tallas_mas_vendidas(request):
    qs = VentaLinea.objects.values(
        talla=F('variante__talla')
    ).annotate(
        total_vendido=Sum('cantidad')
    ).order_by('-total_vendido')

    return Response(qs)