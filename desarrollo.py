from enum import Enum
from dataclasses import dataclass
from typing import List
from datetime import datetime

# ------------------------------
# Clase RequirementType
# ------------------------------
# Esta clase define un enumerador para clasificar los tipos de requerimientos en un proyecto de software.
# Se usa para categorizar cada requerimiento en funcional, no funcional, de negocio, técnico o de usuario.
class RequirementType(Enum):
    FUNCTIONAL = "Funcional"
    NON_FUNCTIONAL = "No Funcional"
    BUSINESS = "Negocio"
    TECHNICAL = "Técnico"
    USER = "Usuario"

# ------------------------------
# Clase VerificationStatus
# ------------------------------
# Define los estados de verificación de un requerimiento.
# Un requerimiento puede estar pendiente, verificado o rechazado.
class VerificationStatus(Enum):
    PENDING = "Pendiente"
    VERIFIED = "Verificado"
    REJECTED = "Rechazado"

# ------------------------------
# Clase Requirement
# ------------------------------
# Representa un requerimiento de software, con atributos como título, descripción, prioridad y criterios SMART.
# Permite validar si cumple con las condiciones necesarias y gestionar su estado de verificación.
@dataclass
class Requirement:
    id: str  # Identificador único del requerimiento
    title: str  # Título breve del requerimiento
    description: str  # Descripción detallada
    type: RequirementType  # Tipo de requerimiento
    priority: int  # Nivel de prioridad (1-5, donde 5 es la más alta)

    # Características SMART (atributos opcionales con valores por defecto en False)
    is_specific: bool = False
    is_measurable: bool = False
    is_achievable: bool = False
    is_relevant: bool = False
    is_time_bound: bool = False

    # Metadatos
    created_date: datetime = datetime.now()
    last_modified: datetime = datetime.now()
    verification_status: VerificationStatus = VerificationStatus.PENDING
    verification_notes: str = ""

    def validate(self) -> List[str]:
        """Verifica y valida si el requerimiento cumple con criterios de calidad y completitud."""
        validation_errors = []

        if not self.description:
            validation_errors.append("La descripción no puede estar vacía")

        if not self.title:
            validation_errors.append("El título no puede estar vacío")

        if not (1 <= self.priority <= 5):
            validation_errors.append("La prioridad debe estar entre 1 y 5")

        if not all([self.is_specific, self.is_measurable, self.is_achievable,
                    self.is_relevant, self.is_time_bound]):
            validation_errors.append("El requerimiento no cumple con todos los criterios SMART")

        return validation_errors

    def is_valid(self) -> bool:
        """Retorna True si el requerimiento es válido (no tiene errores de validación)."""
        return len(self.validate()) == 0

    def verify(self, notes: str) -> None:
        """Verifica el requerimiento, actualiza su estado y registra notas de verificación."""
        if self.is_valid():
            self.verification_status = VerificationStatus.VERIFIED
            self.verification_notes = notes
            self.last_modified = datetime.now()
        else:
            self.verification_status = VerificationStatus.REJECTED
            self.verification_notes = f"Errores de validación: {', '.join(self.validate())}"

# ------------------------------
# Clase RequirementsDocument
# ------------------------------
# Representa un documento que gestiona múltiples requerimientos de software en un proyecto.
# Permite agregar, filtrar y generar reportes de los requerimientos almacenados.
class RequirementsDocument:
    def __init__(self, project_name: str):
        """Inicializa un documento de requerimientos para un proyecto específico."""
        self.project_name = project_name
        self.requirements: List[Requirement] = []
        self.created_date = datetime.now()

    def add_requirement(self, requirement: Requirement) -> None:
        """Añade un nuevo requerimiento al documento."""
        self.requirements.append(requirement)

    def get_requirements_by_type(self, req_type: RequirementType) -> List[Requirement]:
        """Filtra y retorna los requerimientos que pertenecen a un tipo específico."""
        return [req for req in self.requirements if req.type == req_type]

    def generate_report(self) -> str:
        """Genera un reporte con el estado actual de los requerimientos almacenados."""
        report = f"Reporte de Requerimientos - {self.project_name}\n"
        report += f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        # Estadísticas generales
        total_reqs = len(self.requirements)
        verified_reqs = len([r for r in self.requirements if r.verification_status == VerificationStatus.VERIFIED])

        report += f"Total de requerimientos: {total_reqs}\n"
        report += f"Requerimientos verificados: {verified_reqs}\n"
        report += f"Porcentaje de completitud: {(verified_reqs / total_reqs) * 100 if total_reqs > 0 else 0}%\n"

        return report

# ------------------------------
# Función main
# ------------------------------
# Simula la creación y validación de un documento de requerimientos.
def main():
    """Crea un documento de requerimientos, añade un requerimiento y genera un reporte."""
    doc = RequirementsDocument("Sistema de Gestión de Inventario")

    # Crear un requerimiento funcional
    req1 = Requirement(
        id="REQ-001",
        title="Registro de Productos",
        description="El sistema debe permitir registrar nuevos productos con código, nombre, precio y cantidad",
        type=RequirementType.FUNCTIONAL,
        priority=5,
        is_specific=True,
        is_measurable=True,
        is_achievable=True,
        is_relevant=True,
        is_time_bound=True
    )

    if req1.is_valid():
        req1.verify("Requerimiento revisado y aprobado por el equipo técnico")

    # Agregarlo al documento
    doc.add_requirement(req1)

    # Generar y mostrar el reporte
    print(doc.generate_report())

if __name__ == "__main__":
    main()