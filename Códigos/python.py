# Pega tu lista de números directamente entre las comillas triples ('''...''').
# Cada número debe estar en una línea separada.
datos_de_entrada = '''
410
411
412
413
414
415
416
417
418
64
65
66
67
419
420
421
422
423
424
425
426
427
'''

# 1. Definir el desplazamiento para la conversión (1 -> 4256)
DESPLAZAMIENTO = 4255

# 2. Procesar la cadena de texto:
#    a. splitlines() divide el texto en una lista de líneas.
#    b. strip() elimina espacios en blanco y saltos de línea de cada elemento.
#    c. filter(None, ...) elimina las líneas vacías.
#    d. int(num_str) convierte el texto del número a un entero.
ids_a_convertir = [
    int(num_str)
    for num_str in datos_de_entrada.splitlines()
    if num_str.strip()
]

# 3. Realizar la conversión
ids_adaptados = [id_original + DESPLAZAMIENTO for id_original in ids_a_convertir]

# 4. Imprimir el resultado en el formato solicitado
print("--- IDs ADAPTADOS (NUEVA BASE 4256) ---")
for nuevo_id in ids_adaptados:
    print(nuevo_id)