# Definimos las enfermedades y sus síntomas
enfermedades = {
    "Gripe": {
        "comunes": ["dolor de cabeza", "fatiga", "dolor muscular", "congestión nasal", "dolor de garganta", "tos", "estornudos", "dolor de ojos", "cansancio", "dolor en las articulaciones", "náuseas", "malestar general", "pérdida de apetito"],
        "exclusivos": ["picazón en la garganta", "lagrimeo constante"]
    },
    "Influenza": {
        "comunes": ["dolor de cabeza", "fatiga", "dolor muscular", "dolor de garganta", "tos seca", "congestión nasal", "escalofríos", "cansancio extremo", "dolor en las articulaciones", "dolor abdominal leve", "sudoración", "malestar general", "pérdida de apetito"],
        "exclusivos": ["sensibilidad a la luz (fotofobia)", "dolor severo detrás de los ojos"]
    },
    "COVID-19": {
        "comunes": ["dolor de cabeza", "fatiga", "dolor muscular", "dolor de garganta", "tos seca", "congestión nasal", "escalofríos", "dolor en el pecho al respirar", "pérdida de apetito", "náuseas", "malestar general", "cansancio", "dificultad para respirar"],
        "exclusivos": ["pérdida del gusto y del olfato", "tos persistente con falta de aire"]
    },
    "Neumonía": {
        "comunes": ["dolor de cabeza", "fatiga", "dolor muscular", "tos con flema", "dolor en el pecho", "escalofríos", "cansancio", "dolor en las articulaciones", "pérdida de apetito", "sudoración nocturna", "dificultad para respirar", "náuseas", "malestar general"],
        "exclusivos": ["esputo verdoso o amarillento", "dolor agudo al inhalar profundamente"]
    },
    "Malaria": {
        "comunes": ["dolor de cabeza", "fatiga", "dolor muscular", "escalofríos intensos", "cansancio extremo", "dolor abdominal", "náuseas", "vómitos", "debilidad", "dolor en las articulaciones", "sudoración abundante", "pérdida de apetito", "diarrea leve"],
        "exclusivos": ["anemia pronunciada (piel pálida)", "sudoración extrema durante la noche"]
    },
    "Dengue": {
        "comunes": ["dolor de cabeza", "fatiga", "dolor muscular", "dolor de garganta", "náuseas", "vómitos", "debilidad", "pérdida de apetito", "dolor en las articulaciones", "dolor abdominal", "escalofríos", "malestar general", "cansancio"],
        "exclusivos": ["erupción cutánea (exantema en la piel)", "dolor intenso detrás de los ojos"]
    },
    "Fiebre Tifoidea": {
        "comunes": ["dolor de cabeza", "dolor muscular leve", "fatiga", "pérdida de apetito", "diarrea o estreñimiento", "náuseas", "vómitos", "dolor abdominal", "debilidad", "sudoración", "dolor en las articulaciones", "dolor de garganta", "malestar general"],
        "exclusivos": ["manchas rosadas en el pecho y abdomen", "confusión o desorientación en casos avanzados"]
    }
}

# Función para preguntar al usuario sobre los síntomas
def preguntar_sintomas():
    sintomas_usuario = []
    for sintoma in sintomas:
        respuesta = input(f"¿Tiene {sintoma}? (sí/no): ").strip().lower()
        if respuesta == 'sí':
            sintomas_usuario.append(sintoma)
    return sintomas_usuario

# Función para calcular los puntos y el porcentaje de coincidencia
def calcular_probabilidades(sintomas_usuario):
    puntos_enfermedades = {enfermedad: 0 for enfermedad in enfermedades}
    total_puntos_posibles = len(sintomas_usuario)

    for sintoma in sintomas_usuario:
        for enfermedad, detalles in enfermedades.items():
            if sintoma in detalles["comunes"] or sintoma in detalles["exclusivos"]:
                puntos_enfermedades[enfermedad] += 1

    probabilidades = {enfermedad: (puntos / total_puntos_posibles) * 100 for enfermedad, puntos in puntos_enfermedades.items()}
    return probabilidades

# Lista de todos los síntomas posibles
sintomas = [
    "dolor de cabeza", "fatiga", "dolor muscular", "congestión nasal", "dolor de garganta", "tos", "estornudos", "dolor de ojos", "cansancio", "dolor en las articulaciones", "náuseas", "malestar general", "pérdida de apetito",
    "picazón en la garganta", "lagrimeo constante", "tos seca", "escalofríos", "cansancio extremo", "dolor abdominal leve", "sudoración", "sensibilidad a la luz (fotofobia)", "dolor severo detrás de los ojos", "dolor en el pecho al respirar",
    "dificultad para respirar", "esputo verdoso o amarillento", "dolor agudo al inhalar profundamente", "escalofríos intensos", "vómitos", "debilidad", "sudoración abundante", "diarrea leve", "anemia pronunciada (piel pálida)",
    "sudoración extrema durante la noche", "erupción cutánea (exantema en la piel)", "dolor intenso detrás de los ojos", "diarrea o estreñimiento", "manchas rosadas en el pecho y abdomen", "confusión o desorientación en casos avanzados"
]

# Preguntar al usuario sobre los síntomas
sintomas_usuario = preguntar_sintomas()

# Calcular las probabilidades
probabilidades = calcular_probabilidades(sintomas_usuario)

# Mostrar los resultados
for enfermedad, probabilidad in probabilidades.items():
    print(f"La probabilidad de tener {enfermedad} es {probabilidad:.2f}%")