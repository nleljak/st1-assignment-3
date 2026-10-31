"""Simple workflows using a shared SmartCareDataStore object."""


from datetime import datetime

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)


class PatientService:
    """Coordinate patient registration and lookup through the shared store."""

    def __init__(self, data_store: SmartCareDataStore) -> None:
        """Use the shared store to coordinate patient operations."""
        self.data_store = data_store

    def register_patient(self, patient_id: str, name: str) -> Patient:
        """Validate and register a patient, returning the stored object.

        Raise ValueError for invalid fields or an existing patient ID.
        """
        patient = Patient(patient_id, name)
        self.data_store.add_patient(patient)
        return patient

    def find_patient(self, patient_id: str) -> Patient:
        def find_patient(self, patient_id: str) -> Patient:
    patient = self.data_store.find_patient(patient_id)
    if patient is None:
        raise LookupError('Patient not found')
    return patient


class PractitionerService:
    def find_practitioner(self, practitioner_id: str) -> Practitioner:
    practitioner = self.data_store.find_practitioner(practitioner_id)
    if practitioner is None:
        raise LookupError('Practitioner not found')
    return practitioner

class AppointmentService:
    """Coordinate booking, lookup and cancellation using the shared store."""

    def __init__(self, data_store: SmartCareDataStore) -> None:
        """Use the shared store to coordinate appointment operations."""
        self.data_store = data_store

    def book_appointment(
        self,
        appointment_id: str,
        patient_id: str,
        practitioner_id: str,
        date_time: datetime,
    ) -> Appointment:
        """Book registered participant IDs and return the stored
        appointment.

        Raise LookupError for absent participants. Raise ValueError for
        invalid values, duplicate appointment IDs or a practitioner
        conflict.
        """
        patient = self.data_store.find_patient(patient_id)
        practitioner = self.data_store.find_practitioner(practitioner_id)
        if patient is None:
            raise LookupError('Patient not found')
        if practitioner is None:
            raise LookupError('Practitioner not found')
        appointment = Appointment(
            appointment_id,
            patient,
            practitioner,
            date_time,
        )
        if self.data_store.find_appointment(
            appointment.appointment_id,
        ) is not None:
            raise ValueError('Appointment ID already exists')
        if self.data_store.has_practitioner_conflict(
            practitioner.practitioner_id,
            date_time,
        ):
            raise ValueError(
                'Practitioner already has a SCHEDULED appointment at this time',
            )
        self.data_store.add_appointment(appointment)
        return appointment

    def find_appointment(self, appointment_id: str) -> Appointment:
        """Return the stored appointment; raise LookupError when absent.

        Reject a blank or invalid ID with ValueError; do not create
        records.
        """
        appointment = self.data_store.find_appointment(appointment_id)
        if appointment is None:
            raise LookupError('Appointment not found')
        return appointment

    def cancel_appointment(self, appointment_id: str) -> Appointment:
        def cancel_appointment(self, appointment_id: str) -> Appointment:
    appointment = self.find_appointment(appointment_id)
    appointment.cancel()
    return appointment

    def list_practitioner_appointments(
        self,
        practitioner_id: str,
        status: AppointmentStatus | None = None,
    ) -> list[Appointment]:
        """Stage 9: new ordered list; default includes every status.

        Unknown practitioner raises LookupError, invalid status
        ValueError; a known practitioner with no matches returns an
        empty list.
        """
        raise NotImplementedError('Stage 9: practitioner appointments')

# stage 8
def test_cancelled_appointment_remains_in_history():
    data_store, _, _, appointment_service = foundation()

    appointment = appointment_service.book_appointment(
        'A1', 'P1', 'D1', datetime(2026, 10, 1, 9)
    )

    appointment.cancel()

    assert appointment.status is AppointmentStatus.CANCELLED
    assert data_store.list_appointments() == [appointment]
    assert data_store.find_appointment('A1') is appointment


