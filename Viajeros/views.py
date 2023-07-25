from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse, HttpResponseNotFound

from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
# from django.views.generic.list import ListView
import datetime
from django.contrib.auth.decorators import login_required, permission_required
# from django.contrib.auth.views import LoginView


#Definicion de los formularios:
from .forms import EnviarConsultaForm
from .forms import EnviarReservaHotelForm, EnviarReservaRestauranteForm, EnviarReservaExcursionForm, ConsultaReservasForm
from .forms import AltaUsuarioForm
from .models import ReservaExcursion, ReservaRestaurante, Reservas,  Hotel, Excursion, Restaurante, User

from .forms import ModificarDatosForm
from .forms import BusquedaUsuarioForm     #para perfil Admin
from .forms import ReservaHotelForm, ReservaRestauranteForm, ReservaExcursionForm    # forms para perfil Admin



def index(request):
    # hotel = Hotel.objects.all()
    # excursion = Excursion.objects.all()
    # restaurante = Restaurante.objects.all()
    # carousel_images = hotel  # Por ejemplo, se utilizan las imágenes de los hoteles para el carrousel

    # context = {
    #     'carousel_images': carousel_images,
    #     'hotel': hotel,
    #     'excursion': excursion,
    #     'restaurante': restaurante,
    # }

    return render(request, 'Viajeros/index.html')

#####################      Alta de un usuario      ######################
def registro(request):     
    if request.method == "POST":
        alta_usuario_form = AltaUsuarioForm(request.POST)
        if alta_usuario_form.is_valid():
            user = alta_usuario_form.save(commit=False)
            user.save()  #guardamos el usuario
            messages.add_message(request, messages.SUCCESS, 'Usuario dado de alta con éxito', extra_tags="tag1")
            login(request,user)
            messages.add_message(request, messages.SUCCESS, 'Ha iniciado sesion como: ' + alta_usuario_form.cleaned_data.get('username'), extra_tags="tag1")
                              
            return render(request, 'Viajeros/index.html')
    else:
        # GET
        alta_usuario_form = AltaUsuarioForm()
    
    context = {
        'form': alta_usuario_form
    }

    return render(request, 'Viajeros/usuario/registro.html',context) 


############    LOGIN   #####################
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data= request.POST)
        if form.is_valid():
            usuario =form.cleaned_data.get('username')
            contraseña= form.cleaned_data.get('password')
            user= authenticate(username=usuario, password=contraseña)

            if user is not None:
                login(request,user)
                messages.info(request, f"Ha iniciado sesion como: {usuario}")
                return render(request, 'Viajeros/index.html')

    form = AuthenticationForm()
    return render(request, 'Viajeros/usuario/login.html',{"form": form}) 


#####################################################################
# def logout_request(request):
#     logout(request)
#     messages.info(request,"Sesion finalizada")
#     return render(request, 'Viajeros/index.html') 

#####################################################################
@login_required
def mi_cuenta(request):
    usuario = request.user
    datos_usuario = {
        'nombre': usuario.first_name,
        'apellido': usuario.last_name,
        'email': usuario.email,
        
    }
    return render(request, 'Viajeros/usuario/mi_cuenta.html', {'datos_usuario': datos_usuario})



@login_required
def modificar_datos(request):
    usuario = request.user
    if request.method == 'POST':
        form = ModificarDatosForm(request.POST, instance=usuario)

        if form.is_valid():
            form.save()
            messages.success(request, 'Datos actualizados exitosamente.')
            return redirect('mi_cuenta')
    else:
        form = ModificarDatosForm(instance=usuario)

    return render(request, 'Viajeros/usuario/modificar_datos.html', {'form': form})


###########################################################################################
 
# def baja_persona(request):
#     context={}
#     return render(request, 'Viajeros/baja_persona.html', context)

####################  PAGINAS ##########################################

def nosotros(request):
    context={}
    return render(request, 'Viajeros/paginas/nosotros.html', context)


def enviar_consulta(request): 
    
    if request.method == 'POST':
        form = EnviarConsultaForm(request.POST)
        print("post")
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            mensaje = form.cleaned_data['mensaje']
            messages.add_message(request, messages.SUCCESS, 'Tu mensaje ha sido enviado correctamente. Nos pondremos en contacto contigo pronto.', extra_tags="tag1")
            return render(request, 'Viajeros/index.html')
            #return render(request, 'Viajeros/paginas/success.html')
    else:
        print("get")
        form = EnviarConsultaForm()
    return render(request, 'Viajeros/paginas/enviar_consulta.html', {'form': form})


########################## HOTEL  ################################################################

def alojamiento(request):
    hoteles = Hotel.objects.all()
    return render(request, 'Viajeros/paginas/alojamiento.html', {'hoteles': hoteles})


def detalles_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)  #para recuperar el objeto Hotel correspondiente al hotel_id proporcionado
    context = {'hotel': hotel, 'imagen_url': hotel.imagen.url}
   # return render(request, 'Viajeros/paginas/detalles_hotel.html', {'hotel': hotel})
    return render(request, 'Viajeros/paginas/detalles_hotel.html',  context)

# def crear_hotel(request):
#     if request.method == 'POST':
#         form = HotelForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('lista_hoteles')
#     else:
#         form = HotelForm()
    
#     return render(request, 'crear_hotel.html', {'form': form})


#######################################################################

def gastronomia(request):
    context={}
    return render(request, 'Viajeros/paginas/gastronomia.html', context)

def circuito_turistico(request):
    context={}
    return render(request, 'Viajeros/paginas/circuito_turistico.html', context)


def ruta_del_vino(request):
    context={}
    return render(request, 'Viajeros/paginas/ruta_del_vino.html', context)


#########################  RESERVAS  ######################################################################

@login_required
def enviar_reserva_hotel(request):    
    context={}
    if request.method == "POST":       
        form = EnviarReservaHotelForm(request.POST)
        if form.is_valid():
            alta_reserva = form.save(commit=False)
            alta_reserva.usuario= request.user            
            alta_reserva.fecha_registracion= datetime.date.today()
            alta_reserva.save()  #guardamos la reserva
            messages.add_message(request, messages.SUCCESS, 'Reserva enviada con exito', extra_tags="tag1")
            # return render(request, 'Viajeros/index.html', context)
            return render(request, 'Viajeros/reservas/confirmacion_reserva.html')

    else:
        # GET
        form = EnviarReservaHotelForm()
    context = {'form': form}
    return render(request, 'Viajeros/paginas/enviar_reserva_hotel.html', context)



#####################################################################################

@login_required
def enviar_reserva_restaurante(request):    
    context={}
    if request.method == "POST":
        form = EnviarReservaRestauranteForm(request.POST)
        # form = EnviarReservaRestauranteForm(user=request.user) # Pasar el usuario actual al formulario
        if form.is_valid():
            alta_reserva_restaurante = form.save(commit=False)
            alta_reserva_restaurante.usuario= request.user
            alta_reserva_restaurante.Tipo_reserva= "Restaurante"
            alta_reserva_restaurante.fecha_registracion= datetime.date.today()
            alta_reserva_restaurante.save()  #guardamos la reserva
            messages.add_message(request, messages.SUCCESS, 'Reserva enviada con exito', extra_tags="tag1")
            # return render(request, 'Viajeros/index.html', context)
            return render(request, 'Viajeros/reservas/confirmacion_reserva.html')

    else:
        # GET
        form = EnviarReservaRestauranteForm()

    context = {'form': form}
    return render(request, 'Viajeros/paginas/enviar_reserva_restaurante.html', context)


##################################################################################

@login_required
def enviar_reserva_excursion(request):    
    context={}
    if request.method == "POST":
        form = EnviarReservaExcursionForm(request.POST)
        if form.is_valid():
            alta_reserva_excursion = form.save(commit=False)
            alta_reserva_excursion.usuario= request.user
            alta_reserva_excursion.Tipo_reserva= "Excursion"
            alta_reserva_excursion.fecha_registracion= datetime.date.today()
            alta_reserva_excursion.save()  #guardamos la reserva
            messages.add_message(request, messages.SUCCESS, 'Reserva enviada con exito', extra_tags="tag1")
            # return render(request, 'Viajeros/index.html', context)
            return render(request, 'Viajeros/reservas/confirmacion_reserva.html')
    else:
        # GET
         form = EnviarReservaExcursionForm()

    context = {'form': form}
    return render(request, 'Viajeros/paginas/enviar_reserva_excursion.html', context)



############################# LISTAR  RESERVAS     ##########################################################

@login_required
def listar_reservas(request):    
    if request.method == 'POST':
        formulario = ConsultaReservasForm(request.POST)
        if formulario.is_valid():
            seleccion = formulario.cleaned_data['seleccion']
            listado_hotel = Reservas.objects.filter(usuario=request.user) # reservas de hotel
            listado_restaurante = ReservaRestaurante.objects.filter(usuario=request.user) # reservas de restaurante
            listado_excursion = ReservaExcursion.objects.filter(usuario=request.user) # reservas de excursion


            if seleccion == 'hotel':

                resultado = 'hotel'
            elif seleccion == 'restaurante':

                resultado = 'restaurante'
            elif seleccion == 'excursion':

                resultado = 'excursion'
            elif seleccion == 'todo':
                resultado = 'todo'
            
            context ={
                'listado_hotel' : listado_hotel,
                'listado_restaurante': listado_restaurante,
                'listado_excursion': listado_excursion,
                'formulario': formulario ,
                'resultado': resultado,
            }

            return render(request, 'Viajeros/reservas/mis_reservas.html', context )  #{'formulario': formulario, 'resultado': resultado, }
    else:
        formulario = ConsultaReservasForm()
        
    return render(request, 'Viajeros/reservas/mis_reservas.html', {'formulario': formulario})




################  Modificar reservas   ##################################################

@login_required
def modificar_reserva(request, reserva_id):   # modificar reservas de Hotel
    # reserva = get_object_or_404(Reservas, id=reserva_id, usuario=request.user)
    reserva = get_object_or_404(Reservas, id=reserva_id)
    
    if request.method == 'POST':
        # form = ReservaForm(request.POST, instance=reserva)
        form = EnviarReservaHotelForm(request.POST, instance=reserva)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Reserva modificada con exito', extra_tags="tag1")
            # return redirect('detalle_reserva', id=reserva_id)
            # return redirect('index')
            return render(request, 'Viajeros/reservas/confirmacion_reserva.html')
    else:
        # form = ReservaForm(instance=reserva)
        form = EnviarReservaHotelForm(instance=reserva)
    
    return render(request, 'Viajeros/reservas/modificar_reserva.html', {'form': form})


@login_required
def modificar_reserva_restaurante(request, reserva_id):   # modificar reservas de restaurante
    # reserva = get_object_or_404(ReservaRestaurante, id=reserva_id, usuario=request.user)
    reserva = get_object_or_404(ReservaRestaurante, id=reserva_id)
    
    if request.method == 'POST':
        # form = ReservaRestauranteForm(request.POST, instance=reserva)
        form =EnviarReservaRestauranteForm(request.POST, instance=reserva)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Reserva modificada con exito', extra_tags="tag1")
            # return redirect('detalle_reserva', id=reserva_id)
            # return redirect('index')
            return render(request, 'Viajeros/reservas/confirmacion_reserva.html')
    else:
        # form = ReservaRestauranteForm(instance=reserva)
        form = EnviarReservaRestauranteForm(instance=reserva)
    
    return render(request, 'Viajeros/reservas/modificar_reserva.html', {'form': form})


@login_required
def modificar_reserva_excursion(request, reserva_id):   # modificar reservas de restaurante
    # reserva = get_object_or_404(ReservaExcursion, id=reserva_id, usuario=request.user)
    reserva = get_object_or_404(ReservaExcursion, id=reserva_id)
    
    if request.method == 'POST':
        # form = ReservaExcursionForm(request.POST, instance=reserva)
        form =EnviarReservaExcursionForm(request.POST, instance=reserva)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Reserva modificada con exito', extra_tags="tag1")
            # return redirect('detalle_reserva', id=reserva_id)
            # return redirect('index')
            return render(request, 'Viajeros/reservas/confirmacion_reserva.html')
    else:
        # form = ReservaExcursionForm(instance=reserva)
        form = EnviarReservaExcursionForm(instance=reserva)
    
    return render(request, 'Viajeros/reservas/modificar_reserva.html', {'form': form})


##################  Eliminar Reservas  ####################################################

# @login_required
@permission_required('Viajeros.delete_hotel')
def eliminar_reserva(request, reserva_id):    # eliminar reservas de hotel
    reserva = get_object_or_404(Reservas, pk=reserva_id)
    
    if request.method == 'POST':
        # Eliminar la reserva
        reserva.delete()
        messages.add_message(request, messages.SUCCESS, 'Reserva eliminada con exito', extra_tags="tag1")
        # return redirect('listar_reservas')
        return render(request, 'Viajeros/index.html')
    
    return render(request, 'Viajeros/reservas/eliminar_reserva_hotel.html', {'reserva': reserva})


# @login_required
@permission_required('Viajeros.delete_restaurante')
def eliminar_reserva_restaurante(request, reserva_id):    # eliminar reservas de restaurante
    reserva = get_object_or_404(ReservaRestaurante, pk=reserva_id)
    if request.method == 'POST':
        # Eliminar la reserva
        reserva.delete()
        messages.add_message(request, messages.SUCCESS, 'Reserva eliminada con exito', extra_tags="tag1")
        # return redirect('listar_reservas')
        return render(request, 'Viajeros/index.html')
    
    return render(request, 'Viajeros/reservas/eliminar_reserva_restaurante.html', {'reserva': reserva})



# @login_required
@permission_required('Viajeros.delete_excursion')
def eliminar_reserva_excursion(request, reserva_id):    # eliminar reservas de restaurante
    reserva = get_object_or_404(ReservaExcursion, pk=reserva_id)   
    if request.method == 'POST':
        # Eliminar la reserva
        reserva.delete()
        messages.add_message(request, messages.SUCCESS, 'Reserva eliminada con exito', extra_tags="tag1")
        # return redirect('listar_reservas')
        return render(request, 'Viajeros/index.html')
    
    return render(request, 'Viajeros/reservas/eliminar_reserva_excursion.html', {'reserva': reserva})


###############################################################################################

@login_required
def detalle_reserva(request, reserva_id):
    reserva = get_object_or_404(Reservas, pk=reserva_id)
    return render(request, 'Viajeros/reservas/detalle_reserva.html', {'reserva': reserva})



######################################################################################################
###########################  Perfil  ADMIN     #######################################################

# Busqueda de reservas por usuario
@login_required
def buscar_reservas_admin(request):
    if request.method == 'POST':
        formulario = BusquedaUsuarioForm(request.POST)
        if formulario.is_valid():
            username = formulario.cleaned_data['username']
           # usuario = formulario.cleaned_data['username']
            # try:
            usuario = User.objects.get(username=username)
            reservas_hotel = Reservas.objects.filter(usuario=usuario)# reservas de hotel
            reservas_restaurante = ReservaRestaurante.objects.filter(usuario=usuario) # reservas de restaurante
            reservas_excursion = ReservaExcursion.objects.filter(usuario=usuario) # reservas de excursion

        else:
            reservas_hotel = None
            reservas_restaurante= None
            reservas_excursion= None
    else:
        formulario = BusquedaUsuarioForm()
        reservas_hotel = None
        reservas_restaurante= None
        reservas_excursion= None

    context = {
        'formulario': formulario,
        'reservas_hotel': reservas_hotel,
        'reservas_restaurante': reservas_restaurante,
        'reservas_excursion': reservas_excursion,
    }
    return render(request, 'Viajeros/reservas/buscar_reservas_admin.html', context)


#####################################################################
@login_required
def listar_reservas_hotel(request):
    reservas = Reservas.objects.all()   # lista todas las reservas de hotel
    # reservas = Reservas.objects.filter(usuario=request.user)
    return render(request, 'Viajeros/reservas/listar_reservas_hotel.html', {'reservas': reservas})


@login_required
def listar_reservas_restaurante(request):
    reservas = ReservaRestaurante.objects.all()   # lista todas las reservas de gastronomia
    # reservas = Reservas.objects.filter(usuario=request.user)
    return render(request, 'Viajeros/reservas/listar_reservas_restaurante.html', {'reservas': reservas})


@login_required
def listar_reservas_excursion(request):
    reservas = ReservaExcursion.objects.all()   # lista todas las reservas de excursion
    # reservas = Reservas.objects.filter(usuario=request.user)
    return render(request, 'Viajeros/reservas/listar_reservas_excursion.html', {'reservas': reservas})



######################################################################
# Crear reserva de hotel 
def reservar_hotel(request):
    if request.method == 'POST':
        form = ReservaHotelForm(request.POST)
        if form.is_valid():  
            usuario =form.cleaned_data.get('usuario')
            print("usuario:", usuario)
            alta_reserva = form.save(commit=False)
            alta_reserva.Tipo_reserva= "Hotel"
            alta_reserva.fecha_registracion= datetime.date.today()
            alta_reserva.save()

            messages.add_message(request, messages.SUCCESS, 'Reserva enviada con exito', extra_tags="tag1")
            # return render(request, 'Viajeros/index.html')
            return render(request, 'Viajeros/reservas/confirmacion_reserva.html')
    else:
        form = ReservaHotelForm()
    return render(request, 'Viajeros/paginas/enviar_reserva_hotel.html', {'form': form})


# Crear reserva de restaurante 
def reservar_restaurante(request):
    if request.method == 'POST':
        form = ReservaRestauranteForm(request.POST)
        if form.is_valid(): 
            usuario =form.cleaned_data.get('usuario')
            print("usuario:", usuario)
            alta_reserva = form.save(commit=False)
            alta_reserva.Tipo_reserva= "Restaurante"
            alta_reserva.fecha_registracion= datetime.date.today()
            alta_reserva.save()    

            messages.add_message(request, messages.SUCCESS, 'Reserva enviada con exito', extra_tags="tag1")
            #return render(request, 'Viajeros/index.html')
            return render(request, 'Viajeros/reservas/confirmacion_reserva.html')
    else:
        form = ReservaRestauranteForm()
    return render(request, 'Viajeros/paginas/enviar_reserva_restaurante.html', {'form': form})


# Crear reserva de excursion
def reservar_excursion(request):
    if request.method == 'POST':
        form = ReservaExcursionForm(request.POST)
        if form.is_valid(): 
            usuario =form.cleaned_data.get('usuario')
            print("usuario:", usuario)
            alta_reserva = form.save(commit=False)
            alta_reserva.Tipo_reserva= "Excursion"
            alta_reserva.fecha_registracion= datetime.date.today()
            alta_reserva.save()    

            messages.add_message(request, messages.SUCCESS, 'Reserva enviada con exito', extra_tags="tag1")
            # return render(request, 'Viajeros/index.html')
            return render(request, 'Viajeros/reservas/confirmacion_reserva.html')
    else:
        form = ReservaExcursionForm()
    return render(request, 'Viajeros/paginas/enviar_reserva_excursion.html', {'form': form})



######################################################################################################



