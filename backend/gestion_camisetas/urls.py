from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from inventario import views

router = DefaultRouter()
router.register(r'countries', views.CountryViewSet)
router.register(r'temporadas', views.TemporadaViewSet)
router.register(r'equipos', views.EquipoViewSet)
router.register(r'proveedores', views.ProveedorViewSet)
router.register(r'modelos', views.ModeloCamisetaViewSet)
router.register(r'variantes', views.VarianteCamisetaViewSet)
router.register(r'compras', views.CompraViewSet)
router.register(r'compras-lineas', views.CompraLineaViewSet)
router.register(r'ventas', views.VentaViewSet)
router.register(r'ventas-lineas', views.VentaLineaViewSet)
router.register(r'stock-mov', views.StockMovimientoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),        # ← aquí
    path('api/', include(router.urls)),
    # Aquí los reportes:
    path('api/reportes/ventas-por-periodo/', views.ventas_por_periodo, name='ventas-por-periodo'),
    path('api/reportes/modelos-mas-vendidos/', views.modelos_mas_vendidos, name='modelos-mas-vendidos'),
    path('api/reportes/stock-actual/', views.stock_actual, name='stock-actual'),
    path('api/reportes/tallas-mas-vendidas/', views.tallas_mas_vendidas, name='tallas-mas-vendidas'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]