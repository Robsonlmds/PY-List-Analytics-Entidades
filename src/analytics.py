from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.oauth2 import service_account
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Metric
import csv
import calendar
from datetime import datetime

# Caminho para o arquivo de credenciais
KEY_PATH = "credentials/service-account.json"

# ID da propriedade GA4
PROPERTY_ID = "318840837"

# Escolher o mês desejado (Exemplo: Janeiro)
year = datetime.today().year  # Ano atual
month = 1  # Janeiro (mude para outro mês se necessário)

# Obter o último dia do mês corretamente
_, last_day = calendar.monthrange(year, month)

# Definir as datas de início e fim do mês escolhido
start_date = f"{year}-{month:02d}-01"
end_date = f"{year}-{month:02d}-{last_day}"

# Criar cliente da API
credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
client = BetaAnalyticsDataClient(credentials=credentials)

# Definir a consulta com métricas importantes
date_range = DateRange(start_date=start_date, end_date=end_date)
metrics = [
    Metric(name="screenPageViews"),  # Visualizações de página (Views)
    Metric(name="activeUsers"),      # Usuários Ativos
    Metric(name="newUsers"),         # Novos Usuários
    Metric(name="sessions"),         # Sessões
    Metric(name="bounceRate")        # Taxa de Rejeição
]

# Construir o request corretamente
request = RunReportRequest(
    property=f"properties/{PROPERTY_ID}",
    date_ranges=[date_range],
    metrics=metrics
)

# Executar a consulta
response = client.run_report(request)

# Definir o nome do arquivo de saída
output_file = f"analytics_report_{year}_{month:02d}.csv"

# Criar e escrever no arquivo CSV
with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # Escrever o cabeçalho
    writer.writerow(["Metric", "Value"])

    # Escrever os dados
    for row in response.rows:
        views = row.metric_values[0].value        # Visualizações
        active_users = row.metric_values[1].value # Usuários Ativos
        new_users = row.metric_values[2].value    # Novos Usuários
        sessions = row.metric_values[3].value     # Sessões
        bounce_rate = row.metric_values[4].value  # Taxa de Rejeição
        
        # Escrever no arquivo CSV
        writer.writerow(["Views", views])
        writer.writer