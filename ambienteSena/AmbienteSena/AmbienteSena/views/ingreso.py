from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from ..Models.instructor import Instructor
from ..Models.ambiente import Ambiente
from ..Models.ingreso import Ingreso

def RegistrarIngreso(request):
    if request.method == 'POST':
        instructor_id = request.POST.get('instructor')
        ambiente_id = request.POST.get('ambiente')
        observacion = request.POST.get('observacion')
        if not instructor_id or not ambiente_id or not observacion:
            messages.warning(request, 'Todos los campos son obligatorios.')
            return redirect('/Ingresos/RegistrarIngresos')
        instructor = get_object_or_404(Instructor, id=instructor_id)
        ambiente = get_object_or_404(Ambiente, id=ambiente_id)
        Ingreso.objects.create(instructor=instructor, ambiente=ambiente, observacion=observacion)
        messages.success(request, 'Ingreso registrado correctamente')
        return redirect('/Ingresos/ListarIngresos')
    instructores = Instructor.objects.all().order_by('NombreCompleto')
    ambientes = Ambiente.objects.all().order_by('NombreAmbiente')
    return render(request, 'Ingresos/RegistrarIngresos.html', {
        'instructores': instructores,
        'ambientes': ambientes
    })

def ListarIngreso(request):
    ingresos = Ingreso.objects.select_related('instructor', 'ambiente').all().order_by('-fecha_ingreso')
    return render(request, 'Ingresos/ListarIngresos.html', {'ingresos': ingresos})

def MarcarSalida(request, ingreso_id):
    ingreso = get_object_or_404(Ingreso, id=ingreso_id)
    if ingreso.fecha_salida is None:
        ingreso.fecha_salida = timezone.now()
        ingreso.save()
        messages.success(request, 'Salida registrada correctamente')
    return redirect('/Ingresos/ListarIngresos')

def APIConsultarIngreso(request, id_ingreso):
    ingreso = Ingreso.objects.filter(id=id_ingreso).values(
        'id', 'instructor_id', 'ambiente_id', 'observacion', 'fecha_ingreso', 'fecha_salida'
    ).first()
    return JsonResponse([ingreso] if ingreso else [], safe=False)