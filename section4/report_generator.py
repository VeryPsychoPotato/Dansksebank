import pandas as pd
from jinja2 import Environment, FileSystemLoader
from typing import Dict, Any
import os


class ReportGenerator:
    def __init__(self, df: pd.DataFrame, template_path: str):
        self.df = df
        self.template_path = os.path.abspath(template_path)
        template_dir = os.path.dirname(self.template_path)
        template_file = os.path.basename(self.template_path)
        self.env = Environment(
            loader=FileSystemLoader(template_dir)
        )

        self.template = self.env.get_template(template_file)
        print("TEMPLATE PATH:", self.template_path)
        print("TEMPLATE EXISTS:", os.path.exists(self.template_path))

    def _generate_summary(self) -> Dict[str, Any]:
        summary = {
            "num_rows": len(self.df),
            "num_columns": len(self.df.columns),
            "columns": list(self.df.columns),
        }

        # table statistics
        numeric_df = self.df.select_dtypes(include="number")
        if not numeric_df.empty:
            summary["numeric_summary"] = numeric_df.describe().to_dict()

        return summary

    def render_html(self, output_path: str, title: str = "Report") -> None:

        summary = self._generate_summary()

        html_content = self.template.render(
            title=title,
            summary=summary,
            table=self.df.to_html(index=False, classes="table table-striped")
        )

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print("ABSOLUTE OUTPUT FILE:")
        print(os.path.abspath(output_path))
        print("FILE EXISTS:", os.path.exists(output_path))
        
    def export_excel(self, output_path: str) -> None: 
        self.df.to_excel(output_path, index=False)

    def export_txt(self, output_path: str) -> None:
        summary = self._generate_summary()
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("---- REPORT SUMMARY----\n")
            f.write(f"Rows: {summary['num_rows']}\n")
            f.write(f"Columns: {summary['num_columns']}\n")
            f.write(f"Column Names: {', '.join(summary['columns'])}\n\n")
            if "numeric_summary" in summary:
                f.write("---- NUMERIC SUMMARY----\n")
                for col, stats in summary["numeric_summary"].items():
                    f.write(f"\n{col}:\n")
                    for stat_name, value in stats.items():
                        f.write(f"  {stat_name}: {value}\n")

            f.write("\n----DATA TABLE----\n")
            f.write(self.df.to_string(index=False))