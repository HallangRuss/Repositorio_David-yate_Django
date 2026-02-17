from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.core.serializers import serialize
from django.http import HttpResponse

from ..Models.cuentadante import Cuentadante
from ..Models.instructor import Instructor
from ..Models.elemento import Elemento

def RegistrarCuentadante(request):
    if request.method == 'POST':
        instructor_id = request.POST.get('instructor') 
        elementos_id = request.POST.getlist('elementos[]')
        observacion = request.POST.get('observacion')
    
        try:
            # verificar si existe el Instructor
            instructor = get_object_or_404(Instructor, id = instructor_id)
            
            # verificar si el ususario selecciono al menos un elemento 
            if not elementos_id:
                messages.error(request, 'Debe seleccionar al menos un Elemento!!')
                return redirect('/Cuentadante/RegistrarCuentadante')
            # recorrer los elementos
        
            for elemento_id in elementos_id:
                # verificar si existe el elemento_id existe en la base de datos
                elemento = get_object_or_404(Elemento,id=elemento_id)
                # Evitar duplicados
                if Cuentadante.objects.filter(instructor = instructor, elemento = elemento).exists():
                    messages.warning(request,f"El elemento: '{elemento.Nombre}'ya esta asignado al Instructor: '{instructor.NombreCompleto}'")
                    continue
                ##cREAR LOS OBJETOS CUENTADANTE
                cuentadante = Cuentadante(
                    instructor = instructor,
                    elemento = elemento,
                    observacion = observacion
                )
                # GUARDAR LOS DATOS DE LA BASE DE DATOS
                cuentadante.save()
            messages.success(request,'Asignacion del Elemento realizada Correctamente')
            return redirect('/Cuentadante/RegistrarCuentadante')
        except Exception as e:
            messages.error(request,f'Ocurrio un error {e} ')
            return redirect('/Cuentadante/RegistrarCuentadante')
    else:
        listadoInstructores = Instructor.objects.all().order_by('NombreCompleto')
        listadoElementos = Elemento.objects.all().order_by('Nombre')
        return render(request, 'Cuentadante/RegistrarCuentadante.html', {'instructores': listadoInstructores, 'elementos': listadoElementos})

# Listar Cuentadantes
def ListarCuentadantes(request):
    instructores = Instructor.objects.all()
    elementos = Elemento.objects.all()
    listadocuentadantes = Cuentadante.objects.select_related('instructor','elemento').all().order_by('instructor__NombreCompleto','elemento__Nombre')
    return render(request,'Cuentadante/ListarCuentadante.html', {'cuentadantes' : listadocuentadantes})

# Eliminar Cuentadante
def EliminarCuentadante(request):
    if request.method == 'POST':
        if request.POST.get('id'):
            cuentadante = Cuentadante.objects.get(id=request.POST.get('id'))
            cuentadante.delete()
    return redirect('/Cuentadante/ListarCuentadantes')

#definicion de API
def APIConsultarCuentadante(request, id_cuentadante):
    un_cunetadante = Cuentadante.objects.filter(id = id_cuentadante)
    cuentadante_json = serialize('json', un_cunetadante)
    print(cuentadante_json)
    return HttpResponse(cuentadante_json,content_type = 'application/json')