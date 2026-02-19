"""
Vistas genéricas base para modelos de activos.

Este módulo contiene clases base reutilizables que eliminan la duplicación
de código para las operaciones CRUD estándar de todos los modelos de equipos.
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
from django.conf import settings

from adr.utils import enviar_notificacion_asunto
from adr.decorators import add_group_name_to_context


@add_group_name_to_context
class ActivoListView(LoginRequiredMixin, ListView):
    """
    Vista genérica para listar cualquier modelo de activo con paginación y búsqueda.
    
    Attributes:
        model: El modelo Django a listar
        template_name: Template a usar
        context_object_name: Nombre de la variable en el contexto
        paginate_by: Número de items por página (default: 25)
    """
    paginate_by = 25
    ordering = ['activo', '-fecha_creacion']
    
    def get_queryset(self):
        """Filtra el queryset según búsqueda (por texto o por ID)."""
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '').strip()
        search_by_pk = self.request.GET.get('search_by_pk', 'false').lower() == 'true'
        
        if search_by_pk:
            if search_query.isdigit():
                return queryset.filter(pk=int(search_query))
            else:
                return queryset.none()
        
        if search_query:
            # Búsqueda en campos comunes de todos los activos
            queryset = queryset.filter(
                Q(ubicacion__icontains=search_query) |
                Q(activo__icontains=search_query) |
                Q(marca__icontains=search_query) |
                Q(modelo__icontains=search_query) |
                Q(n_serie__icontains=search_query) |
                Q(etiqueta__icontains=search_query) |
                Q(bdo__icontains=search_query) |
                Q(creado_por__first_name__icontains=search_query) |
                Q(creado_por__last_name__icontains=search_query) |
                Q(fecha_creacion__icontains=search_query)
            )
        
        return queryset.select_related('creado_por').order_by('activo', '-fecha_creacion')
    
    def get_context_data(self, **kwargs):
        """Agrega el término de búsqueda al contexto."""
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '').strip()
        return context


@add_group_name_to_context
class ActivoCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    """
    Vista genérica para crear un nuevo activo.
    
    Verifica permisos, asigna el usuario creador, y envía notificación por email.
    
    Attributes:
        model: El modelo Django a crear
        form_class: Formulario a usar
        template_name: Template a usar
        success_url: URL de redirección tras éxito
        allowed_groups: Lista de grupos con permiso (default: ['ADR', 'Operadores ADR'])
    """
    allowed_groups = ['ADR', 'Operadores ADR']
    
    def test_func(self):
        """Verifica que el usuario pertenezca a un grupo permitido."""
        first_group = self.request.user.groups.first()
        return bool(first_group and first_group.name in self.allowed_groups)
    
    def handle_no_permission(self):
        """Redirecciona a error si no tiene permisos."""
        messages.error(self.request, 'No tienes permisos para realizar esta acción.')
        return redirect('error')
    
    def get_context_data(self, **kwargs):
        """Agrega lista de items existentes al contexto."""
        context = super().get_context_data(**kwargs)
        context['items'] = self.model.objects.select_related('creado_por').order_by('-fecha_creacion')[:10]
        return context
    
    def form_valid(self, form):
        """Guarda el objeto asignando el usuario creador y envía notificación."""
        instance = form.save(commit=False)
        instance.creado_por = self.request.user
        instance.save()
        
        # Enviar notificación
        try:
            from adr.email_template import notificacion_equipo

            model_verbose = self.model._meta.verbose_name
            user = self.request.user
            user_name = user.get_full_name() or user.username
            user_group = user.groups.first().name if user.groups.exists() else 'Sin grupo'

            datos = [
                ('Activo', str(getattr(instance, 'activo', ''))),
                ('Marca', str(getattr(instance, 'marca', ''))),
                ('Modelo', str(getattr(instance, 'modelo', ''))),
                ('N° Serie', str(getattr(instance, 'n_serie', ''))),
                ('Etiqueta', str(getattr(instance, 'etiqueta', ''))),
                ('BDO', str(getattr(instance, 'bdo', ''))),
                ('Estado', str(getattr(instance, 'estado', ''))),
                ('Ubicación', str(getattr(instance, 'ubicacion', ''))),
            ]

            html, plain = notificacion_equipo(
                accion=f"Creación — Nuevo {model_verbose}",
                usuario_nombre=user_name,
                usuario_grupo=user_group,
                modelo_nombre=str(model_verbose).title(),
                datos_registro=datos,
            )

            enviar_notificacion_asunto(
                asunto=f"Nuevo {model_verbose} Registrado",
                mensaje=plain,
                destinatarios=getattr(settings, 'EMAIL_RECIPIENTS', []),
                html_content=html,
            )
        except Exception as e:
            messages.warning(self.request, f'{model_verbose} creado, pero falló el envío de notificación: {str(e)}')
        
        messages.success(self.request, f'{model_verbose} agregado exitosamente.')
        return redirect(self.success_url)
    
    def form_invalid(self, form):
        """Manejo de errores del formulario."""
        messages.error(self.request, 'Por favor corrige los errores en el formulario.')
        return super().form_invalid(form)


@add_group_name_to_context  
class ActivoUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    """
    Vista genérica para editar un activo existente.
    
    Verifica permisos, rastrea cambios, y envía notificación por email.
    
    Attributes:
        model: El modelo Django a editar
        form_class: Formulario a usar
        template_name: Template a usar
        success_url: URL de redirección tras éxito
        allowed_groups: Lista de grupos con permiso (default: ['ADR', 'Operadores ADR'])
    """
    allowed_groups = ['ADR', 'Operadores ADR']
    
    def test_func(self):
        """Verifica que el usuario pertenezca a un grupo permitido."""
        first_group = self.request.user.groups.first()
        return bool(first_group and first_group.name in self.allowed_groups)
    
    def handle_no_permission(self):
        """Redirecciona a error si no tiene permisos."""
        messages.error(self.request, 'No tienes permisos para realizar esta acción.')
        return redirect('error')
    
    def get_context_data(self, **kwargs):
        """Agrega el objeto actual al contexto."""
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        return context
    
    def form_valid(self, form):
        """Guarda cambios y envía notificación."""
        instance = form.save()
        
        # Enviar notificación
        try:
            from adr.email_template import notificacion_equipo

            model_verbose = self.model._meta.verbose_name
            user = self.request.user
            user_name = user.get_full_name() or user.username
            user_group = user.groups.first().name if user.groups.exists() else 'Sin grupo'

            datos = [
                ('Activo', str(getattr(instance, 'activo', ''))),
                ('Marca', str(getattr(instance, 'marca', ''))),
                ('Modelo', str(getattr(instance, 'modelo', ''))),
                ('N° Serie', str(getattr(instance, 'n_serie', ''))),
                ('Etiqueta', str(getattr(instance, 'etiqueta', ''))),
                ('BDO', str(getattr(instance, 'bdo', ''))),
                ('Estado', str(getattr(instance, 'estado', ''))),
                ('Ubicación', str(getattr(instance, 'ubicacion', ''))),
            ]

            html, plain = notificacion_equipo(
                accion=f"Modificación — {model_verbose} Editado",
                usuario_nombre=user_name,
                usuario_grupo=user_group,
                modelo_nombre=str(model_verbose).title(),
                datos_registro=datos,
            )

            enviar_notificacion_asunto(
                asunto=f"{model_verbose} Modificado",
                mensaje=plain,
                destinatarios=getattr(settings, 'EMAIL_RECIPIENTS', []),
                html_content=html,
            )
        except Exception as e:
            messages.warning(self.request, f'{model_verbose} actualizado, pero falló el envío de notificación: {str(e)}')
        
        messages.success(self.request, f'{model_verbose} actualizado exitosamente.')
        return redirect(self.success_url)
    
    def form_invalid(self, form):
        """Manejo de errores del formulario."""
        messages.error(self.request, 'Por favor corrige los errores en el formulario.')
        return super().form_invalid(form)


@add_group_name_to_context
class ActivoDetailView(LoginRequiredMixin, DetailView):
    """
    Vista genérica para ver detalles de un activo.
    
    Attributes:
        model: El modelo Django a mostrar
        template_name: Template a usar
        context_object_name: Nombre de la variable en el contexto
    """
    pass  # Hereda toda la funcionalidad de DetailView
