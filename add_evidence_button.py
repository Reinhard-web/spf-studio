from pathlib import Path

path = Path("app/web/innovation.html")
html = path.read_text(encoding="utf-8")

if 'onclick="showCreateEvidenceForm()"' in html:
    print("Create Evidence button already exists.")
    raise SystemExit

marker = "<!-- CREATE EVIDENCE -->"

button = r'''
<div class="problem-create-bar">
    <button
        type="button"
        class="problem-create-button"
        onclick="showCreateEvidenceForm()"
    >
        + Create Evidence
    </button>
</div>

'''

if marker not in html:
    raise SystemExit(f"Marker not found: {marker}")

html = html.replace(marker, button + marker, 1)

path.write_text(html, encoding="utf-8")

print("Create Evidence button inserted successfully.")