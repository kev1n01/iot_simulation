# Define realistic parameter ranges for a hypothetical aquaponic system
# This includes the target and range for each parameter
import pandas as pd

# Load the user's uploaded data to inspect it
file_path = 'datos_simulados_sistema_acuaponico.csv'
data = pd.read_csv(file_path)

# Display the first few rows of the data to understand its structure
data.head()

parameter_ranges = {
    'nivel_de_oxigeno_agua_mg_L': {'min': 5.0, 'max': 8.5, 'target': 7.5, 'adjustment': 'Increase aeration if low, decrease if high'},
    'nivel_de_ph': {'min': 6.5, 'max': 7.5, 'target': 7.0, 'adjustment': 'Add acid to lower pH, base to increase'},
    'nivel_de_nitratos_ppm': {'min': 10.0, 'max': 40.0, 'target': 30.0, 'adjustment': 'Adjust feeding or filtration to regulate'},
    'nivel_de_nitritos_ppm': {'min': 0.0, 'max': 1.0, 'target': 0.5, 'adjustment': 'Increase filtration efficiency'},
    'temperatura_agua_C': {'min': 20.0, 'max': 28.0, 'target': 24.0, 'adjustment': 'Use heaters or coolers to maintain'},
    'temperatura_ambiente_C': {'min': 18.0, 'max': 30.0, 'target': 25.0, 'adjustment': 'Adjust greenhouse temperature'},
    'humedad_ambiente_%': {'min': 40.0, 'max': 70.0, 'target': 55.0, 'adjustment': 'Use humidifiers or dehumidifiers'},
    'cantidad_alimento_g': {'min': 50.0, 'max': 100.0, 'target': 75.0, 'adjustment': 'Feed more if low, reduce if high'},
    'flujo_de_agua_L_min': {'min': 5.0, 'max': 10.0, 'target': 7.5, 'adjustment': 'Adjust pump speed to maintain flow'},
    'intensidad_de_luz_lux': {'min': 10000, 'max': 50000, 'target': 30000, 'adjustment': 'Increase or decrease lighting'},
    'nivel_de_agua_cm': {'min': 20.0, 'max': 80.0, 'target': 50.0, 'adjustment': 'Add or remove water to maintain level'},
}

# Create a DataFrame to store the adjustments
adjustments = []

for index, row in data.iterrows():
    for parameter, limits in parameter_ranges.items():
        if row[parameter] < limits['min'] or row[parameter] > limits['max']:
            adjustment = {
                'marca_de_tiempo': row['marca_de_tiempo'],
                'parameter': parameter,
                'current_value': row[parameter],
                'target_value': limits['target'],
                'adjustment': limits['adjustment']
            }
            adjustments.append(adjustment)

# Convert to DataFrame for export
adjustments_df = pd.DataFrame(adjustments)

# Save the adjustments to an Excel file with filtering and formatting
output_path = './data/ajustes_sistema_acuaponico.xlsx'
with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
    adjustments_df.to_excel(writer, sheet_name='Ajustes', index=False)
    workbook = writer.book
    worksheet = writer.sheets['Ajustes']
    
    # Apply autofilter to all columns
    worksheet.autofilter(0, 0, adjustments_df.shape[0], adjustments_df.shape[1] - 1)
    
    # Add a logo (using a placeholder if logo is not specified)
    worksheet.insert_image('F1', 'https://t3.ftcdn.net/jpg/02/77/90/42/360_F_277904250_ntgzV5Y9aagdBl75ssigmBZx9rXv7xal.jpg',
                           {'x_scale': 0.3, 'y_scale': 0.3, 'x_offset': 15, 'y_offset': 10})
    
    # Set column widths for better readability
    worksheet.set_column('A:A', 20)
    worksheet.set_column('B:B', 25)
    worksheet.set_column('C:D', 15)
    worksheet.set_column('E:E', 30)

output_path
