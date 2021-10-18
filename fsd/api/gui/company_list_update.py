import sqlite3
from config.settings import TEMPLATES
from tabulate import tabulate
import os

# TODO: Automate?

COINFO_DB = os.getenv("COINFO_DB")
QUERY = "SELECT DISTINCT * FROM distinct_coinfo_in_db;"
COMPANY_PAGE = "gui/companies_table.html"


def update_company_table_html():
    """updates the list inside the supported companies page"""
    conn = sqlite3.connect(COINFO_DB)
    c = conn.cursor()
    query = c.execute(QUERY)
    rows = query.fetchall()
    html_table = tabulate(rows, tablefmt="html")
    html_table_clean = html_table.replace("<table>",
                                          "").replace("</table>", "")
    with open(TEMPLATES[0]["DIRS"][0] / COMPANY_PAGE, "w") as f:
        f.write("{% extends " + COMPANY_PAGE +
                " %}\n{% block company_table %}")
        f.write(html_table_clean)
        f.write("{% endblock company_table %}")
    print("Supported company HTML updated.")


if __name__ == "__main__":
    update_company_table_html()
