from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.core.serializers import serialize # Importante para la API
from django.http import HttpResponse # Importante para la API
from ..Models.cuentadante import Cuentadante
from ..Models.instructor import Instructor
from ..Models.ambiente import Ambiente 

def RegistrarCuentadante(request):
    if request.method == 'POST':
        instructor_id = request.POST.get('instructor') 
        ambiente_id = request.POST.get('ambiente')
        observacion = request.POST.get('observacion')
    
        try:
            instructor = get_object_or_404(Instructor, id=instructor_id)
            ambiente = get_object_or_404(Ambiente, id=ambiente_id)
            
            Cuentadante.objects.create(
                instructor=instructor,
                ambiente=ambiente,
                observacion=observacion
            )
            
            messages.success(request, 'Asignación de ambiente registrada correctamente.')
            return redirect('/Cuentadante/RegistrarCuentadante')

        except Exception as e:
            messages.error(request, f'Error al registrar: {e}')
            return redirect('/Cuentadante/RegistrarCuentadante')

    else:
        listadoInstructores = Instructor.objects.all().order_by('NombreCompleto')
        listadoAmbientes = Ambiente.objects.all().order_by('NombreAmbiente')
        
        return render(request, 'Cuentadante/RegistrarCuentadante.html', {
            'instructores': listadoInstructores, 
            'ambientes': listadoAmbientes 
        })

def ListarCuentadantes(request):
    # Traemos las asignaciones y también instructores/ambientes para el modal
    asignaciones = Cuentadante.objects.all().order_by('-fechaasignacion')
    listadoInstructores = Instructor.objects.all().order_by('NombreCompleto')
    listadoAmbientes = Ambiente.objects.all().order_by('NombreAmbiente')
    
    return render(request, 'Cuentadante/ListarCuentadantes.html', {
        'asignaciones': asignaciones,
        'instructores': listadoInstructores,
        'ambientes': listadoAmbientes
    })

def EliminarCuentadante(request):
    if request.method == 'POST':
        if request.POST.get('id'):
            cuentadante = Cuentadante.objects.get(id=request.POST.get('id'))
            cuentadante.delete()
    return redirect('/Cuentadante/ListarCuentadantes')

def APIConsultarCuentadante(request, id_cuentadante):
    un_cuentadante = Cuentadante.objects.filter(id = id_cuentadante)
    cuentadante_json = serialize('json', un_cuentadante)
    return HttpResponse(cuentadante_json, content_type = 'application/json')