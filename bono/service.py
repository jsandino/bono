from abc import ABC
import re
import pandas as pd
from pandas import DataFrame

from bono.service_type import ServiceType

"""
A type of preventive service offered during the calendar year.
"""
class Service:

  service_type_key = 'PREVENTIVE SERVICE TYPE'

  patient_id_key = 'HEALTH NUMBER LAST NAME FIRST NAME'

  def __init__(self, type: ServiceType, has_excluded_date=True):
    self.type = type
    self._done = 0
    self._skipped = 0
    self._excluded = 0
    self._has_excluded_date = has_excluded_date
    self._processed_records = set()


  @staticmethod
  def create(service_type):
    match(service_type):
      case ServiceType.COLORECTAL: return ColorectalScreening()
      case ServiceType.CHILDHOOD: return ChildhoodImmunization()
      case ServiceType.MAMMOGRAPHY: return Mammography()
      case ServiceType.PAP: return PapSmear()
      case ServiceType.INFLUENZA: return Influenza()

    raise ValueError(f"Invalid service type '{service_type}'")


  @classmethod
  def get_type(cls, text):
    result = re.search(fr'{cls.service_type_key}:\s+(\w+\s?\w+)\s+\\*\\*', text.strip())
    if not result:
      raise Exception(f'Service type not found in: {text}')
    
    return result[1]
  

  @property
  def patient_id_index(self):
    return 0

  @property
  def age_index(self):
    return 2


  @property
  def service_date_index(self):
    return 3


  @property
  def excluded_date_index(self):
    return 4


  @property
  def total_done(self):
    return self._done
  

  @property
  def total_skipped(self):
    return self._skipped
  

  @property
  def total_excluded(self):
    return self._excluded
  

  @property
  def total_target(self):
    return self._done + self._skipped
  

  @property
  def total_patients(self):
    return self._done + self._skipped + self._excluded
  

  def add_data(self, data: DataFrame):
    for idx, row in data.iterrows():
      is_data_row = idx != 0
      if self.is_new_patient(row) and is_data_row:
        self._update_done(row)
        self._update_skipped(row)
        self._update_excluded(row)
        self._mark_processed(row)


  """
  Determines whether or not the row corresponds to a new patient record.

  Some patients have multiple records (ie table spanning across two pages);
  we only want to process one row per patient.
  """
  def is_new_patient(self, row):
    id = row[self.patient_id_index]
    return id != Service.patient_id_key and id not in self._processed_records
  

  def _mark_processed(self, row):
    id = row[self.patient_id_index]
    self._processed_records.add(id)


  def _update_done(self, row):
    # There could be multiple rows with different service dates for the same patient:
    # use the age column to filter duplicate rows, to ensure a patient is only counted once    
    age, service_date = row[self.age_index], row[self.service_date_index]
    if _valid(age) and _valid(service_date):
      # print(f'row: {row}')
      self._done += 1


  def _update_skipped(self, row):
    service_date = row[self.service_date_index]
    if self._has_excluded_date:
      excluded_date = row[self.excluded_date_index]
      if _invalid(service_date) and _invalid(excluded_date):
        self._skipped += 1
    else:
      if _invalid(service_date):
        self._skipped += 1


  def _update_excluded(self, row):
    if self._has_excluded_date:
      excluded_date = row[self.excluded_date_index]
      if _valid(excluded_date):
        self._excluded += 1


  @property
  def percent_done(self):
    if self._total_patients:
      total = (self._done / self._total_patients) * 100
      return round(total, 2)
    else:    
      return 0
  

  @property
  def percent_skipped(self):
    if self._total_patients:
      total = (self._skipped / self._total_patients) * 100
      return round(total, 2)
    else:
      return 0
  

  @property
  def percent_excluded(self):
    if self._total_patients:
      total = (self._excluded / self._total_patients) * 100
      return round(total, 2)
    else:
      return 0
  

  @property
  def percent_target_done(self):
    if self.total_target:
      total = (self._done / self.total_target) * 100
      return round(total, 2)
    else:
      return 0


  @property
  def _total_patients(self):
    return self._done + self._skipped + self._excluded

"""
COLORECTAL SCREENING
"""
class ColorectalScreening(Service):
  def __init__(self):
    super().__init__(ServiceType.COLORECTAL)


"""
CHILDHOOD IMMUNIZATION
"""
class ChildhoodImmunization(Service):
  def __init__(self):
    super().__init__(ServiceType.CHILDHOOD, has_excluded_date=False)


"""
MAMMOGRAPHY
"""
class Mammography(Service):
  def __init__(self):
    super().__init__(ServiceType.MAMMOGRAPHY)


  @property
  def age_index(self):
    return 3


  @property
  def service_date_index(self):
    return 4


  @property
  def excluded_date_index(self):
    return 5 


"""
PAP SMEAR
"""
class PapSmear(Service):
  def __init__(self):
    super().__init__(ServiceType.PAP)


  @property
  def age_index(self):
    return 3


  @property
  def service_date_index(self):
    return 4


  @property
  def excluded_date_index(self):
    return 5             


"""
INFLUENZA
"""
class Influenza(Service):
  def __init__(self):
    super().__init__(ServiceType.INFLUENZA, has_excluded_date=False)


  @property
  def age_index(self):
    return 3


  @property
  def service_date_index(self):
    return 4


"""
Helper, top-level functions
"""
def _valid(value):
  return not _invalid(value)


def _invalid(value):  
  return pd.isnull(value)

