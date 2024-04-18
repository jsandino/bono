from pandas import DataFrame
from tabula import read_pdf

from bono.service import Service

class ReportReader:

  def __init__(self, filename):
    self.filename = filename
    self._services = dict()


  def load(self):
    dfs = read_pdf(self.filename, stream=True, columns=[128.05, 691.15, 706.35, 789.85, 803.5], pages="all")
    # dfs = read_pdf(self.filename, stream=True, columns=[128.05, 691.15, 706.35, 789.85, 803.5], pages=[1,2])
    # print(dfs[0])
    # print("-----")
    # print(dfs[2])
    # print("-----")
    # print(dfs[4])
    # print("-----")
    # print(dfs[6])    


    for df in dfs:
      try:
        service: Service = self._get_service(df)
        service.add_data(df)
        self._update_service(service)
      except Exception as e:
        print(e)


  def _get_service(self, df: DataFrame):
    service_type = Service.get_type(list(df)[0])
    service = self._services.get(service_type, Service.create(service_type))
    return service


  @property
  def services(self):
    return self._services.copy()
  

  def _update_service(self, service: Service):
    self._services[service.type] = service


  def summary(self) -> str:
    results = []
    results.append('\n')
    for k, v in self.services.items():
      results.append(k)
      results.append('=' * len(k))
      results.append('')
      results.append(f'Total patients: {v.total_patients:>12}')
      results.append(f'Total target population: {v.total_target:>3}')
      results.append(f'Patients examined: {v.total_done:>9} ({v.percent_done}%)')
      results.append(f'Patients not examined: {v.total_skipped:>5} ({v.percent_skipped}%)')
      results.append(f'Patients excluded: {v.total_excluded:>9} ({v.percent_excluded}%)')
      results.append(f'Target population covered: {v.percent_target_done:>3}%')
      results.append('\n')

    return "\n".join(results)
