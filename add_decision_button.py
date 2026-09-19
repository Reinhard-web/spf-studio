from pathlib import Path

path = Path("app/web/innovation.html")
html = path.read_text(encoding="utf-8")

if 'onclick="showCreateDecisionForm()"' in html:
    print("Create Decision button already exists.")
    raise SystemExit

marker = "<!-- CREATE DECISION -->"

button = r'''
<div class="problem-create-bar">
    <button
        type="button"
        class="problem-create-button"
        onclick="showCreateDecisionForm()"
    >
        + Create Decision
    </button>
</div>

'''

if marker not in html:
    raise SystemExit(f"Marker not found: {marker}")

html = html.replace(marker, button + marker, 1)

path.write_text(html, encoding="utf-8")

print("Create Decision button inserted successfully.")