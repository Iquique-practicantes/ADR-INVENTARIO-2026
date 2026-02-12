"""
Vistas para Gestión de Historial de Cambios
"""
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Case, When, Value, F, CharField
from django.utils.timezone import make_aware
from django.views.generic import ListView

from adr.decorators import add_group_name_to_context
from adr.models import HistorialCambios


@add_group_name_to_context
class HistorialCambiosView(LoginRequiredMixin, ListView):
    """Vista para listar historial de cambios con filtros"""
    model = HistorialCambios
    template_name = 'historial_cambios.html'
    context_object_name = 'historial'
    paginate_by = 20

    def get_queryset(self):
        """
        Obtiene y filtra el historial de cambios
        Aplica filtros por usuario, rango de fechas,  modelo y ID de objeto
        """
        queryset = super().get_queryset()

        # Filtro por usuario
        usuario = self.request.GET.get('usuario', 'todos')
        if usuario != 'todos':
            queryset = queryset.filter(usuario__username=usuario)

        # Filtro por rango de fechas
        fecha_inicio = self.request.GET.get('fecha_inicio', '')
        if fecha_inicio:
            try:
                fecha_inicio_dt = make_aware(datetime.strptime(fecha_inicio, '%Y-%m-%d'))
                queryset = queryset.filter(fecha_modificacion__gte=fecha_inicio_dt)
            except ValueError:
                pass

        fecha_fin = self.request.GET.get('fecha_fin', '')
        if fecha_fin:
            try:
                fecha_fin_dt = make_aware(
                    datetime.strptime(fecha_fin, '%Y-%m-%d')
                ).replace(hour=23, minute=59, second=59)
                queryset = queryset.filter(fecha_modificacion__lte=fecha_fin_dt)
            except ValueError:
                pass

        # Filtro por modelo y objeto específico (para detail views)
        model_name = self.kwargs.get('model_name')
        object_id = self.kwargs.get('object_id')
        if model_name and object_id:
            queryset = queryset.filter(modelo=model_name, objeto_id=object_id)

        # Evitar paginación si no hay resultados
        if not queryset.exists():
            self.paginate_by = None

        # Normalizar nombres de modelo para visualización
        queryset = queryset.annotate(
            modelo_display=Case(
                When(modelo='allinoneadmins', then=Value('AllInOneAdmins')),
                default=F('modelo'),
                output_field=CharField()
            )
        )

        return queryset.order_by('-fecha_modificacion', '-pk')

    def get_context_data(self, **kwargs):
        """Agrega información de filtros al contexto"""
        context = super().get_context_data(**kwargs)
        context['usuario_seleccionado'] = self.request.GET.get('usuario', 'todos')
        context['fecha_inicio'] = self.request.GET.get('fecha_inicio', '')
        context['fecha_fin'] = self.request.GET.get('fecha_fin', '')
        context['usuarios'] = self.get_usuarios_disponibles()
        return context

    def get_usuarios_disponibles(self):
        """Retorna usuarios activos para el filtro"""
        return User.objects.filter(is_active=True)
