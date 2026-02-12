"""
Paquete de vistas del módulo ADR.

Este paquete organiza las vistas en módulos especializados:
- base: Vistas genéricas reutilizables
- equipos: CRUD de equipos refactorizados (TODOS los modelos)
- delete: Vistas de eliminación lógica y gestión de eliminados
- historial: Vistas de historial de cambios
- auth: Vistas de autenticación y perfil de usuario
- excel: Vistas de descarga de datos en Excel
- views_legacy: Archivo original (temporalmente para backward compatibility)

ESTRATEGIA INCREMENTAL:
1. Importamos TODAS las vistas del archivo legacy
2. Sobrescribimos con las vistas refactorizadas
3. urls.py sigue funcionando sin cambios
"""

# Importar vistas restantes (upload, users, utils) de views_other
# NOTA: Este archivo contiene vistas especializadas aún no refactorizadas
from adr.views_other import *

# Sobrescribir con TODAS las vistas refactorizadas de equipos
from .equipos import (
    # AllInOne
    AllInOneListView as AllInOneView,
    AllInOneCreateView as Add_AllInOneView,
    AllInOneUpdateView as Edit_AllInOneView,
    AllInOneDetailView,
    
    # AllInOne Admins
    AllInOneAdminListView as AllInOneAdminView,
    AllInOneAdminCreateView as Add_AllInOneAdminView,
    AllInOneAdminUpdateView as Edit_AllInOneAdmView,
    
    # Notebooks
    NotebookListView as NotebooksView,
    NotebookCreateView as AddNotebooksView,
    NotebookUpdateView as EditNotebooksView,
    NotebookDetailView,
    
    # MiniPC
    MiniPCListView as MiniPCsView,
    MiniPCCreateView as AddMiniPCView,
    MiniPCUpdateView as EditMiniPCView,
    MiniPCDetailView,
    
    # Proyectores
    ProyectorListView as ProyectoresView,
    ProyectorCreateView as AddProyectorView,
    ProyectorUpdateView as EditProyectorView,
    ProyectorDetailView,
    
    # Bodega ADR
    BodegaADRListView as BodegaADRView,
    BodegaADRCreateView as AddBodegaADRView,
    BodegaADRUpdateView as EditBodegaADRView,
    BodegaADRDetailView,
    
    # Azotea
    AzoteaListView as AzoteaView,
    AzoteaCreateView as AddAzoteaView,
    AzoteaUpdateView as EditAzoteaView,
    AzoteaDetailView,
    
    # Monitor
    MonitorListView as MonitorView,
    MonitorCreateView as AddMonitorView,
    MonitorUpdateView as EditMonitorView,
    MonitorDetailView,
    
    # Audio
    AudioListView as AudioView,
    AudioCreateView as AddAudioView,
    AudioUpdateView as EditAudioView,
    AudioDetailView,
    
    # Tablet
    TabletListView as TabletView,
    TabletCreateView as AddTabletView,
    TabletUpdateView as EditTabletView,
    TabletDetailView,
    
    # Equipos Isla
    EquiposIslaListView as EquiposIslaView,
    EquiposIslaCreateView as Add_EquiposIslaView,
    EquiposIslaUpdateView as Edit_EquiposIslaView,
    EquiposIslaDetailView,
    
    # Switch De Red
    SwitchDeRedListView as SwitchDeRedView,
    SwitchDeRedCreateView as Add_SwitchDeRedView,
    SwitchDeRedUpdateView as Edit_SwitchDeRedView,
    SwitchDeRedDetailView,
    
    # Televisor
    TelevisorListView as TelevisorView,
    TelevisorCreateView as AddTelevisorView,
    TelevisorUpdateView as EditTelevisorView,
    TelevisorDetailView,
)

# Sobrescribir vistas de eliminación y eliminados
from .delete import (
    DeleteToEliminadosView,
    EliminadosListView,
)

# Sobrescribir vista de historial
from .historial import (
    HistorialCambiosView,
)

# Sobrescribir vistas de autenticación y perfil
from .auth import (
    my_profile,
    UserPasswordChangeView,
    CustomPasswordResetView,
)

# Sobrescribir vistas de Excel
from .excel import (
    DescargarExcelView,
)

# Otras vistas siguen viniendo de views_legacy.py
