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
    ya NO inserta datos en base de datos.
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
            hora_inicio = fecha_base.replace(
                hour=int(inicio.split(':')[0]),
                minute=int(inicio.split(':')[1]),
                second=0
            )
            hora_fin = fecha_base.replace(
                hour=int(fin.split(':')[0]),
                minute=int(fin.split(':')[1]),
                second=0
            )
        except Exception as e:
            print(f"❌ Error en formato de hora en línea {idx}: {inicio} - {fin}")
            continue

        duracion = (hora_fin - hora_inicio).total_seconds() / 60
        num_stops = len(stop_ids)
        intervalo_por_parada = duracion / (num_stops - 1) if num_stops > 1 else 0

        tiempo_actual = hora_inicio
        for i, stop_id in enumerate(stop_ids):
            stop_sequence = i + 1
            segundos = (tiempo_actual - fecha_base).total_seconds()
            horas = int(segundos // 3600)
            minutos = int((segundos % 3600) // 60)
            segundos = int(segundos % 60)
            tiempo_gtfs = f"{horas:02d}:{minutos:02d}:{segundos:02d}"

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
RUTA = "BinniBusRT02.0"

PARADAS_RAW = """
1
2
3
4
5
6
7
8
9
10
11
975
12
270
271
272
225
226
227
228
229
230
231
1360
1361
1362
1363
1364
732
757
"""

HORARIOS_RAW = """
06:00	07:30
06:10	07:40
06:20	07:50
06:30	08:00
06:40	08:10
06:50	08:20
07:00	08:30
07:10	08:40
07:20	08:50
07:30	09:00
07:40	09:10
07:50	09:20
08:00	09:30
08:10	09:40
08:20	09:50
08:30	10:00
08:40	10:10
08:50	10:20
09:00	10:30
09:10	10:40
09:20	10:50
09:30	11:00
09:40	11:10
09:50	11:20
10:00	11:30
10:10	11:40
10:20	11:50
10:30	12:00
10:40	12:10
10:50	12:20
11:00	12:30
11:10	12:40
11:20	12:50
11:30	13:00
11:40	13:10
11:50	13:20
12:00	13:30
12:10	13:40
12:20	13:50
12:30	14:00
12:40	14:10
12:50	14:20
13:00	14:30
13:10	14:40
13:20	14:50
13:30	15:00
13:40	15:10
13:50	15:20
14:00	15:30
14:10	15:40
14:20	15:50
14:30	16:00
14:40	16:10
14:50	16:20
15:00	16:30
15:10	16:40
15:20	16:50
15:30	17:00
15:40	17:10
15:50	17:20
16:00	17:30
16:10	17:40
16:20	17:50
16:30	18:00
16:40	18:10
16:50	18:20
17:00	18:30
17:10	18:40
17:20	18:50
17:30	19:00
17:40	19:10
17:50	19:20
18:00	19:30
18:10	19:40
18:20	19:50
18:30	20:00
18:40	20:10
18:50	20:20
19:00	20:30
19:10	20:40
19:20	20:50
19:30	21:00
19:40	21:10
19:50	21:20
20:00	21:30
20:10	21:40
20:20	21:50
20:30	22:00
20:40	22:10
20:50	22:20
21:00	22:30
21:10	22:40

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
