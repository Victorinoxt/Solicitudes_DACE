from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.db.models import Q
import csv
import io
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Estudiante
from .forms import EstudianteForm

@login_required
def lista_estudiantes(request, es_egresado):
    query = request.GET.get('q')
    if query:
        estudiantes_list = Estudiante.objects.filter(
            Q(nombre__icontains=query) | Q(apellido__icontains=query) | Q(cedula__icontains=query),
            es_egresado=es_egresado
        )
    else:
        estudiantes_list = Estudiante.objects.filter(es_egresado=es_egresado)
    
    paginator = Paginator(estudiantes_list, 10)  # 10 estudiantes por página
    page_number = request.GET.get('page')
    estudiantes = paginator.get_page(page_number)
    return render(request, 'solicitudes/lista_estudiantes.html', {'estudiantes': estudiantes, 'es_egresado': es_egresado})

@login_required
def crear_estudiante(request):
    if request.method == "POST":
        form = EstudianteForm(request.POST)
        if form.is_valid():
            estudiante = form.save()
            return redirect('lista_estudiantes', es_egresado=int(estudiante.es_egresado))
    else:
        form = EstudianteForm()
    return render(request, 'solicitudes/formulario_estudiante.html', {'form': form})

@login_required
def actualizar_estudiante(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    if request.method == "POST":
        form = EstudianteForm(request.POST, instance=estudiante)
        if form.is_valid():
            estado_anterior = estudiante.estado_solicitud
            estudiante = form.save(commit=False)
            if 'enviar_correo' in request.POST or estado_anterior != estudiante.estado_solicitud:
                enviar_correo_cambio_estado(estudiante)
            estudiante.save()
            return redirect('lista_estudiantes', es_egresado=int(estudiante.es_egresado))
    else:
        form = EstudianteForm(instance=estudiante)
    return render(request, 'solicitudes/formulario_estudiante.html', {'form': form, 'es_egresado': int(estudiante.es_egresado)})

@login_required
def eliminar_estudiante(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    es_egresado = int(estudiante.es_egresado)
    estudiante.delete()
    return redirect('lista_estudiantes', es_egresado=es_egresado)

def enviar_correo_cambio_estado(estudiante):
    subject = f'Solicitud {estudiante.estado_solicitud}'
    if estudiante.estado_solicitud == 'Aprobado':
        message = f"Estimado/a {estudiante.nombre} {estudiante.apellido},\n\nSu solicitud ha sido aprobada."
    elif estudiante.estado_solicitud == 'Rechazado':
        message = f"Estimado/a {estudiante.nombre} {estudiante.apellido},\n\nSu solicitud ha sido rechazada."
    else:
        message = f"Estimado/a {estudiante.nombre} {estudiante.apellido},\n\nEl estado de su solicitud ha cambiado a: {estudiante.estado_solicitud}."

    try:
        send_mail(subject, message, 'admin@solicitudesdace.com', [estudiante.email])
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'solicitudes/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def exportar_estudiantes_csv(request, es_egresado):
    estudiantes = Estudiante.objects.filter(es_egresado=es_egresado)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="estudiantes.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nombre', 'Apellido', 'Cédula', 'Teléfono', 'Email', 'Año de Ingreso', 'Carrera', 'Estado de Solicitud'])

    for estudiante in estudiantes:
        writer.writerow([estudiante.nombre, estudiante.apellido, estudiante.cedula, estudiante.telefono, estudiante.email, estudiante.ano_ingreso, estudiante.carrera, estudiante.estado_solicitud])

    return response

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return result.getvalue()
    return None

@login_required
def exportar_estudiantes_pdf(request, es_egresado):
    estudiantes = Estudiante.objects.filter(es_egresado=es_egresado)
    template_path = 'solicitudes/estudiantes_pdf.html'
    context = {'estudiantes': estudiantes}
    pdf = render_to_pdf(template_path, context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="estudiantes.pdf"'
        return response
    return HttpResponse("Error al generar el PDF", status=500)
