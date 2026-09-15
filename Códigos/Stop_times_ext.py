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
RUTA = "BinniBusRA03.0"

PARADAS_RAW = """
21
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
1325
1326
1327
1328
1329
1330
"""

HORARIOS_RAW = """
06:30	07:15
06:50	07:35
07:10	08:00
07:30	08:20
07:50	08:40
08:10	09:00
08:30	09:20
08:50	09:40
09:10	10:00
09:32	10:22
09:54	10:44
10:16	11:06
10:38	11:28
11:00	11:50
11:22	12:12
11:44	12:34
12:06	12:56
12:28	13:18
12:50	13:40
13:12	14:07
13:34	14:29
13:56	14:51
14:18	15:18
14:40	15:40
15:04	16:04
15:28	16:28
15:54	16:54
16:20	17:20
16:46	17:46
17:12	18:12
17:36	18:36
18:02	19:02
18:28	19:28
18:54	19:54
19:20	20:20
19:46	20:46
20:12	21:07
20:36	21:26
20:58	21:43
21:22	22:02

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
