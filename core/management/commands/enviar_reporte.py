import os
import io
import pandas as pd
from datetime import datetime
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.conf import settings
from django.apps import apps
from adr.models import ActivoBase

class Command(BaseCommand):
    help = 'Genera un reporte Excel de todos los activos y lo envía por correo'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando generación de reporte...'))

        # 1. Identificar modelos de inventario
        # Obtenemos todos los modelos de la app 'adr'
        app_config = apps.get_app_config('adr')
        all_models = app_config.get_models()

        # Filtramos solo los que heredan de ActivoBase (ignora abstractos automáticamente get_models)
        inventory_models = [
            m for m in all_models 
            if issubclass(m, ActivoBase) and not m._meta.abstract
        ]

        if not inventory_models:
            self.stdout.write(self.style.ERROR('No se encontraron modelos de inventario.'))
            return

        # 2. Generar Excel en memoria
        output = io.BytesIO()
        
        # Usamos ExcelWriter para crear múltiples hojas
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            models_processed = 0
            for model in inventory_models:
                model_name = model._meta.verbose_name_plural.title()
                # Cortar nombre de hoja a 31 caracteres (limite de Excel)
                sheet_name = model_name[:31]
                
                # Obtener queryset con todos los campos
                queryset = model.objects.all().values()
                
                # Crear DataFrame
                df = pd.DataFrame(list(queryset))
                
                if df.empty:
                    # Crear hoja vacía con columnas si no hay datos
                    df = pd.DataFrame(columns=[field.name for field in model._meta.fields])
                
                # Limpiar datetimes para que Excel no reclame por timezone
                for col in df.select_dtypes(include=['datetimetz', 'datetime']).columns:
                    df[col] = df[col].apply(lambda x: x.replace(tzinfo=None) if pd.notnull(x) else x)

                # Escribir a Excel
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                models_processed += 1
                self.stdout.write(f'Agregado hoja: {sheet_name} ({len(df)} registros)')

        output.seek(0)
        
        # 3. Enviar correo
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = f'Inventario_ADR_{date_str}.xlsx'
        
        subject = f'Reporte de Inventario ADR - {date_str}'
        body = f'Adjunto encontrará el reporte actualizado del inventario con {models_processed} categorías de equipos.'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_emails = settings.EMAIL_RECIPIENTS

        email = EmailMessage(
            subject,
            body,
            from_email,
            to_emails,
        )
        
        # Adjuntar archivo desde memoria
        email.attach(filename, output.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        
        try:
            email.send()
            self.stdout.write(self.style.SUCCESS(f'Reporte enviado exitosamente a {len(to_emails)} destinatarios.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al enviar correo: {str(e)}'))
