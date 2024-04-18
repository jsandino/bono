from report_reader import ReportReader

def main():
  reader = ReportReader("input/Bono2024.pdf")
  # reader = ReportReader("input/test_data.pdf")
  reader.load()
  print(reader.summary())

if __name__ == "__main__":
  main()