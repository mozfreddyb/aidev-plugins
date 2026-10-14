#!/usr/bin/env python3
"""Build a portable theme/layout gallery and component sampler.

Usage: python3 -I build_demo.py --output /tmp/mozilla-demo
"""
import argparse
import importlib.util
import sys
import json
import pathlib

sys.dont_write_bytecode = True
ROOT = pathlib.Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output", type=pathlib.Path, default=pathlib.Path("mozilla-demo"))
args = parser.parse_args()
spec = importlib.util.spec_from_file_location("markdown_renderer", ROOT / "scripts/render_markdown.py")
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)
OUT = args.output.resolve()
OUT.mkdir(parents=True, exist_ok=True)
pages = {}
themes = ["acorn", "firefox", "mozilla"]
layouts = ["reading", "wide", "sidebar"]
for theme in themes:
    for layout in layouts:
        key = f"{theme}-{layout}"
        output = renderer.render(ROOT / "examples/report.md", OUT / f"{key}.html", theme=theme, layout=layout)
        pages[key] = output.read_text()

sampler = '''
<header class="moz-page-header"><div class="heading"><h1>Component sampler</h1><span class="moz-badge">Example data</span></div>
<p class="description">Explore the components included in this PR. Values here are illustrative.</p></header>
<section class="moz-section" aria-labelledby="messages"><h2 id="messages">Message bars</h2>
<div class="moz-message-bar"><span class="icon-container"><svg class="moz-icon" data-icon="information-fill"></svg></span><div class="content"><div class="text"><strong class="heading">Measurement context</strong><span class="message">A message bar can keep context close to the results it explains.</span></div></div></div>
<div class="moz-message-bar warning"><span class="icon-container"><svg class="moz-icon" data-icon="warning-fill"></svg></span><div class="content"><div class="text"><strong class="heading">Partial data</strong><span class="message">This example shows a caveat alongside an icon and words.</span></div></div></div></section>
<section class="moz-section" aria-labelledby="cards"><h2 id="cards">Cards and numbers</h2><div class="moz-grid">
<article class="moz-card moz-stat"><span class="label">Example latency</span><span class="value">64<span class="unit"> ms</span></span><span class="delta neutral"><svg class="moz-icon" data-icon="arrow-trending"></svg>Stable in this example</span></article>
<article class="moz-card"><h3 class="moz-card-heading">Finding card</h3><div class="moz-card-content"><p>Cards group related content. They can carry findings, methodology, or a small chart.</p><span class="moz-badge">Illustration</span></div></article></div>
<details class="moz-card accordion" open><summary>Read the example methodology</summary><div class="moz-card-content"><p>This is a native HTML disclosure. It works with JavaScript disabled.</p></div></details></section>
<section class="moz-section" aria-labelledby="tables"><h2 id="tables">Table styles</h2>
<div class="moz-table-wrapper"><table class="moz-table striped"><caption>Accent header</caption><thead><tr><th scope="col">Example path</th><th scope="col" class="num">Latency</th><th scope="col">Status</th></tr></thead><tbody><tr><td>Path A</td><td class="num">64 ms</td><td>Complete</td></tr><tr><td>Path B</td><td class="num">77 ms</td><td>Complete</td></tr></tbody></table></div>
<div class="moz-table-wrapper"><table class="moz-table plain compact"><caption>Plain, compact header</caption><thead><tr><th scope="col">Example path</th><th scope="col" class="num">Latency</th></tr></thead><tbody><tr><td>Path A</td><td class="num">64 ms</td></tr><tr><td>Path B</td><td class="num">77 ms</td></tr></tbody></table></div></section>
<section class="moz-section" aria-labelledby="controls"><h2 id="controls">Controls</h2><div class="moz-grid">
<div class="moz-input"><label for="example-name">Campaign name</label><input id="example-name" value="Example campaign"><p class="description">A labeled text field.</p></div>
<div class="moz-input"><label for="example-browser">Browser</label><div class="moz-select"><select id="example-browser"><option>Firefox</option><option>Chrome</option></select></div></div></div>
<div class="moz-field"><label class="moz-toggle"><input type="checkbox" role="switch" checked><span class="track"></span><span class="text">Include example stalls</span></label></div>
<div class="moz-segmented-control" role="radiogroup" aria-label="Example view"><label><input type="radio" name="view" checked>Summary</label><label><input type="radio" name="view">Details</label></div>
<p class="text-deemphasized">These controls demonstrate appearance and native behavior; they do not filter data.</p></section>
<section class="moz-section" aria-labelledby="actions"><h2 id="actions">Buttons and dialogs</h2>
<div class="moz-row"><button class="moz-button primary" type="button" onclick="document.getElementById('example-dialog').showModal()">Open example dialog</button><button class="moz-button" type="button" onclick="window.print()"><svg class="moz-icon" data-icon="print"></svg>Print sampler</button><button class="moz-button" type="button" disabled>Export unavailable</button></div>
<dialog class="moz-dialog" id="example-dialog" aria-labelledby="dialog-heading"><h2 id="dialog-heading">Example dialog</h2><p>This uses the browser’s native dialog behavior and Acorn styles.</p><form method="dialog" class="moz-button-group"><button class="moz-button" value="close">Close dialog</button></form></dialog></section>
'''
for theme in themes:
    attr = f' data-brand="{theme}"' if theme != "acorn" else ""
    fonts = renderer.FONT_LINK if theme != "acorn" else ""
    masthead = f'<header class="moz-masthead"><svg data-logo="{theme}-lockup" aria-label="{theme.capitalize()}"></svg></header>' if theme != "acorn" else ""
    source = OUT / f"{theme}-components.src.html"
    source.write_text(f'''<!DOCTYPE html><html lang="en"{attr}><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Component sampler</title>
<link rel="stylesheet" href="{ROOT}/assets/tokens.css"><link rel="stylesheet" href="{ROOT}/assets/components.css">{fonts}
<style>.moz-message-bar,.moz-card.accordion,.moz-field,.moz-segmented-control{{margin-block:var(--space-large)}}.moz-row{{margin-block:var(--space-large)}}</style></head><body>{masthead}<main class="moz-main wide">{sampler}</main></body></html>''')
    output = OUT / f"{theme}-components.html"
    renderer.bundle(source, output)
    pages[f"{theme}-components"] = output.read_text()

gallery = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Mozilla Markdown demo</title>
<link rel="stylesheet" href="$tokens$"><link rel="stylesheet" href="$components$">
<style>
.demo-main { max-width:none; padding:var(--space-xxlarge); }
.demo-controls { display:flex; flex-wrap:wrap; gap:var(--space-large); align-items:end; margin-block:var(--space-large); }
.demo-controls .moz-input { flex:1; min-width:10rem; }
.demo-panes { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:var(--space-large); }
.demo-pane { min-width:0; }
.demo-pane h2 { font-size:var(--font-size-large); }
.preview { border:var(--border-width) solid var(--border-color); border-radius:var(--border-radius-medium); background:var(--background-color-box); overflow:auto; }
iframe { display:block; width:100%; height:72vh; border:0; background:var(--background-color-canvas); }
.phone iframe { width:500px; max-width:100%; margin-inline:auto; }
.single .demo-panes { grid-template-columns:1fr; }
.single .demo-pane:last-child { display:none; }
.demo-intro { max-width:80ch; }
@media(max-width:900px) { .demo-panes { grid-template-columns:1fr; } .demo-main { padding:var(--space-large); } }
</style></head><body><main class="moz-main demo-main">
<header class="moz-page-header"><div class="heading"><h1>Mozilla Markdown demo</h1><span class="moz-badge">Markdown</span></div><p class="description demo-intro">Compare the same Markdown report in three themes and three layouts, or explore the components supplied by the skill.</p>
<p class="meta">Brand fonts load from Google Fonts; everything else is embedded.</p></header>
<div class="demo-controls">
<div class="moz-input"><label for="content">Content</label><div class="moz-select"><select id="content"><option value="report">Sample document</option><option value="components">Component sampler</option></select></div></div>
<div class="moz-input"><label for="scheme">Color scheme</label><div class="moz-select"><select id="scheme"><option value="light">Light</option><option value="dark">Dark</option><option value="auto">System</option></select></div></div>
<div class="moz-input"><label for="width">Preview width</label><div class="moz-select"><select id="width"><option value="fill">Fill panel</option><option value="phone">Narrow (500 px)</option></select></div></div>
<div class="moz-input"><label for="compare">Comparison</label><div class="moz-select"><select id="compare"><option value="both">Side by side</option><option value="single">One full-width preview</option></select></div></div>
</div>
<div class="demo-panes">
$panes$
</div>
<p class="text-deemphasized">Each preview is a complete HTML document. Choose “Download preview” to save the selected theme and color scheme as a portable file.</p>
<noscript><p>Interactive previews require JavaScript. Open a generated variant such as <a href="acorn-sidebar.html">Acorn with sidebar</a> or <a href="mozilla-reading.html">Mozilla reading layout</a>.</p></noscript>
</main><script>
const pages = $pages$;
const byId = id => document.getElementById(id);
function selected(side) {
 const theme = byId(side+'-theme').value;
 const content = byId('content').value;
 const layout = content === 'components' ? 'components' : byId(side+'-layout').value;
 const scheme = byId('scheme').value;
 let source = pages[theme+'-'+layout];
 if (scheme !== 'auto') source = source.replace('<html lang="en"','<html data-color-scheme="'+scheme+'" lang="en"');
 return {source, name:theme+'-'+layout+'-'+scheme+'.html'};
}
function update() {
 const scheme = byId('scheme').value;
 if (scheme === 'auto') delete document.documentElement.dataset.colorScheme;
 else document.documentElement.dataset.colorScheme = scheme;
 document.body.classList.toggle('phone',byId('width').value === 'phone');
 document.body.classList.toggle('single',byId('compare').value === 'single');
 for (const side of ['left','right']) {
   byId(side+'-layout').disabled = byId('content').value === 'components';
   byId(side+'-frame').srcdoc = selected(side).source;
 }
}
document.querySelectorAll('select').forEach(select=>select.addEventListener('change',update));
for (const side of ['left','right']) byId(side+'-download').addEventListener('click',()=>{
 const {source,name} = selected(side);
 const url = URL.createObjectURL(new Blob([source],{type:'text/html'}));
 const link = document.createElement('a'); link.href=url; link.download=name; link.click();
 setTimeout(()=>URL.revokeObjectURL(url),1000);
});
update();
</script></body></html>'''
panes = []
for side, default in [("left", "acorn"), ("right", "mozilla")]:
    theme_options = "".join(f'<option value="{theme}"{" selected" if theme == default else ""}>{theme.capitalize()}</option>' for theme in themes)
    layout_options = "".join(f'<option value="{layout}">{layout.capitalize()}</option>' for layout in layouts)
    panes.append(f'''<section class="demo-pane" aria-labelledby="{side}-heading"><h2 id="{side}-heading">{"First" if side == "left" else "Second"} preview</h2><div class="demo-controls">
<div class="moz-input"><label for="{side}-theme">Theme</label><div class="moz-select"><select id="{side}-theme">{theme_options}</select></div></div>
<div class="moz-input"><label for="{side}-layout">Layout</label><div class="moz-select"><select id="{side}-layout">{layout_options}</select></div></div>
<button class="moz-button" type="button" id="{side}-download">Download preview</button></div>
<div class="preview"><iframe id="{side}-frame" title="{side.capitalize()} design preview" sandbox="allow-scripts allow-modals allow-downloads allow-forms"></iframe></div></section>''')
gallery = gallery.replace("$tokens$", str(ROOT / "assets/tokens.css")).replace("$components$", str(ROOT / "assets/components.css"))
gallery = gallery.replace("$panes$", "".join(panes)).replace("$pages$", json.dumps(pages).replace("</", "<\\/"))
src = OUT / "index.src.html"
src.write_text(gallery)
renderer.bundle(src, OUT / "index.html")
print(f"Open {OUT / 'index.html'}")
