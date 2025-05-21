import os
import re

# Logo local/remoto
def get_logo_url():
    logo_local = 'logo_telko.png'
    return logo_local if os.path.exists(logo_local) else 'https://www.telkouy.com/wp-content/uploads/2021/09/logo_telko.png'

empresa_info = '''
TELKO USA<br>
P.O Box 986 Farmingdale, NY 11735<br>
P: (631) 741-0501<br>
tcabal@telkousa.com<br>
'''

# SVG iconos
svg_gafas = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1a237e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="7" cy="17" r="3"/><circle cx="17" cy="17" r="3"/><path d="M7 17h10"/><path d="M3 17v-2a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4v2"/></svg>'
svg_regla = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1976d2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="6" rx="2"/><path d="M6 7v6"/><path d="M10 7v6"/><path d="M14 7v6"/><path d="M18 7v6"/></svg>'
svg_material = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#43a047" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/></svg>'

# Encuentra todas las carpetas de primer nivel que sean marcas
marcas = [d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.')]
marcas = sorted(marcas)

# Estructura: {marca: [ {modelo, imagenes: [img_path]} ] }
cat_data = {}
for marca in marcas:
    modelos = []
    for modelo_folder in sorted(os.listdir(marca)):
        modelo_path = os.path.join(marca, modelo_folder)
        if os.path.isdir(modelo_path):
            modelo_nombre = modelo_folder
            imagenes = []
            for archivo in sorted(os.listdir(modelo_path)):
                if archivo.lower().endswith('.jpg') and 'img_02' in archivo.lower():
                    imagenes.append(os.path.join(modelo_path, archivo))
            if imagenes:
                modelos.append({
                    'modelo': modelo_nombre,
                    'imagenes': imagenes
                })
    if modelos:
        cat_data[marca] = modelos

logo_url = get_logo_url()

html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Catálogo General de Marcas</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Montserrat:wght@600;900&display=swap" rel="stylesheet">
    <style>
        @page {{ size: A4; margin: 2.2cm 1.5cm 2.2cm 1.5cm; }}
        body {{ font-family: 'Inter', Arial, sans-serif; margin: 0; background: #fff; color: #1a237e; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #1a237e; padding: 0 0 18px 0; margin-bottom: 32px; }}
        .logo {{ height: 80px; }}
        .empresa-info {{ font-size: 1.1em; color: #1a237e; text-align: right; line-height: 1.5; font-family: 'Montserrat', Arial, sans-serif; }}
        .portada {{ text-align: center; margin-bottom: 40px; }}
        .titulo-principal {{ font-size: 2.8em; font-weight: 900; color: #1a237e; letter-spacing: -2px; font-family: 'Montserrat', Arial, sans-serif; margin-bottom: 10px; }}
        .subtitulo {{ font-size: 1.3em; color: #1976d2; margin-bottom: 18px; font-family: 'Montserrat', Arial, sans-serif; }}
        .indice-section {{ margin: 0 auto 40px auto; max-width: 700px; }}
        .indice-title {{ font-size: 1.5em; color: #1976d2; font-weight: 700; margin-bottom: 10px; border-left: 6px solid #1a237e; padding-left: 12px; }}
        .indice-list {{ list-style: none; padding: 0; margin: 0; columns: 2; column-gap: 40px; }}
        .indice-list li {{ margin-bottom: 8px; font-size: 1.1em; }}
        .indice-list a {{ color: #1a237e; text-decoration: underline; font-weight: 600; }}
        .indice-list a:hover {{ color: #1976d2; }}
        .marca-section {{ page-break-before: always; margin: 0 auto 0 auto; max-width: 1000px; }}
        .marca-titulo {{ font-size: 2em; color: #1976d2; font-weight: 900; margin-bottom: 18px; border-left: 8px solid #1a237e; padding-left: 16px; letter-spacing: -1px; font-family: 'Montserrat', Arial, sans-serif; background: #f4f6fa; border-radius: 6px; }}
        .catalogo {{ display: flex; flex-wrap: wrap; justify-content: flex-start; gap: 24px; }}
        .card {{ background: #fff; border-radius: 12px; box-shadow: 0 2px 8px #1a237e10; width: 320px; margin-bottom: 24px; padding: 18px 12px 12px 12px; display: flex; flex-direction: column; align-items: center; border: 1.5px solid #e3e6ee; position: relative; min-height: 420px; }}
        .card-header {{ width: 100%; display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }}
        .modelo-nombre {{ font-size: 1.13em; font-weight: 700; color: #1a237e; display: flex; align-items: center; gap: 7px; font-family: 'Montserrat', Arial, sans-serif; }}
        .medidas {{ color: #1976d2; font-weight: 700; font-size: 1em; display: flex; align-items: center; gap: 4px; }}
        .imagenes {{ width: 100%; margin: 10px 0 10px 0; display: flex; justify-content: center; }}
        .imagenes img {{ width: 100%; max-width: 260px; max-height: 180px; object-fit: contain; border-radius: 10px; border: 2px solid #e3e6ee; background: #fff; box-shadow: 0 2px 8px #1a237e10; }}
        .material {{ color: #1976d2; font-size: 1em; font-weight: 600; display: flex; align-items: center; gap: 7px; margin-top: 10px; background: #e3f6ee; border-radius: 6px; padding: 4px 12px; font-family: 'Montserrat', Arial, sans-serif; }}
        .notas {{ margin-top: 18px; width: 90%; min-height: 32px; border-top: 1px dashed #b0b4c1; color: #b0b4c1; font-size: 0.95em; font-style: italic; text-align: left; padding-top: 4px; }}
        @media print {{
            body {{ background: #fff !important; color: #1a237e; }}
            .header {{ border-bottom: 3px solid #1a237e; box-shadow: none; }}
            .portada, .indice-section {{ page-break-after: always; }}
            .marca-section {{ page-break-before: always; }}
            .cta-bar, .cta-btn {{ display: none !important; }}
            a {{ color: #1a237e !important; text-decoration: underline; }}
        }}
        @media (max-width: 900px) {{ .catalogo {{ gap: 12px; }} .card {{ width: 98vw; max-width: 99vw; }} }}
        @media (max-width: 600px) {{ .header {{ flex-direction: column; align-items: flex-start; padding: 10px 0 10px 0; }} .titulo-principal {{ font-size: 1.5em; }} .marca-section {{ padding: 0; }} .card {{ width: 98vw; max-width: 99vw; padding: 8px 2px 8px 2px; }} .imagenes img {{ max-width: 98vw; max-height: 120px; }} }}
        footer {{ text-align:center;color:#b0b4c1;font-size:1em;margin:40px 0 18px 0; font-family: 'Inter', Arial, sans-serif; }}
    </style>
</head>
<body>
    <div class="portada">
        <div class="header" role="banner">
            <img src="{logo_url}" class="logo" alt="Logo Telko" loading="lazy">
            <div class="empresa-info">{empresa_info}</div>
        </div>
        <div class="titulo-principal">Catálogo General de Marcas</div>
        <div class="subtitulo">Armazones de Receta y Sol &mdash; Exportación y Distribución</div>
    </div>
    <div class="indice-section">
        <div class="indice-title">Índice de Marcas</div>
        <ul class="indice-list">
'''
for marca in cat_data.keys():
    html += f'            <li><a href="#{marca.replace(" ", "_")}">{marca}</a></li>\n'
html += '''        </ul>
    </div>
'''
for marca, modelos in cat_data.items():
    html += f'<section class="marca-section" id="{marca.replace(" ", "_")}">\n'
    html += f'  <div class="marca-titulo">{marca}</div>\n'
    html += '  <div class="catalogo">\n'
    for item in modelos:
        medidas = ''
        match = re.search(r'(\d{2,3}-\d{2,3}-\d{2,3})', item['modelo'])
        if match:
            medidas = match.group(1)
        else:
            medidas = ''
        material = 'Acetate'
        html += f'''    <div class="card">
            <div class="card-header">
                <span class="modelo-nombre">{svg_gafas} {item['modelo']}</span>
                <span class="medidas">{svg_regla} {medidas}</span>
            </div>
            <div class="imagenes">
'''
        for img_path in item['imagenes']:
            rel_path = os.path.relpath(img_path)
            html += f'                <img src="{rel_path}" alt="{item["modelo"]} - vista principal" loading="lazy">\n'
        html += f'''            </div>
            <div class="material">{svg_material} {material}</div>
            <div class="notas">Notas / Precio:</div>
        </div>
'''
    html += '  </div>\n</section>\n'
html += '''    <footer>Catálogo generado por Telko USA &copy; 2024. Todos los derechos reservados.</footer>
</body>
</html>'''

# Guardar el HTML
output_file = 'catalogo_todas_las_marcas.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'Catálogo HTML general generado: {output_file}\n¡Listo para exportar a PDF A4 desde tu navegador!') 