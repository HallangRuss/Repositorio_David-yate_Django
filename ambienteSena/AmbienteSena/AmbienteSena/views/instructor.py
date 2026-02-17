from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from AmbienteSena.Models.instructor import Instructor

# Función para validar datos del instructor
def validar_datos(request):
    nombre = request.POST.get('nombre', '').strip()
    area = request.POST.get('area', '').strip()
    celular = request.POST.get('celular', '').strip()
    cedula = request.POST.get('cedula', '').strip()

    # Validación de campos vacíos
    if not (nombre and area and celular and cedula):
        return False, 'Todos los campos son obligatorios'

    # Validación de límites y formatos
    if len(nombre) > 100:
        return False, 'El nombre no puede superar los 100 caracteres'
    if len(area) > 50:
        return False, 'El área no puede superar los 50 caracteres'
    if not celular.isdigit() or len(celular) != 10:
        return False, 'El celular debe contener 10 dígitos numéricos'
    if not cedula.isdigit() or len(cedula) not in [8, 10]:
        return False, 'La cédula debe contener 8 o 10 dígitos numéricos'

    return True, {'nombre': nombre, 'area': area, 'celular': celular, 'cedula': cedula}


# Registrar Instructor
def RegistrarInstructor(request):
    if request.method == 'POST':
        valido, datos = validar_datos(request)
        if not valido:
            messages.error(request, datos)
            return redirect('/Instructores/RegistrarInstructor')

        try:
            instructor = Instructor(
                NombreCompleto=datos['nombre'],
                Area=datos['area'],
                Celular=datos['celular'],
                Cedula=datos['cedula']
            )
            instructor.save()
            messages.success(request, 'Instructor registrado correctamente')
        except Exception as e:
            messages.error(request, f'Ocurrió un error al registrar: {e}')
        return redirect('/Instructores/ListarInstructores')

    return render(request, 'Instructores/RegistrarInstructor.html')


# Listar Instructores
def ListarInstructores(request):
    try:
        listadoInstructores = Instructor.objects.all().order_by('-id')
    except Exception as e:
        messages.error(request, f'Ocurrió un error al listar: {e}')
        listadoInstructores = []

    return render(request, 'Instructores/ListarInstructores.html', {
        'listadoInstructores': listadoInstructores
    })


# Eliminar Instructor
def EliminarInstructor(request):
    if request.method == 'POST':
        try:
            instructor = Instructor.objects.get(id=request.POST.get('id'))
            instructor.delete()
            messages.success(request, 'Instructor eliminado correctamente')
        except Exception as e:
            messages.error(request, f'Ocurrió un error al eliminar: {e}')
    return redirect('/Instructores/ListarInstructores')


# Actualizar Instructor
def ActualizarInstructor(request, id_instructor):
    instructor = get_object_or_404(Instructor, id=id_instructor)

    if request.method == 'POST':
        valido, datos = validar_datos(request)
        if not valido:
            messages.error(request, datos)
            return redirect(f'/Instructores/ActualizarInstructor/{id_instructor}')

        try:
            instructor.NombreCompleto = datos['nombre']
            instructor.Area = datos['area']
            instructor.Celular = datos['celular']
            instructor.Cedula = datos['cedula']
            instructor.save()
            messages.success(request, 'Instructor actualizado correctamente')
        except Exception as e:
            messages.error(request, f'Ocurrió un error al actualizar: {e}')

        return redirect('/Instructores/ListarInstructores')

    return render(request, 'Instructores/ActualizarInstructor.html', {
        'instructor': instructor
    })
