import csv
import re


def leer_coordenadas_kml(archivo_kml):
    """
    Lee un archivo KML y obtiene los bloques <coordinates>.
    El primero se considera Ida y el segundo Regreso.
    """

    with open(archivo_kml, "r", encoding="utf-8") as f:
        contenido = f.read()

    bloques = re.findall(r"<coordinates>(.*?)</coordinates>", contenido, re.DOTALL)

    if len(bloques) < 2:
        raise Exception("El archivo KML debe contener al menos dos bloques <coordinates>.")

    return bloques[0], bloques[1]


def kml_to_latlon(coords_kml):
    """
    Convierte coordenadas KML (lon,lat,alt) a [(lat, lon)].
    """
    coords = []

    for linea in coords_kml.strip().splitlines():
        linea = linea.strip()

        if not linea:
            continue

        partes = linea.split(",")

        if len(partes) >= 2:
            lon = float(partes[0])
            lat = float(partes[1])
            coords.append((lat, lon))

    return coords


def generar_shapes(shape_id, archivo_kml, archivo_salida="shapes.txt"):

    # Leer los dos bloques del KML
    coords_ida_kml, coords_regreso_kml = leer_coordenadas_kml(archivo_kml)

    coords_ida = kml_to_latlon(coords_ida_kml)
    coords_regreso = kml_to_latlon(coords_regreso_kml)

    with open(archivo_salida, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "shape_id",
            "shape_pt_lat",
            "shape_pt_lon",
            "shape_pt_sequence"
        ])

        seq = 1

        # Ida
        for lat, lon in coords_ida:
            writer.writerow([shape_id, lat, lon, seq])
            seq += 1

        # Regreso
        for lat, lon in coords_regreso:
            writer.writerow([shape_id, lat, lon, seq])
            seq += 1

    print(f"✅ shapes generado correctamente")
    print(f"Shape ID: {shape_id}")
    print(f"Puntos ida: {len(coords_ida)}")
    print(f"Puntos regreso: {len(coords_regreso)}")
    print(f"Total: {seq-1}")


# ===========================
# USO
# ===========================

shape_id = "BinniBusRA01"

archivo_kml = "Kml/RA-01.kml"

generar_shapes(shape_id, archivo_kml)