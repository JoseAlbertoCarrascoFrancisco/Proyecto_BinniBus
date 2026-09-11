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
RUTA = "BinniBusRC07.1"

PARADAS_RAW = """
1093
1094
474
475
476
477
478
1095
1096
1097
1098
1099
1100
1101
1102
1084
"""

HORARIOS_RAW = """
06:33	07:06
06:48	07:21
07:03	07:36
07:18	07:51
07:33	08:06
07:49	08:22
08:07	08:42
08:23	08:58
08:44	09:24
09:00	09:40
09:17	09:57
09:34	10:14
09:51	10:31
10:08	10:48
10:25	11:05
10:42	11:22
10:59	11:39
11:16	11:56
11:33	12:13
11:50	12:30
12:07	12:47
12:19	12:54
12:36	13:11
12:53	13:28
13:10	13:45
13:27	14:02
13:44	14:19
14:01	14:36
14:23	15:03
14:40	15:20
14:57	15:37
15:14	15:54
15:31	16:11
15:48	16:28
16:05	16:45
16:22	17:02
16:39	17:19
16:56	17:36
17:13	17:53
17:30	18:10
17:47	18:27
18:04	18:44
18:21	19:01
18:38	19:18
18:55	19:35
19:12	19:52
19:29	20:09
19:46	20:26
20:03	20:43
20:20	21:00

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
