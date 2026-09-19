from pathlib import Path

path = Path("app/web/innovation.html")
html = path.read_text(encoding="utf-8")

old = '''        const response = await fetch("/innovation/evidence", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });
'''

new = '''        const token = localStorage.getItem("spf_access_token");

        if (!token) {
            throw new Error("Authentication token not found.");
        }

        const response = await fetch(
            "/innovation/evidence",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                    "X-Organization-ID": "7"
                },

                body: JSON.stringify(payload)
            }
        );
'''

if old not in html:
    raise SystemExit("Evidence POST request block not found.")

html = html.replace(old, new, 1)

path.write_text(html, encoding="utf-8")

print("Evidence POST authentication fixed successfully.")