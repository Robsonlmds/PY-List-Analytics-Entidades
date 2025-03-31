from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.oauth2 import service_account
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Metric
import csv
import calendar
from datetime import datetime

KEY_PATH = "credentials/service-account.json"

def read_properties(file_path):
    properties = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split("\t")
            if len(parts) == 2:
                properties.append((parts[0], parts[1]))  
    return properties

def get_report_date(year=None, month=None):
    if not year:
        year = datetime.today().year  # Ano atual
    if not month:
        month = 2  # Mês de consulta

    _, last_day = calendar.monthrange(year, month)

    start_date = f"{year}-{month:02d}-01"
    end_date = f"{year}-{month:02d}-{last_day}"

    return start_date, end_date

properties = read_properties("propiedades.txt")

year = 2025  # Ano de 2025
month = 2  # Mês de consulta

start_date, end_date = get_report_date(year, month)

credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
client = BetaAnalyticsDataClient(credentials=credentials)

metrics = [
    Metric(name="screenPageViews"),  
    Metric(name="activeUsers"),      
    Metric(name="newUsers"),        
    Metric(name="sessions"),       
    Metric(name="bounceRate")       
]

output_file = f"analytics_report_{year}_{month:02d}.csv"

property_metrics = {}

for property_name, property_id in properties:
    date_range = DateRange(start_date=start_date, end_date=end_date)

    request = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[date_range],
        metrics=metrics
    )

    try:
        response = client.run_report(request)

        if response.rows:  
            metrics_values = {
                "Views": response.rows[0].metric_values[0].value,
                "Active Users": response.rows[0].metric_values[1].value,
                "New Users": response.rows[0].metric_values[2].value,
                "Sessions": response.rows[0].metric_values[3].value,
                "Bounce Rate": response.rows[0].metric_values[4].value
            }

            property_metrics[property_name] = metrics_values
        else:
            property_metrics[property_name] = {
                "Views": "No data",
                "Active Users": "No data",
                "New Users": "No data",
                "Sessions": "No data",
                "Bounce Rate": "No data"
            }

    except Exception as e:
        print(f"Erro ao coletar dados para a propriedade {property_name}: {e}")
        property_metrics[property_name] = {
            "Views": "Error",
            "Active Users": "Error",
            "New Users": "Error",
            "Sessions": "Error",
            "Bounce Rate": "Error"
        }

with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    writer.writerow(["Property Name", "Views", "Active Users", "New Users", "Sessions", "Bounce Rate"])

    for property_name, metrics_values in property_metrics.items():
        writer.writerow([property_name, 
                         metrics_values["Views"], 
                         metrics_values["Active Users"], 
                         metrics_values["New Users"], 
                         metrics_values["Sessions"], 
                         metrics_values["Bounce Rate"]])

print(f"Dados de {year}-{month:02d} salvos em {output_file}")
