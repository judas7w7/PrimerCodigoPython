from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

# Definición de tipos de requisitos
class RequirementType(Enum):
  FUNCTIONAL = "Funcional"
  NON_FUNCTIONAL = "No Funcional"
  BUSINESS = "Negocio"
  TECHNICAL = "Técnico"
  USER = "Usuario"

# Definición de estados de verificación
class VerificationStatus(Enum):
  PENDING = "Pendiente"
  VERIFIED = "Verificado"
  REJECTED = "Rechazado"


@dataclass
class Requirement:
    """Clase para documentar y validar requerimientos de software"""

    # Atributos basicos del requerimiento
    id: str
    title: str
    description: str
    type: RequirementType
    priority: int # 1-5, donde 5 es la mas alta

    # Características deseables (SMART)
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
        """Verifica y valida el requerimiento segun criterios de calidad"""
        validation_errors = []

        # Validacion de completitud
        if not self.description:
            validation_errors.append("La descripcion no puede estar vacia")

        if not self.title:
            validation_errors.append("El titulo no puede estar vacio")

        # Validación de prioridad
        if not (1 <= self.priority <= 5):
            validation_errors.append("La prioridad debe estar entre 1 y 5")

        # Validación de caracteristicas SMART
        if not all([self.is_specific, self.is_measurable, self.is_achievable,
                self.is_relevant, self.is_time_bound]):
            validation_errors.append("El requerimiento no cumple con todos los criterios")

        return validation_errors


    def is_valid(self) -> bool:
        """Verifica si el requerimiento es valido"""
        return len(self.validate()) == 0

    def verify(self, notes: str) -> None:
        """Verifica el requerimiento y actualiza su estado"""

        if self.is_valid():
            self.verification_status = VerificationStatus.VERIFIED
            self.veritication_notes = notes
            self.last_modified = datetime.now()
        else:
            self.verification_status = VerificationStatus.REJECTED
            self.verification_notes = f"Errores de validacion: {', '.join(self.validate())}"

class RequirementsDocument:
    """Clase para gestionar la documentación de requerimientos"""

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.requirements: List[Requirement] = []
        self.created_date = datetime.now()

    def add_requirement(self, requirement: Requirement) -> None:
        """Añade un nuevo requerimiento al documento"""
        self.requirements.append(requirement)

    def get_requirements_by_type(self, req_type: RequirementType) -> List[Requirement]:
        """Filtra requerimientos por tipo"""
        return [req for req in self.requirements if req.type == req_type]

    def generate_report(self) -> str:
        """Genera un reporte del estado de los requerimientos"""
        report = f"Reporte de Requerimientos - {self.project_name}\n"
        report += f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S' )}\n\n"

        # Estadísticas generales
        total_reqs = len(self.requirements)
        verified_reqs = len([r for r in self.requirements
                            if r.verification_status == VerificationStatus.VERIFIED])

        report += f"Total de requerimientos: {total_reqs}\n"
        report += f"Requerimientos verificados: {verified_reqs}\n"
        report += f"Porcentaje de completitud: {(verified_reqs/total_reqs)*100 if total_reqs > 0 else 0}%\n"

        return report
# Ejemplo de uso
def main():
    """Crear un nuevo documento de requerimientos y generar un reporte"""
    doc = RequirementsDocument("Sistema de Gestión de Inventario")

    # Crear un requerimiento funcional
    req1 = Requirement(
        id="REQ-001",
        title="Registro de Productos",
        description="El sistema debe permitir registrar nuevos productos con: código, nombre, precio y cantidad",
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