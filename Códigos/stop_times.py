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
RUTA = "BinniBusRC09.1"

PARADAS_RAW = """
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
185
186
562
563
564
565
566
567
317
568
569
148
150
45
46
47
48
49
151
50
152
153
53
570
571
572
573
574
575
576
577
578
509
"""

HORARIOS_RAW = """
07:15	08:40
07:40	09:05
08:10	09:35
08:35	10:00
09:00	10:25
09:25	10:50
09:50	11:15
10:15	11:40
10:40	12:05
11:05	12:30
11:30	12:55
11:55	13:20
12:20	13:45
12:45	14:10
13:15	14:45
13:40	15:10
14:05	15:35
14:30	16:00
14:55	16:25
15:20	16:50
15:48	17:18
16:21	17:51
16:49	18:19
17:17	18:47
17:45	19:15
18:11	19:41
18:37	20:07
19:03	20:33
19:29	21:04
19:55	21:30
20:21	21:56
20:42	22:07
21:08	22:28

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
