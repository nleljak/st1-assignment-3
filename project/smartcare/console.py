"""Console helpers and a small runnable starting demonstration."""


import re
from datetime import datetime

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def parse_date_time(text: str) -> datetime:
    """Parse YYYY-MM-DD HH:MM; raise ValueError for invalid input."""
    if (
        not isinstance(text, str)
        or re.fullmatch(
            '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}', text
        ) is None
    ):
        raise ValueError('Use date/time format YYYY-MM-DD HH:MM')
    try:
        return datetime.strptime(text, '%Y-%m-%d %H:%M')
    except ValueError:
        raise ValueError(
            'Invalid calendar date/time; use YYYY-MM-DD HH:MM',
        ) from None


def format_appointment(appointment: Appointment) -> str:
    """Return readable synthetic appointment details without changing
    state.
    """
    return (
        f'{appointment.appointment_id}: '
        f'{appointment.patient.patient_id} with '
        f'{appointment.practitioner.practitioner_id}, '
        f'{appointment.date_time:%Y-%m-%d %H:%M}, {appointment.status.value}'
    )


def run_demo() -> None:
    """Demonstrate supplied registration and booking using synthetic
    records.
    """
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)
    patients.register_patient('P1', 'Alex Example')
    practitioners.register_practitioner(
        'DR1',
        'Taylor Example',
        'General practice',
    )
    try:
        appointments.book_appointment(
            'A1',
            'P1',
            'DR1',
            parse_date_time('2026-10-01 09:00'),
        )
        print(format_appointment(appointments.find_appointment('A1')))
    except (ValueError, LookupError) as error:
        print(f'Error: {error}')
    print('Session-only data: records are lost on exit.')


def menu_option() -> None:
    print(f'---SmartCare Menu---')
    print(f'------------')
    print('Session-only data: records are lost on exit.')
    print(f'------------')
    print(f'[1] Register Patient')
    print(f'[2] Find Patient')
    print(f'[3] Register Practitioner')
    print(f'[4] Find Practitioner')
    print(f'[5] Book Appointment')
    print(f'[6] Cancel Appointment')
    print(f'[7] Find Appointments')
    print(f'[8] List Practitioner Appointments')
    print(f'[0] Exit')


def run_menu() -> None:
    """Stage 9: implement the register/find/book/cancel/list/exit menu.

    Call services, recover from expected input errors, and keep this
    session's data until exit. main.py reports the incomplete menu
    without crashing.
    """

    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)

    def menu_register_patient():
        patient_id = str(input('Enter Patient ID:'))
        patient_name = str(input('Enter Patient name:'))
        patient = patients.register_patient(patient_id, patient_name)
        print(f'Patient registered successfully')
        print(f'Patient ID: {patient.patient_id}')
        print(f'Name: {patient.name}')

    def menu_find_patient():
        patient_id = str(input('Enter Patient ID:'))
        patient = patients.find_patient(patient_id)
        print(f'Patient Found. {patient.patient_id}:{patient.name}')
        print(f'Patient ID: {patient.patient_id}')
        print(f'Name: {patient.name}')

    def menu_register_practitioner():
        practitioner_id = str(input('Enter Practitioner ID:'))
        practitioner_name = str(input('Enter Practitioner Name:'))
        practitioner_specialty = str(input('Enter Practitioner Specialty:'))

        practitioner = practitioners.register_practitioner(
            practitioner_id, practitioner_name, practitioner_specialty)

        print(f'Practitioner registered successfully')
        print(f'Practitioner ID: {practitioner.practitioner_id}')
        print(f'Name: {practitioner.name}')
        print(f'Specialty: {practitioner.specialty}')

    def menu_find_practitioner():
        practitioner_id = str(input('Enter Practitioner ID:'))
        practitioner = practitioners.find_practitioner(practitioner_id)

        print(f'Practitioner found.'
              f' {practitioner.practitioner_id}:,'
              f' {practitioner.name},'
              f' {practitioner.specialty}')

        print(f'Practitioner ID: {practitioner.practitioner_id}')
        print(f'Name: {practitioner.name}')
        print(f'Specialty: {practitioner.specialty}')

    def menu_book_appointment():
        appointment_id = str(input('Enter Appointment ID:'))
        patient_id = str(input('Enter Patient ID:'))
        practitioner_id = str(input('Enter Practitioner ID:'))
        date_time = parse_date_time(str(input("Enter Date Time in the following Format 'YYYY-MM-DD HH:MM':")))

        appointment = appointments.book_appointment(appointment_id, patient_id, practitioner_id, date_time)

        print(f'Appointment booked successfully.')
        print(f'Appointment ID:{appointment.appointment_id}')
        print(f'Patient: {appointment.patient.name} ({appointment.patient.patient_id})')
        print(f'Practitioner: {appointment.practitioner.name} ({appointment.practitioner.practitioner_id})')
        print(f'Specialty: {appointment.practitioner.specialty}')
        print(f'Date/Time: {appointment.date_time}')
        print(f'Status: {appointment.status.value}')
        print(f'Reference: {format_appointment(appointment)}')

    def menu_cancel_appointment():
        appointment_id = str(input('Enter Appointment ID:'))

        appointment = appointments.cancel_appointment(appointment_id)

        print(f'Appointment cancelled successfully.')
        print(f'Appointment ID:{appointment.appointment_id}')
        print(f'Patient: {appointment.patient.name} ({appointment.patient.patient_id})')
        print(f'Practitioner: {appointment.practitioner.name} ({appointment.practitioner.practitioner_id})')
        print(f'Specialty: {appointment.practitioner.specialty}')
        print(f'Date/Time: {appointment.date_time}')
        print(f'Status: {appointment.status.value}')
        print(f'Reference: {format_appointment(appointment)}')

    def menu_find_appointment():
        appointment_id = str(input('Enter Appointment ID:'))

        appointment = appointments.find_appointment(appointment_id)

        print(f'Appointment found.')
        print(f'Appointment ID:{appointment.appointment_id}')
        print(f'Patient: {appointment.patient.name} ({appointment.patient.patient_id})')
        print(f'Practitioner: {appointment.practitioner.name} ({appointment.practitioner.practitioner_id})')
        print(f'Specialty: {appointment.practitioner.specialty}')
        print(f'Date/Time: {appointment.date_time}')
        print(f'Status: {appointment.status.value}')
        print(f'Reference: {format_appointment(appointment)}')

    def menu_list_practitioner_appointments():
        practitioner_id = str(input('Enter Practitioner ID:'))
        status_filter = str(input('Status filter [scheduled, cancelled, completed, blank = all]'))

        appointment = appointments.list_practitioner_appointments(practitioner_id, status_filter)

        print(f'Appointments for {appointment.practitioner.name} ({appointment.practitioner.practitioner_id})')
        print(f'Filter:')

    while True:
        menu_option()
        try:
            user_choice = int(input("Enter a your choice: "))

            if user_choice == 0:
                print(f'Exiting SmartCare')
                break

            if user_choice > 8:
                print(f'Unknown Choice. Choose a number between 0 to 8.')

            if user_choice == 1:
                try:
                    menu_register_patient()
                except Exception as e:
                    print(f"{e}")

            if user_choice == 2:
                try:
                    menu_find_patient()
                except Exception as e:
                    print(f"{e}")

            if user_choice == 3:
                try:
                    menu_register_practitioner()
                except Exception as e:
                    print(f"{e}")

            if user_choice == 4:
                try:
                    menu_find_practitioner()
                except Exception as e:
                    print(f"{e}")

            if user_choice == 5:
                try:
                    menu_book_appointment()
                except Exception as e:
                    print(f"{e}")

            if user_choice == 6:
                try:
                    menu_cancel_appointment()
                except Exception as e:
                    print(f"{e}")

            if user_choice == 7:
                try:
                    menu_find_appointment()
                except Exception as e:
                    print(f"{e}")

            if user_choice == 8:
                try:
                    menu_list_practitioner_appointments()
                except Exception as e:
                    print(f"{e}")

        except ValueError:
            print(f'Enter a valid number!')
