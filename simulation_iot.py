import pandas as pd
import random
from datetime import datetime, timedelta
import os

# Definiendo cantidad de registros
num_records = 1000

# Generando datos aleatorios para cada columna
data = {
    "marca_de_tiempo": [(datetime.now() - timedelta(minutes=random.randint(0, 10000))).strftime('%Y-%m-%d %H:%M:%S') for _ in range(num_records)],
    "nivel_de_oxigeno_agua_mg_L": [round(random.uniform(4, 12), 2) for _ in range(num_records)],
    "nivel_de_ph": [round(random.uniform(6.0, 8.5), 2) for _ in range(num_records)],
    "nivel_de_nitratos_ppm": [round(random.uniform(0, 50), 2) for _ in range(num_records)],
    "nivel_de_nitritos_ppm": [round(random.uniform(0, 5), 2) for _ in range(num_records)],
    "temperatura_agua_C": [round(random.uniform(15, 30), 2) for _ in range(num_records)],
    "temperatura_ambiente_C": [round(random.uniform(10, 40), 2) for _ in range(num_records)],
    "humedad_ambiente_%": [round(random.uniform(30, 100), 2) for _ in range(num_records)],
    "cantidad_alimento_g": [round(random.uniform(0, 100), 2) for _ in range(num_records)],
    "flujo_de_agua_L_min": [round(random.uniform(0, 20), 2) for _ in range(num_records)],
    "intensidad_de_luz_lux": [round(random.uniform(0, 100000), 2) for _ in range(num_records)],
    "nivel_de_agua_cm": [round(random.uniform(0, 100), 2) for _ in range(num_records)],
    "estado_filtro": [random.choice(["Limpio", "Necesita limpieza"]) for _ in range(num_records)],
    "consumo_energia_kWh": [round(random.uniform(0, 10), 2) for _ in range(num_records)]
}

# Crear DataFrame
df = pd.DataFrame(data)

# Crear carpeta data
if not os.path.exists('data'):
    os.makedirs('data')

# Guardar como CSV
csv_path = 'data/datos_simulados_sistema_acuaponico.csv'
df.to_csv(csv_path, index=False)

csv_path