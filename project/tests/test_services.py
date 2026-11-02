from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def foundation() -> tuple[
    SmartCareDataStore,
    Patient,
    Practitioner,
    AppointmentService,
]:
    """Create fresh registered participants and services for a supplied
    check.
    """
    data_store = SmartCareDataStore()
    patient = PatientService(data_store).register_patient('P1', 'Alex Example')
    practitioner = PractitionerService(
        data_store,
    ).register_practitioner('D1', 'Taylor Example', 'General')
    return data_store, patient, practitioner, AppointmentService(data_store)


def test_find_patient():
    data_store, patient, _, _ = foundation()
    service = PatientService(data_store)
    assert service.find_patient("P1") is patient


def test_find_unknown_patient():
    data_store, _, _, _ = foundation()
    service = PatientService(data_store)

    with pytest.raises(LookupError):
        service.find_patient("UNKNOWN")


def test_find_practitioner():
    data_store, _, practitioner, _ = foundation()
    service = PractitionerService(data_store)

    assert service.find_practitioner("D1") is practitioner


def test_find_unknown_practitioner():
    data_store, _, _, _ = foundation()
    service = PractitionerService(data_store)

    with pytest.raises(LookupError):
        service.find_practitioner("UNKNOWN")


def test_patient_construction():
    patient = Patient("P1", "Alex Example")

    assert patient.patient_id == "P1"
    assert patient.name == "Alex Example"


# TEST-C02: Blank patient ID is rejected
def test_patient_blank_id_rejected():
    with pytest.raises(ValueError):
        Patient(" ", "Alex Example")


# TEST-C03: Whitespace-only patient name is rejected
def test_patient_blank_name_rejected():
    with pytest.raises(ValueError):
        Patient("P1", "   ")


# TEST-C04: Practitioner construction stores valid values
def test_practitioner_construction():
    practitioner = Practitioner("D1", "Taylor Example", "General")

    assert practitioner.practitioner_id == "D1"
    assert practitioner.name == "Taylor Example"
    assert practitioner.specialty == "General"


# TEST-C05: Blank practitioner ID is rejected
def test_practitioner_blank_id_rejected():
    with pytest.raises(ValueError):
        Practitioner(" ", "Taylor Example", "General")


# TEST-C06: Whitespace-only practitioner name is rejected
def test_practitioner_blank_name_rejected():
    with pytest.raises(ValueError):
        Practitioner("D1", "   ", "General")


# TEST-C07: Whitespace-only practitioner specialty is rejected
def test_practitioner_blank_specialty_rejected():
    with pytest.raises(ValueError):
        Practitioner("D1", "Taylor Example", "   ")


# TEST-C08: Appointment construction stores valid values
def test_appointment_construction():
    patient = Patient("P1", "Alex Example")
    practitioner = Practitioner("D1", "Taylor Example", "General")
    appointment_time = datetime(2026, 10, 1, 9, 0)

    appointment = Appointment(
        "A1", patient, practitioner, appointment_time
    )

    assert appointment.appointment_id == "A1"
    assert appointment.patient is patient
    assert appointment.practitioner is practitioner
    assert appointment.date_time == appointment_time


# TEST-C09: New appointment starts as SCHEDULED
def test_new_appointment_starts_scheduled():
    patient = Patient("P1", "Alex Example")
    practitioner = Practitioner("D1", "Taylor Example", "General")

    appointment = Appointment(
        "A1",
        patient,
        practitioner,
        datetime(2026, 10, 1, 9, 0),
    )

    assert appointment.status is AppointmentStatus.SCHEDULED


# TEST-C10: Cancelling an appointment changes its status
def test_cancellation_changes_status():
    patient = Patient("P1", "Alex Example")
    practitioner = Practitioner("D1", "Taylor Example", "General")

    appointment = Appointment(
        "A1",
        patient,
        practitioner,
        datetime(2026, 10, 1, 9, 0))

    appointment.cancel()

    assert appointment.status is AppointmentStatus.CANCELLED


# TEST-C11: Repeated cancellation is rejected
def test_repeated_cancellation_rejected():
    patient = Patient("P1", "Alex Example")
    practitioner = Practitioner("D1", "Taylor Example", "General")

    appointment = Appointment(
        "A1",
        patient,
        practitioner,
        datetime(2026, 10, 1, 9, 0))

    appointment.cancel()

    with pytest.raises(ValueError):
        appointment.cancel()

    assert appointment.status is AppointmentStatus.CANCELLED


def test_service_cancellation_retains_history():
    data_store, _, _, appointment_service = foundation()

    appointment = appointment_service.book_appointment(
        'A1',
        'P1',
        'D1',
        datetime(2026, 10, 1, 9),
    )

    cancelled = appointment_service.cancel_appointment('A1')

    assert cancelled is appointment
    assert cancelled.status is AppointmentStatus.CANCELLED
    assert data_store.find_appointment('A1') is appointment


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
