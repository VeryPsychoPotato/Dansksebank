import os
import pandas as pd
from report_generator import ReportGenerator

output_path = os.path.join(os.path.dirname(__file__), "report.html")

# test data
data = {
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Age": [25, 30, 35, 28],
    "Salary": [50000, 60000, 70000, 65000]
}

df = pd.DataFrame(data)

report = ReportGenerator(df, template_path="C:/Users/Kernius/Danskebank/section4/template.html")

report.render_html("report.html", title="Employee Report")
report.export_excel("report.xlsx")
report.export_txt("report.txt")

print("Report is done")
