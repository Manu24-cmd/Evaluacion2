import requests
import urllib.parse

# 1. Reemplaza esto con tu token real de Graphhopper
api_key = "369e7569-e74b-47d0-a617-8f67b0c9f013"

while True:
    print("\n--- Planificador de Rutas ---")
    
    # Opción para salir del programa (Requisito 3)
    origen = input("Ingrese el punto de origen (o escriba 's' o 'salir' para terminar): ")
    
    if origen.lower() in ['s', 'salir']:
        print("Saliendo del programa. ¡Hasta luego!")
        break
        
    destino = input("Ingrese el punto de destino: ")

    # Construir URLs para obtener coordenadas (Geocoding API)
    geocode_url_orig = f"https://graphhopper.com/api/1/geocode?q={urllib.parse.quote(origen)}&key={api_key}"
    geocode_url_dest = f"https://graphhopper.com/api/1/geocode?q={urllib.parse.quote(destino)}&key={api_key}"

    try:
        req_orig = requests.get(geocode_url_orig).json()
        req_dest = requests.get(geocode_url_dest).json()
        
        lat_origen = req_orig['hits'][0]['point']['lat']
        lng_origen = req_orig['hits'][0]['point']['lng']
        lat_destino = req_dest['hits'][0]['point']['lat']
        lng_destino = req_dest['hits'][0]['point']['lng']
    except (IndexError, KeyError):
        print("Error: No se pudo encontrar una de las ubicaciones. Intente de nuevo.")
        continue

    # Solicitud de ruta con locale=es para narrativa en español (Requisito 1 y 4)
    route_url = f"https://graphhopper.com/api/1/route?point={lat_origen},{lng_origen}&point={lat_destino},{lng_destino}&vehicle=car&locale=es&key={api_key}"
    
    req_route = requests.get(route_url).json()

    if 'paths' not in req_route:
        print("No se pudo calcular una ruta entre esos puntos.")
        continue

    # Formateo de valores numéricos a máximo dos decimales (Requisito 2)
    distancia_km = req_route['paths'][0]['distance'] / 1000
    tiempo_min = req_route['paths'][0]['time'] / 60000

    print(f"\nResumen del viaje:")
    print(f"Distancia total: {distancia_km:.2f} kilómetros")
    print(f"Tiempo estimado: {tiempo_min:.2f} minutos\n")
    
    print("Instrucciones paso a paso:")
    instrucciones = req_route['paths'][0]['instructions']
    for paso in instrucciones:
        dist_paso = paso['distance'] / 1000
        print(f"- {paso['text']} ({dist_paso:.2f} km)")