import sqlite3
from config.settings import DATABASES, TEMPLATES
from tabulate import tabulate


def update_company_table_html():
    """updates the list of supported companies page"""
    conn = sqlite3.connect(str(DATABASES["default"]["NAME"]))
    c = conn.cursor()

    query = c.execute("SELECT DISTINCT * FROM distinct_coinfo_in_db;")
    rows = query.fetchall()
    html_table = tabulate(rows, tablefmt="html")
    html_table_clean = html_table.replace("<table>", "").replace("</table>", "")
    with open(TEMPLATES[0]["DIRS"][0] / "gui/companies_table.html", "w") as f:
        f.write("{% extends 'gui/companies.html' %}\n{% block company_table %}")
        f.write(html_table_clean)
        f.write("{% endblock company_table %}")
    print("Supported company HTML updated.")


if __name__ == "__main__":
    update_company_table_html()
