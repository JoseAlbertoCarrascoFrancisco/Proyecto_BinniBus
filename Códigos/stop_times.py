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

"""

HORARIOS_RAW = """

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
