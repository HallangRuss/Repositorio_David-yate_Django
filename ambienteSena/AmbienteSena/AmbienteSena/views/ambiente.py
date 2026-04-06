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
                    # Usamos execute para llamar al procedimiento de inserción
                    cursor.execute('CALL sp_insertarambiente(%s, %s, %s)', [nombre, tipo, observacion])
                messages.success(request, 'Ambiente registrado correctamente')
                return redirect('/Ambientes/ListaAmbientes')
            except Exception as e:
                messages.error(request, f'Error en la base de datos: {e}')
                return redirect('/Ambientes/RegistrarAmbiente')
    
    return render(request, 'Ambientes/RegistrarAmbiente.html')

def ListarAmbientes(request):
    try:
        with connection.cursor() as cursor:
            # En Linux/Render es más seguro usar execute('CALL...') para obtener filas
            cursor.execute('CALL sp_listarambientes()')
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
                cursor.execute('CALL sp_eliminarambiente(%s)', [id_amb])
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
                cursor.execute('CALL sp_actualizarambiente(%s,%s,%s,%s)', [id_ambiente, nombre, tipo, obs])
            messages.success(request, 'Ambiente actualizado')
            return redirect('/Ambientes/ListaAmbientes')
        except Exception as e:
            messages.error(request, f'Error: {e}')
            return redirect('/Ambientes/ListaAmbientes')
            
    with connection.cursor() as cursor:
        cursor.execute('CALL sp_consultarambiente(%s)', [id_ambiente])
        ambiente = cursor.fetchone()
    return render(request, 'Ambientes/ActualizarAmbiente.html', {'ambiente': ambiente})