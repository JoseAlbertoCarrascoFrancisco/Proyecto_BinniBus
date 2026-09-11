import csv
import os
from collections import defaultdict
from xml.etree.ElementTree import Element, SubElement, ElementTree

# Archivo GTFS
archivo_shapes = "shapes.txt"

# Carpeta de salida
carpeta_salida = "KML"
os.makedirs(carpeta_salida, exist_ok=True)

# Agrupar puntos por shape_id
rutas = defaultdict(list)

with open(archivo_shapes, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for fila in reader:
        rutas[fila["shape_id"]].append({
            "lat": float(fila["shape_pt_lat"]),
            "lon": float(fila["shape_pt_lon"]),
            "seq": int(fila["shape_pt_sequence"])
        })

# Crear un KML por cada ruta
for shape_id, puntos in rutas.items():

    puntos.sort(key=lambda x: x["seq"])

    kml = Element("kml", xmlns="http://www.opengis.net/kml/2.2")
    document = SubElement(kml, "Document")

    nombre = SubElement(document, "name")
    nombre.text = shape_id

    # Estilo de la línea
    style = SubElement(document, "Style", id="ruta")

    line_style = SubElement(style, "LineStyle")

    color = SubElement(line_style, "color")
    color.text = "ff0000ff"      # Rojo

    width = SubElement(line_style, "width")
    width.text = "4"

    placemark = SubElement(document, "Placemark")

    name = SubElement(placemark, "name")
    name.text = shape_id

    style_url = SubElement(placemark, "styleUrl")
    style_url.text = "#ruta"

    line = SubElement(placemark, "LineString")

    tessellate = SubElement(line, "tessellate")
    tessellate.text = "1"

    coordinates = SubElement(line, "coordinates")
    coordinates.text = "\n".join(
        f"{p['lon']},{p['lat']},0"
        for p in puntos
    )

    salida = os.path.join(carpeta_salida, f"{shape_id}.kml")
    ElementTree(kml).write(salida, encoding="utf-8", xml_declaration=True)

    print(f"Generado: {salida}")

print(f"\nSe generaron {len(rutas)} archivos KML.")