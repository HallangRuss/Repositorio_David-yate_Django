from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from ..Models import Instructor, Ambiente, Ingreso

def RegistrarIngreso(request):
    if request.method == 'POST':
        instructor_id = request.POST.get('instructor')
        ambiente_id = request.POST.get('ambiente')  # solo uno
        observacion = request.POST.get('observacion')

        # Validaciones
        if not instructor_id:
            messages.warning(request, 'Debe seleccionar un instructor.')
            return redirect('/Ingresos/RegistrarIngresos')

        if not ambiente_id:
            messages.warning(request, 'Debe seleccionar un ambiente.')
            return redirect('/Ingresos/RegistrarIngresos')

        if not observacion:
            messages.warning(request, 'La observación es obligatoria.')
            return redirect('/Ingresos/RegistrarIngresos')

        # Obtener objetos
        instructor = get_object_or_404(Instructor, id=instructor_id)
        ambiente = get_object_or_404(Ambiente, id=ambiente_id)

        # Verificar duplicado: mismo instructor y ambiente sin salida
        if Ingreso.objects.filter(instructor=instructor, ambiente=ambiente, fecha_salida__isnull=True).exists():
            messages.warning(
                request,
                f"El instructor {instructor.NombreCompleto} ya tiene asignado el ambiente {ambiente.NombreAmbiente} sin salida."
            )
            return redirect('/Ingresos/RegistrarIngresos')

        # Guardar ingreso
        Ingreso.objects.create(
            instructor=instructor,
            ambiente=ambiente,
            observacion=observacion
        )

        messages.success(request, 'Ingreso registrado correctamente ✅')
        return redirect('/Ingresos/ListarIngresos')

    # GET: cargar instructores y ambientes
    instructores = Instructor.objects.all().order_by('NombreCompleto')
    ambientes = Ambiente.objects.all().order_by('NombreAmbiente')

    return render(request, 'Ingresos/registrarIngresos.html', {
        'instructores': instructores,
        'ambientes': ambientes
    })


def ListarIngreso(request):
    ingresos = Ingreso.objects.select_related('instructor', 'ambiente').all().order_by('-fecha_ingreso')
    return render(request, 'Ingresos/listarIngresos.html', {'ingresos': ingresos})


def MarcarSalida(request, ingreso_id):
    ingreso = get_object_or_404(Ingreso, id=ingreso_id)
    if ingreso.fecha_salida is None:
        ingreso.fecha_salida = timezone.now()
        ingreso.save()
        messages.success(request, f'Salida registrada para {ingreso.instructor.NombreCompleto} ✅')
    else:
        messages.info(request, f'La salida de {ingreso.instructor.NombreCompleto} ya estaba registrada.')
    return redirect('/Ingresos/ListarIngresos')


def APIConsultarIngreso(request, id_ingreso):
    ingreso = Ingreso.objects.filter(id=id_ingreso).values(
        'id',
        'instructor_id',
        'ambiente_id',
        'observacion',
        'fecha_ingreso',
        'fecha_salida'
    ).first()

    if ingreso:
        return JsonResponse([ingreso], safe=False)
    else:
        return JsonResponse([], safe=False)

