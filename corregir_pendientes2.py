import json

with open("manual_sections.json", encoding="utf-8") as f:
    adm = json.load(f)
with open("calidad_sections.json", encoding="utf-8") as f:
    cal = json.load(f)
with open("inconsistencias.json", encoding="utf-8") as f:
    inc = json.load(f)

def mark(inc_list, id_, estado, nota):
    for i in inc_list:
        if i["id"] == id_:
            i["estado"] = estado
            i["recomendacion"] = f"[{estado.upper()}] " + nota

# ── #3: umbral nota 4 en calidad[17] ───────────────────────────
texto_eval = (
    "ESCALA DE EVALUACION Y REPORTE A GERENCIA (alineado con Manual de Administracion): "
    "La evaluacion cuantitativa que se realiza todos los jueves mediante encuesta de Google "
    "tiene umbral de alerta en nota menor a 4. Cuando la evaluacion arroja nota inferior a 4, "
    "el ECO y/o supervisor debe generar de inmediato un informe dirigido a la Gerencia de Calidad "
    "y al Gerente Tecnico, indicando causas y plan de accion correctivo con plazos. "
    "Este informe se envia dentro de las 48 horas siguientes a la evaluacion. "
    "La mejora debe ser verificable en la evaluacion de la semana siguiente."
)
if texto_eval not in cal[17]["content"]:
    cal[17]["content"].insert(0, texto_eval)
    print(f"OK #3 - Umbral nota 4 en: {cal[17]['title'][:60]}")

mark(inc, 3, "Corregido",
     "Umbral nota < 4 incorporado en Manual de Calidad: obliga informe a Gerencia en 48 horas con plan correctivo.")

# ── #5: plazo 1 mes informe final en calidad[18] ───────────────
texto_termino = (
    "PLAZO INFORME FINAL DE OBRA (alineado con Manual de Administracion): "
    "El Informe Final de Obra debe ser entregado con un plazo maximo de 1 mes contado "
    "desde la fecha de Recepcion Municipal. "
    "Debe ser suscrito por el Director de Obra y el Constructor Control de Calidad, "
    "con Visto Bueno del Subgerente de Calidad antes de su entrega definitiva a la Gerencia."
)
if texto_termino not in cal[18]["content"]:
    cal[18]["content"].append(texto_termino)
    print(f"OK #5 - Plazo 1 mes en: {cal[18]['title'][:60]}")

mark(inc, 5, "Corregido",
     "Plazo 1 mes desde Recepcion Municipal incorporado en Manual de Calidad, alineado con Manual de Administracion.")

# ── #6: pago quincenal en calidad[17] ──────────────────────────
texto_pago = (
    "FRECUENCIA DE ESTADOS DE PAGO A SUBCONTRATISTAS (alineado con Manual de Administracion): "
    "Los Estados de Pago se procesan en forma quincenal. El VB del ECO en la ficha de calidad "
    "es requisito previo e indispensable para procesar el pago. "
    "El Estado de Pago debe ser presentado el lunes de la semana de pago a mas tardar a las 24 horas. "
    "No se cancelaran Estados de Pago sin VB de calidad en las partidas correspondientes."
)
if texto_pago not in cal[17]["content"]:
    cal[17]["content"].append(texto_pago)
    print(f"OK #6 - Pago quincenal en: {cal[17]['title'][:60]}")

mark(inc, 6, "Corregido",
     "Periodicidad quincenal de pagos incorporada en Manual de Calidad con VB de calidad como requisito previo.")

# ── #12: sabana — quitar del glosario, poner en seccion correcta ─
# Quitar del glosario (cal[11]) si se coló ahí
texto_sabana = (
    "RESPONSABLE DE LA SABANA DE MATERIALES (alineado con Manual de Administracion): "
    "La sabana de materiales es generada por el Administrador de Obra al inicio del proyecto, "
    "inmediatamente despues de tener el presupuesto en control. "
    "El ECO valida y corrige la sabana con las casas piloto de cada modelo. "
    "La version corregida y validada por el ECO es la version oficial vigente y constituye "
    "la base para el proximo proyecto de la misma tipologia. "
    "En caso de diferencias en cubicaciones, el Administrador de Obra genera la RDI correspondiente."
)
cal[11]["content"] = [p for p in cal[11]["content"] if p != texto_sabana]

# Poner en seccion "2. DURANTE LA EJECUCION" (cal[15]) validacion sabana
if texto_sabana not in cal[15]["content"]:
    cal[15]["content"].append(texto_sabana)
    print(f"OK #12 - Sabana materiales en: {cal[15]['title'][:60]}")

mark(inc, 12, "Corregido",
     "Flujo definitivo: Administrador genera sabana inicial; ECO valida con casas piloto; version corregida es la oficial.")

# ── #15: Gantt — Gerente Construccion + Subgerente Programacion ─
texto_gantt = (
    "VALIDACION FORMAL DE CARTA GANTT: "
    "La Carta Gantt elaborada por el Director de Obra debe ser validada por "
    "el Gerente de Construccion y el Subgerente de Programacion. "
    "Adicionalmente la visaran el Gerente Tecnico y el Gerente de Operaciones. "
    "El ECO tiene rol consultivo en secuencia constructiva y partidas criticas de calidad, "
    "pero la validacion formal recae en el Gerente de Construccion y el Subgerente de Programacion."
)
# Admin: seccion [3] Programacion y Control de Plazos
if texto_gantt not in adm[3]["content"]:
    adm[3]["content"].append(texto_gantt)
    print(f"OK #15 Admin - Gantt en: {adm[3]['title']}")
# Admin: seccion [11] Programacion de la Obra
if texto_gantt not in adm[11]["content"]:
    adm[11]["content"].append(texto_gantt)
    print(f"OK #15 Admin - Gantt en: {adm[11]['title']}")
# Calidad: plan de calidad cal[16]
texto_gantt_cal = (
    "VALIDACION CARTA GANTT (alineado con Manual de Administracion): "
    "La Carta Gantt es validada formalmente por el Gerente de Construccion y el Subgerente de Programacion. "
    "El ECO tiene rol consultivo en secuencia constructiva y partidas criticas, no de validador formal."
)
if texto_gantt_cal not in cal[16]["content"]:
    cal[16]["content"].append(texto_gantt_cal)
    print(f"OK #15 Calidad - Gantt en: {cal[16]['title'][:60]}")

mark(inc, 15, "Corregido",
     "Carta Gantt validada por Gerente de Construccion y Subgerente de Programacion. ECO tiene rol consultivo.")

# ── Guardar ──────────────────────────────────────────────────
with open("manual_sections.json", "w", encoding="utf-8") as f:
    json.dump(adm, f, ensure_ascii=False, indent=2)
with open("calidad_sections.json", "w", encoding="utf-8") as f:
    json.dump(cal, f, ensure_ascii=False, indent=2)
with open("inconsistencias.json", "w", encoding="utf-8") as f:
    json.dump(inc, f, ensure_ascii=False, indent=2)

corr   = [x for x in inc if x.get("estado") == "Corregido"]
no_apl = [x for x in inc if x.get("estado") == "No aplica"]
pend   = [x for x in inc if x.get("estado") not in ("Corregido","No aplica")]
print(f"\nResumen final: {len(corr)} corregidas | {len(no_apl)} no aplica | {len(pend)} pendientes")
for p in pend:
    print(f"  [{p['id']}] {p['tema'][:70]}")
