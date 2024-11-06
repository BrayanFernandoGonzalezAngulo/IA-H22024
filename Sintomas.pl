% Definición de enfermedades y sus síntomas
sintomas(gripe, comunes, ["dolor de cabeza", "fatiga", "dolor muscular", "congestión nasal", "dolor de garganta", "tos", "estornudos", "dolor de ojos", "cansancio", "dolor en las articulaciones", "náuseas", "malestar general", "pérdida de apetito"]).
sintomas(gripe, exclusivos, ["picazón en la garganta", "lagrimeo constante"]).

sintomas(influenza, comunes, ["dolor de cabeza", "fatiga", "dolor muscular", "dolor de garganta", "tos seca", "congestión nasal", "escalofríos", "cansancio extremo", "dolor en las articulaciones", "dolor abdominal leve", "sudoración", "malestar general", "pérdida de apetito"]).
sintomas(influenza, exclusivos, ["sensibilidad a la luz (fotofobia)", "dolor severo detrás de los ojos"]).

sintomas(covid19, comunes, ["dolor de cabeza", "fatiga", "dolor muscular", "dolor de garganta", "tos seca", "congestión nasal", "escalofríos", "dolor en el pecho al respirar", "pérdida de apetito", "náuseas", "malestar general", "cansancio", "dificultad para respirar"]).
sintomas(covid19, exclusivos, ["pérdida del gusto y del olfato", "tos persistente con falta de aire"]).

sintomas(neumonia, comunes, ["dolor de cabeza", "fatiga", "dolor muscular", "tos con flema", "dolor en el pecho", "escalofríos", "cansancio", "dolor en las articulaciones", "pérdida de apetito", "sudoración nocturna", "dificultad para respirar", "náuseas", "malestar general"]).
sintomas(neumonia, exclusivos, ["esputo verdoso o amarillento", "dolor agudo al inhalar profundamente"]).

sintomas(malaria, comunes, ["dolor de cabeza", "fatiga", "dolor muscular", "escalofríos intensos", "cansancio extremo", "dolor abdominal", "náuseas", "vómitos", "debilidad", "dolor en las articulaciones", "sudoración abundante", "pérdida de apetito", "diarrea leve"]).
sintomas(malaria, exclusivos, ["anemia pronunciada (piel pálida)", "sudoración extrema durante la noche"]).

sintomas(dengue, comunes, ["dolor de cabeza", "fatiga", "dolor muscular", "dolor de garganta", "náuseas", "vómitos", "debilidad", "pérdida de apetito", "dolor en las articulaciones", "dolor abdominal", "escalofríos", "malestar general", "cansancio"]).
sintomas(dengue, exclusivos, ["erupción cutánea (exantema en la piel)", "dolor intenso detrás de los ojos"]).

sintomas(fiebre_tifoidea, comunes, ["dolor de cabeza", "dolor muscular leve", "fatiga", "pérdida de apetito", "diarrea o estreñimiento", "náuseas", "vómitos", "dolor abdominal", "debilidad", "sudoración", "dolor en las articulaciones", "dolor de garganta", "malestar general"]).
sintomas(fiebre_tifoidea, exclusivos, ["manchas rosadas en el pecho y abdomen", "confusión o desorientación en casos avanzados"]).

% Predicado para preguntar al usuario si tiene un síntoma específico
preguntar_sintoma(Sintoma, Respuesta) :-
    write("¿Tienes "), write(Sintoma), write("? (s/n): "),
    read(Resp),
    (Resp = 's' -> Respuesta = 1 ; Respuesta = 0).

% Preguntar por todos los síntomas comunes una sola vez
preguntar_sintomas_comunes([], []).
preguntar_sintomas_comunes([Sintoma | Resto], [Respuesta | Respuestas]) :-
    preguntar_sintoma(Sintoma, Respuesta),
    preguntar_sintomas_comunes(Resto, Respuestas).

% Calcular el porcentaje de coincidencia para cada enfermedad
calcular_porcentaje(Enfermedad, CoincidenciasComunes, CoincidenciasExclusivos, Porcentaje) :-
    sintomas(Enfermedad, comunes, SintomasComunes),
    sintomas(Enfermedad, exclusivos, SintomasExclusivos),
    length(SintomasComunes, TotalSintomasComunes),
    length(SintomasExclusivos, TotalSintomasExclusivos),
    TotalSintomas is TotalSintomasComunes + TotalSintomasExclusivos,
    TotalCoincidencias is CoincidenciasComunes + CoincidenciasExclusivos,
    Porcentaje is (TotalCoincidencias / TotalSintomas) * 100.

% Consultar enfermedades y calcular coincidencias
consultar_enfermedades(Resultados, RespuestasComunes, RespuestasExclusivos) :-
    findall(Enfermedad, sintomas(Enfermedad, _, _), Enfermedades),
    consultar_enfermedades_aux(Enfermedades, [], RespuestasComunes, RespuestasExclusivos, Resultados).

consultar_enfermedades_aux([], Resultados, _, _, Resultados).
consultar_enfermedades_aux([Enfermedad | Resto], Acc, RespuestasComunes, RespuestasExclusivos, Resultados) :-
    sintomas(Enfermedad, comunes, SintomasComunes),
    sintomas(Enfermedad, exclusivos, SintomasExclusivos),
    contar_coincidencias_comunes(SintomasComunes, RespuestasComunes, CoincidenciasComunes),
    contar_coincidencias_exclusivos(SintomasExclusivos, RespuestasExclusivos, CoincidenciasExclusivos),
    calcular_porcentaje(Enfermedad, CoincidenciasComunes, CoincidenciasExclusivos, Porcentaje),
    consultar_enfermedades_aux(Resto, [(Enfermedad, Porcentaje) | Acc], RespuestasComunes, RespuestasExclusivos, Resultados).

% Contar síntomas comunes coincidentes
contar_coincidencias_comunes([], [], 0).
contar_coincidencias_comunes([Sintoma | Sintomas], [Respuesta | Respuestas], Coincidencias) :-
    contar_coincidencias_comunes(Sintomas, Respuestas, CoincidenciasPrevias),
    Coincidencias is CoincidenciasPrevias + Respuesta.

% Contar síntomas exclusivos coincidentes
contar_coincidencias_exclusivos([], _, 0).
contar_coincidencias_exclusivos([Sintoma | Sintomas], RespuestasExclusivos, Coincidencias) :-
    memberchk((Sintoma, Respuesta), RespuestasExclusivos),
    contar_coincidencias_exclusivos(Sintomas, RespuestasExclusivos, CoincidenciasPrevias),
    Coincidencias is CoincidenciasPrevias + Respuesta.

% Eliminar duplicados de la lista de síntomas exclusivos
eliminar_duplicados([], []).
eliminar_duplicados([Cabeza | Cola], [Cabeza | SinDuplicados]) :-
    \+ member(Cabeza, Cola),
    eliminar_duplicados(Cola, SinDuplicados).
eliminar_duplicados([_ | Cola], SinDuplicados) :-
    eliminar_duplicados(Cola, SinDuplicados).

% Preguntar por los síntomas exclusivos una sola vez
preguntar_sintomas_exclusivos([], []).
preguntar_sintomas_exclusivos([Sintoma | Resto], [(Sintoma, Respuesta) | Respuestas]) :-
    preguntar_sintoma(Sintoma, Respuesta),
    preguntar_sintomas_exclusivos(Resto, Respuestas).

% Consultar síntomas exclusivos sin duplicados
consultar_sintomas_exclusivos(SintomasExclusivos) :-
    findall(Sintoma, (sintomas(_, exclusivos, Sintomas), member(Sintoma, Sintomas)), TodosSintomasExclusivos),
    eliminar_duplicados(TodosSintomasExclusivos, SintomasExclusivos).

% Iniciar el diagnóstico
diagnostico :-
    write("Responde las siguientes preguntas sobre tus síntomas."), nl,
    sintomas(_, comunes, SintomasComunes),
    preguntar_sintomas_comunes(SintomasComunes, RespuestasComunes),
    consultar_sintomas_exclusivos(SintomasExclusivos),
    preguntar_sintomas_exclusivos(SintomasExclusivos, RespuestasExclusivos),
    consultar_enfermedades(Resultados, RespuestasComunes, RespuestasExclusivos),
    mostrar_resultados(Resultados).

% Mostrar resultados ordenados por probabilidad
mostrar_resultados(Resultados) :-
    sort(2, @>=, Resultados, ResultadosOrdenados),
    write("Resultados de probabilidad de enfermedades:"), nl,
    mostrar_enfermedades(ResultadosOrdenados).

mostrar_enfermedades([]).
mostrar_enfermedades([(Enfermedad, Porcentaje) | Resto]) :-
    format("~w: ~2f% de probabilidad~n", [Enfermedad, Porcentaje]),
    mostrar_enfermedades(Resto).
