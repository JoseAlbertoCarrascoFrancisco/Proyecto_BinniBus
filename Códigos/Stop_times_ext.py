import csv
from datetime import datetime, timedelta

def generar_stop_times_desde_horarios(
    ruta_nombre: str,
    paradas_raw: str,
    horarios_raw: str,
    nombre_archivo: str = "stop_timesd.txt"
):
    """
    Genera el archivo GTFS stop_times.txt y lo guarda en TXT.
    Soporta horarios que cruzan medianoche (ej. 23:30 → 00:40).
    """

    # -----------------------------------------------------------
    # 1. Procesar entradas
    # -----------------------------------------------------------
    stop_ids = [s.strip() for s in paradas_raw.split('\n') if s.strip()]
    horarios = []
    for linea in horarios_raw.split('\n'):
        if linea.strip():
            partes = linea.strip().split()
            if len(partes) >= 2:
                hora_inicio, hora_fin = partes[0], partes[1]
                horarios.append((hora_inicio, hora_fin))

    fecha_base = datetime(2000, 1, 1)

    todas_las_filas = []
    encabezado = [
        "trip_id",
        "stop_sequence",
        "arrival_time",
        "departure_time",
        "stop_id",
        "stop_headsign",
        "pickup_type",
        "drop_off_type"
    ]

    # -----------------------------------------------------------
    # 2. Generar filas de datos
    # -----------------------------------------------------------
    for idx, (inicio, fin) in enumerate(horarios, start=1):
        trip_id = f"{ruta_nombre}.{idx:03d}"

        try:
            h_i, m_i = map(int, inicio.split(':'))
            h_f, m_f = map(int, fin.split(':'))

            hora_inicio = fecha_base.replace(hour=h_i, minute=m_i, second=0)
            hora_fin = fecha_base.replace(hour=h_f, minute=m_f, second=0)

            # Detectar cruce de medianoche
            cruza_medianoche = False
            if hora_fin < hora_inicio:
                hora_fin += timedelta(days=1)
                cruza_medianoche = True
                print(f"⚠️ Viaje cruza medianoche: {inicio} → {fin} en {trip_id}")

        except Exception:
            print(f"❌ Error en formato de hora en línea {idx}: {inicio} - {fin}")
            continue

        duracion = (hora_fin - hora_inicio).total_seconds() / 60
        num_stops = len(stop_ids)
        intervalo_por_parada = duracion / (num_stops - 1) if num_stops > 1 else 0

        tiempo_actual = hora_inicio
        for i, stop_id in enumerate(stop_ids):
            stop_sequence = i + 1

            # Convertir a segundos desde fecha_base
            segundos = int((tiempo_actual - fecha_base).total_seconds())
            horas = segundos // 3600   # GTFS soporta >24h
            minutos = (segundos % 3600) // 60
            segs = segundos % 60

            tiempo_gtfs = f"{horas:02d}:{minutos:02d}:{segs:02d}"

            fila = [
                trip_id,
                stop_sequence,
                tiempo_gtfs,
                tiempo_gtfs,
                stop_id,
                "",
                "0",
                "0"
            ]
            todas_las_filas.append(fila)

            if i < num_stops - 1:
                tiempo_actual += timedelta(minutes=intervalo_por_parada)

    # -----------------------------------------------------------
    # 3. Escribir archivo .txt
    # -----------------------------------------------------------
    with open(nombre_archivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(encabezado)
        writer.writerows(todas_las_filas)

    print(f"✅ Archivo '{nombre_archivo}' generado con {len(horarios)} viajes y {len(todas_las_filas)} filas.")


# =================================================================
# === CONFIGURACIÓN ===
# =================================================================
RUTA = "BinniBusRC14.1"

PARADAS_RAW = """
237
202
203
204
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
46
47
48
49
264
50
51
52
53
54
55
56
57
58
59
60
61
62
265
266
1
"""

HORARIOS_RAW = """
06:00	07:10
06:15	07:30
06:30	07:50
06:45	08:10
07:00	08:30
07:20	08:50
07:40	09:10
08:00	09:30
08:20	09:50
08:35	10:05
09:05	10:35
09:20	10:50
09:35	11:05
09:50	11:20
10:05	11:35
10:30	12:00
10:50	12:20
11:10	12:40
11:30	13:00
11:45	13:15
12:15	13:45
12:30	14:00
12:45	14:15
13:00	14:30
13:15	14:45
13:40	15:10
14:00	15:30
14:20	15:50
14:40	16:10
14:55	16:25
15:25	16:55
15:40	17:10
15:55	17:25
16:10	17:40
16:25	17:55
16:50	18:00
17:10	18:20
17:30	18:40
17:50	19:00
18:05	19:15
18:35	19:45
18:50	20:00
19:05	20:15
19:20	20:30
19:35	20:45
19:40	20:50
20:00	21:10
20:30	21:40
20:50	22:00
21:05	22:15
22:20	23:30
22:50	23:55
23:15	00:15
23:45	00:45
"""

# =================================================================
# === EJECUCIÓN ===
# =================================================================
if __name__ == "__main__":
    generar_stop_times_desde_horarios(
        ruta_nombre=RUTA,
        paradas_raw=PARADAS_RAW,
        horarios_raw=HORARIOS_RAW
    )
