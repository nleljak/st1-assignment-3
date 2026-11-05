
"""Stage 8 regression tests for SmartCare."""

from datetime import datetime

import pytest

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)
from smartcare.data_store import SmartCareDataStore


def create_test_data():
    """Create a fresh store with synthetic patients and practitioners."""

    store = SmartCareDataStore()

    patient1 = Patient("P001", "Test Patient One")
    patient2 = Patient("P002", "Test Patient Two")

    practitioner1 = Practitioner(
        "PR001", "Test Practitioner One", "GP"
    )
    practitioner2 = Practitioner(
        "PR002", "Test Practitioner Two", "GP"
    )

    store.add_patient(patient1)
    store.add_patient(patient2)

    store.add_practitioner(practitioner1)
    store.add_practitioner(practitioner2)

    return store, patient1, patient2, practitioner1, practitioner2


# F8-01

def test_same_practitioner_overlapping_appointment_is_rejected():
    """Reject two overlapping appointments for the same practitioner."""

    store, patient1, patient2, practitioner1, _ = create_test_data()

    appointment1 = Appointment(
        "A001",
        patient1,
        practitioner1,
        datetime(2026, 11, 10, 10, 0),
    )

    appointment2 = Appointment(
        "A002",
        patient2,
        practitioner1,
        datetime(2026, 11, 10, 10, 0),
    )

    store.add_appointment(appointment1)

    with pytest.raises(ValueError):
        store.add_appointment(appointment2)

    assert store.find_appointment("A001") is appointment1
    assert store.find_appointment("A002") is None


def test_different_practitioners_can_have_same_appointment_time():
    """Allow different practitioners to have appointments simultaneously."""

    store, patient1, patient2, practitioner1, practitioner2 = (
        create_test_data()
    )

    appointment1 = Appointment(
        "A001",
        patient1,
        practitioner1,
        datetime(2026, 11, 10, 10, 0),
    )

    appointment2 = Appointment(
        "A002",
        patient2,
        practitioner2,
        datetime(2026, 11, 10, 10, 0),
    )

    store.add_appointment(appointment1)
    store.add_appointment(appointment2)

    assert store.find_appointment("A001") is appointment1
    assert store.find_appointment("A002") is appointment2


def test_same_practitioner_can_have_non_overlapping_appointments():
    """Allow appointments for the same practitioner at different times."""

    store, patient1, patient2, practitioner1, _ = create_test_data()

    appointment1 = Appointment(
        "A001",
        patient1,
        practitioner1,
        datetime(2026, 11, 10, 10, 0),
    )

    appointment2 = Appointment(
        "A002",
        patient2,
        practitioner1,
        datetime(2026, 11, 10, 11, 0),
    )

    store.add_appointment(appointment1)
    store.add_appointment(appointment2)

    assert store.find_appointment("A001") is appointment1
    assert store.find_appointment("A002") is appointment2

# F8-02:

def test_cancelled_appointment_remains_retrievable():
    """Ensure cancellation does not remove appointment history."""

    store, patient1, _, practitioner1, _ = create_test_data()

    appointment = Appointment(
        "A001",
        patient1,
        practitioner1,
        datetime(2026, 11, 10, 10, 0),
    )

    store.add_appointment(appointment)

    appointment.cancel()

    assert appointment.status == AppointmentStatus.CANCELLED

    retrieved_appointment = store.find_appointment("A001")

    assert retrieved_appointment is appointment


def test_cancelled_appointment_is_not_scheduled():
    """Ensure cancellation changes the appointment status."""

    store, patient1, _, practitioner1, _ = create_test_data()

    appointment = Appointment(
        "A001",
        patient1,
        practitioner1,
        datetime(2026, 11, 10, 10, 0),
    )

    store.add_appointment(appointment)

    appointment.cancel()

    retrieved_appointment = store.find_appointment("A001")

    

    assert retrieved_appointment is not None
    assert retrieved_appointment.status == AppointmentStatus.CANCELLED
    assert retrieved_appointment.status != AppointmentStatus.SCHEDULED

