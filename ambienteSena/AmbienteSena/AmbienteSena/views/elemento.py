import os
import uuid

from django.core.serializers import serialize
from django.http import HttpResponse

from django.db import DatabaseError
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.files.storage import FileSystemStorage


from AmbienteSena import settings
from AmbienteSena.Models.ambiente import Ambiente
from AmbienteSena.Models.elemento import Elemento


def RegistrarElemento(request):
    ambientes = Ambiente.objects.all().order_by('NombreAmbiente')
    if request.method == 'POST':
        if request.POST.get('nombre') and request.POST.get('tipo') and request.POST.get('observacion') and request.POST.get('ambiente') and request.FILES.get('foto'):
            try:
                ambiente = Ambiente.objects.get(
                    id=request.POST.get('ambiente'))
                elemento = Elemento()
                elemento.Nombre = request.POST.get('nombre')
                elemento.Tipo = request.POST.get('tipo')
                elemento.Observacion = request.POST.get('observacion')
                elemento.ambiente = ambiente
                elemento.Foto = request.FILES.get('foto')

                imagen = FileSystemStorage(
                    location='AmbienteSena/Public/Img/elementos')
                extencion = os.path.splitext(elemento.Foto.name)[1]
                nombrealeatorio = str(uuid.uuid4()) + extencion
                imagen.save(nombrealeatorio, elemento.Foto)
                elemento.Foto = nombrealeatorio
                elemento.save()
                messages.success(request, 'Elemento registrado correctamente')
            except DatabaseError as e:
                messages.error(
                    request, f'Ocurrio un error en la base de datos {e}')
            return redirect('/Elementos/ListarElementos')
        else:
            messages.error(request, 'Todos los campos son obligatorios')
            return render(request, 'Elementos/RegistrarElementos.html', {'ambientes': ambientes})
    else:
        return render(request, 'Elementos/RegistrarElementos.html', {'ambientes': ambientes})


def ListarElementos(request):
    try:
        listadoelementos = Elemento.objects.all().order_by('-id')
        listadoambientes = Ambiente.objects.all().order_by('NombreAmbiente')
        return render(request, 'Elementos/ListarElementos.html', {'listadoelementos': listadoelementos,
                                                                  'ambientes': listadoambientes})
    except DatabaseError as e:
        messages.error(request, f'Ocurrio un error en el sistema {e}')
    return render(request, 'Elementos/ListarElementos.html', {'listadoelementos': listadoelementos})


def APIConsultarElemento(request, idelemento):

    elemento = Elemento.objects.filter(id=idelemento)
    elementojson = serialize('json', elemento)
    return HttpResponse(elementojson, content_type='application/json')

# METODO PARA  ACTUALIZAR ELEMENTO


def ActualizarElemento(request):
    try:
        ambientes = Ambiente.objects.all().order_by('NombreAmbiente')
        if request.method == 'POST':
            if (request.POST.get('nombre') and request.POST.get('tipo')
                    and request.POST.get('observacion') and request.POST.get('ambiente')):

                # Obtener el elemento existente en lugar de crear uno nuevo
                elemento = Elemento.objects.get(
                    id=request.POST.get('idelemento'))
                elemento.Nombre = request.POST.get('nombre')
                elemento.Tipo = request.POST.get('tipo')
                elemento.Observacion = request.POST.get('observacion')
                elemento.ambiente = Ambiente.objects.get(
                    id=request.POST.get('ambiente'))

                if request.FILES.get('foto'):
                    elemento.Foto = request.FILES.get('foto')
                    fs = FileSystemStorage(
                        location='AmbienteSena/Public/Img/elementos')
                    extencion = os.path.splitext(elemento.Foto.name)[1]
                    nombrealeatorio = str(uuid.uuid4()) + extencion
                    fs.save(nombrealeatorio, elemento.Foto)
                    fs.delete(request.POST.get('nombre-foto'))
                    elemento.Foto = nombrealeatorio
                else:
                    elemento.Foto = request.POST.get('nombre-foto')
                elemento.save()
                messages.success(request, 'Elemento actualizado correctamente')
                return redirect('/Elementos/ListarElementos')
            else:
                messages.error(request, 'Error: faltan datos en el formulario')
                return redirect('/Elementos/ListarElementos')
    except DatabaseError as e:
        messages.error(request, f'Ocurrió un error en el sistema: {e}')
        return redirect('/Elementos/ListarElementos')
## METODOPARA ELIMINAR ELEMENTO ##
def EliminarElemento(request):
    if request.method == 'POST':
        if request.POST.get('id'):
            try:
                elemento = Elemento.objects.get(id = request.POST.get('id'))
                ruta_imagen = settings.RUTA_IMAGENES_ELEMENTOS / str(elemento.Foto)
                if ruta_imagen.exists():
                    os.remove(ruta_imagen)
                    elemento.delete()
                    messages.success(request,'Elemento elmininado CorrectAMENTE ')
            except DatabaseError as e:
                messages.error(request,f'Ocurrio Un ERROR EN EL SISTEMA {e}')
            return redirect('/Elementos/ListarElementos')
        else:
            messages.error(request,'ERROR EL ELEMENTO ID QUE DESEA ELIMINAR NO EXISTE EN LA BASE DE DATOS')
            return redirect('/Elementos/ListarElementos')
