from django.contrib import messages
from django.db import connection
from django.shortcuts import render, redirect


def RegistrarAmbiente(request):
    if request.method == 'POST':
        if request.POST.get('nombre') and request.POST.get('tipo') and request.POST.get('observacion'):
            nombre = request.POST.get('nombre')
            tipo = request.POST.get('tipo')
            observacion = request.POST.get('observacion')
            try:
                insertar = connection.cursor()
                insertar.execute('CALL sp_insertarambiente(%s, %s, %s)', [nombre, tipo, observacion])
                messages.success(request, 'Ambiente de formacion registrado correctamente')
            except Exception as e:
                messages.error(request, f'Ocurrio un error en el sistema: {e}')
            return redirect('/Ambientes/ListaAmbientes')
    else:
        return render(request, 'Ambientes/RegistrarAmbiente.html')


def ListarAmbientes(request):
    try:
        cursor = connection.cursor()
        cursor.execute('CALL sp_listarambientes()')
        ambientes = cursor.fetchall()
    except Exception as e:
        messages.error(request, 'Ocurrio un error en el sistema')
        return render(request, 'Ambientes/ListaAmbientes.html')
    return render(request, 'Ambientes/ListaAmbientes.html', {'ambientes': ambientes})


def EliminarAmbiente(request):
    if request.method == 'POST':
        try:
            eliminar = connection.cursor()
            eliminar.execute('CALL sp_eliminarambiente(%s)', [request.POST.get('id')])
            messages.success(request, 'Se Elimino el Ambiente de Formacion Exitosamente')
        except Exception as e:
            messages.error(request, f'Ocurrio un error en el sistema: {e}')
        return redirect('/Ambientes/ListaAmbientes')


def ActualizarAmbiente(request, id_ambiente):
    if request.method == 'POST':
        try:
            actualizar = connection.cursor()
            actualizar.execute('CALL sp_actualizarambiente(%s,%s,%s,%s)', [id_ambiente, request.POST.get('nombre'),
                                                                           request.POST.get('tipo'),
                                                                           request.POST.get('observacion')])
            messages.success(request, 'Se actualizo con Exito el Ambiente')
        except Exception as e:
            messages.error(request, 'Error en el sistema , Vuelva mas tarde')
        return redirect('/Ambientes/ListaAmbientes')
    try:
        consulta = connection.cursor()
        consulta.execute('CALL sp_consultarambiente(%s)', [id_ambiente])
        ambiente = consulta.fetchone()
        return render(request, 'Ambientes/ActualizarAmbiente.html', {'ambiente': ambiente})
    except Exception as e:
        messages.error(request, 'Error en el sistema')
        return redirect('/Ambientes/ListaAmbientes')