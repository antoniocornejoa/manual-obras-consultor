"""
Aplica correcciones según indicaciones del usuario:
1. Cartas de inicio en check list Admin y Calidad
2. Instructivos de reciclaje con contenido completo
3. DIA procedimiento completo
4. Cierre perimetral y caja acustica como informacion de consulta
5 y 6. Marcar como No aplica
"""
import json

# ── Cargar archivos ───────────────────────────────────────────
with open("manual_sections.json", encoding="utf-8") as f:
    adm = json.load(f)
with open("calidad_sections.json", encoding="utf-8") as f:
    cal = json.load(f)
with open("ambiental_sections.json", encoding="utf-8") as f:
    amb = json.load(f)
with open("inconsistencias.json", encoding="utf-8") as f:
    inc = json.load(f)

# ══════════════════════════════════════════════════════════════
# CORRECCIÓN 1: Agregar cartas de inicio al check list Admin
# ══════════════════════════════════════════════════════════════
cartas_texto = (
    "DOCUMENTACION AMBIENTAL OBLIGATORIA PREVIA AL INICIO DE FAENAS: "
    "Antes de iniciar cualquier obra se deben tramitar las siguientes cartas ambientales: "
    "(a) Carta a los vecinos: notificacion formal a vecinos colindantes informando inicio, "
    "duracion estimada y medidas de mitigacion adoptadas. "
    "(b) Carta conductora DOM (Direccion de Obras Municipales): carta de inicio con documentacion de respaldo "
    "y Plan de Mitigacion adjunto que describe medidas contra ruido, polvo, trafico y residuos. "
    "(c) Carta Carabineros: requerida para obras con intervencion en via publica. "
    "Estas cartas son requisito bloqueante: ninguna obra puede iniciar faenas sin su tramitacion previa."
)

for s in adm:
    if s.get("title", "").strip().lower().startswith("inicio de obra") or \
       "inicio" in s.get("title", "").lower() and "obra" in s.get("title", "").lower():
        if cartas_texto not in s["content"]:
            s["content"].append(cartas_texto)
            print(f"Admin - cartas inicio agregadas en: {s['title']}")
        break

# Buscar tambien en 'Actividades Previas al Inicio' o similar
for s in adm:
    if "actividad" in s.get("title", "").lower() and "previa" in s.get("title", "").lower():
        if cartas_texto not in s["content"]:
            s["content"].append(cartas_texto)
            print(f"Admin - cartas inicio agregadas en: {s['title']}")

# En Calidad: la seccion de check list previa al inicio
for s in cal:
    if "PREVIA AL INICIO" in s.get("title", "").upper():
        if cartas_texto not in s["content"]:
            s["content"].append(cartas_texto)
            print(f"Calidad - cartas inicio agregadas en: {s['title']}")
        break

# Marcar inconsistencia 16 como corregida
for i in inc:
    if i["id"] == 16:
        i["estado"] = "Corregido"
        i["recomendacion"] = "[CORREGIDO] " + i["recomendacion"]

# ══════════════════════════════════════════════════════════════
# CORRECCIÓN 2 y 3: Expandir instructivos y DIA en ambiental
# ══════════════════════════════════════════════════════════════

# Reemplazar la seccion 3 con instructivos completos
for idx, s in enumerate(amb):
    if s["title"] == "3. Instructivos Ambientales":
        s["content"] = [
            "INSTRUCTIVO GENERAL DE MANEJO DE RESIDUOS",
            "Todo residuo generado en obra debe ser clasificado en el punto de origen. Se prohibe la mezcla de residuos. "
            "Los contenedores deben estar claramente identificados por tipo. El registro de retiro debe quedar en el formulario 4.1.",

            "3.1 INSTRUCTIVO DE MANEJO DE RESIDUOS",
            "Clasificacion obligatoria en obra: (1) Material inerte / escombro limpio — hormigon, ceramica, mortero sin contaminantes. "
            "(2) Madera — separada segun estado: reutilizable, reciclable o para disposicion. "
            "(3) Fierro y metales — separados para venta a reciclador certificado. "
            "(4) Plastico — bolsas, envoltorios, tuberia PVC. "
            "(5) Carton y papel — cajas, embalajes. "
            "(6) Residuos peligrosos — pinturas, solventes, aceites, deben ser retirados por empresa autorizada.",

            "3.2 INSTRUCTIVO DE CONTROL EN TERRENO DE RESIDUOS",
            "El encargado de obra (o quien designe el Director de Obra) debe: "
            "(a) Verificar diariamente que los contenedores de clasificacion esten en uso correcto. "
            "(b) Registrar en formulario 4.1 el volumen/peso estimado de cada tipo de residuo retirado. "
            "(c) Exigir guia de despacho y certificado de disposicion final a cada empresa de retiro. "
            "(d) Archivar certificados en carpeta de calidad junto con las fichas de protocolos.",

            "3.3 INSTRUCTIVO DE RECICLAJE DE LADRILLOS",
            "Separacion en obra: los ladrillos en buen estado se acopian en palet identificado 'LADRILLO RECICLABLE'. "
            "Los ladrillos rotos o contaminados van a escombro limpio. "
            "El material en buen estado puede ser cedido a vecinos, vendido o donado previo registro en formulario 4.1. "
            "No se permite acumular ladrillos reciclables por mas de 30 dias sin retiro.",

            "3.4 INSTRUCTIVO DE RECICLAJE DE MADERA",
            "Clasificacion: (a) Madera reutilizable en obra — moldajes, andamios, tapas provisorias. Debe identificarse con cinta verde. "
            "(b) Madera reciclable — listones, tablas sin clavos ni pintura. Acopio en palet separado. "
            "(c) Madera para disposicion — con clavos, pintada, tratada con CCA. Retiro por empresa autorizada. "
            "Se prohibe quemar madera en obra bajo cualquier circunstancia.",

            "3.5 INSTRUCTIVO DE RECICLAJE DE FIERRO",
            "Todo despunte, recorte y fierro en desuso debe ser separado y acopiado en contenedor metalico identificado. "
            "El retiro debe realizarse por empresa certificada de compra de chatarra con guia de despacho. "
            "El ingreso por venta de fierro debe registrarse en el control de bodega. "
            "Procedimiento de despunte: cortar en trozos menores a 1.5m para facilitar el retiro. Ver instructivo 3.9.",

            "3.6 INSTRUCTIVO DE RECICLAJE DE CARTON",
            "Cajas, tubos de carton y embalajes deben compactarse (aplanar) antes del acopio. "
            "Contenedor identificado 'CARTON' en lugar techado y seco. "
            "Frecuencia de retiro: semanal o al completar el contenedor. "
            "Retiro por empresa de reciclaje con guia de despacho y registro en formulario 4.1.",

            "3.7 INSTRUCTIVO DE RECICLAJE DE PLASTICO",
            "Tipos a separar: (a) Film de envoltura de materiales (plastico transparente, stretch film). "
            "(b) Tuberia PVC en buen estado — ver instructivo 3.8. "
            "(c) Baldes, contenedores plasticos limpios. "
            "El plastico contaminado con adhesivos, pintura o solventes va a residuo peligroso. "
            "Compactar al maximo antes del acopio. Retiro por empresa certificada.",

            "3.8 INSTRUCTIVO DE RECICLAJE DE PVC Y CONDUIT",
            "Tuberia PVC y conduit electrico sobrante debe separarse por tipo: "
            "(a) PVC sanitario — alcantarillado, camaras. "
            "(b) PVC presion — agua potable. "
            "(c) Conduit corrugado electrico. "
            "Los tramos mayores a 0.5m se acopian como material reutilizable. Los menores van a reciclaje plastico. "
            "Retiro por empresa certificada de reciclaje PVC o entrega a proveedor que acepte devoluciones.",

            "3.9 INSTRUCTIVO DE VENTA Y DESPUNTE DE FIERRO",
            "Proceso de venta: (1) Acumular minimo 200 kg antes de gestionar retiro. "
            "(2) Solicitar cotizacion a empresa compradora certificada (ver listado seccion 10). "
            "(3) Pesar y registrar en presencia del representante comprador. "
            "(4) Exigir guia de despacho con peso, precio y datos de la empresa. "
            "(5) Registrar ingreso en libro de obra y en formulario 4.1. "
            "El monto obtenido por venta de fierro debe informarse al Administrador de Obra.",

            "3.10 INSTRUCTIVO DE MITIGACION DE RUIDOS",
            "Horarios permitidos de trabajo con maquinaria ruidosa: lunes a viernes 8:00 a 20:00 hrs, sabado 9:00 a 14:00 hrs. "
            "Fuera de estos horarios queda prohibido el uso de: martillos hidraulicos, vibradores de hormigon, compresores sin caja acustica. "
            "Medidas obligatorias: (a) Instalar caja acustica en grupo electrogeno y compresor antes del inicio de faenas. "
            "(b) Mantener cierre perimetral en buen estado como barrera acustica. "
            "(c) Ante reclamo de vecino: detener la actividad ruidosa, registrar el incidente en libro de obra, "
            "notificar al Director de Obra y gestionar solucion dentro de 24 horas.",
        ]
        print(f"Instructivos 3.1-3.10 expandidos con contenido completo")
        break

# ══════════════════════════════════════════════════════════════
# CORRECCIÓN 3: DIA completo
# ══════════════════════════════════════════════════════════════
for idx, s in enumerate(amb):
    if s["title"] == "7. Resolucion DIA — Declaracion de Impacto Ambiental":
        s["content"] = [
            "QUE ES LA DIA: La Declaracion de Impacto Ambiental (DIA) es el instrumento de gestion ambiental del "
            "Sistema de Evaluacion de Impacto Ambiental (SEIA) de Chile. Toda obra o actividad que pueda causar "
            "impacto ambiental significativo debe ingresar al SEIA. La DIA es la alternativa a la Evaluacion de "
            "Impacto Ambiental (EIA) para proyectos de menor impacto.",

            "CUANDO APLICA: Una obra de construccion debe ingresar al SEIA si supera los umbrales del articulo 10 "
            "de la Ley 19.300 o si se trata de un proyecto habitacional en zona con restricciones ambientales especiales "
            "(plan regulador ambiental, zona de proteccion, etc.). El equipo de oficina central determina si el proyecto "
            "requiere DIA antes del inicio de los tramites municipales.",

            "OBLIGACIONES DEL DIRECTOR DE OBRA CON LA DIA:",
            "1. Mantener copia vigente de la Resolucion de Calificacion Ambiental (RCA) aprobada en la oficina de obra, "
            "accesible en cualquier momento para fiscalizacion.",
            "2. Conocer todos los compromisos ambientales voluntarios declarados en la DIA "
            "(medidas de mitigacion, plan de seguimiento, monitoreos exigidos).",
            "3. Verificar mensualmente el cumplimiento de cada compromiso DIA durante la ejecucion de la obra.",
            "4. Registrar el cumplimiento en la Matriz de Cumplimiento Ambiental (seccion 6.1).",
            "5. Informar de inmediato a la Gerencia Tecnica y al area ambiental de oficina central ante cualquier "
            "desviacion de un compromiso DIA.",
            "6. En caso de modificacion del proyecto que pueda afectar la DIA aprobada, solicitar pronunciamiento "
            "al area ambiental antes de ejecutar el cambio.",

            "CONSECUENCIAS DEL INCUMPLIMIENTO: El incumplimiento de compromisos DIA puede resultar en: "
            "(a) Denuncia ante el Servicio de Evaluacion Ambiental (SEA) por parte de la comunidad o la autoridad. "
            "(b) Multa del Tribunal Ambiental (hasta 10.000 UTA en casos graves). "
            "(c) Paralizacion de faenas ordenada por la Superintendencia del Medio Ambiente (SMA). "
            "(d) Revocacion de la RCA en casos de incumplimiento reiterado.",

            "SEGUIMIENTO MENSUAL DE COMPROMISOS DIA:",
            "El Director de Obra debe completar mensualmente la Matriz de Cumplimiento (formato 6.1) verificando:",
            "- Medidas de control de polvo (humectacion de caminos, cierre perimetral).",
            "- Control de ruido (horarios, caja acustica, monitoreo si exige la DIA).",
            "- Manejo de residuos conforme al plan de gestion.",
            "- Control de escurrimiento superficial (cunetas, sedimentadores si aplica).",
            "- Cualquier monitoreo especifico exigido en la RCA (calidad de agua, flora, fauna, etc.).",
            "La matriz completada debe enviarse mensualmente al area ambiental de oficina central.",

            "RELACION CON EL MANUAL DE CALIDAD: El Manual de Calidad menciona la DIA en el check list de "
            "inicio de obra (ultima actualizacion de DIA y de EISTU). Esta mencion debe complementarse con el "
            "seguimiento mensual descrito en esta seccion. El ECO y el Director de Obra tienen responsabilidades "
            "conjuntas en el cumplimiento ambiental durante la ejecucion.",
        ]
        print("DIA: seccion expandida con procedimiento completo")
        break

# ══════════════════════════════════════════════════════════════
# CORRECCIÓN 4: Cierre perimetral y caja acustica como consulta
# ══════════════════════════════════════════════════════════════
for idx, s in enumerate(amb):
    if s["title"] == "8. Medidas de Mitigacion":
        s["content"] = [
            "Las medidas de mitigacion son requisitos obligatorios antes y durante la ejecucion de toda obra urbana. "
            "Su instalacion debe verificarse en el check list de inicio de obra.",

            "8.1 CIERRE PERIMETRAL DE OBRA — ESPECIFICACIONES TECNICAS:",
            "Altura minima: 2.0 metros en perimetro que da a la via publica.",
            "Material aceptado: paneles de metal galvanizado, zinc o similar de alta resistencia; "
            "o tablas de madera de minimo 1 pulgada de espesor correctamente trabadas.",
            "Fundacion: los postes deben estar empotrados minimo 0.5m en el suelo o con base de hormigon.",
            "Senaletica obligatoria en el cierre: nombre de la empresa, nombre de la obra, "
            "numero de permiso de edificacion, datos de contacto del Director de Obra, "
            "senales de peligro y prohibicion de ingreso.",
            "Mantenimiento: revisar semanalmente la integridad del cierre. "
            "Los danos deben repararse dentro de las 24 horas siguientes.",
            "Puerta de acceso: debe tener cierre con llave y permanecer cerrada fuera del horario de obra.",
            "El cierre perimetral actua adicionalmente como barrera acustica y de polvo.",

            "8.2 CAJA ACUSTICA — ESPECIFICACIONES:",
            "Equipos que requieren caja acustica obligatoria en obras urbanas: "
            "grupos electrogenos de cualquier potencia, compresores de aire, motobombas.",
            "Reduccion acustica minima requerida: 15 dB(A) sobre el nivel de fondo del entorno.",
            "Construccion: estructura de madera o metal con revestimiento interior de material "
            "fonoabsorbente (espuma de poliuretano de alta densidad o paneles de lana mineral de minimo 50mm).",
            "Ventilacion: la caja debe tener entradas y salidas de aire tipo laberinto "
            "para disipar calor sin perder eficiencia acustica.",
            "Instalacion: la caja debe estar montada sobre base antivibracion "
            "(soportes de goma o similar) para evitar transmision de vibraciones al suelo.",
            "Verificacion: medir el nivel sonoro en el limite del predio con la caja instalada. "
            "Si supera los limites de la ordenanza municipal vigente, reforzar el aislamiento.",

            "8.3 LAVADO DE RUEDAS — ESPECIFICACIONES:",
            "Obligatorio en toda obra con acceso de camiones de alto tonelaje a via publica.",
            "Sistema minimo aceptado: fosa de agua con cepillos o rejilla metalica + manguera a presion.",
            "Ubicacion: inmediatamente antes de la salida a la via publica.",
            "El agua de lavado debe ser captada y enviada a la red de alcantarillado "
            "o a decantador antes de su descarga.",
            "Control: el personal de porteria es responsable de verificar el lavado de ruedas "
            "de cada camion antes de su salida.",
        ]
        print("Cierre perimetral y caja acustica: especificaciones completas agregadas")
        break

# ══════════════════════════════════════════════════════════════
# CORRECCIONES 5 y 6: No aplica — validado en instructivo
# ══════════════════════════════════════════════════════════════
for i in inc:
    if i["id"] == 20:
        i["estado"] = "No aplica"
        i["recomendacion"] = "[NO APLICA] La validacion de empresas certificadas de escombros se realiza dentro del instructivo ambiental de control de residuos (seccion 3.2 y 10.1). No requiere modificacion en el proceso de subcontratacion."
    if i["id"] == 21:
        i["estado"] = "No aplica"
        i["recomendacion"] = "[NO APLICA] El registro de consumo de agua y luz esta integrado en los instructivos ambientales (formulario 4.2). No requiere modificacion en el control administrativo principal."

# Marcar inconsistencias 17 (residuos) como corregida
for i in inc:
    if i["id"] == 17:
        i["estado"] = "Corregido"
        i["recomendacion"] = "[CORREGIDO] Instructivos de reciclaje 3.1-3.10 agregados con contenido completo al Manual Ambiental. Responsable: Director de Obra con apoyo del ECO."

# Marcar inconsistencia 18 (DIA) como corregida
for i in inc:
    if i["id"] == 18:
        i["estado"] = "Corregido"
        i["recomendacion"] = "[CORREGIDO] Procedimiento completo de seguimiento DIA agregado al Manual Ambiental con obligaciones del Director de Obra, consecuencias de incumplimiento y seguimiento mensual."

# Marcar inconsistencia 19 (cierre perimetral) como corregida
for i in inc:
    if i["id"] == 19:
        i["estado"] = "Corregido"
        i["recomendacion"] = "[CORREGIDO] Especificaciones tecnicas de cierre perimetral y caja acustica agregadas al Manual Ambiental como informacion de consulta."

# ── Guardar ──────────────────────────────────────────────────
with open("manual_sections.json", "w", encoding="utf-8") as f:
    json.dump(adm, f, ensure_ascii=False, indent=2)
with open("calidad_sections.json", "w", encoding="utf-8") as f:
    json.dump(cal, f, ensure_ascii=False, indent=2)
with open("ambiental_sections.json", "w", encoding="utf-8") as f:
    json.dump(amb, f, ensure_ascii=False, indent=2)
with open("inconsistencias.json", "w", encoding="utf-8") as f:
    json.dump(inc, f, ensure_ascii=False, indent=2)

corr = [x for x in inc if x.get("estado") == "Corregido"]
no_apl = [x for x in inc if x.get("estado") == "No aplica"]
pend = [x for x in inc if x.get("estado") not in ("Corregido", "No aplica")]
print(f"\nResumen inconsistencias: {len(corr)} corregidas | {len(no_apl)} no aplica | {len(pend)} pendientes")
