"""
Genera index.html estático con WebLLM.
Incluye Manual de Administración + Manual de Calidad + Manual Ambiental + Panel de Inconsistencias.
"""
import json, os, re

# ── Cargar manuales ──────────────────────────────────────────
with open('manual_sections.json', 'r', encoding='utf-8') as f:
    raw_admin = json.load(f)

with open('calidad_sections.json', 'r', encoding='utf-8') as f:
    calidad_sections = json.load(f)

with open('ambiental_sections.json', 'r', encoding='utf-8') as f:
    ambiental_sections = json.load(f)

with open('inconsistencias.json', 'r', encoding='utf-8') as f:
    inconsistencias = json.load(f)

# Filtrar índice del manual de administración
def filter_admin(raw):
    import re
    secs = [s for s in raw if not re.search(r'- \d+ -', s['title'])]
    first_h1 = next(i for i,s in enumerate(secs) if s['level'] == 1)
    return secs[first_h1:]

admin_sections = filter_admin(raw_admin)

# Añadir campo 'manual' a cada sección
for s in admin_sections:
    s['manual'] = 'admin'
for s in calidad_sections:
    s['manual'] = 'calidad'
for s in ambiental_sections:
    s['manual'] = 'ambiental'

admin_json     = json.dumps(admin_sections,    ensure_ascii=False)
calidad_json   = json.dumps(calidad_sections,  ensure_ascii=False)
ambiental_json = json.dumps(ambiental_sections, ensure_ascii=False)
incons_json    = json.dumps(inconsistencias,   ensure_ascii=False)

altas      = [x for x in inconsistencias if x['severidad'] == 'Alta'  and x.get('estado') != 'Corregido']
medias     = [x for x in inconsistencias if x['severidad'] == 'Media' and x.get('estado') != 'Corregido']
bajas      = [x for x in inconsistencias if x['severidad'] == 'Baja'  and x.get('estado') != 'Corregido']
corregidas = [x for x in inconsistencias if x.get('estado') == 'Corregido']

HTML = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Manual de Obras — Consultor IA</title>
<style>
  :root {{
    --teal-dark:#1a5c52;--teal:#1f7a6d;--teal-light:#2a9d8f;
    --accent:#e9c46a;--bg:#f0f4f3;--white:#fff;
    --text:#1a1a2e;--text-muted:#5a6a65;--border:#d0e0dc;
    --sidebar-w:260px;--red:#e63946;--orange:#f4a261;--green:#4caf50;
  }}
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--text);height:100vh;display:flex;overflow:hidden}}

  /* Sidebar */
  #sidebar{{width:var(--sidebar-w);background:var(--teal-dark);display:flex;flex-direction:column;flex-shrink:0;height:100vh;overflow:hidden}}
  .sb-header{{padding:18px 16px 12px;border-bottom:1px solid rgba(255,255,255,.1)}}
  .sb-logo{{display:flex;align-items:center;gap:10px}}
  .logo-icon{{width:34px;height:34px;background:var(--teal-light);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:17px}}
  .logo-text{{color:#fff;font-size:14px;font-weight:700}}.logo-sub{{color:rgba(255,255,255,.55);font-size:11px}}
  .sb-nav{{padding:8px;display:flex;flex-direction:column;gap:2px;flex-shrink:0}}
  .nav-btn{{display:flex;align-items:center;gap:10px;padding:9px 12px;border-radius:8px;color:rgba(255,255,255,.75);cursor:pointer;font-size:13px;transition:all .15s;border:none;background:none;width:100%;text-align:left}}
  .nav-btn:hover{{background:rgba(255,255,255,.1);color:#fff}}
  .nav-btn.active{{background:rgba(255,255,255,.18);color:#fff;font-weight:600}}
  .nav-badge{{margin-left:auto;background:var(--red);color:#fff;border-radius:10px;padding:1px 7px;font-size:11px;font-weight:700}}
  .nav-badge.orange{{background:var(--orange)}}
  .sb-sections{{display:none}}

  /* Main */
  #main{{flex:1;display:flex;flex-direction:column;overflow:hidden}}
  .topbar{{background:#fff;border-bottom:1px solid var(--border);padding:12px 24px;display:flex;align-items:center;justify-content:space-between;flex-shrink:0}}
  .topbar-title strong{{color:var(--teal-dark);font-size:17px;display:block}}
  .topbar-title span{{font-size:12.5px;color:var(--text-muted)}}
  .topbar-actions{{display:flex;gap:8px;align-items:center}}
  .btn{{padding:6px 13px;border-radius:8px;font-size:12.5px;font-weight:500;cursor:pointer;border:none;display:flex;align-items:center;gap:5px;transition:all .15s}}
  .btn-outline{{background:transparent;border:1.5px solid var(--border);color:var(--text-muted)}}
  .btn-outline:hover{{border-color:var(--teal);color:var(--teal)}}
  .btn-primary{{background:var(--teal);color:#fff}}.btn-primary:hover{{background:var(--teal-dark)}}

  /* Views */
  .view{{display:none;flex:1;overflow:hidden;flex-direction:column}}.view.active{{display:flex}}

  /* Chat */
  #chat-messages{{flex:1;overflow-y:auto;padding:24px;display:flex;flex-direction:column;gap:16px;scrollbar-width:thin}}
  .message{{display:flex;gap:12px;max-width:820px;animation:fadeIn .2s ease}}
  @keyframes fadeIn{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:translateY(0)}}}}
  .message.user{{align-self:flex-end;flex-direction:row-reverse}}
  .msg-av{{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;flex-shrink:0}}
  .message.assistant .msg-av{{background:var(--teal);color:#fff}}
  .message.user .msg-av{{background:var(--accent);font-size:15px}}
  .msg-bub{{padding:11px 15px;border-radius:12px;font-size:14px;line-height:1.65;max-width:calc(100% - 44px)}}
  .message.assistant .msg-bub{{background:#fff;border:1px solid var(--border);border-top-left-radius:4px}}
  .message.user .msg-bub{{background:var(--teal);color:#fff;border-top-right-radius:4px}}
  .msg-bub p{{margin-bottom:7px}}.msg-bub p:last-child{{margin-bottom:0}}
  .msg-bub ul,.msg-bub ol{{padding-left:18px;margin:5px 0}}.msg-bub li{{margin-bottom:3px}}
  .typing-indicator span{{display:inline-block;width:7px;height:7px;background:var(--teal-light);border-radius:50%;animation:bounce 1.2s infinite;margin:0 2px}}
  .typing-indicator span:nth-child(2){{animation-delay:.2s}}.typing-indicator span:nth-child(3){{animation-delay:.4s}}
  @keyframes bounce{{0%,60%,100%{{transform:translateY(0)}}30%{{transform:translateY(-6px)}}}}
  .chat-input-area{{padding:12px 24px 16px;background:#fff;border-top:1px solid var(--border);flex-shrink:0}}
  .chat-hints{{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:9px}}
  .hint-chip{{padding:4px 11px;background:#fff;border:1px solid var(--border);border-radius:20px;font-size:12px;color:var(--text-muted);cursor:pointer;transition:all .15s}}
  .hint-chip:hover{{border-color:var(--teal);color:var(--teal);background:#f0faf8}}
  .chat-input-wrap{{display:flex;gap:9px;align-items:flex-end;background:var(--bg);border:1.5px solid var(--border);border-radius:12px;padding:9px 11px;transition:border-color .15s}}
  .chat-input-wrap:focus-within{{border-color:var(--teal)}}
  #chat-input{{flex:1;border:none;background:none;font-size:14px;color:var(--text);resize:none;outline:none;max-height:110px;min-height:22px;line-height:1.5;font-family:inherit}}
  #chat-input::placeholder{{color:var(--text-muted)}}
  #send-btn{{width:32px;height:32px;background:var(--teal);border:none;border-radius:8px;color:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:15px;flex-shrink:0;transition:background .15s}}
  #send-btn:hover{{background:var(--teal-dark)}}.#send-btn:disabled{{background:var(--border);cursor:not-allowed}}

  /* Manual toggle tabs */
  .manual-tabs{{display:flex;gap:6px;padding:10px 16px;background:#fff;border-bottom:1px solid var(--border);flex-shrink:0}}
  .mtab{{padding:5px 14px;border-radius:20px;font-size:12.5px;font-weight:600;cursor:pointer;border:1.5px solid var(--border);color:var(--text-muted);transition:all .15s}}
  .mtab.active{{background:var(--teal);color:#fff;border-color:var(--teal)}}
  .mtab:hover:not(.active){{border-color:var(--teal);color:var(--teal)}}

  /* Manual view */
  #manual-view{{flex-direction:column}}
  .manual-inner{{display:flex;flex:1;overflow:hidden}}
  .manual-toc{{width:250px;flex-shrink:0;border-right:1px solid var(--border);overflow-y:auto;background:#fff;padding:10px 7px;scrollbar-width:thin}}
  .toc-title{{font-size:11px;font-weight:700;color:var(--text-muted);text-transform:uppercase;letter-spacing:.8px;padding:4px 8px 7px}}
  .toc-item{{padding:5px 9px;border-radius:6px;font-size:12px;cursor:pointer;color:var(--text-muted);transition:all .15s;line-height:1.35}}
  .toc-item:hover{{background:var(--bg);color:var(--teal)}}.toc-item.active{{background:#e8f5f3;color:var(--teal);font-weight:600}}
  .toc-item.lv1{{font-weight:700;color:var(--text)}}.toc-item.lv4{{padding-left:20px;font-size:11.5px}}
  .manual-content{{flex:1;overflow-y:auto;padding:28px 36px}}
  .sec-header{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px}}
  .sec-title{{font-size:21px;font-weight:700;color:var(--teal-dark);flex:1}}
  .edit-btn{{padding:5px 11px;font-size:12px;background:transparent;border:1.5px solid var(--border);border-radius:6px;color:var(--text-muted);cursor:pointer;transition:all .15s;margin-left:14px;white-space:nowrap}}
  .edit-btn:hover{{border-color:var(--teal);color:var(--teal)}}
  .sec-body p{{font-size:14px;line-height:1.75;color:var(--text);margin-bottom:11px}}
  .empty-state{{text-align:center;padding:60px 24px;color:var(--text-muted);font-size:14px}}
  .empty-state .icon{{font-size:38px;margin-bottom:11px}}

  /* Search */
  #search-view .sw{{padding:28px 36px;overflow-y:auto}}
  .sw-title{{font-size:21px;font-weight:700;color:var(--teal-dark);margin-bottom:7px}}
  .sw-sub{{font-size:13.5px;color:var(--text-muted);margin-bottom:18px}}
  #ms-input{{width:100%;max-width:580px;padding:11px 15px;border:1.5px solid var(--border);border-radius:10px;font-size:14px;font-family:inherit;margin-bottom:18px;outline:none;transition:border-color .15s}}
  #ms-input:focus{{border-color:var(--teal)}}
  .ms-result{{background:#fff;border:1px solid var(--border);border-radius:10px;padding:12px 16px;margin-bottom:9px;cursor:pointer;transition:all .15s;max-width:580px}}
  .ms-result:hover{{border-color:var(--teal);box-shadow:0 2px 8px rgba(31,122,109,.1)}}
  .ms-title{{font-size:13.5px;font-weight:600;color:var(--teal-dark);margin-bottom:3px}}
  .ms-badge{{display:inline-block;padding:1px 8px;border-radius:10px;font-size:11px;font-weight:600;margin-bottom:4px}}
  .ms-badge.admin{{background:#e8f5f3;color:var(--teal)}}.ms-badge.calidad{{background:#fff3cd;color:#856404}}.ms-badge.ambiental{{background:#e8f5ea;color:#2d6a4f}}
  .ms-snip{{font-size:12.5px;color:var(--text-muted);line-height:1.5}}

  /* Inconsistencias */
  #incons-view .iw{{padding:28px 36px;overflow-y:auto;max-width:900px}}
  .iw-title{{font-size:21px;font-weight:700;color:var(--teal-dark);margin-bottom:6px}}
  .iw-sub{{font-size:13.5px;color:var(--text-muted);margin-bottom:20px}}
  .iw-stats{{display:flex;gap:10px;margin-bottom:22px}}
  .stat-pill{{padding:7px 16px;border-radius:10px;font-size:13px;font-weight:700;display:flex;align-items:center;gap:6px}}
  .stat-pill.alta{{background:#fde8ea;color:var(--red)}}.stat-pill.media{{background:#fff3cd;color:#856404}}.stat-pill.baja{{background:#e8f5f3;color:var(--teal)}}
  .incon-card{{background:#fff;border:1px solid var(--border);border-radius:12px;padding:18px 20px;margin-bottom:12px;border-left:4px solid var(--border)}}
  .incon-card.alta{{border-left-color:var(--red)}}.incon-card.media{{border-left-color:var(--orange)}}.incon-card.baja{{border-left-color:var(--green)}}
  .ic-header{{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:10px}}
  .ic-tema{{font-size:14px;font-weight:700;color:var(--text);flex:1;line-height:1.35}}
  .ic-badges{{display:flex;gap:6px;flex-shrink:0;margin-left:12px}}
  .ic-badge{{padding:2px 9px;border-radius:10px;font-size:11.5px;font-weight:600}}
  .ic-badge.alta{{background:#fde8ea;color:var(--red)}}.ic-badge.media{{background:#fff3cd;color:#856404}}.ic-badge.baja{{background:#e8f5f3;color:var(--teal)}}
  .ic-badge.tipo{{background:var(--bg);color:var(--text-muted)}}
  .ic-badge.corregido{{background:#e8f5f3;color:var(--green);border:1px solid #c3e8e0}}
  .incon-card.corregido{{border-left-color:var(--green);opacity:.75}}
  .ic-row{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:10px}}
  .ic-block{{background:var(--bg);border-radius:8px;padding:10px 12px}}
  .ic-block-label{{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.6px;margin-bottom:5px}}
  .ic-block-label.admin{{color:var(--teal)}}.ic-block-label.calidad{{color:#856404}}
  .ic-block p{{font-size:12.5px;color:var(--text);line-height:1.55}}
  .ic-rec{{background:#f0faf8;border:1px solid #c3e8e0;border-radius:8px;padding:9px 12px}}
  .ic-rec-label{{font-size:11px;font-weight:700;color:var(--teal);text-transform:uppercase;letter-spacing:.6px;margin-bottom:4px}}
  .ic-rec p{{font-size:12.5px;color:var(--text);line-height:1.55}}

  /* Settings */
  .settings-inner{{padding:28px 36px;overflow-y:auto;max-width:580px}}
  .set-title{{font-size:21px;font-weight:700;color:var(--teal-dark);margin-bottom:7px}}
  .set-sub{{font-size:13.5px;color:var(--text-muted);margin-bottom:24px}}
  .set-group{{margin-bottom:20px}}
  .set-label{{font-size:13px;font-weight:600;color:var(--text);margin-bottom:4px}}
  .set-desc{{font-size:12px;color:var(--text-muted);margin-bottom:7px;line-height:1.5}}
  .set-input{{width:100%;padding:9px 11px;border:1.5px solid var(--border);border-radius:8px;font-size:13.5px;font-family:inherit;transition:border-color .15s}}
  .set-input:focus{{outline:none;border-color:var(--teal)}}
  .save-btn{{background:var(--teal);color:#fff;border:none;padding:9px 22px;border-radius:8px;font-size:13.5px;font-weight:600;cursor:pointer}}
  .save-btn:hover{{background:var(--teal-dark)}}
  .save-ok{{display:none;font-size:13px;color:var(--teal);margin-left:11px}}

  /* Model overlay */
  #model-overlay{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:200;align-items:center;justify-content:center}}
  #model-overlay.open{{display:flex}}
  .model-card{{background:#fff;border-radius:16px;padding:32px 36px;width:460px;max-width:95vw;text-align:center;box-shadow:0 24px 60px rgba(0,0,0,.25)}}
  .model-card h2{{font-size:19px;color:var(--teal-dark);margin-bottom:7px}}.model-card p{{font-size:13px;color:var(--text-muted);line-height:1.6;margin-bottom:18px}}
  .progress-wrap{{background:#e8f5f3;border-radius:99px;height:9px;overflow:hidden;margin-bottom:9px}}
  .progress-bar{{height:100%;background:var(--teal);border-radius:99px;transition:width .3s;width:0%}}
  .progress-label{{font-size:12px;color:var(--text-muted);margin-bottom:18px;min-height:17px}}
  .model-select-wrap{{margin-bottom:18px;text-align:left}}
  .model-select-label{{font-size:11.5px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:.5px;margin-bottom:5px}}
  .model-select{{width:100%;padding:8px 11px;border:1.5px solid var(--border);border-radius:8px;font-size:13px;font-family:inherit;color:var(--text);background:var(--bg);outline:none}}
  .model-select:focus{{border-color:var(--teal)}}
  .load-btn{{background:var(--teal);color:#fff;border:none;padding:10px 26px;border-radius:10px;font-size:14px;font-weight:600;cursor:pointer;width:100%;transition:background .15s}}
  .load-btn:hover{{background:var(--teal-dark)}}.load-btn:disabled{{background:var(--border);cursor:not-allowed}}
  .model-status{{display:flex;align-items:center;gap:7px;justify-content:center;font-size:12.5px;margin-top:9px;min-height:20px;color:var(--text-muted)}}
  .dot{{width:7px;height:7px;border-radius:50%;background:var(--border);flex-shrink:0}}
  .dot.loading{{background:var(--accent);animation:pulse 1s infinite}}.dot.ready{{background:var(--green)}}
  @keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.4}}}}
  .model-pill{{display:flex;align-items:center;gap:6px;background:#e8f5f3;border:1px solid var(--border);border-radius:20px;padding:4px 11px;font-size:11.5px;color:var(--teal-dark);cursor:pointer}}

  /* Edit modal */
  .modal-overlay{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.4);z-index:100;align-items:center;justify-content:center}}
  .modal-overlay.open{{display:flex}}
  .modal{{background:#fff;border-radius:12px;width:660px;max-width:95vw;max-height:85vh;display:flex;flex-direction:column;box-shadow:0 20px 60px rgba(0,0,0,.2);overflow:hidden}}
  .modal-header{{padding:18px 22px 14px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between}}
  .modal-title{{font-size:15px;font-weight:700;color:var(--teal-dark)}}
  .modal-close{{background:none;border:none;font-size:19px;cursor:pointer;color:var(--text-muted);padding:3px}}
  .modal-body{{padding:18px 22px;overflow-y:auto;flex:1}}
  .modal-footer{{padding:14px 22px;border-top:1px solid var(--border);display:flex;gap:7px;justify-content:flex-end}}
  .form-label{{font-size:11.5px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:.5px;margin-bottom:5px}}
  .form-input{{width:100%;padding:9px 11px;border:1.5px solid var(--border);border-radius:8px;font-size:13.5px;color:var(--text);font-family:inherit;transition:border-color .15s;margin-bottom:14px}}
  .form-input:focus{{outline:none;border-color:var(--teal)}}
  textarea.form-input{{min-height:190px;resize:vertical;line-height:1.6}}

  /* Welcome hero */
  .welcome-hero{{max-width:700px;margin:0 auto;width:100%}}
  .hero-top{{background:linear-gradient(135deg,var(--teal-dark) 0%,var(--teal) 100%);border-radius:16px;padding:32px 36px 28px;color:#fff;margin-bottom:18px;position:relative;overflow:hidden}}
  .hero-top::before{{content:'🏗️';position:absolute;right:28px;top:50%;transform:translateY(-50%);font-size:74px;opacity:.12;pointer-events:none}}
  .hero-label{{font-size:10.5px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:var(--accent);margin-bottom:9px}}
  .hero-title{{font-size:24px;font-weight:800;line-height:1.2;margin-bottom:9px}}
  .hero-sub{{font-size:13.5px;color:rgba(255,255,255,.75);line-height:1.6;margin-bottom:22px;max-width:460px}}
  .hero-stats{{display:flex;gap:22px}}
  .hero-stat .num{{font-size:24px;font-weight:800;color:var(--accent);line-height:1}}
  .hero-stat .lbl{{font-size:10.5px;color:rgba(255,255,255,.55);text-transform:uppercase;letter-spacing:.6px;margin-top:3px}}
  .topics-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:9px;margin-bottom:4px}}
  .topic-card{{background:#fff;border:1.5px solid var(--border);border-radius:12px;padding:13px 15px;cursor:pointer;transition:all .18s;display:flex;align-items:flex-start;gap:9px}}
  .topic-card:hover{{border-color:var(--teal);box-shadow:0 4px 16px rgba(31,122,109,.12);transform:translateY(-2px)}}
  .tc-icon{{font-size:21px;flex-shrink:0}}
  .tc-text{{font-size:13px;font-weight:600;color:var(--teal-dark);line-height:1.3}}
  .tc-hint{{font-size:11px;color:var(--text-muted);margin-top:3px}}
</style>
</head>
<body>

<!-- SIDEBAR -->
<div id="sidebar">
  <div class="sb-header">
    <div class="sb-logo">
      <div class="logo-icon">🏗️</div>
      <div><div class="logo-text">inplanner</div><div class="logo-sub">Control de obra</div></div>
    </div>
  </div>
  <div class="sb-nav">
    <button class="nav-btn active" onclick="showView('chat')" id="nav-chat"><span>💬</span> Consultor IA</button>
    <button class="nav-btn" onclick="showView('manual')" id="nav-manual"><span>📖</span> Manuales</button>
    <button class="nav-btn" onclick="showView('search')" id="nav-search"><span>🔍</span> Buscar</button>
    <button class="nav-btn" onclick="showView('incons')" id="nav-incons">
      <span>⚠️</span> Inconsistencias
      <span class="nav-badge">{len(altas)+len(medias)}</span>
    </button>
    <button class="nav-btn" onclick="showView('settings')" id="nav-settings"><span>⚙️</span> Configuración</button>
  </div>
  <div class="sb-sections" id="sb-sections"></div>
</div>

<!-- MAIN -->
<div id="main">
  <div class="topbar">
    <div class="topbar-title">
      <strong id="view-title">Consultor IA</strong>
      <span id="view-sub">IA local — sin API, sin servidor</span>
    </div>
    <div class="topbar-actions" id="topbar-actions">
      <div class="model-pill" onclick="openModelOverlay()" id="model-pill">
        <div class="dot" id="pill-dot"></div>
        <span id="pill-label">Sin modelo</span>
      </div>
      <button class="btn btn-outline" onclick="clearChat()">🗑 Limpiar</button>
    </div>
  </div>

  <!-- CHAT -->
  <div class="view active" id="chat-view">
    <div id="chat-messages">
      <div class="welcome-hero">
        <div class="hero-top">
          <div class="hero-label">Constructora Independencia S.A.</div>
          <div class="hero-title">Manual de Administración<br>y Control de Calidad</div>
          <div class="hero-sub">Consulta ambos manuales con IA que corre en tu navegador. Sin API, sin servidor, 100% privado.</div>
          <div class="hero-stats">
            <div class="hero-stat"><div class="num">{len(admin_sections)}</div><div class="lbl">Secciones Admin.</div></div>
            <div class="hero-stat"><div class="num">{len(calidad_sections)}</div><div class="lbl">Secciones Calidad</div></div>
            <div class="hero-stat"><div class="num">{len(ambiental_sections)}</div><div class="lbl">Secciones Ambiental</div></div>
            <div class="hero-stat"><div class="num">{len(inconsistencias)}</div><div class="lbl">Inconsistencias</div></div>
          </div>
        </div>
        <div class="topics-grid">
          <div class="topic-card" onclick="ask('¿Cuáles son las funciones del Director de Obras?')"><div class="tc-icon">👷</div><div><div class="tc-text">Director de Obras</div><div class="tc-hint">Roles y responsabilidades</div></div></div>
          <div class="topic-card" onclick="ask('¿Cómo se controla la calidad durante la ejecución de la obra?')"><div class="tc-icon">✅</div><div><div class="tc-text">Control de Calidad</div><div class="tc-hint">ECO, protocolos, fichas</div></div></div>
          <div class="topic-card" onclick="ask('¿Cómo se controlan los plazos con la Carta Gantt?')"><div class="tc-icon">📅</div><div><div class="tc-text">Plazos y Programación</div><div class="tc-hint">Carta Gantt y avance</div></div></div>
          <div class="topic-card" onclick="ask('¿Cómo se maneja el presupuesto y control de costos?')"><div class="tc-icon">💰</div><div><div class="tc-text">Presupuesto</div><div class="tc-hint">Costos, RDI, desviaciones</div></div></div>
          <div class="topic-card" onclick="ask('¿Cuáles son los procedimientos de bodega y abastecimiento?')"><div class="tc-icon">📦</div><div><div class="tc-text">Bodega</div><div class="tc-hint">Materiales, órdenes de compra</div></div></div>
          <div class="topic-card" onclick="ask('¿Cómo se paga y controla a subcontratistas?')"><div class="tc-icon">🤝</div><div><div class="tc-text">Subcontratistas</div><div class="tc-hint">Contratos, retenciones, pagos</div></div></div>
          <div class="topic-card" onclick="ask('¿Cuál es el procedimiento de inicio de obra según ambos manuales?')"><div class="tc-icon">🚀</div><div><div class="tc-text">Inicio de Obra</div><div class="tc-hint">Check list y responsables</div></div></div>
          <div class="topic-card" onclick="ask('¿Qué dice el Manual de Calidad sobre no conformidades?')"><div class="tc-icon">🔴</div><div><div class="tc-text">No Conformidades</div><div class="tc-hint">Plazos y correcciones</div></div></div>
        </div>
      </div>
    </div>
    <div class="chat-input-area">
      <div class="chat-hints">
        <span class="hint-chip" onclick="ask('¿Qué hace el ECO en obra?')">Rol del ECO</span>
        <span class="hint-chip" onclick="ask('¿Cuál es el plazo para corregir una no conformidad?')">No conformidades</span>
        <span class="hint-chip" onclick="ask('¿Cómo se controla el hormigón?')">Control hormigón</span>
        <span class="hint-chip" onclick="ask('¿Qué dice cada manual sobre el inicio de obra?')">Inicio de obra</span>
        <span class="hint-chip" onclick="ask('¿Cuáles son las principales inconsistencias entre manuales?')">Ver inconsistencias</span>
      </div>
      <div class="chat-input-wrap">
        <textarea id="chat-input" placeholder="Pregunta sobre administración, calidad o inconsistencias..." rows="1" onkeydown="handleKey(event)" oninput="autoResize(this)"></textarea>
        <button id="send-btn" onclick="sendMessage()">➤</button>
      </div>
    </div>
  </div>

  <!-- MANUAL -->
  <div class="view" id="manual-view">
    <div class="manual-tabs">
      <button class="mtab active" id="mtab-admin" onclick="switchManual('admin')">📋 Manual de Administración</button>
      <button class="mtab" id="mtab-calidad" onclick="switchManual('calidad')">✅ Manual de Calidad</button>
      <button class="mtab" id="mtab-ambiental" onclick="switchManual('ambiental')">🌿 Manual Ambiental</button>
    </div>
    <div class="manual-inner">
      <div class="manual-toc" id="manual-toc"><div class="toc-title">Secciones</div></div>
      <div class="manual-content" id="manual-content">
        <div class="empty-state"><div class="icon">📖</div>Selecciona una sección del índice</div>
      </div>
    </div>
  </div>

  <!-- SEARCH -->
  <div class="view" id="search-view">
    <div class="sw">
      <div class="sw-title">Buscar en ambos manuales</div>
      <div class="sw-sub">Busca en los tres manuales: Administración, Calidad y Ambiental</div>
      <input id="ms-input" placeholder="Ej: no conformidad, presupuesto, ECO, bodega..." oninput="mainSearch(this.value)">
      <div id="ms-results"></div>
    </div>
  </div>

  <!-- INCONSISTENCIAS -->
  <div class="view" id="incons-view">
    <div class="iw">
      <div class="iw-title">⚠️ Inconsistencias detectadas</div>
      <div class="iw-sub">Análisis cruzado entre los tres manuales (Administración, Calidad y Ambiental). {len(inconsistencias)} hallazgos — {len(corregidas)} corregidos, {len(inconsistencias)-len(corregidas)} pendientes.</div>
      <div class="iw-stats">
        <div class="stat-pill alta">🔴 {len(altas)} Alta pendiente</div>
        <div class="stat-pill media">🟡 {len(medias)} Media pendiente</div>
        <div class="stat-pill baja">🟢 {len(bajas)} Baja pendiente</div>
        <div class="stat-pill baja" style="background:#e8f5f3;color:var(--green)">✅ {len(corregidas)} Corregidas</div>
      </div>
      <div id="incons-list"></div>
    </div>
  </div>

  <!-- SETTINGS -->
  <div class="view" id="settings-view">
    <div class="settings-inner">
      <div class="set-title">Configuración</div>
      <div class="set-sub">Selecciona el modelo de IA. Se descarga una sola vez y se cachea en tu navegador.</div>
      <div class="set-group">
        <div class="set-label">Modelo de IA</div>
        <div class="set-desc">Requiere Chrome/Edge con WebGPU. El modelo corre 100% en tu computador.</div>
        <select class="set-input" id="model-setting">
          <option value="Qwen2.5-0.5B-Instruct-q4f16_1-MLC">Qwen 2.5 — 0.5B · ~400 MB (Rápido)</option>
          <option value="Qwen2.5-1.5B-Instruct-q4f16_1-MLC" selected>Qwen 2.5 — 1.5B · ~900 MB (Recomendado)</option>
          <option value="Phi-3.5-mini-instruct-q4f16_1-MLC">Phi-3.5 Mini · ~2.2 GB (Mejor calidad)</option>
        </select>
      </div>
      <div style="display:flex;align-items:center">
        <button class="save-btn" onclick="saveSettings()">Guardar y cargar modelo</button>
        <span class="save-ok" id="save-ok">✓ Guardado</span>
      </div>
    </div>
  </div>
</div>

<!-- MODEL OVERLAY -->
<div id="model-overlay">
  <div class="model-card">
    <h2>🧠 Cargar modelo de IA</h2>
    <p>El modelo se ejecuta en tu navegador. Sin servidor, sin API, 100% privado. La primera descarga puede tardar varios minutos.</p>
    <div class="model-select-wrap">
      <div class="model-select-label">Modelo</div>
      <select class="model-select" id="overlay-model-select">
        <option value="Qwen2.5-0.5B-Instruct-q4f16_1-MLC">Qwen 2.5 — 0.5B · ~400 MB (Rápido)</option>
        <option value="Qwen2.5-1.5B-Instruct-q4f16_1-MLC" selected>Qwen 2.5 — 1.5B · ~900 MB (Recomendado)</option>
        <option value="Phi-3.5-mini-instruct-q4f16_1-MLC">Phi-3.5 Mini · ~2.2 GB (Mejor calidad)</option>
      </select>
    </div>
    <div class="progress-wrap"><div class="progress-bar" id="prog-bar"></div></div>
    <div class="progress-label" id="prog-label">Esperando...</div>
    <button class="load-btn" id="load-btn" onclick="loadModel()">⚡ Descargar y cargar</button>
    <div class="model-status"><div class="dot" id="status-dot"></div><span id="status-text">Sin modelo</span></div>
  </div>
</div>

<!-- EDIT MODAL -->
<div class="modal-overlay" id="edit-modal">
  <div class="modal">
    <div class="modal-header"><div class="modal-title">✏️ Editar sección</div><button class="modal-close" onclick="closeEditModal()">✕</button></div>
    <div class="modal-body">
      <div class="form-label">Título</div><input type="text" class="form-input" id="edit-title">
      <div class="form-label">Contenido</div><textarea class="form-input" id="edit-content"></textarea>
    </div>
    <div class="modal-footer">
      <button class="btn btn-outline" onclick="closeEditModal()">Cancelar</button>
      <button class="btn btn-primary" onclick="saveSection()">Guardar</button>
    </div>
  </div>
</div>

<script type="module">
import * as webllm from 'https://esm.run/@mlc-ai/web-llm';
window._webllm = webllm;
</script>

<script>
// ── DATOS ─────────────────────────────────────────────────────
const ADMIN_BASE      = {admin_json};
const CALIDAD_BASE    = {calidad_json};
const AMBIENTAL_BASE  = {ambiental_json};
const INCONSISTENCIAS = {incons_json};

let adminSections     = JSON.parse(JSON.stringify(ADMIN_BASE));
let calidadSections   = JSON.parse(JSON.stringify(CALIDAD_BASE));
let ambientalSections = JSON.parse(JSON.stringify(AMBIENTAL_BASE));

// Cargar ediciones guardadas
try {{
  const e = localStorage.getItem('manual_edits_admin');
  if (e) JSON.parse(e).forEach(x => {{ if (adminSections[x.id]) {{ adminSections[x.id].title=x.title; adminSections[x.id].content=x.content; }} }});
  const c = localStorage.getItem('manual_edits_calidad');
  if (c) JSON.parse(c).forEach(x => {{ if (calidadSections[x.id]) {{ calidadSections[x.id].title=x.title; calidadSections[x.id].content=x.content; }} }});
  const a = localStorage.getItem('manual_edits_ambiental');
  if (a) JSON.parse(a).forEach(x => {{ if (ambientalSections[x.id]) {{ ambientalSections[x.id].title=x.title; ambientalSections[x.id].content=x.content; }} }});
}} catch(e) {{}}

// ── ESTADO ─────────────────────────────────────────────────────
let chatHistory = [], engine = null, modelLoading = false;
let currentManual = 'admin', currentSectionId = null, editingManual = null, editingId = null;
let searchTimer = null;
let selectedModel = localStorage.getItem('selected_model') || 'Qwen2.5-1.5B-Instruct-q4f16_1-MLC';

document.addEventListener('DOMContentLoaded', () => {{
  document.getElementById('model-setting').value = selectedModel;
  document.getElementById('overlay-model-select').value = selectedModel;
  renderToc('admin');
  renderInconsistencias();
  updatePill('idle');
}});

// ── VISTAS ────────────────────────────────────────────────────
function showView(name) {{
  document.querySelectorAll('.view').forEach(v=>v.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b=>b.classList.remove('active'));
  document.getElementById(name+'-view').classList.add('active');
  document.getElementById('nav-'+name).classList.add('active');
  const t = {{
    chat:    ['Consultor IA','Pregunta sobre administración, calidad o inconsistencias entre manuales'],
    manual:  ['Manuales','Navega y edita las secciones de ambos manuales'],
    search:  ['Buscar','Busca en el Manual de Administración y el de Calidad'],
    incons:  ['Inconsistencias','Hallazgos del análisis cruzado entre manuales'],
    settings:['Configuración','Modelo de IA y preferencias']
  }};
  document.getElementById('view-title').textContent = t[name][0];
  document.getElementById('view-sub').textContent   = t[name][1];
  const ta = document.getElementById('topbar-actions');
  ta.innerHTML = name==='chat'
    ? `<div class="model-pill" onclick="openModelOverlay()" id="model-pill"><div class="dot" id="pill-dot"></div><span id="pill-label">Sin modelo</span></div><button class="btn btn-outline" onclick="clearChat()">🗑 Limpiar</button>`
    : '';
  if (name==='chat') updatePill(engine?'ready':'idle');
}}
window.showView = showView;

function switchManual(m) {{
  currentManual = m;
  document.getElementById('mtab-admin').classList.toggle('active', m==='admin');
  document.getElementById('mtab-calidad').classList.toggle('active', m==='calidad');
  document.getElementById('mtab-ambiental').classList.toggle('active', m==='ambiental');
  renderToc(m);
  document.getElementById('manual-content').innerHTML = '<div class="empty-state"><div class="icon">📖</div>Selecciona una sección del índice</div>';
}}
window.switchManual = switchManual;

function getSecs(m) {{
  if(m==='admin') return adminSections;
  if(m==='calidad') return calidadSections;
  return ambientalSections;
}}

function renderToc(m) {{
  const secs = getSecs(m);
  document.getElementById('manual-toc').innerHTML = '<div class="toc-title">Secciones</div>' +
    secs.map((s,i) => `<div class="toc-item lv${{s.level}}" id="toc-${{i}}" onclick="openSection(${{i}})">${{s.title.substring(0,55)}}${{s.title.length>55?'…':''}}</div>`).join('');
}}

function openSection(id) {{
  currentSectionId = id;
  showView('manual');
  document.querySelectorAll('.toc-item').forEach(e=>e.classList.remove('active'));
  const tEl = document.getElementById('toc-'+id);
  if (tEl) {{ tEl.classList.add('active'); tEl.scrollIntoView({{block:'nearest'}}); }}
  const s = getSecs(currentManual)[id];
  const badgeColor = currentManual==='admin' ? '#e8f5f3' : currentManual==='calidad' ? '#fff3cd' : '#e8f5ea';
  const badgeText  = currentManual==='admin' ? '📋 Administración' : currentManual==='calidad' ? '✅ Calidad' : '🌿 Ambiental';
  document.getElementById('manual-content').innerHTML = `
    <div class="sec-header">
      <div style="flex:1">
        <div style="display:inline-block;padding:2px 10px;border-radius:10px;font-size:11.5px;font-weight:600;background:${{badgeColor}};margin-bottom:8px">${{badgeText}}</div>
        <div class="sec-title">${{esc(s.title)}}</div>
      </div>
      <button class="edit-btn" onclick="openEditModal(${{id}})">✏️ Editar</button>
    </div>
    <div class="sec-body">${{(s.content||[]).map(p=>`<p>${{esc(p)}}</p>`).join('')}}</div>
  `;
}}
window.openSection = openSection;

// ── INCONSISTENCIAS ────────────────────────────────────────────
function renderInconsistencias() {{
  const order = {{Alta:0,Media:1,Baja:2,Baja_c:3}};
  const sorted = [...INCONSISTENCIAS].sort((a,b)=>{{
    const ac = a.estado==='Corregido';
    const bc = b.estado==='Corregido';
    if(ac&&!bc)return 1; if(!ac&&bc)return -1;
    return (order[a.severidad]||2)-(order[b.severidad]||2);
  }});
  document.getElementById('incons-list').innerHTML = sorted.map(ic => {{
    const corr = ic.estado==='Corregido';
    const cardClass = corr ? 'corregido' : ic.severidad.toLowerCase();
    const rec = corr ? ic.recomendacion.replace('[CORREGIDO] ','') : ic.recomendacion;
    return `<div class="incon-card ${{cardClass}}">
      <div class="ic-header">
        <div class="ic-tema">${{esc(ic.tema)}}</div>
        <div class="ic-badges">
          ${{corr ? '<span class="ic-badge corregido">✅ Corregido</span>' : `<span class="ic-badge ${{ic.severidad.toLowerCase()}}">${{ic.severidad}}</span>`}}
          <span class="ic-badge tipo">${{ic.tipo}}</span>
        </div>
      </div>
      <div class="ic-row">
        <div class="ic-block"><div class="ic-block-label admin">📋 Administración dice</div><p>${{esc(ic.admin_dice)}}</p></div>
        <div class="ic-block"><div class="ic-block-label calidad">${{ic.manual_origen==='ambiental'?'🌿 Ambiental dice':'✅ Calidad dice'}}</div><p>${{esc(ic.manual_origen==='ambiental'?(ic.ambiental_dice||ic.calidad_dice):ic.calidad_dice)}}</p></div>
      </div>
      <div class="ic-rec"><div class="ic-rec-label">${{corr?'✅ Corrección aplicada':'💡 Recomendación'}}</div><p>${{esc(rec)}}</p></div>
    </div>`;
  }}).join('');
}}

// ── CHAT ──────────────────────────────────────────────────────
const SYSTEM_PROMPT = `Eres un asistente experto en los manuales de Constructora Independencia S.A.
Tienes acceso a TRES manuales:
1. Manual de Administración y Control de Obras
2. Manual de Control de Calidad 2025
3. Índice de Documentación Ambiental (gestión de residuos, cartas de inicio, DIA, mitigación)

Responde SIEMPRE en español, de forma clara y profesional.
Cuando corresponda, indica de qué manual proviene la información.
Si hay una inconsistencia conocida entre los manuales, menciónala.

INCONSISTENCIAS DETECTADAS:
${{INCONSISTENCIAS.map(i=>`- ${{i.tema}}: ${{i.tipo}} (${{i.severidad}})`).join('\\n')}}
`;

function buildContext(query) {{
  const tokens = tokenize(query);
  const adminRelev    = bm25(tokens, adminSections,    4).map(r=>(`[ADMIN] ${{r.s.title}}\\n${{(r.s.content||[]).join('\\n').substring(0,500)}}`));
  const calidadRelev  = bm25(tokens, calidadSections,  3).map(r=>(`[CALIDAD] ${{r.s.title}}\\n${{(r.s.content||[]).join('\\n').substring(0,400)}}`));
  const ambientalRelev= bm25(tokens, ambientalSections, 3).map(r=>(`[AMBIENTAL] ${{r.s.title}}\\n${{(r.s.content||[]).join('\\n').substring(0,400)}}`));
  return [...adminRelev, ...calidadRelev, ...ambientalRelev].join('\\n\\n---\\n\\n');
}}

function ask(q) {{ document.getElementById('chat-input').value=q; sendMessage(); }}
window.ask = ask;
function handleKey(e) {{ if(e.key==='Enter'&&!e.shiftKey){{e.preventDefault();sendMessage();}} }}
window.handleKey = handleKey;
function autoResize(el) {{ el.style.height='auto'; el.style.height=Math.min(el.scrollHeight,110)+'px'; }}
window.autoResize = autoResize;

async function sendMessage() {{
  const input = document.getElementById('chat-input');
  const text  = input.value.trim();
  if (!text) return;
  if (!engine) {{ openModelOverlay(); return; }}
  input.value=''; input.style.height='auto';
  document.getElementById('send-btn').disabled = true;
  document.querySelector('.chat-hints').style.display = 'none';
  chatHistory.push({{role:'user',content:text}});
  appendMsg('user', text);
  const tid = 'ty-'+Date.now();
  appendTyping(tid);
  try {{
    const context = buildContext(text);
    const messages = [
      {{role:'system', content: SYSTEM_PROMPT + '\\n\\nCONTEXTO RELEVANTE:\\n---\\n' + context + '\\n---'}},
      ...chatHistory.slice(-6)
    ];
    removeEl(tid);
    const msgEl = appendMsg('assistant','');
    const bubble = msgEl.querySelector('.msg-bub');
    let full = '';
    const stream = await engine.chat.completions.create({{messages,stream:true,max_tokens:600,temperature:0.3}});
    for await (const chunk of stream) {{
      const delta = chunk.choices[0]?.delta?.content || '';
      full += delta;
      bubble.innerHTML = fmtMd(full);
      scrollBottom();
    }}
    chatHistory.push({{role:'assistant',content:full}});
  }} catch(err) {{
    removeEl(tid);
    appendMsg('assistant','❌ Error: '+err.message);
  }}
  document.getElementById('send-btn').disabled = false;
  scrollBottom();
}}
window.sendMessage = sendMessage;

function appendMsg(role, text) {{
  const c=document.getElementById('chat-messages');
  const d=document.createElement('div'); d.className='message '+role;
  d.innerHTML=`<div class="msg-av">${{role==='assistant'?'IA':'👤'}}</div><div class="msg-bub">${{fmtMd(text)}}</div>`;
  c.appendChild(d); scrollBottom(); return d;
}}
function appendTyping(id) {{
  const c=document.getElementById('chat-messages');
  const d=document.createElement('div'); d.className='message assistant'; d.id=id;
  d.innerHTML='<div class="msg-av">IA</div><div class="msg-bub"><div class="typing-indicator"><span></span><span></span><span></span></div></div>';
  c.appendChild(d); scrollBottom();
}}
function removeEl(id){{const el=document.getElementById(id);if(el)el.remove();}}
function scrollBottom(){{const c=document.getElementById('chat-messages');c.scrollTop=c.scrollHeight;}}
function clearChat(){{
  chatHistory=[];
  document.getElementById('chat-messages').innerHTML=`<div class="welcome-hero"><div class="hero-top"><div class="hero-label">Constructora Independencia S.A.</div><div class="hero-title">Manual de Administración<br>y Control de Calidad</div><div class="hero-sub">Consulta ambos manuales con IA local.</div></div><div class="topics-grid"><div class="topic-card" onclick="ask('¿Cuáles son las funciones del Director de Obras?')"><div class="tc-icon">👷</div><div><div class="tc-text">Director de Obras</div><div class="tc-hint">Roles y responsabilidades</div></div></div><div class="topic-card" onclick="ask('¿Cómo se controla la calidad en obra?')"><div class="tc-icon">✅</div><div><div class="tc-text">Control de Calidad</div><div class="tc-hint">ECO, protocolos, fichas</div></div></div><div class="topic-card" onclick="ask('¿Cuáles son las principales inconsistencias entre manuales?')"><div class="tc-icon">⚠️</div><div><div class="tc-text">Inconsistencias</div><div class="tc-hint">Ver diferencias críticas</div></div></div><div class="topic-card" onclick="ask('¿Qué dice el manual de calidad sobre no conformidades?')"><div class="tc-icon">🔴</div><div><div class="tc-text">No Conformidades</div><div class="tc-hint">Plazos y correcciones</div></div></div></div></div>`;
  document.querySelector('.chat-hints').style.display='flex';
}}
window.clearChat = clearChat;

// ── BM25 ──────────────────────────────────────────────────────
function tokenize(text) {{
  return text.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'')
    .split(/\\W+/).filter(t=>t.length>2&&!['que','con','los','las','una','del','por','para','como','son'].includes(t));
}}
function bm25(tokens, secs, topK) {{
  const k1=1.5,b=0.75;
  return secs.map((s,i)=>{{
    const doc=(s.title+' '+(s.content||[]).join(' ')).toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');
    const dtoks=doc.split(/\\W+/).filter(t=>t.length>2);
    const titleToks=s.title.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').split(/\\W+/);
    let score=0;
    for(const t of tokens){{
      const tf=dtoks.filter(x=>x===t).length;
      if(!tf)continue;
      const df=secs.filter(x=>(x.title+' '+(x.content||[]).join(' ')).toLowerCase().includes(t)).length;
      const idf=Math.log(1+(secs.length-df+0.5)/(df+0.5));
      score+=idf*(tf*(k1+1))/(tf+k1*(1-b+b*(dtoks.length/150)));
      if(titleToks.includes(t))score+=2.5;
    }}
    return {{id:i,s,score}};
  }}).filter(x=>x.score>0).sort((a,b)=>b.score-a.score).slice(0,topK);
}}

// ── BÚSQUEDA ─────────────────────────────────────────────────
function mainSearch(q) {{
  clearTimeout(searchTimer);
  const el=document.getElementById('ms-results');
  if(!q.trim()){{el.innerHTML='';return;}}
  searchTimer=setTimeout(()=>{{
    const ql=q.toLowerCase();
    const searchIn = (secs, manualKey) => secs.map((s,i)=>{{
      const ct=(s.content||[]).join(' ');
      const tm=s.title.toLowerCase().includes(ql),cm=ct.toLowerCase().includes(ql);
      if(!tm&&!cm)return null;
      let snip='';if(cm){{const idx=ct.toLowerCase().indexOf(ql),st=Math.max(0,idx-70),en=Math.min(ct.length,idx+110);snip=(st>0?'…':'')+ct.slice(st,en)+(en<ct.length?'…':'');}}
      return {{id:i,title:s.title,snip,manual:manualKey}};
    }}).filter(Boolean);
    const results=[
      ...searchIn(adminSections,'admin'),
      ...searchIn(calidadSections,'calidad'),
      ...searchIn(ambientalSections,'ambiental')
    ].slice(0,30);
    const badgeLabel = {{admin:'📋 Administración', calidad:'✅ Calidad', ambiental:'🌿 Ambiental'}};
    if(!results.length){{el.innerHTML=`<div style="color:var(--text-muted);font-size:14px;padding:10px 0">Sin resultados para "${{esc(q)}}"</div>`;return;}}
    el.innerHTML=results.map(r=>`<div class="ms-result" onclick="switchManual('${{r.manual}}');openSection(${{r.id}})">
      <span class="ms-badge ${{r.manual}}">${{badgeLabel[r.manual]}}</span>
      <div class="ms-title">${{esc(r.title)}}</div>
      ${{r.snip?`<div class="ms-snip">${{esc(r.snip)}}</div>`:''}}
    </div>`).join('');
  }},280);
}}
window.mainSearch = mainSearch;

// ── EDICIÓN ───────────────────────────────────────────────────
function openEditModal(id) {{
  editingId=id; editingManual=currentManual;
  const s=getSecs(currentManual)[id];
  document.getElementById('edit-title').value=s.title;
  document.getElementById('edit-content').value=(s.content||[]).join('\\n\\n');
  document.getElementById('edit-modal').classList.add('open');
}}
window.openEditModal=openEditModal;
function closeEditModal(){{document.getElementById('edit-modal').classList.remove('open');}}
window.closeEditModal=closeEditModal;
function saveSection(){{
  const title=document.getElementById('edit-title').value.trim();
  const content=document.getElementById('edit-content').value.trim().split('\\n\\n').map(p=>p.trim()).filter(p=>p);
  const secs=getSecs(editingManual);
  secs[editingId]={{...secs[editingId],title,content}};
  const key='manual_edits_'+editingManual;
  localStorage.setItem(key,JSON.stringify(secs.map((s,i)=>{{return {{id:i,title:s.title,content:s.content}};}})));
  closeEditModal(); renderToc(currentManual); openSection(editingId);
}}
window.saveSection=saveSection;
document.getElementById('edit-modal').addEventListener('click',e=>{{if(e.target===document.getElementById('edit-modal'))closeEditModal();}});

// ── MODELO ────────────────────────────────────────────────────
function updatePill(state,label) {{
  const dot=document.getElementById('pill-dot');
  const lbl=document.getElementById('pill-label');
  if(!dot||!lbl)return;
  dot.className='dot '+(state==='ready'?'ready':state==='loading'?'loading':'');
  lbl.textContent=label||(state==='ready'?'IA lista':state==='loading'?'Cargando…':'Sin modelo');
}}
function openModelOverlay(){{document.getElementById('model-overlay').classList.add('open');}}
window.openModelOverlay=openModelOverlay;

async function loadModel(){{
  if(modelLoading)return;
  const sel=document.getElementById('overlay-model-select').value;
  selectedModel=sel; localStorage.setItem('selected_model',sel);
  modelLoading=true;
  document.getElementById('load-btn').disabled=true;
  document.getElementById('status-dot').className='dot loading';
  document.getElementById('status-text').textContent='Iniciando…';
  updatePill('loading');
  try{{
    const webllm=window._webllm;
    if(!webllm)throw new Error('WebLLM no cargado. Espera un momento y reintenta.');
    engine=await webllm.CreateMLCEngine(sel,{{
      initProgressCallback:(p)=>{{
        const pct=Math.round((p.progress||0)*100);
        document.getElementById('prog-bar').style.width=pct+'%';
        document.getElementById('prog-label').textContent=p.text||`Descargando… ${{pct}}%`;
        document.getElementById('status-text').textContent=p.text||`${{pct}}%`;
      }}
    }});
    document.getElementById('status-dot').className='dot ready';
    document.getElementById('status-text').textContent='✓ Modelo listo';
    document.getElementById('prog-bar').style.width='100%';
    document.getElementById('prog-label').textContent='✓ Listo para usar';
    updatePill('ready',sel.split('-q4')[0].replace('Qwen2.5-','Qwen ').replace('Phi-3.5-mini-instruct','Phi-3.5'));
    setTimeout(()=>document.getElementById('model-overlay').classList.remove('open'),1200);
  }}catch(err){{
    document.getElementById('status-dot').className='dot';
    document.getElementById('status-text').textContent='❌ '+err.message;
    updatePill('idle'); engine=null;
  }}
  modelLoading=false;
  document.getElementById('load-btn').disabled=false;
}}
window.loadModel=loadModel;

function saveSettings(){{
  selectedModel=document.getElementById('model-setting').value;
  localStorage.setItem('selected_model',selectedModel);
  document.getElementById('overlay-model-select').value=selectedModel;
  engine=null; updatePill('idle');
  const ok=document.getElementById('save-ok');
  ok.style.display='inline'; setTimeout(()=>ok.style.display='none',2000);
  openModelOverlay();
}}
window.saveSettings=saveSettings;

// ── UTILS ─────────────────────────────────────────────────────
function esc(s){{return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}}
function fmtMd(t){{
  return t.replace(/\\*\\*(.*?)\\*\\*/g,'<strong>$1</strong>')
          .replace(/\\*(.*?)\\*/g,'<em>$1</em>')
          .replace(/^#{{1,3}} (.*)$/gm,'<strong>$1</strong>')
          .replace(/^[-•] (.*)$/gm,'• $1')
          .replace(/\\n\\n/g,'</p><p>')
          .replace(/\\n/g,'<br>')
          .replace(/^(.*)$/,'<p>$1</p>');
}}
</script>
</body>
</html>"""

output = 'index.html'
with open(output, 'w', encoding='utf-8') as f:
    f.write(HTML)

size_kb = os.path.getsize(output) / 1024
print(f"Generado: {output} ({size_kb:.1f} KB)")
print(f"  Admin:         {len(admin_sections)} secciones")
print(f"  Calidad:       {len(calidad_sections)} secciones")
print(f"  Inconsistencias: {len(inconsistencias)} ({len(altas)} altas, {len(medias)} medias, {len(bajas)} bajas)")
