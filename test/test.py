from shapely.geometry import Point, Polygon

# Coordenadas de San José
san_jose_coords = [
            [
              -58.611025606786455,
              -34.67572876006122
            ],
            [
              -58.61865018511533,
              -34.66945818292894
            ],
            [
              -58.619877556261514,
              -34.670069967448114
            ],
            [
              -58.62757652072021,
              -34.67658519228527
            ],
            [
              -58.62445230325868,
              -34.679185021570724
            ],
            [
              -58.62880389186563,
              -34.68276347662244
            ],
            [
              -58.62355966969784,
              -34.6870146025611
            ],
            [
              -58.611025606786455,
              -34.67572876006122
            ]
          ]

# Crear polígono
polygon = Polygon(san_jose_coords)

# Puntos de prueba
puntos_prueba = [
    Point(-58.6208062723505, -34.6727729301963),  # Debería estar dentro de San José
    Point(-58.620, -34.680),  # Debería estar dentro
    Point(-58.430, -34.580),  # Debería estar en Palermo
    Point(-58.625, -34.680)   # Debería estar cerca del borde
]

# Verificar
for i, punto in enumerate(puntos_prueba):
    if polygon.contains(punto):
        print(f"✅ Punto {i+1} está dentro de San José")
    else:
        print(f"❌ Punto {i+1} NO está en San José")