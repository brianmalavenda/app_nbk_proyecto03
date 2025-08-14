import json
from shapely.geometry import Point, Polygon
import requests

# Cargar personas desde JSON
def cargar_personas():
    try:
        with open('./documents/personas.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error cargando personas: {e}")
        return []

# Cargar barrios desde JSON
def cargar_barrios():
    try:
        with open('./documents/barrios.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error cargando barrios: {e}")
        return {}

# Buscar dirección usando la API
def buscar_direccion(direccion, localidad):
    res = requests.get("https://apis.datos.gob.ar/georef/api/direcciones",
    params={"direccion": direccion, "provincia": "06", "localidad": localidad}, timeout=5)
    jsonbody = res.json()
    if res.status_code != 200 or jsonbody['cantidad'] == 0:
        print(f"\n❌ Dirección '{direccion}, {localidad}' no encontrada")
        return None
    ubicacion = jsonbody["direcciones"][0]["ubicacion"]
    return {'latitud': ubicacion["lat"], 'longitud': ubicacion["lon"]}

def asignar_barrios_a_personas():    
    # Cargar datos al iniciar
    personas = cargar_personas()
    barrios = cargar_barrios()

    # Lista para resultados
    personas_con_barrio = []
    
    # Contadores para estadísticas
    encontrados = 0
    no_encontrados = 0
    
    for persona in personas:
        try:
            print(f"\n🔍 Procesando: {persona['nombre']} {persona['apellido']}")
            direccion = buscar_direccion(persona['direccion'], persona['localidad'])

            if not direccion:
                print(f"❌ Dirección no encontrada: {persona['direccion']}")
                persona['barrio'] = "Dirección no encontrada"
                no_encontrados += 1
                personas_con_barrio.append(persona)
                continue

            punto = Point(direccion['longitud'], direccion['latitud'])
            print(f"📍 Punto creado: {punto}")
            barrio_encontrado = None
            
            for barrio in barrios:
                try:
                    polygon = Polygon(barrio['coordinates'])
                    if polygon.contains(punto):
                        barrio_encontrado = barrio
                        break
                    else:
                        print(f"❌ Punto {punto} no está en {barrio['name']}")
                except Exception as e:
                    print(f"⚠️ Error en polígono de {barrio['name']}: {str(e)}")
            
            if barrio_encontrado:
                print(f"✅ Barrio encontrado: {barrio_encontrado['name']}")
                persona['barrio'] = barrio_encontrado['name']
                encontrados += 1
            else:
                print(f"❌ Barrio no identificado")
                persona['barrio'] = "No identificado"
                no_encontrados += 1
                
            personas_con_barrio.append(persona)
            
        except Exception as e:
            print(f"(🔥 Error procesando persona {persona['id']}: {str(e)}")
            persona['barrio'] = "Error en procesamiento"
            personas_con_barrio.append(persona)
    
    # Guardar resultados
    with open('./documents/personas_con_barrio.json', 'w', encoding='utf-8') as f:
        json.dump(personas_con_barrio, f, indent=4, ensure_ascii=False)
    
    print(f"\n✅ Proceso completado:")
    print(f"   Personas procesadas: {len(personas_con_barrio)}")
    print(f"   Barrios encontrados: {encontrados}")
    print(f"   Barrios no identificados: {no_encontrados}")
    print(f"   Archivo guardado: personas_con_barrio.json")
    
    return personas_con_barrio

# Ejecutar el proceso
if __name__ == '__main__':
    personas_con_barrio = asignar_barrios_a_personas()