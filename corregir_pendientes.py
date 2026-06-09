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

# ══════════════════════════════════════════════════════════════
# #3 — Evaluacion semanal: agregar umbral nota 4 a Calidad
# ══════════════════════════════════════════════════════════════
texto_eval = (
    "ESCALA DE EVALUACION Y REPORTE A GERENCIA (alineado con Manual de Administracion): "
    "La evaluacion semanal que se realiza todos los jueves mediante encuesta de Google es cuantitativa. "
    "Si la nota obtenida es menor a 4, el ECO y/o supervisor debe generar de inmediato un informe "
    "dirigido a la Gerencia de Calidad y al Gerente Tecnico, indicando las causas de la baja evaluacion "
    "y el plan de accion correctivo con plazos. Este informe debe ser enviado dentro de las 48 horas "
    "siguientes a la evaluacion. La mejora debe ser verificable en la evaluacion de la semana siguiente."
)
for s in cal:
    if "evaluacion de caracter cuantitativo" in s.get("title", "").lower():
        if texto_eval not in s["content"]:
            s["content"].insert(0, texto_eval)
        print("OK #3 - Umbral nota 4 agregado a Calidad")
        break

mark(inc, 3, "Corregido",
     "Umbral nota menor a 4 incorporado en Manual de Calidad: obliga a informe a Gerencia dentro de 48 horas con plan correctivo.")

# ══════════════════════════════════════════════════════════════
# #5 — Termino de obra: agregar plazo 1 mes a Calidad
# ══════════════════════════════════════════════════════════════
texto_termino = (
    "PLAZO INFORME FINAL DE OBRA (alineado con Manual de Administracion): "
    "El Informe Final de Obra debe ser entregado con un plazo maximo de 1 mes "
    "contado desde la fecha de Recepcion Municipal. "
    "El informe debe ser suscrito por el Director de Obra y el Constructor Control de Calidad, "
    "con Visto Bueno del Subgerente de Calidad antes de su entrega definitiva a la Gerencia."
)
for s in cal:
    if "informe final de obra" in s.get("title", "").lower():
        if texto_termino not in s["content"]:
            s["content"].append(texto_termino)
        print("OK #5 - Plazo 1 mes agregado a Calidad (Informe Final)")
        break

mark(inc, 5, "Corregido",
     "Plazo de 1 mes desde Recepcion Municipal incorporado en Manual de Calidad, alineado con Manual de Administracion.")

# ══════════════════════════════════════════════════════════════
# #6 — Pago subcontratistas: quincenal en Calidad
# ══════════════════════════════════════════════════════════════
texto_pago = (
    "FRECUENCIA DE ESTADOS DE PAGO A SUBCONTRATISTAS (alineado con Manual de Administracion): "
    "Los Estados de Pago se procesan en forma quincenal. "
    "El VB del ECO en la ficha de calidad (protocolo) de cada partida es requisito previo e indispensable "
    "para procesar el Estado de Pago correspondiente. "
    "El Estado de Pago debe ser presentado el lunes de la semana de pago a mas tardar a las 24 horas. "
    "No se cancelaran Estados de Pago que no cumplan este requisito ni que tengan partidas sin VB de calidad."
)
for s in cal:
    if "evaluacion de caracter cuantitativo" in s.get("title", "").lower():
        if texto_pago not in s["content"]:
            s["content"].append(texto_pago)
        print("OK #6 - Periodicidad quincenal pagos subcontratistas agregada a Calidad")
        break

mark(inc, 6, "Corregido",
     "Periodicidad quincenal de pagos a subcontratistas y VB de calidad como requisito previo incorporados en Manual de Calidad.")

# ══════════════════════════════════════════════════════════════
# #8 — Acceso a bodegas: lista definitiva en Admin
# ══════════════════════════════════════════════════════════════
lista_acceso = (
    "PERSONAS AUTORIZADAS A INGRESAR A LAS BODEGAS: "
    "Las unicas personas autorizadas a ingresar a las bodegas son: "
    "bodeguero, ayudante de bodega, digitador, administrador de obra, director de obra, "
    "administrativo de abastecimiento, auditores, jefes de oficina, subgerentes y gerentes. "
    "Toda persona ajena a esta lista debera permanecer fuera del recinto. "
    "Cuando personal no autorizado solicite materiales, debera esperar fuera de la bodega "
    "mientras el bodeguero gestiona la entrega."
)
for s in adm:
    title_l = s.get("title", "").lower()
    if "bodega" in title_l and ("acceso" in title_l or "bodeguero" in title_l):
        # Reemplazar el parrafo restrictivo anterior si existe
        s["content"] = [
            p for p in s["content"]
            if "unicas personas" not in p.lower() and "solo el bodeguero" not in p.lower()
        ]
        if lista_acceso not in s["content"]:
            s["content"].insert(0, lista_acceso)
        print(f"OK #8 - Lista acceso bodega actualizada en: {s['title']}")

# Buscar en todas las secciones que contengan el texto restrictivo original
for s in adm:
    for p in s["content"]:
        if "unicas personas autorizadas a ingresar" in p.lower() and "solo el bodeguero" not in p.lower():
            idx = s["content"].index(p)
            s["content"][idx] = lista_acceso
            print(f"OK #8 - Parrafo acceso bodega reemplazado en: {s['title']}")

mark(inc, 8, "Corregido",
     "Lista definitiva de personas autorizadas a ingresar a bodegas: bodeguero, ayudante, digitador, administrador, director, administrativo abastecimiento, auditores, jefes oficina, subgerentes y gerentes.")

# ══════════════════════════════════════════════════════════════
# #10 — Terminologia: No aplica
# ══════════════════════════════════════════════════════════════
mark(inc, 10, "No aplica",
     "La diferencia de terminologia entre manuales no es considerada relevante para la operacion diaria.")

# ══════════════════════════════════════════════════════════════
# #11 — Control hormigones: No aplica
# ══════════════════════════════════════════════════════════════
mark(inc, 11, "No aplica",
     "El flujo diferenciado entre Admin (control cuantitativo) y Calidad (ensayos tecnicos) es la forma correcta de operacion.")

# ══════════════════════════════════════════════════════════════
# #12 — Sabana materiales: la genera Administrador de Obra
# ══════════════════════════════════════════════════════════════
texto_sabana = (
    "RESPONSABLE DE LA SABANA DE MATERIALES (alineado con Manual de Administracion): "
    "La sabana de materiales es generada por el Administrador de Obra al inicio del proyecto, "
    "inmediatamente despues de tener el presupuesto en control. "
    "El ECO valida y corrige la sabana con las casas piloto de cada modelo. "
    "La version corregida y validada por el ECO es la version oficial vigente y constituye "
    "la base para el proximo proyecto de la misma tipologia. "
    "En caso de diferencias en cubicaciones, el Administrador de Obra genera la RDI correspondiente."
)
for s in cal:
    if "sabana" in s.get("title", "").lower() or \
       any("sabana" in p.lower() for p in s.get("content", [])):
        if texto_sabana not in s["content"]:
            s["content"].append(texto_sabana)
        print(f"OK #12 - Responsable sabana materiales agregado a Calidad: {s['title']}")
        break

# Tambien actualizar en Admin para que sea coherente
for s in adm:
    if "sabana" in s.get("title", "").lower() or \
       any("sabana de materiales" in p.lower() for p in s.get("content", [])[:3]):
        if texto_sabana not in s["content"]:
            s["content"].append(texto_sabana)
        print(f"OK #12 - Nota sabana materiales en Admin: {s['title']}")
        break

mark(inc, 12, "Corregido",
     "Flujo definitivo: Administrador de Obra genera la sabana inicial; ECO la valida con casas piloto; version corregida queda como oficial para proximos proyectos.")

# ══════════════════════════════════════════════════════════════
# #15 — Carta Gantt: valida Gerente de Construccion y
#        Subgerente de Programacion
# ══════════════════════════════════════════════════════════════
texto_gantt_admin = (
    "VALIDACION DE LA CARTA GANTT: "
    "La programacion de obra (Carta Gantt) es confeccionada por el Director de Obra "
    "y debe ser validada por el Gerente de Construccion y el Subgerente de Programacion. "
    "Adicionalmente el Gerente Tecnico y el Gerente de Operaciones visaran la programacion. "
    "El ECO participa en calidad consultiva en lo que respecta a la secuencia constructiva "
    "y partidas criticas de calidad, pero la validacion formal recae en el Gerente de Construccion "
    "y el Subgerente de Programacion."
)
texto_gantt_cal = (
    "VALIDACION DE LA CARTA GANTT (alineado con Manual de Administracion): "
    "La Carta Gantt elaborada por el Director de Obra debe ser validada formalmente por "
    "el Gerente de Construccion y el Subgerente de Programacion. "
    "El ECO tiene rol consultivo en la validacion, especialmente en lo que respecta a "
    "la secuencia constructiva y partidas criticas de calidad, pero no es validador formal."
)

for s in adm:
    title_l = s.get("title", "").lower()
    if "gantt" in title_l or "programacion" in title_l or "programa" in title_l:
        if texto_gantt_admin not in s["content"]:
            s["content"].append(texto_gantt_admin)
        print(f"OK #15 - Validacion Gantt actualizada en Admin: {s['title']}")
        break

for s in cal:
    if "plan de calidad" in s.get("title", "").lower() or \
       "estrategia" in s.get("title", "").lower():
        if texto_gantt_cal not in s["content"]:
            s["content"].append(texto_gantt_cal)
        print(f"OK #15 - Validacion Gantt agregada a Calidad: {s['title']}")
        break

mark(inc, 15, "Corregido",
     "Validacion formal de Carta Gantt: Gerente de Construccion y Subgerente de Programacion. ECO tiene rol consultivo en secuencia constructiva.")

# ── Guardar ──────────────────────────────────────────────────
with open("manual_sections.json", "w", encoding="utf-8") as f:
    json.dump(adm, f, ensure_ascii=False, indent=2)
with open("calidad_sections.json", "w", encoding="utf-8") as f:
    json.dump(cal, f, ensure_ascii=False, indent=2)
with open("inconsistencias.json", "w", encoding="utf-8") as f:
    json.dump(inc, f, ensure_ascii=False, indent=2)

corr    = [x for x in inc if x.get("estado") == "Corregido"]
no_apl  = [x for x in inc if x.get("estado") == "No aplica"]
pend    = [x for x in inc if x.get("estado") not in ("Corregido","No aplica")]
print(f"\nResumen: {len(corr)} corregidas | {len(no_apl)} no aplica | {len(pend)} pendientes")
for p in pend:
    print(f"  Pendiente: [{p['id']}] {p['tema'][:70]}")
