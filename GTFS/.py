import csv

archivo_csv = "stops.txt"
archivo_kml = "coordenadas.kml"

with open(archivo_csv, "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)

    with open(archivo_kml, "w", encoding="utf-8") as kmlfile:
        kmlfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        kmlfile.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        kmlfile.write('  <Document>\n')

        # Estilo del icono
        kmlfile.write('    <Style id="iconoParada">\n')
        kmlfile.write('      <IconStyle>\n')
        kmlfile.write('        <scale>1.2</scale>\n')
        kmlfile.write('        <Icon>\n')
        kmlfile.write('          <href>http://maps.google.com/mapfiles/kml/shapes/bus.png</href>\n')
        kmlfile.write('        </Icon>\n')
        kmlfile.write('      </IconStyle>\n')
        kmlfile.write('    </Style>\n')

        for row in reader:
            nombre = row["stop_name"]
            lat = row["stop_lat"]
            lon = row["stop_lon"]

            kmlfile.write('    <Placemark>\n')
            kmlfile.write(f'      <name>{nombre}</name>\n')
            kmlfile.write('      <styleUrl>#iconoParada</styleUrl>\n')
            kmlfile.write('      <Point>\n')
            kmlfile.write(f'        <coordinates>{lon},{lat},0</coordinates>\n')
            kmlfile.write('      </Point>\n')
            kmlfile.write('    </Placemark>\n')

        kmlfile.write('  </Document>\n')
        kmlfile.write('</kml>\n')

print(f"KML generado correctamente: {archivo_kml}")