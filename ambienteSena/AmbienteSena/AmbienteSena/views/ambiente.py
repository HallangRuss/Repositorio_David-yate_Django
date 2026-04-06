from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages

def RegistrarAmbiente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        tipo = request.POST.get('tipo')
        observacion = request.POST.get('observacion')
        if nombre and tipo and observacion:
            try:
                with connection.cursor() as cursor:
                    # Usamos el nombre exacto del SP que creamos en PHPMyAdmin
                    cursor.callproc('sp_insertarambiente', [nombre, tipo, observacion])
                messages.success(request, 'Ambiente registrado correctamente')
                return redirect('/Ambientes/ListaAmbientes')
            except Exception as e:
                messages.error(request, f'Error en la base de datos: {e}')
                return redirect('/Ambientes/RegistrarAmbiente')
    
    # IMPORTANTE: Verifica que la carpeta en VS Code se llame 'Ambientes' (con A mayúscula)
    return render(request, 'Ambientes/RegistrarAmbiente.html')

def ListarAmbientes(request):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('sp_listarambientes')
            ambientes = cursor.fetchall()
        return render(request, 'Ambientes/ListaAmbientes.html', {'ambientes': ambientes})
    except Exception as e:
        messages.error(request, f'Error al listar: {e}')
        return render(request, 'Ambientes/ListaAmbientes.html', {'ambientes': []})

def EliminarAmbiente(request):
    if request.method == 'POST':
        id_amb = request.POST.get('id')
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_eliminarambiente', [id_amb])
            messages.success(request, 'Ambiente eliminado')
        except Exception as e:
            messages.error(request, f'Error: {e}')
    return redirect('/Ambientes/ListaAmbientes')

def ActualizarAmbiente(request, id_ambiente):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        tipo = request.POST.get('tipo')
        obs = request.POST.get('observacion')
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_actualizarambiente', [id_ambiente, nombre, tipo, obs])
            messages.success(request, 'Ambiente actualizado')
            return redirect('/Ambientes/ListaAmbientes')
        except Exception as e:
            messages.error(request, f'Error: {e}')
            return redirect('/Ambientes/ListaAmbientes')
            
    with connection.cursor() as cursor:
        cursor.callproc('sp_consultarambiente', [id_ambiente])
        ambiente = cursor.fetchone()
    return render(request, 'Ambientes/ActualizarAmbiente.html', {'ambiente': ambiente})