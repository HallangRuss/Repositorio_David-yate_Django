"""
URL configuration for AmbienteSena project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from.views.home import home
from .views import RegistrarAmbiente, ListarAmbientes, EliminarAmbiente, ActualizarAmbiente
from .views import RegistrarInstructor, ListarInstructores, EliminarInstructor , ActualizarInstructor
from .views import RegistrarElemento,ListarElementos,APIConsultarElemento,ActualizarElemento,EliminarElemento
from .views import RegistrarCuentadante,ListarCuentadantes,EliminarCuentadante,APIConsultarCuentadante
from .views import RegistrarIngreso,ListarIngreso,MarcarSalida,APIConsultarIngreso,ActualizarCuentadante

urlpatterns = [
    path('',home),
    path('admin/', admin.site.urls),
    path('Ambientes/RegistrarAmbiente',RegistrarAmbiente),
    path('Ambientes/ListaAmbientes', ListarAmbientes),
    path('Ambientes/EliminarAmbiente', EliminarAmbiente),
    path('Ambientes/ActualizarAmbiente/<int:id_ambiente>', ActualizarAmbiente),
    path('Instructores/RegistrarInstructor', RegistrarInstructor),
    path('Instructores/ListarInstructores', ListarInstructores),
    path('Instructores/EliminarInstructor', EliminarInstructor),
    path('Instructores/ActualizarInstructor/<int:id_instructor>', ActualizarInstructor),
    path('Elementos/RegistrarElementos', RegistrarElemento),
    path('Elementos/ListarElementos', ListarElementos),
    path('Elementos/APIConsultarElemento/<int:idelemento>', APIConsultarElemento),
    path('Elementos/ActualizarElemento', ActualizarElemento),
    path('Elementos/EliminarElemento', EliminarElemento),
    path('Cuentadante/RegistrarCuentadante', RegistrarCuentadante),
    path('Cuentadante/ListarCuentadantes', ListarCuentadantes),
    path('Cuentadante/EliminarCuentadante', EliminarCuentadante),
    path('Cuentadante/APIConsultarCuentadante/<int:id_cuentadante>',APIConsultarCuentadante),
    path('Ingresos/RegistrarIngresos', RegistrarIngreso),
    path('Ingresos/ListarIngresos', ListarIngreso),
    path('Ingresos/MarcarSalida/<int:ingreso_id>', MarcarSalida),
    path('Ingresos/APIConsultarIngreso/<int:id_ingreso>', APIConsultarIngreso),
    path('Cuentadante/ActualizarCuentadante/<int:id_cuentadante>', ActualizarCuentadante),
]
