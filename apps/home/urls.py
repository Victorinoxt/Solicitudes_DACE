from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('estudiantes/<int:es_egresado>/', views.lista_estudiantes, name='lista_estudiantes'),
    path('estudiante/nuevo/', views.crear_estudiante, name='crear_estudiante'),
    path('estudiante/<int:pk>/editar/', views.actualizar_estudiante, name='actualizar_estudiante'),
    path('estudiante/<int:pk>/eliminar/', views.eliminar_estudiante, name='eliminar_estudiante'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('exportar_estudiantes/<int:es_egresado>/', views.exportar_estudiantes_csv, name='exportar_estudiantes_csv'),
    path('exportar_estudiantes_pdf/<int:es_egresado>/', views.exportar_estudiantes_pdf, name='exportar_estudiantes_pdf'),
]
