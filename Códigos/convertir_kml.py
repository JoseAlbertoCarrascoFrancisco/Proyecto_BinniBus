import zipfile
import os

def kmz_to_kml(kmz_path, output_path=None):
    # Validamos que el archivo KMZ exista
    if not os.path.isfile(kmz_path):
        print(f"No se encontró el archivo: {kmz_path}")
        return None

    # Si no se indica output_path, se crea en la misma carpeta con el mismo nombre que el KMZ
    if output_path is None:
        output_path = os.path.splitext(kmz_path)[0] + '.kml'

    # Abrimos el archivo KMZ
    with zipfile.ZipFile(kmz_path, 'r') as kmz:
        # Buscamos cualquier archivo KML
        for file in kmz.namelist():
            if file.lower().endswith('.kml'):
                # Extraemos el KML a la carpeta del output
                extracted_path = kmz.extract(file, os.path.dirname(output_path))
                # Renombramos el archivo extraído al nombre deseado
                os.rename(extracted_path, output_path)
                print(f"KML extraído en: {output_path}")
                return output_path

    print("No se encontró un archivo KML dentro del KMZ.")
    return None

# Ejemplo de uso
kmz_file = 'Nombre_del_archivo.kmz'
kml_file = kmz_to_kml(kmz_file)
