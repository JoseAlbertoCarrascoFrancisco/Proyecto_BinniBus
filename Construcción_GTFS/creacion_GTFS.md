# Creación de un archivo GTFS

Para la construcción del archivo GTFS (General Transit Feed Specification) es necesario generar y estructurar un conjunto de archivos en formato CSV que contienen toda la información del sistema de transporte. Cada archivo cumple una función específica dentro del modelo de datos y debe respetar la estructura de columnas establecida por el estándar GTFS.

A continuación se detalla cada uno de los archivos requeridos y los campos que deben incluir:

1. agency.txt

Define las agencias u operadores responsables del servicio de transporte.
Objetivo: Identificar a la(s) agencia(s) u operador(es).

Campos obligatorios:

* agency_id: Identificador único de la agencia. Id corto (si solo hay una agencia puedes usar agency_id = 1 o dejar vacío en algunos validadores, pero es mejor incluirlo).

* agency_name: Nombre oficial de la agencia.

* agency_url: Sitio web público de la agencia. URL completa (https://...).

* agency_timezone: Zona horaria en la que opera. (ej. America/Mexico_City).

* agency_lang: Idioma principal utilizado por la agencia. (ej. es).

**Ejemplo:**

```
1,Transporte Ejemplo,https://www.transporte-ejemplo.mx,America/Mexico_City,es
```

2. calendar.txt

Especifica los patrones de servicio semanales para cada servicio.
Objetivo: Definir qué días opera cada service_id y su vigencia.

Campos:

* service_id: Identificador del servicio.

* monday,tuesday,wednesday,thursday,friday,saturday,sunday:Indican si el servicio opera cada día (1 = sí, 0 = no).

* start_date: Fecha de inicio de vigencia del servicio (AAAAMMDD).

* end_date: Fecha final de vigencia (AAAAMMDD).

**Ejemplo:**

```
WKD,1,1,1,1,1,0,0,20250101,20251231
```

3. calendar_dates.txt

Permite agregar excepciones a los calendarios regulares, como días festivos o servicios especiales.
Objetivo: Agregar o eliminar servicios en fechas concretas.

Campos:

* service_id: Debe coincidir con calendar.txt.

* date: Fecha específica (AAAAMMDD).

* exception_type: Tipo de excepción (1 = servicio agregado, 2 = servicio eliminado).

**Ejemplo:**

```
WKD,1,1,1,1,1,0,0,20250101,20251231
```

4. fare_attributes.txt

Define las tarifas disponibles dentro del sistema.
Objetivo: Definir las tarifas y cómo se aplican.

Campos:

* fare_id: Identificador único de la tarifa.

* price: Costo de la tarifa.

* currency_type – Moneda (ej. MXN).

* payment_method – Método de pago (0 = pagar a bordo, 1 = pagar antes).

* transfers – Número de transbordos permitidos.

* agency_id – Agencia a la que pertenece la tarifa.

**Ejemplo:**

```
F1,12.50,MXN,0,0,1
```

5. fare_rules.txt

Relaciona tarifas con rutas y zonas específicas.
Objetivo: Aplica tarifas a rutas.

Campos:

* fare_id: Debe coincidir con fare_attributes.

* route_id: Ruta a la que se aplica la tarifa.

* origin_id: Zona de origen.

* destination_id: Zona de destino.

**Ejemplo:**

```
F1,R1,,
```

6. feed_info.txt

Proporciona metadatos del feed, útil para control de versiones y actualizaciones.
Objetivo: Información del feed (útil para control/versiones).

Campos:

* feed_publisher_name: Nombre del publicador del feed.

* feed_publisher_url: Sitio web del publicador.

* feed_lang: Idioma principal del feed.

* feed_start_date: Fecha de inicio del feed.

* feed_end_date: Fecha de expiración.

* feed_version: Versión del feed (definida por el creador).

* feed_contact_email: Correo de contacto para soporte.

**Ejemplo:**

```
Transporte Ejemplo,https://www.transporte-ejemplo.mx,es,20250101,20251231,1.0,info@transporte-ejemplo.mx
```

7. routes.txt

Contiene las rutas o líneas del sistema de transporte.
Objetivo: Definir líneas/rutas del sistema.

Campos:

* route_id: Identificador único de la ruta.

* agency_id: Agencia responsable.

* route_short_name: Nombre corto o clave de la ruta.

* route_long_name: Nombre largo o descriptivo de la ruta.

* route_type: Tipo de transporte (ej. 3 = autobús).

* route_color: Color representativo en formato hexadecimal.

**Ejemplo:**

```
R1,1,B12,Barranca - Centro,3,FF0000
```

8. shapes.txt

Define la geometría del recorrido en coordenadas GPS.
Objetivo: Polígonos / polilíneas que representan visualmente la ruta.

Campos:

* shape_id: Identificador del trazo.

* shape_pt_lat: Latitud del punto.

* shape_pt_lon: Longitud del punto.

* shape_pt_sequence: Orden secuencial del punto en la ruta.

**Ejemplo:**

```
SH1,19.4326,-99.1332,1
SH1,19.4400,-99.1200,2
SH1,19.4500,-99.1100,3
```

Consejos:

* Secuencia ordenada a lo largo del recorrido.

* Puedes incluir shape_dist_traveled si tienes distancias acumuladas.


9. stops.txt

Registra todas las paradas del sistema, con su ubicación geográfica.
Objetivo: Geolocalizar paradas y estaciones.

Campos:

* stop_id – Identificador de la parada.

* stop_name: Nombre de la parada.

* stop_desc: Descripción opcional.

* stop_lat: Latitud del punto.

* stop_lon: Longitud del punto.

* location_type: Tipo de ubicación (0 = parada, 1 = estación).

* parent_station: Estación principal si aplica.

Columnas opcionales útiles:

* stop_desc, location_type (0=stop,1=station), parent_station (si forma parte de una estación), zone_id.

**Ejemplo:**

```
S100,Parada Centro,Descripción corta,19.432608,-99.133209,0,
```
Validaciones:

* Latitud entre -90 y 90; longitud entre -180 y 180.

* stop_id único.


10. stop_times.txt

Define el orden de las paradas dentro de cada viaje (trip), así como los horarios.
Objetivo: Decir qué paradas visita cada trip y sus horas.

Campos:

* trip_id: Identificador del viaje.

* stop_sequence: Número que indica el orden de la parada.

* arrival_time: Hora de llegada (HH:MM:SS).

* departure_time: Hora de salida.

* stop_id: Parada correspondiente.

* stop_headsign: Destino mostrado al pasajero.

* pickup_type: Tipo de subida (0 = permitido).

* drop_off_type: Tipo de bajada (0 = permitido).

**Ejemplo:**

```
T001,08:00:00,08:00:00,S100,1
T001,08:10:00,08:10:00,S101,2
T001,08:25:00,08:25:00,S102,3
```

Notas importantes sobre tiempos:
* Formato HH:MM:SS.

* Para servicios que cruzan medianoche, GTFS permite horas mayores a 24: 25:30:00 = 1:30 del día siguiente (útil para trenes nocturnos).

* arrival_time ≤ departure_time para la misma parada (normalmente iguales si no hay parada).

* stop_sequence entero y creciente por trip_id.

Errores comunes:

* Horas mal formateadas (ej. 8:00 en vez de 08:00:00).

* Orden de stop_sequence incorrecto.

* stop_id que no existe en stops.txt.


11. trips.txt

Define cada viaje (trip) que recorre una ruta específica bajo un servicio.

Campos:

* route_id: Ruta a la que pertenece el viaje.

* service_id: Servicio (según calendar o calendar_dates).

* trip_id: Identificador del viaje. Se usan en stop_times para enlazar horarios.

* direction_id: Dirección (0 = ida, 1 = vuelta).

* shape_id: Identificador del trazo asociado.

**Ejemplo:**

```
R1,WKD,T001,0,SH1
```










Uso del Archivo GTFS

Una vez generados todos los archivos, deben exportarse en formato CSV UTF-8, sin separadores adicionales y con encabezados exactos. Posteriormente, se almacenan dentro de un archivo comprimido .zip, conservando los nombres obligatorios para que el feed pueda ser validado por herramientas GTFS y plataformas de transporte.