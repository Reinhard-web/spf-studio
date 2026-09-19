from pathlib import Path

path = Path("app/web/innovation.html")
html = path.read_text(encoding="utf-8")

if "function createEvidence()" in html:
    print("Evidence JavaScript already exists.")
    raise SystemExit

js = r'''
<script>
async function showCreateEvidenceForm() {
    const form = document.getElementById("createEvidenceForm");

    if (!form) {
        console.error("Create Evidence form not found.");
        return;
    }

    form.style.display = "flex";

    await populateEvidenceExperiments();
}

function hideCreateEvidenceForm() {
    const form = document.getElementById("createEvidenceForm");

    if (form) {
        form.style.display = "none";
    }
}

async function populateEvidenceExperiments() {
    const select = document.getElementById("evidenceExperiment");

    if (!select) {
        return;
    }

    select.innerHTML = '<option value="">Select experiment</option>';

    try {
        const response = await fetch("/innovation/experiments");

        if (!response.ok) {
            throw new Error("Unable to load experiments.");
        }

        const experiments = await response.json();

        experiments.forEach(experiment => {
            const option = document.createElement("option");
            option.value = experiment.id;
            option.textContent = experiment.title;
            select.appendChild(option);
        });

    } catch (error) {
        console.error("Error loading experiments:", error);
    }
}

async function createEvidence(event) {
    event.preventDefault();

    const message = document.getElementById("evidenceFormMessage");

    const experimentValue =
        document.getElementById("evidenceExperiment").value;

    const title =
        document.getElementById("evidenceTitle").value.trim();

    const description =
        document.getElementById("evidenceDescription").value.trim();

    const evidenceType =
        document.getElementById("evidenceType").value;

    const sourceType =
        document.getElementById("evidenceSourceType").value;

    const sourceReference =
        document.getElementById("evidenceSourceReference").value.trim();

    const observedAt =
        document.getElementById("evidenceObservedAt").value;

    const status =
        document.getElementById("evidenceStatus").value;

    const payload = {
        title: title,
        description: description,
        evidence_type: evidenceType,
        source_type: sourceType || null,
        source_reference: sourceReference || null,
        status: status,
        observed_at: observedAt
            ? new Date(observedAt).toISOString()
            : null
    };

    if (experimentValue) {
        payload.experiment_id = Number(experimentValue);
    }

    message.textContent = "Creating evidence...";

    try {
        const response = await fetch("/innovation/evidence", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Unable to create evidence."
            );
        }

        message.textContent = "Evidence created successfully.";

        document.getElementById("evidenceForm").reset();

        setTimeout(() => {
            hideCreateEvidenceForm();
        }, 1000);

        if (typeof loadDashboard === "function") {
            await loadDashboard();
        }

    } catch (error) {
        console.error("Error creating evidence:", error);

        message.textContent =
            error.message || "Unable to create evidence.";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("evidenceForm");

    if (form) {
        form.addEventListener("submit", createEvidence);
    }
});
</script>
'''

marker = "</body>"

if marker not in html:
    raise SystemExit("Could not find </body> marker.")

html = html.replace(marker, js + "\n" + marker, 1)

path.write_text(html, encoding="utf-8")

print("Evidence JavaScript inserted successfully.")