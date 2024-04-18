import pytest

from bono.report_reader import ReportReader
from bono.service import Service

@pytest.fixture
def reader():
  reader = ReportReader('input/test_data.pdf')
  reader.load()
  return reader


def test_services_initialized(reader):
  services = reader.services
  assert len(services) == 4


def test_service_types_set(reader):
  services = reader.services.keys()
  assert "COLORECTAL SCREENING" in services
  assert "CHILDHOOD IMMUNIZATION" in services
  assert "MAMMOGRAPHY" in services
  assert "PAP SMEAR" in services


def test_colorectal_counts(reader):
  service: Service = reader.services["COLORECTAL SCREENING"]
  assert service.total_done == 9
  assert service.total_excluded == 7
  assert service.total_skipped == 3


def test_childhood_counts(reader):
  service: Service = reader.services["CHILDHOOD IMMUNIZATION"]
  assert service.total_done == 4
  assert service.total_excluded == 0
  assert service.total_skipped == 0  


def test_mammography_counts(reader):
  service: Service = reader.services["MAMMOGRAPHY"]
  assert service.total_done == 13
  assert service.total_excluded == 0
  assert service.total_skipped == 7  


def test_pap_counts(reader):
  service: Service = reader.services["PAP SMEAR"]
  assert service.total_done == 6
  assert service.total_excluded == 0
  assert service.total_skipped == 2      