import os
import pandas as pd
from jinja2 import Template
import shutil

# Configure your tools
TOOLS = {
    'image-compressor': {
        'csv': 'data/image-compressor-keywords.csv',
        'output_folder': 'image-compressor',
        'tool_type': 'image',
        'script': 'assets/js/image-tool.js'
    },
    'pdf-merger': {
        'csv': 'data/pdf-merger-keywords.csv',
        'output_folder': 'pdf-merger',
        'tool_type': 'pdf',
        'script': 'assets/js/pdf-tool.js'
    },
    'unit-converter': {
        'csv': 'data/unit-converter-keywords.csv',
        'output_folder': 'unit-converter',
        'tool_type': 'converter',
        'script': 'assets/js/converter-tool.js'
    }
}

# Load template
with open('templates/tool-template.html', 'r') as f:
    template = Template(f.read())

# Load all scripts
scripts = {}
for tool_name, config in TOOLS.items():
    try:
        with open(config['script'], 'r') as f:
            scripts[tool_name] = f.read()
    except:
        print(f"⚠️ Missing script for {tool_name}")
        scripts[tool_name] = ''

all_pages = {}
os.makedirs('generated_pages', exist_ok=True)

for tool_name, config in TOOLS.items():
    print(f"🔧 Generating {tool_name}...")
    
    try:
        df = pd.read_csv(config['csv'])
        keywords = df.to_dict('records')
        print(f"   📄 {len(keywords)} keywords found")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        continue
    
    output_folder = f'generated_pages/{config["output_folder"]}'
    os.makedirs(output_folder, exist_ok=True)
    
    pages_for_tool = []
    for kw in keywords:
        # Clean data
        for key, val in kw.items():
            if pd.isna(val):
                kw[key] = ''
            else:
                kw[key] = str(val)
        
        # Add tool_type
        kw['tool_type'] = config['tool_type']
        
        # Render
        html = template.render(**kw)
        
        # Inject tool script
        tool_script = scripts.get(tool_name, '')
        html = html.replace('<!-- TOOL SPECIFIC CONTENT', f'<script>{tool_script}</script>')
        
        # Save
        slug = kw.get('slug', f'page-{keywords.index(kw)}')
        page_folder = f'{output_folder}/{slug}'
        os.makedirs(page_folder, exist_ok=True)
        
        with open(f'{page_folder}/index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"   ✅ {slug}")
        pages_for_tool.append({'slug': slug, 'title': kw.get('h1_title', slug)})
    
    all_pages[tool_name] = pages_for_tool
    print(f"   ✅ {tool_name}: {len(pages_for_tool)} pages generated")

# Generate Homepage
print("🏠 Generating homepage...")
homepage = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Free Online Tools - Image Compressor, PDF Merger, Unit Converter</title>
    <meta name="description" content="Free online tools including image compressor, PDF merger, unit converter, and more. All tools are free to use, no registration required.">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: #f8f9fa; }
        .hero {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 0;
            border-radius: 10px;
            margin: 20px 0;
        }
        .tool-card {
            background: white;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.2s;
            height: 100%;
        }
        .tool-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }
        .tool-card ul {
            list-style: none;
            padding: 0;
        }
        .tool-card ul li {
            padding: 5px 0;
            border-bottom: 1px solid #f0f0f0;
        }
        .tool-card ul li:last-child { border-bottom: none; }
        .tool-card ul li a { color: #667eea; text-decoration: none; }
        .tool-card ul li a:hover { text-decoration: underline; }
        .badge-count {
            background: #667eea;
            color: white;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="hero text-center">
            <h1>🚀 Free Online Tools</h1>
            <p class="lead">Professional tools for image compression, PDF merging, unit conversion & more</p>
            <p class="small">Free - No registration - Works in your browser</p>
        </div>
        <div class="row">
"""
total_pages = 0
for tool_name, pages in all_pages.items():
    display_name = tool_name.replace('-', ' ').title()
    total_pages += len(pages)
    homepage += f"""
            <div class="col-md-6 col-lg-4">
                <div class="tool-card">
                    <h3>{display_name}</h3>
                    <span class="badge-count">{len(pages)} Pages</span>
                    <ul>
    """
    for page in pages[:10]:
        homepage += f'<li><a href="/{tool_name}/{page["slug"]}/">{page["title"]}</a></li>'
    if len(pages) > 10:
        homepage += f'<li><small class="text-muted">+ {len(pages)-10} more</small></li>'
    homepage += """
                    </ul>
                </div>
            </div>
    """

homepage += f"""
        </div>
        <div class="row mt-5">
            <div class="col-12">
                <div class="card">
                    <div class="card-body">
                        <h3>About This Tool Engine</h3>
                        <p>This is a collection of free, professional online tools that work entirely in your browser. 
                        All tools are designed to be fast, secure, and easy to use. No data is uploaded to our servers - 
                        everything stays on your device.</p>
                        <p><strong>Total Tools:</strong> {len(TOOLS)} | <strong>Total Pages:</strong> {total_pages}</p>
                        <p class="text-muted"><small>More tools being added regularly. Bookmark this page!</small></p>
                    </div>
                </div>
            </div>
        </div>
        <footer class="text-center text-muted py-4">
            <p>&copy; 2024 Tool Engine - Free Online Tools</p>
        </footer>
    </div>
</body>
</html>
"""

with open('generated_pages/index.html', 'w', encoding='utf-8') as f:
    f.write(homepage)

# Generate Sitemap
print("🗺️ Generating sitemap...")
sitemap = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://YOUR-USERNAME.github.io/multi-tool-engine/</loc>
        <priority>1.0</priority>
    </url>
"""
for tool_name, pages in all_pages.items():
    for page in pages:
        sitemap += f"""    <url>
        <loc>https://YOUR-USERNAME.github.io/multi-tool-engine/{tool_name}/{page['slug']}/</loc>
        <priority>0.8</priority>
    </url>
"""
sitemap += """</urlset>"""

with open('generated_pages/sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap)

print(f"🎉 COMPLETE! {len(TOOLS)} tools, {total_pages} pages generated")
