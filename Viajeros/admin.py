from django.contrib import admin

from .models import  Hotel, Servicio, Restaurante, Excursion, Reservas, ReservaRestaurante, ReservaExcursion

from django.contrib.auth.models import Group, Permission



# Register your models here.


admin.site.register(Hotel)
#admin.site.register(Servicios)
admin.site.register(Servicio)
admin.site.register(Restaurante)
admin.site.register(Excursion)
admin.site.register(Reservas)
admin.site.register(ReservaRestaurante)
admin.site.register(ReservaExcursion)


# def create_groups():
#     # Crear grupo para hoteles
#     hotel_group, created = Group.objects.get_or_create(name='Hoteles')
#     hotel_group.permissions.add(
#         Permission.objects.get(codename='add_hotel'),
#         Permission.objects.get(codename='change_hotel'),
#         Permission.objects.get(codename='delete_hotel'),
#         Permission.objects.get(codename='view_hotel')
#     )

#     # Crear grupo para restaurantes
#     restaurante_group, created = Group.objects.get_or_create(name='Restaurantes')
#     restaurante_group.permissions.add(
#         Permission.objects.get(codename='add_restaurante'),
#         Permission.objects.get(codename='change_restaurante'),
#         Permission.objects.get(codename='delete_restaurante'),
#         Permission.objects.get(codename='view_restaurante')
#     )

#     # Crear grupo para excursiones
#     excursion_group, created = Group.objects.get_or_create(name='Excursiones')
#     excursion_group.permissions.add(
#         Permission.objects.get(codename='add_excursion'),
#         Permission.objects.get(codename='change_excursion'),
#         Permission.objects.get(codename='delete_excursion'),
#         Permission.objects.get(codename='view_excursion')
#     )

#     # Crear grupo para servicios
#     servicio_group, created = Group.objects.get_or_create(name='Servicios')
#     servicio_group.permissions.add(
#         Permission.objects.get(codename='add_servicio'),
#         Permission.objects.get(codename='change_servicio'),
#         Permission.objects.get(codename='delete_servicio'),
#         Permission.objects.get(codename='view_servicio')
#     )

#     # Crear grupo para reservas
#     reserva_group, created = Group.objects.get_or_create(name='Reservas')
#     reserva_group.permissions.add(
#         Permission.objects.get(codename='add_reserva'),
#         Permission.objects.get(codename='change_reserva'),
#         Permission.objects.get(codename='delete_reserva'),
#         Permission.objects.get(codename='view_reserva')
#     )




