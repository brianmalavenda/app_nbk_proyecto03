# app.py
import json

def punto_en_poligono(x, y, poligono):
    """Determina si un punto está dentro de un polígono usando el algoritmo de Ray Casting"""
    n = len(poligono)
    dentro = False
    p1x, p1y = poligono[0]
    for i in range(n + 1):
        p2x, p2y = poligono[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        dentro = not dentro
        p1x, p1y = p2x, p2y
    return dentro

def obtener_barrio_por_utm(x, y):
    """Busca en qué barrio están las coordenadas UTM"""
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT id, nombre, coordenadas FROM barrios')
    barrios = c.fetchall()
    
    for barrio in barrios:
        id_barrio, nombre, coords_str = barrio
        poligono = json.loads(coords_str)
        if punto_en_poligono(x, y, poligono):
            return nombre
    
    return "Barrio no encontrado"