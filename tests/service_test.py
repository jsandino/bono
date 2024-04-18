import pytest
import pandas as pd
import numpy as np
from bono.service import ChildhoodImmunization, ColorectalScreening, Mammography, PapSmear, Service
from bono.service_type import ServiceType

@pytest.fixture
def colorectal_sample():
  return pd.DataFrame(
    {
      'PREVENTIVE SERVICE TYPE:  COLORECTAL SCREENING **' : ['HEALTH NUMBER LAST NAME FIRST NAME', 'A', np.nan, 'B', 'C', np.nan, 'D', 'E', 'F', 'G', 'G'],
      'Unnamed: 0' : ['BIRTH DATE', '1968-01-30', np.nan, '1966-10-28', '1966-12-26', np.nan, '1960-04-28', '1967-08-19', '1964-12-13', '1949-10-01', '1949-10-01'],
      'Unnamed: 1' : ['AGE AS OF 2024-03-31', 56, np.nan, 57, 57, np.nan, 63, 56, 59, 74, 74],
      'Unnamed: 2' : ['SERVICE DATE***', '2024-02-22', '2022-01-31', '2022-05-18', '2023-09-15', '2021-10-01', '2022-08-26', np.nan, np.nan, np.nan, np.nan],
      'Unnamed: 3' : ['EXCLUDED DATE', np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, '2022-06-05', np.nan, np.nan, np.nan]
    }
  )

@pytest.fixture
def childhood_sample():
  return pd.DataFrame(
    {
      'PREVENTIVE SERVICE TYPE: CHILDHOOD IMMUNIZATION **' : ['HEALTH NUMBER LAST NAME FIRST NAME', 'A', np.nan, np.nan, np.nan, np.nan, np.nan, 'B', 'B', np.nan],
      'Unnamed: 0' : ['BIRTH DATE', '2021-09-10', np.nan, np.nan, np.nan, np.nan, np.nan, '2021-01-11', '2021-01-11', np.nan],
      'Unnamed: 1' : ['AGE AS OF 2024-03-31', 2.6, np.nan, np.nan, np.nan, np.nan, np.nan, 3.2, 3.2, np.nan],
      'Unnamed: 2' : ['SERVICE DATE***', '2023-03-29', '2022-12-13', '2022-09-13', '2022-03-30', '2022-02-02', '2021-11-24', '2023-01-13', '2023-01-13', '2022-08-09']
    }
  )


def test_get_type_colorectal():
  input = '   PREVENTIVE SERVICE TYPE:  COLORECTAL SCREENING **  '
  type = Service.get_type(input)
  assert type == 'COLORECTAL SCREENING'


def test_get_type_childhood_immunization():
  input = '   PREVENTIVE SERVICE TYPE: CHILDHOOD IMMUNIZATION **   '
  type = Service.get_type(input)
  assert type == 'CHILDHOOD IMMUNIZATION'


def test_get_type_mammography():
  input = '    PREVENTIVE SERVICE TYPE: MAMMOGRAPHY ** '
  type = Service.get_type(input)
  assert type == 'MAMMOGRAPHY'


def test_get_type_pap_smear():
  input = '   PREVENTIVE SERVICE TYPE: PAP SMEAR **   '
  type = Service.get_type(input)
  assert type == 'PAP SMEAR'


def test_create_colorectal():
  service = Service.create(ServiceType.COLORECTAL)
  assert isinstance(service, ColorectalScreening)


def test_create_childhood_immunization():
  service = Service.create(ServiceType.CHILDHOOD)
  assert isinstance(service, ChildhoodImmunization)


def test_create_mammography():
  service = Service.create(ServiceType.MAMMOGRAPHY)
  assert isinstance(service, Mammography)


def test_create_pap_smear():
  service = Service.create(ServiceType.PAP)
  assert isinstance(service, PapSmear)      


def test_create_with_invalid_service_type(capsys):
  with pytest.raises(ValueError) as pytest_error:
    Service.create('garbage')

  assert pytest_error.value.args[0] == "Invalid service type 'garbage'"

def test_is_new_patient_with_id_key(colorectal_sample):
  service = Service.create(ServiceType.COLORECTAL)
  row = colorectal_sample.iloc[0]
  assert service.is_new_patient(row) == False


def test_is_new_patient_with_new_record(colorectal_sample):
  service = Service.create(ServiceType.COLORECTAL)
  row = colorectal_sample.iloc[1]
  assert len(service._processed_records) == 0
  assert service.is_new_patient(row) == True


def test_is_new_patient_with_existing_record(colorectal_sample):
  service = Service.create(ServiceType.COLORECTAL)
  row = colorectal_sample.iloc[1]
  patient_id = row[0]
  service._processed_records.add(patient_id)
  assert service.is_new_patient(row) == False


def test_mark_processed(colorectal_sample):
  service = Service.create(ServiceType.COLORECTAL)
  row = colorectal_sample.iloc[1]
  patient_id = row[0]
  assert len(service._processed_records) == 0
  service._mark_processed(row)
  assert len(service._processed_records) == 1
  assert patient_id in service._processed_records


def test_colorectal_total_done(colorectal_sample):
  service = Service('COLORECTAL')
  assert service.total_done == 0
  service.add_data(colorectal_sample)
  assert service.total_done == 4


def test_colorectal_total_done_updates(colorectal_sample):
  service = Service('COLORECTAL')
  service.add_data(colorectal_sample.iloc[:4])
  assert service.total_done == 2
  service.add_data(colorectal_sample.iloc[4:])
  assert service.total_done == 4


def test_colorectal_total_skipped(colorectal_sample):
  service = Service('COLORECTAL')
  assert service.total_skipped == 0
  service.add_data(colorectal_sample)
  assert service.total_skipped == 2


def test_colorectal_total_skipped_updates(colorectal_sample):
  service = Service('COLORECTAL')
  service.add_data(colorectal_sample.iloc[:9])
  assert service.total_skipped == 1
  service.add_data(colorectal_sample.iloc[9:])
  assert service.total_skipped == 2


def test_colorectal_total_excluded(colorectal_sample):
  service = Service('COLORECTAL')
  assert service.total_skipped == 0
  service.add_data(colorectal_sample)
  assert service.total_excluded == 1  


def test_colorectal_total_target(colorectal_sample):
  service = Service('COLORECTAL')
  assert service.total_target == 0
  service.add_data(colorectal_sample)
  assert service.total_target == 6


def test_colorectal_percent_done(colorectal_sample):
  service = Service('COLORECTAL')
  service.add_data(colorectal_sample)
  # Total patients = 4 done + 1 excluded + 2 skipped = 7
  assert service.percent_done == 57.14


def test_colorectal_percent_skipped(colorectal_sample):
  service = Service('COLORECTAL')
  service.add_data(colorectal_sample)
  # Total patients = 4 done + 1 excluded + 2 skipped = 7
  assert service.percent_skipped == 28.57


def test_colorectal_percent_excluded(colorectal_sample):
  service = Service('COLORECTAL')
  service.add_data(colorectal_sample)
  # Total patients = 4 done + 1 excluded + 2 skipped = 7
  assert service.percent_excluded == 14.29  


def test_colorectal_percent_target_done(colorectal_sample):
  service = Service('COLORECTAL')
  service.add_data(colorectal_sample)
  # Total target population = 4 done + 2 skipped = 6
  assert service.percent_target_done == 66.67  


def test_childhood_total_done(childhood_sample):
  service = Service.create(ServiceType.CHILDHOOD)
  assert service.total_done == 0
  service.add_data(childhood_sample)
  assert service.total_done == 2


def test_childimmu_total_done_updates(childhood_sample):
  service = Service.create(ServiceType.CHILDHOOD)
  service.add_data(childhood_sample.iloc[:4])
  assert service.total_done == 1
  service.add_data(childhood_sample.iloc[4:])
  assert service.total_done == 2


def test_childhood_total_skipped(childhood_sample):
  service = Service.create(ServiceType.CHILDHOOD)
  assert service.total_skipped == 0
  service.add_data(childhood_sample)
  assert service.total_skipped == 0


def test_childhood_total_excluded(childhood_sample):
  service = Service.create(ServiceType.CHILDHOOD)
  assert service.total_skipped == 0
  service.add_data(childhood_sample)
  assert service.total_excluded == 0


def test_childhood_percent_done(childhood_sample):
  service = Service.create(ServiceType.CHILDHOOD)
  service.add_data(childhood_sample)
  # Total patients = 2 done + 0 excluded + 0 skipped = 2
  assert service.percent_done == 100.0


def test_childhood_percent_skipped(childhood_sample):
  service = Service.create(ServiceType.CHILDHOOD)
  service.add_data(childhood_sample)
  # Total patients = 4 done + 0 excluded + 0 skipped = 0
  assert service.percent_skipped == 0


def test_childhood_percent_excluded(childhood_sample):
  service = Service.create(ServiceType.CHILDHOOD)
  service.add_data(childhood_sample)
  # Total patients = 4 done + 0 excluded + 0 skipped = 0
  assert service.percent_excluded == 0  


def test_childhood_percent_target_done(childhood_sample):
  service = Service.create(ServiceType.CHILDHOOD)
  service.add_data(childhood_sample)
  # Total target population = 4 done + 0 skipped = 4
  assert service.percent_target_done == 100.0 
  
