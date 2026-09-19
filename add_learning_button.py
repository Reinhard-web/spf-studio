from pathlib import Path

path = Path("app/web/innovation.html")
html = path.read_text(encoding="utf-8")

if 'onclick="showCreateLearningForm()"' in html:
    print("Create Learning button already exists.")
    raise SystemExit

marker = '<!-- CREATE LEARNING -->'

button = '''
<div class="problem-create-bar">
    <button
        type="button"
        class="problem-create-button"
        onclick="showCreateLearningForm()"
    >
        + Create Learning
    </button>
</div>

'''

if marker not in html:
    raise SystemExit("CREATE LEARNING marker not found.")

html = html.replace(marker, button + marker, 1)

path.write_text(html, encoding="utf-8")

print("Create Learning button inserted successfully.")