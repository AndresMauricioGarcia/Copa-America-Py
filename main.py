import json
import random

## Cargar datos desde "copa-america.json"
with open("copa-america.json", "r") as archivo:
    datos = json.load(archivo)

## Obtener los equipos por grupos
grupos = {}
for equipo in datos["teams"]:
    grupo = equipo["group"]
    if grupo not in grupos:
        grupos[grupo] = []
    grupos[grupo].append(equipo)

## Función para generar enfrentamientos y resultados aleatorios
def generar_enfrentamientos(equipos):
    enfrentamientos = []
    for i in range(len(equipos)):
        for j in range(i + 1, len(equipos)):
            equipo1 = equipos[i]
            equipo2 = equipos[j]
            goles_equipo1 = random.randint(0, 3)
            goles_equipo2 = random.randint(0, 3)
            equipo1['games_played'] += 1
            equipo2['games_played'] += 1
            equipo1['pro_goals'] += goles_equipo1
            equipo1['ag_goal'] += goles_equipo2
            equipo2['pro_goals'] += goles_equipo2
            equipo2['ag_goal'] += goles_equipo1
            enfrentamientos.append({
                "equipo1": equipo1["name"],
                "equipo2": equipo2["name"],
                "goles_equipo1": goles_equipo1,
                "goles_equipo2": goles_equipo2
            })
    return enfrentamientos

## Función para calcular la puntuación
def calcular_puntuacion(enfrentamientos, equipos):
    puntuacion = {equipo['name']: 0 for equipo in equipos}
    for enfrentamiento in enfrentamientos:
        equipo1 = enfrentamiento["equipo1"]
        equipo2 = enfrentamiento["equipo2"]
        goles_equipo1 = enfrentamiento["goles_equipo1"]
        goles_equipo2 = enfrentamiento["goles_equipo2"]
        
        if goles_equipo1 > goles_equipo2:
            puntuacion[equipo1] += 3
        elif goles_equipo1 < goles_equipo2:
            puntuacion[equipo2] += 3
        else:
            puntuacion[equipo1] += 1
            puntuacion[equipo2] += 1
    
    for equipo in equipos:
        equipo['points'] = puntuacion[equipo['name']]
    
    return puntuacion

## Función para mostrar los enfrentamientos de los equipos en cada grupo
def mostrar_enfrentamientos_por_grupo(grupos, resultados_por_grupo):
    for grupo, enfrentamientos in resultados_por_grupo.items():
        print(f"Grupo {grupo}:")
        for enfrentamiento in enfrentamientos:
            print(f"{enfrentamiento['equipo1']} vs {enfrentamiento['equipo2']}: {enfrentamiento['goles_equipo1']} - {enfrentamiento['goles_equipo2']}")

## Generar enfrentamientos y calcular puntuación para cada grupo
resultados_por_grupo = {}
puntuaciones_por_grupo = {}
for grupo, equipos in grupos.items():
    enfrentamientos = generar_enfrentamientos(equipos)
    puntuacion = calcular_puntuacion(enfrentamientos, equipos)
    resultados_por_grupo[grupo] = enfrentamientos
    puntuaciones_por_grupo[grupo] = puntuacion

## Llamar a la función para mostrar los enfrentamientos por grupo
mostrar_enfrentamientos_por_grupo(grupos, resultados_por_grupo)

## Clasificar los dos equipos con mayor puntuación por grupo
clasificados_por_grupo = {}
for grupo, puntuacion in puntuaciones_por_grupo.items():
    clasificados = sorted(puntuacion, key=lambda x: (-puntuacion[x], x))[:2]
    clasificados_por_grupo[grupo] = clasificados

## Crear el JSON con los clasificados y sus detalles
clasificados_detalles = {}
for grupo, clasificados in clasificados_por_grupo.items():
    clasificados_detalles[grupo] = [
        {
            "name": equipo["name"],
            "group": equipo["group"],
            "games_played": equipo["games_played"],
            "pro_goals": equipo["pro_goals"],
            "ag_goal": equipo["ag_goal"],
            "points": equipo["points"]
        }
        for equipo in datos["teams"] if equipo["name"] in clasificados
    ]

clasificados_json = json.dumps(clasificados_detalles, indent=4)

## Guardar el JSON en un archivo
with open("clasificados.json", "w") as archivo_salida:
    archivo_salida.write(clasificados_json)

print("Resultados guardados en clasificados.json")
