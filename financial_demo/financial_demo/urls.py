from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from reporteo import views as rv
from checklist import views as cv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',  auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('',        rv.dashboard,      name='dashboard'),
    path('proceso/nuevo/',            rv.proceso_nuevo,    name='proceso_nuevo'),
    path('proceso/<int:pk>/',         rv.proceso_detalle,  name='proceso_detalle'),
    path('proceso/<int:pk>/avanzar/', rv.avanzar_paso,     name='avanzar_paso'),
    path('proceso/<int:pk>/datos/',   rv.captura_datos,    name='captura_datos'),
    path('proceso/<int:pk>/reporte/', rv.reporte_html,     name='reporte_html'),
    path('proceso/<int:pk>/checklist/cuentas/',     cv.checklist_cuentas,     name='checklist_cuentas'),
    path('proceso/<int:pk>/checklist/data/',        cv.checklist_data,        name='checklist_data'),
    path('proceso/<int:pk>/checklist/expedientes/', cv.checklist_expedientes, name='checklist_expedientes'),
]
