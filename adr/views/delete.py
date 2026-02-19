"""
Vistas para Eliminación Lógica y Gestión de Registros Eliminados
"""
import logging
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db import transaction, IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, View

from adr.decorators import add_group_name_to_context
from adr.models import (
    AllInOne, AllInOneAdmins, Notebook, MiniPC,
    Proyectores, BodegaADR, Azotea, Monitor, Audio, Tablet,
    EquiposIsla, SwitchDeRed, Televisor, Eliminados
)
from adr.utils import enviar_notificacion_asunto

logger = logging.getLogger(__name__)

# Diccionario de modelos para eliminación
MODELS_DICT = {
    'all_in_one': AllInOne,
    'all_in_one_admin': AllInOneAdmins,
'mini_pc': MiniPC,
    'notebook': Notebook,
    'proyector': Proyectores,
    'bodegaadr': BodegaADR,
    'azotea': Azotea,
    'monitor': Monitor,
    'audio': Audio,
    'tablet': Tablet,
    'equipos_isla': EquiposIsla,
    'switch_de_red': SwitchDeRed,
    'televisor': Televisor,
}


@add_group_name_to_context
class DeleteToEliminadosView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Vista genérica para eliminar registros moviéndolos a la tabla de Eliminados"""
    success_url = reverse_lazy('eliminados')

    def test_func(self):
        """Solo ADR y Operadores pueden eliminar"""
        return self.request.user.groups.filter(
            name__in=['ADR', 'Operador ADR', 'Operadores ADR']
        ).exists()

    def handle_no_permission(self):
        """Manejo de acceso denegado"""
        messages.error(self.request, "No tienes permisos para realizar esta acción.")
        return redirect('inicio')

    def get(self, request, *args, **kwargs):
        """Permitir eliminación vía GET para enlaces directos"""
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Procesa la eliminación lógica moviendo el registro a Eliminados"""
        model_name = kwargs.get('model_name')
        pk = kwargs.get('pk')

        # Validación
        if not model_name or not pk:
            messages.error(request, 'Información del modelo o registro no proporcionada.')
            return redirect(self.success_url)

        model_name = model_name.lower()
        model = MODELS_DICT.get(model_name)

        if not model:
            messages.error(request, f'Modelo no encontrado: {model_name}')
            logger.warning(f"Intento de eliminar modelo inexistente: {model_name}")
            return redirect(self.success_url)

        try:
            instance = get_object_or_404(model, pk=pk)

            with transaction.atomic():
                # Crear registro en Eliminados
                eliminado_data = {
                    'activo': model._meta.verbose_name,
                    'modelo': getattr(instance, 'modelo', 'Desconocido'),
                    'n_serie': getattr(instance, 'n_serie', '') or '',
                    'etiqueta': getattr(instance, 'etiqueta', None),
                    'bdo': getattr(instance, 'bdo', 0),
                    'estado': getattr(instance, 'estado', 'Desconocido'),
                    'marca': getattr(instance, 'marca', 'Desconocido'),
                    'netbios': getattr(instance, 'netbios', ''),
                    'ubicacion': getattr(instance, 'ubicacion', ''),
                    'eliminado_por': request.user,
                    'fecha_eliminacion': timezone.now()
                }

                eliminado = Eliminados.objects.create(**eliminado_data)

                if eliminado:
                    instance.delete()

                    # Notificación por correo
                    self._enviar_notificacion(request, model_name, instance)

                    messages.success(
                        request,
                        f'{model_name.title()} movido correctamente a Eliminados.'
                    )
                else:
                    raise IntegrityError("Error al guardar en la tabla de Eliminados")

        except IntegrityError as e:
            logger.error(f'Error de integridad al mover {model_name} (pk={pk}): {e}')
            messages.error(
                request,
                'Error al mover el registro: Problema de integridad.'
            )
        except Exception as e:
            logger.error(f'Error al mover {model_name} (pk={pk}): {e}')
            messages.error(request, f'Error al mover el registro: {str(e)}')

        return redirect(self.success_url)

    def _enviar_notificacion(self, request, model_name, instance):
        """Envía notificación por correo de la eliminación"""
        try:
            from adr.email_template import notificacion_equipo

            user = request.user
            user_name = user.get_full_name() or user.username
            user_group = user.groups.first().name if user.groups.exists() else "Sin grupo"

            datos = [
                ('Activo', str(getattr(instance, 'activo', ''))),
                ('Marca', str(getattr(instance, 'marca', ''))),
                ('Modelo', str(getattr(instance, 'modelo', ''))),
                ('N° Serie', str(getattr(instance, 'n_serie', ''))),
                ('Etiqueta', str(getattr(instance, 'etiqueta', ''))),
                ('BDO', str(getattr(instance, 'bdo', ''))),
                ('Estado', str(getattr(instance, 'estado', ''))),
                ('NetBIOS', str(getattr(instance, 'netbios', ''))),
                ('Ubicación', str(getattr(instance, 'ubicacion', ''))),
                ('Creado por', instance.creado_por.get_full_name() if getattr(instance, 'creado_por', None) else 'N/A'),
                ('Fecha Creación', instance.fecha_creacion.strftime('%d/%m/%Y') if getattr(instance, 'fecha_creacion', None) else ''),
                ('Fecha Modificación', instance.fecha_modificacion.strftime('%d/%m/%Y') if getattr(instance, 'fecha_modificacion', None) else ''),
            ]

            if model_name in ('monitor', 'notebook'):
                datos.append(('Asignado a', str(getattr(instance, 'asignado_a', 'N/A'))))

            verbose = MODELS_DICT[model_name]._meta.verbose_name

            html, plain = notificacion_equipo(
                accion=f"Eliminación — Movido a Eliminados",
                usuario_nombre=user_name,
                usuario_grupo=user_group,
                modelo_nombre=str(verbose).title(),
                datos_registro=datos,
            )

            enviar_notificacion_asunto(
                asunto=f"Registro Movido a Eliminados — {verbose}",
                mensaje=plain,
                destinatarios=settings.EMAIL_RECIPIENTS,
                html_content=html,
            )
        except Exception as e:
            logger.error(f'Error al enviar notificación de eliminación: {e}')
            messages.warning(
                request,
                f'{model_name.title()} movido a Eliminados pero hubo un error al enviar la notificación.'
            )


@add_group_name_to_context
class EliminadosListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Vista para listar registros eliminados"""
    model = Eliminados
    template_name = 'modulos/eliminados.html'
    context_object_name = 'eliminados'
    paginate_by = 15

    def test_func(self):
        """Solo ADR y Operadores pueden ver eliminados"""
        return self.request.user.groups.filter(
            name__in=['ADR', 'Operadores ADR', 'Auxiliares Operadores ADR']
        ).exists()

    def handle_no_permission(self):
        """Redirección si no tiene permisos"""
        messages.error(self.request, "No tienes permisos para acceder a esta página.")
        return redirect('inicio')

    def get_queryset(self):
        """Filtra la lista según búsqueda"""
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '').strip()

        if search_query:
            queryset = queryset.filter(
                Q(activo__icontains=search_query) |
                Q(modelo__icontains=search_query) |
                Q(n_serie__icontains=search_query) |
                Q(etiqueta__icontains=search_query) |
                Q(bdo__icontains=search_query) |
                Q(marca__icontains=search_query) |
                Q(ubicacion__icontains=search_query) |
                Q(eliminado_por__first_name__icontains=search_query) |
                Q(eliminado_por__last_name__icontains=search_query)
            )

        return queryset.select_related('eliminado_por').order_by('-fecha_eliminacion')

    def get_context_data(self, **kwargs):
        """Agrega contexto adicional"""
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '').strip()
        return context
