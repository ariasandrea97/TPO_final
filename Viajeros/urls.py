from django.urls import path, re_path , include
from . import views

from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('', views.index, name="index"),

    ### USUARIO ###
    path('registro/', views.registro, name="registro"),
    path('mi_cuenta/', views.mi_cuenta, name="mi_cuenta"),
    path('modificar_datos/', views.modificar_datos, name='modificar_datos'),

    ### PAGINAS ###
    path('nosotros/', views.nosotros, name="nosotros"),
    path('enviar_consulta',views.enviar_consulta, name="enviar_consulta"),
    
    path('alojamiento/', views.alojamiento, name="alojamiento"),
    path('hoteles/<int:hotel_id>/detalles/', views.detalles_hotel, name='detalles_hotel'),

    path('gastronomia/', views.gastronomia, name="gastronomia"),
    path('circuito_turistico/', views.circuito_turistico, name="circuito_turistico"),
    path('ruta_del_vino/', views.ruta_del_vino, name="ruta_del_vino"),
   

    ### RESERVAS  ###
    path('enviar_reserva_hotel',views.enviar_reserva_hotel, name="enviar_reserva_hotel"),
    path('enviar_reserva_restaurante',views.enviar_reserva_restaurante, name="enviar_reserva_restaurante"),
    path('enviar_reserva_excursion',views.enviar_reserva_excursion, name="enviar_reserva_excursion"),
    
    path('listar_reservas/', views.listar_reservas, name="listar_reservas"),
 
    # path('reservas/<int:reserva_id>/detalles/', views.detalle_reserva, name='detalle_reserva'),
    path('reservas/<int:reserva_id>/modificar/', views.modificar_reserva, name='modificar_reserva'),
    path('reservas/<int:reserva_id>/eliminar/', views.eliminar_reserva, name='eliminar_reserva'),

    path('reservas/restaurante/<int:reserva_id>/modificar/', views.modificar_reserva_restaurante, name='modificar_reserva_restaurante'),
    path('reservas/restaurante/<int:reserva_id>/eliminar/', views.eliminar_reserva_restaurante, name='eliminar_reserva_restaurante'),

    path('reservas/excursion/<int:reserva_id>/modificar/', views.modificar_reserva_excursion, name='modificar_reserva_excursion'),
    path('reservas/excursion/<int:reserva_id>/eliminar/', views.eliminar_reserva_excursion, name='eliminar_reserva_excursion'),



    #############   Perfil ADMIN  ###############
    path('admin/buscar_reservas_admin/', views.buscar_reservas_admin, name='buscar_reservas_admin'), 
    path('admin/reservar_hotel/', views.reservar_hotel, name='reservar_hotel'), 
    path('admin/reservar_excursion/', views.reservar_excursion, name='reservar_excursion'), 
    path('admin/reservar_restaurante/', views.reservar_restaurante, name='reservar_restaurante'), 

    path('admin/listar_reservas_hotel/', views.listar_reservas_hotel, name='listar_reservas_hotel'),
    path('admin/listar_reservas_restaurante/', views.listar_reservas_restaurante, name='listar_reservas_restaurante'),
    path('admin/listar_reservas_excursion/', views.listar_reservas_excursion, name='listar_reservas_excursion'),
   
] 