from pathlib import Path

path = Path("app/web/innovation.html")
html = path.read_text(encoding="utf-8")

old = '''        const response = await fetch("/innovation/experiments");

        if (!response.ok) {
            throw new Error("Unable to load experiments.");
        }
'''

new = '''        const token = localStorage.getItem("token");

        if (!token) {
            throw new Error("Authentication token not found.");
        }

        const response = await fetch(
            "/innovation/experiments",
            {
                method: "GET",

                headers: {
                    "Authorization": `Bearer ${token}`,
                    "X-Organization-ID": "7"
                }
            }
        );

        if (!response.ok) {
            throw new Error("Unable to load experiments.");
        }
'''

if old not in html:
    raise SystemExit("Evidence experiment fetch code not found.")

html = html.replace(old, new, 1)

path.write_text(html, encoding="utf-8")

print("Evidence experiment authentication fixed successfully.")