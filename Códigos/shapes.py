import csv

def kml_to_latlon(coords_kml):
    """
    Convierte coordenadas en formato KML (lon,lat,alt) a lista [(lat, lon)].
    Ignora la altitud.
    """
    coords = []
    for line in coords_kml.strip().splitlines():
        parts = line.strip().split(",")
        if len(parts) >= 2:
            lon = float(parts[0])  # KML = lon,lat,alt
            lat = float(parts[1])
            coords.append((lat, lon))
    return coords


def generar_shapes(shape_id, coords_kml_ida, coords_kml_regreso, archivo_salida="shapes_codigo.txt"):
    """
    Genera shapes.txt para GTFS con un único shape_id (sin _ida ni _regreso)
    concatenando los puntos de ida y regreso en secuencia continua.
    """

    coords_ida = kml_to_latlon(coords_kml_ida)
    coords_regreso = kml_to_latlon(coords_kml_regreso)

    with open(archivo_salida, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["shape_id","shape_pt_lat","shape_pt_lon","shape_pt_sequence"])

        seq = 1

        # Puntos de ida
        for lat, lon in coords_ida:
            writer.writerow([shape_id, lat, lon, seq])
            seq += 1
        
        # Puntos de regreso (continúa secuencia)
        for lat, lon in coords_regreso:
            writer.writerow([shape_id, lat, lon, seq])
            seq += 1

    print(f"✅ shapes.txt generado exitosamente con shape_id: {shape_id}")
    print(f"➡️ Total de puntos: {seq-1}")


# ==============================
# EJEMPLO DE USO
# ==============================

shape_id = "BinniBusR"

coords_kml_ida = """
 
"""

coords_kml_regreso = """
 
 """

generar_shapes(shape_id, coords_kml_ida, coords_kml_regreso)
