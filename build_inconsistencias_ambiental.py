"""
Analiza inconsistencias entre el indice ambiental y los manuales de Admin y Calidad.
Agrega nuevas inconsistencias al archivo inconsistencias.json.
"""
import json

with open("inconsistencias.json", encoding="utf-8") as f:
    inc = json.load(f)

nuevas = [
  {
    "id": 16,
    "tema": "Inicio de obra — Cartas ambientales obligatorias no mencionadas en check list",
    "tipo": "Brecha",
    "severidad": "Alta",
    "estado": "Pendiente",
    "manual_origen": "ambiental",
    "admin_dice": "El check list de inicio de obra (sección 'Inicio de Obra') lista antecedentes técnicos, contractuales y de loteo, pero NO menciona las cartas ambientales obligatorias (carta a vecinos, carta DOM, carta Carabineros, plan de mitigación).",
    "calidad_dice": "El check list del Anexo 1 del Manual de Calidad tampoco incluye la verificación de las cartas ambientales de inicio como requisito previo para el inicio de faenas.",
    "ambiental_dice": "La sección 2 del índice ambiental establece que TODA obra debe tramitar ANTES de iniciar faenas: carta a vecinos, carta DOM con plan de mitigación, y carta Carabineros (para obras con intervención en vía pública).",
    "recomendacion": "Incorporar en el check list de inicio de obra (tanto del Manual de Administración como del Anexo 1 del Manual de Calidad) la verificación de las cartas ambientales obligatorias como requisito bloqueante para el inicio de faenas."
  },
  {
    "id": 17,
    "tema": "Manejo de residuos — Sin responsable definido en Manual de Administración ni de Calidad",
    "tipo": "Brecha",
    "severidad": "Alta",
    "estado": "Pendiente",
    "manual_origen": "ambiental",
    "admin_dice": "El Manual de Administración no menciona ni al responsable del manejo de residuos ni el procedimiento de clasificación, reciclaje y disposición final de escombros, madera, fierro, plástico, PVC y cartón.",
    "calidad_dice": "El Manual de Calidad menciona que se debe 'supervisar el buen almacenaje de materiales' pero no establece procedimientos de manejo de residuos de construcción ni define un responsable formal.",
    "ambiental_dice": "El índice ambiental cuenta con 8 instructivos específicos de reciclaje (ladrillos, madera, fierro, cartón, plástico, PVC) y un instructivo general de manejo de residuos. Existe además un formulario de registro (4.1) para control periódico.",
    "recomendacion": "Incorporar en el Manual de Administración y/o Calidad una sección de 'Gestión Ambiental en Obra' que defina al responsable (¿Director de Obra? ¿Encargado Ambiental?) y haga referencia expresa a los instructivos ambientales de reciclaje y al formulario de registro."
  },
  {
    "id": 18,
    "tema": "Resolución DIA — Citada en Calidad pero no integrada al flujo operacional",
    "tipo": "Brecha",
    "severidad": "Media",
    "estado": "Pendiente",
    "manual_origen": "ambiental",
    "admin_dice": "El Manual de Administración no hace referencia a la Resolución DIA ni al cumplimiento de compromisos ambientales durante la ejecución.",
    "calidad_dice": "El Manual de Calidad menciona el 'DIA' en el contexto de la estrategia de calidad ('Atender observaciones de inspecciones DS49' y en el check list de inicio menciona 'Última actualización de DIA'), pero no define un procedimiento de seguimiento de compromisos DIA.",
    "ambiental_dice": "La sección 7 del índice ambiental establece que toda obra con DIA debe mantener la documentación en obra y cumplir sus compromisos, con riesgo de paralización por la autoridad ambiental en caso de incumplimiento.",
    "recomendacion": "Definir en el Manual de Administración o en el Manual de Calidad el procedimiento de seguimiento de compromisos DIA: responsable, frecuencia de revisión, registro de cumplimiento y acción ante incumplimiento. El DIA es un instrumento legal vinculante."
  },
  {
    "id": 19,
    "tema": "Cierre perimetral y medidas de mitigación — Sin referencia en manuales operacionales",
    "tipo": "Brecha",
    "severidad": "Media",
    "estado": "Pendiente",
    "manual_origen": "ambiental",
    "admin_dice": "El Manual de Administración no menciona el cierre perimetral, cajas acústicas ni sistema de lavado de ruedas como requisitos de inicio o de operación continua.",
    "calidad_dice": "El Manual de Calidad no incluye las medidas de mitigación ambiental (cierre perimetral, caja acústica, lavado de ruedas) dentro del plan de calidad ni del check list de inicio.",
    "ambiental_dice": "La sección 8 del índice ambiental establece el cierre perimetral como requisito previo al inicio de faenas, y la caja acústica como obligatoria en obras urbanas.",
    "recomendacion": "Incorporar en el check list de inicio de obra (Admin y Calidad) la verificación de cierre perimetral instalado, caja acústica operativa (para obras urbanas) y sistema de lavado de ruedas como requisitos bloqueantes."
  },
  {
    "id": 20,
    "tema": "Empresas de retiro de escombros — Sin validación en proceso de contratación de subcontratistas",
    "tipo": "Brecha",
    "severidad": "Media",
    "estado": "Pendiente",
    "manual_origen": "ambiental",
    "admin_dice": "El Manual de Administración describe el proceso de contratación de subcontratistas (cotizaciones, contratos, retenciones) pero no incluye la verificación de certificación ambiental para empresas de retiro de escombros.",
    "calidad_dice": "El Manual de Calidad no menciona la validación de certificación ambiental como requisito para la contratación de empresas de retiro de escombros y residuos especiales.",
    "ambiental_dice": "La sección 10 del índice ambiental establece que solo se pueden contratar empresas que figuren en el listado de empresas certificadas o que acrediten autorización de la autoridad sanitaria/ambiental.",
    "recomendacion": "Incorporar en el proceso de aprobación de subcontratistas del Manual de Administración la verificación de certificación ambiental para empresas de retiro de escombros y residuos especiales."
  },
  {
    "id": 21,
    "tema": "Registro de consumo de agua y luz — No integrado al control administrativo",
    "tipo": "Brecha",
    "severidad": "Baja",
    "estado": "Pendiente",
    "manual_origen": "ambiental",
    "admin_dice": "El Manual de Administración controla el consumo de agua en el contexto de la humectación (control de hormigones, riego), pero no integra el registro de consumo de servicios básicos como indicador de eficiencia ambiental.",
    "calidad_dice": "El Manual de Calidad incluye planillas de control de riego (Anexo 12) pero no las vincula a un registro ambiental de consumo.",
    "ambiental_dice": "La sección 4.2 del índice ambiental establece un formulario específico de 'Registro de servicios básicos (agua y luz)' como indicador de eficiencia ambiental.",
    "recomendacion": "Incorporar el registro de consumo de agua y luz como parte del informe mensual de obra o de la evaluación semanal de calidad, vinculándolo al formulario ambiental 4.2."
  }
]

# Agregar solo los que no existan
ids_existentes = {i["id"] for i in inc}
for n in nuevas:
    if n["id"] not in ids_existentes:
        inc.append(n)

with open("inconsistencias.json", "w", encoding="utf-8") as f:
    json.dump(inc, f, ensure_ascii=False, indent=2)

total = len(inc)
amb = [x for x in inc if x.get("manual_origen") == "ambiental"]
print(f"Total inconsistencias: {total} ({len(amb)} nuevas desde Manual Ambiental)")
