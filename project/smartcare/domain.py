"""SmartCare objects and their local validation rules."""


from datetime import datetime
from enum import Enum


def required_text(value: str, label: str) -> str:
    """Return trimmed non-blank text; raise ValueError for invalid text."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{label} cannot be blank')
    return value.strip()


def validate_date_time(value: datetime) -> datetime:
    """Return a naive, minute-precision datetime; otherwise raise
    ValueError.
    """
    if not isinstance(value, datetime):
        raise ValueError('Date/time must be a datetime value')
    if value.tzinfo is not None or value.second != 0 or value.microsecond != 0:
        raise ValueError('Use a local date/time at minute precision')
    return value


class AppointmentStatus(Enum):
    """The supported appointment states; only guarded operations change
    state.
    """
    SCHEDULED = 'scheduled'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'


class Patient:
    """A patient with a validated name and read-only identity."""

    def __init__(self, patient_id: str, name: str) -> None:
        """Initialise validated fields; raise ValueError for invalid
        values.
        """
        self._patient_id = required_text(patient_id, 'Patient ID')
        self.name = required_text(name, 'Patient name')

    @property
    def patient_id(self) -> str:
        """Return the patient identity supplied at construction."""
        return self._patient_id

def update_details(self, name: str) -> None:
    """Update the patient's name after validation."""
    self.name = required_text(name, 'Patient name')

class Practitioner:
    """A practitioner with validated identity, name and specialty."""

    def __init__(
        self,
        practitioner_id: str,
        name: str,
        specialty: str,
    ) -> None:
        """Initialise validated fields; raise ValueError for invalid
        values.
        """
        self._practitioner_id = required_text(
            practitioner_id,
            'Practitioner ID',
        )
        self.name = required_text(name, 'Practitioner name')
        self.specialty = required_text(specialty, 'Specialty')

    @property
    def practitioner_id(self) -> str:
        """Return the practitioner identity supplied at construction."""
        return self._practitioner_id


class Appointment:
    """An appointment linking participant objects with guarded status
    changes.
    """

    def __init__(
        self,
        appointment_id: str,
        patient: Patient,
        practitioner: Practitioner,
        date_time: datetime,
        status: AppointmentStatus = AppointmentStatus.SCHEDULED,
    ) -> None:
        """Initialise validated fields; raise ValueError for invalid
        values.
        """
        self._appointment_id = required_text(appointment_id, 'Appointment ID')
        if not isinstance(patient, Patient):
            raise ValueError('Appointment requires a Patient object')
        if not isinstance(practitioner, Practitioner):
            raise ValueError('Appointment requires a Practitioner object')
        if not isinstance(status, AppointmentStatus):
            raise ValueError('Invalid appointment status')
        self._patient = patient
        self._practitioner = practitioner
        self._date_time = validate_date_time(date_time)
        self._status = status

    @property
    def appointment_id(self) -> str:
        """Return the immutable appointment identity."""
        return self._appointment_id

    @property
    def patient(self) -> Patient:
        """Return the patient object associated with this appointment."""
        return self._patient

    @property
    def practitioner(self) -> Practitioner:
        """Return the practitioner object associated with this appointment."""
        return self._practitioner

    @property
    def date_time(self) -> datetime:
        """Return the appointment time."""
        return self._date_time

    @property
    def status(self) -> AppointmentStatus:
        """Return the current appointment status."""
        return self._status

    def cancel(self) -> None:
        """Cancel a SCHEDULED appointment without deleting it.

        Raise ValueError for an illegal transition; leave failed state
        unchanged.
        """
        if self.status is not AppointmentStatus.SCHEDULED:
            raise ValueError('Only SCHEDULED appointments may be cancelled')
        self._status = AppointmentStatus.CANCELLED

#stage 8

def test_patient_update_details():
    patient = Patient("P1", "Alex Example")

    patient.update_details("Alex Smith")

    assert patient.name == "Alex Smith"


def test_patient_update_details_rejects_blank_name():
    patient = Patient("P1", "Alex Example")

    with pytest.raises(ValueError):
        patient.update_details("")

    assert patient.name == "Alex Example"
