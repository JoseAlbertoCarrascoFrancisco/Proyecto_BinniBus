import csv

# ========================
# CONFIGURA TUS ARCHIVOS
# ========================
stops_original = "stops.txt"   # <-- archivo con IDs viejos
stop_times_file = "stop_times.txt"
output_file = "stop_times_nuevo.txt"

# ========================
# PASO 1: CREAR MAPPING
# ========================
mapping = {}

with open(stops_original, newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    
    header = next(reader)  # saltar encabezado

    for i, row in enumerate(reader, start=1):
        old_id = row[0]
        mapping[old_id] = str(i)

print(f"✅ Mapping creado con {len(mapping)} elementos")

# ========================
# PASO 2: REEMPLAZAR IDs
# ========================
no_encontrados = 0

with open(stop_times_file, newline='', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    header = next(reader)
    writer.writerow(header)

    for row in reader:
        old_stop_id = row[3]  # columna stop_id

        if old_stop_id in mapping:
            row[3] = mapping[old_stop_id]
        else:
            no_encontrados += 1
            print(f"⚠️ No encontrado: {old_stop_id}")

        writer.writerow(row)

print("===================================")
print(f"✅ Archivo generado: {output_file}")
print(f"⚠️ IDs no encontrados: {no_encontrados}")