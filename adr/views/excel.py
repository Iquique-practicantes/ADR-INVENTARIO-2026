"""
Vistas para Descarga de Datos en Formato Excel
"""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import TemplateView
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

from adr.decorators import add_group_name_to_context
from adr.models import (
    AllInOne, AllInOneAdmins, Notebook, MiniPC, Proyectores,
    BodegaADR, Azotea, Monitor, Audio, Tablet,
    EquiposIsla, SwitchDeRed, Televisor,
    Eliminados, HistorialCambios
)


@add_group_name_to_context
class DescargarExcelView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """Vista para descargar datos en formato Excel"""

    def test_func(self):
        """Solo ADR o Operadores ADR pueden descargar"""
        return self.request.user.groups.filter(
            name__in=['ADR', 'Operadores ADR', 'Auxiliares Operadores ADR']
        ).exists()

    def handle_no_permission(self):
        """Redirección si no tiene permisos"""
        return redirect('error')

    def get(self, request, *args, **kwargs):
        """Genera y descarga archivo Excel del modelo especificado"""
        model_name = kwargs.get('model_name')
        fecha_actual = timezone.now().strftime('%d-%m-%Y')

        # Mapeo de modelos a clases y nombres de archivo
        model_mapping = {
            'allinone': (AllInOne, f'AllInOne_{fecha_actual}.xlsx'),
            'allinoneadmin': (AllInOneAdmins, f'AllInOneAdmins_{fecha_actual}.xlsx'),
            'equiposisla': (EquiposIsla, f'EquiposIsla_{fecha_actual}.xlsx'),
            'notebook': (Notebook, f'Notebooks_{fecha_actual}.xlsx'),
            'minipc': (MiniPC, f'MiniPCs_{fecha_actual}.xlsx'),
            'proyector': (Proyectores, f'Proyectores_{fecha_actual}.xlsx'),
            'bodegaadr': (BodegaADR, f'BodegaADR_{fecha_actual}.xlsx'),
            'azotea': (Azotea, f'Azotea_{fecha_actual}.xlsx'),
            'eliminados': (Eliminados, f'Eliminados_{fecha_actual}.xlsx'),
            'historialcambios': (HistorialCambios, f'HistorialCambios_{fecha_actual}.xlsx'),
            'monitor': (Monitor, f'Monitores_{fecha_actual}.xlsx'),
            'audio': (Audio, f'Audio_{fecha_actual}.xlsx'),
            'tablet': (Tablet, f'Tablets_{fecha_actual}.xlsx'),
            'switchdered': (SwitchDeRed, f'SwitchDeRed_{fecha_actual}.xlsx'),
            'televisor': (Televisor, f'Televisores_{fecha_actual}.xlsx'),
        }

        # Validación del modelo
        if model_name not in model_mapping:
            return HttpResponse(status=404)

        model_class, filename = model_mapping[model_name]

        # Aplicar filtro de búsqueda si existe
        search_query = request.GET.get('search', '').strip()
        if search_query:
            queryset = model_class.objects.filter(
                Q(activo__icontains=search_query) |
                Q(marca__icontains=search_query) |
                Q(modelo__icontains=search_query) |
                Q(n_serie__icontains=search_query) |
                Q(etiqueta__icontains=search_query) |
                Q(bdo__icontains=search_query) |
                Q(netbios__icontains=search_query) |
                Q(ubicacion__icontains=search_query) |
                Q(creado_por__first_name__icontains=search_query) |
                Q(creado_por__last_name__icontains=search_query)
            )
        else:
            queryset = model_class.objects.all()

        # Crear archivo Excel
        wb = Workbook()
        ws = wb.active
        ws.title = model_name.capitalize()

        # Agregar encabezados
        columns = [field.name for field in model_class._meta.fields]
        for col_num, column_title in enumerate(columns, 1):
            column_letter = get_column_letter(col_num)
            ws[f"{column_letter}1"] = column_title.capitalize()

        # Rellenar datos
        for row_num, obj in enumerate(queryset, 2):
            for col_num, field_name in enumerate(columns, 1):
                column_letter = get_column_letter(col_num)
                field_value = getattr(obj, field_name)
                ws[f"{column_letter}{row_num}"] = str(field_value) if field_value is not None else ''

        # Configurar respuesta HTTP
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        wb.save(response)
        return response
