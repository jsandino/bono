import sys
from bono.report_reader import ReportReader

default_report = "input/Bono2024.pdf"

def main():  
  report = sys.argv[1] if len(sys.argv) == 2 else default_report
  reader = ReportReader(report)
  reader.load()
  print(reader.summary())

if __name__ == "__main__":
  main()