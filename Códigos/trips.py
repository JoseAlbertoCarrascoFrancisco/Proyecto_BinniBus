import csv

def generar_trips(
    route_id: str,
    service_id: str,
    shape_id: str,
    direction_id: int,
    cantidad_trips: int,
    nombre_archivo: str = "tripsd.txt"
):
    """
    Genera el archivo GTFS trips.txt y lo guarda en un archivo .txt
    (Ya NO inserta datos en base de datos)
    """

    trip_prefix = "BinniBusRA11.0."
    trips = []

    # === 1️⃣ Generar el archivo trips.txt ===
    with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["route_id", "service_id", "trip_id", "direction_id", "shape_id"])

        for i in range(1, cantidad_trips + 1):
            trip_id = f"{trip_prefix}{i:03d}"  # Ej: BinniBusRC14.0.001
            writer.writerow([route_id, service_id, trip_id, direction_id, shape_id])
            trips.append((route_id, service_id, trip_id, direction_id, shape_id))

    print(f"✅ Archivo '{nombre_archivo}' generado correctamente con {cantidad_trips} trips.")


# === 🧭 CONFIGURACIÓN DEL USUARIO ===
route_id = "RA11"
service_id = "FULLBNB"
shape_id = "BinniBusRA11"
direction_id = 0
cantidad_trips = 32

# === 🚀 EJECUCIÓN ===
generar_trips(route_id, service_id, shape_id, direction_id, cantidad_trips)
