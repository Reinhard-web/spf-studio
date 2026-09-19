from pathlib import Path

path = Path("app/web/innovation.html")
html = path.read_text(encoding="utf-8")

if "function createDecision(event)" in html:
    print("Decision JavaScript already exists.")
    raise SystemExit

js = r'''
<script>
async function showCreateDecisionForm() {
    const form = document.getElementById("createDecisionForm");

    if (!form) {
        console.error("Create Decision form not found.");
        return;
    }

    form.style.display = "flex";

    await Promise.all([
        populateDecisionProblems(),
        populateDecisionOpportunities(),
        populateDecisionIdeas(),
        populateDecisionExperiments(),
        populateDecisionLearnings(),
        populateDecisionEvidence()
    ]);
}

function hideCreateDecisionForm() {
    const form = document.getElementById("createDecisionForm");

    if (form) {
        form.style.display = "none";
    }
}

function getSPFHeaders() {
    const token = localStorage.getItem("spf_access_token");

    if (!token) {
        throw new Error("Authentication token not found.");
    }

    return {
        "Authorization": `Bearer ${token}`,
        "X-Organization-ID": "7"
    };
}

async function loadDecisionOptions(endpoint) {
    const response = await fetch(
        endpoint,
        {
            method: "GET",
            headers: getSPFHeaders()
        }
    );

    if (!response.ok) {
        const data = await response.json().catch(() => ({}));

        throw new Error(
            data.detail || `Unable to load ${endpoint}.`
        );
    }

    return await response.json();
}

async function populateDecisionProblems() {
    const select = document.getElementById("decisionProblem");

    if (!select) {
        return;
    }

    try {
        const items =
            await loadDecisionOptions("/innovation/problems");

        select.innerHTML =
            '<option value="">Select problem</option>';

        items.forEach(item => {
            const option =
                document.createElement("option");

            option.value = item.id;
            option.textContent = item.title;

            select.appendChild(option);
        });

    } catch (error) {
        console.error("Error loading problems:", error);
    }
}

async function populateDecisionOpportunities() {
    const select =
        document.getElementById("decisionOpportunity");

    if (!select) {
        return;
    }

    try {
        const items =
            await loadDecisionOptions("/innovation/opportunities");

        select.innerHTML =
            '<option value="">Select opportunity</option>';

        items.forEach(item => {
            const option =
                document.createElement("option");

            option.value = item.id;
            option.textContent = item.title;

            select.appendChild(option);
        });

    } catch (error) {
        console.error("Error loading opportunities:", error);
    }
}

async function populateDecisionIdeas() {
    const select =
        document.getElementById("decisionIdea");

    if (!select) {
        return;
    }

    try {
        const items =
            await loadDecisionOptions("/innovation/ideas");

        select.innerHTML =
            '<option value="">Select idea</option>';

        items.forEach(item => {
            const option =
                document.createElement("option");

            option.value = item.id;
            option.textContent = item.title;

            select.appendChild(option);
        });

    } catch (error) {
        console.error("Error loading ideas:", error);
    }
}

async function populateDecisionExperiments() {
    const select =
        document.getElementById("decisionExperiment");

    if (!select) {
        return;
    }

    try {
        const items =
            await loadDecisionOptions("/innovation/experiments");

        select.innerHTML =
            '<option value="">Select experiment</option>';

        items.forEach(item => {
            const option =
                document.createElement("option");

            option.value = item.id;
            option.textContent = item.title;

            select.appendChild(option);
        });

    } catch (error) {
        console.error("Error loading experiments:", error);
    }
}

async function populateDecisionLearnings() {
    const select =
        document.getElementById("decisionLearning");

    if (!select) {
        return;
    }

    try {
        const items =
            await loadDecisionOptions("/innovation/learnings");

        select.innerHTML =
            '<option value="">Select learning</option>';

        items.forEach(item => {
            const option =
                document.createElement("option");

            option.value = item.id;
            option.textContent = item.title;

            select.appendChild(option);
        });

    } catch (error) {
        console.error("Error loading learnings:", error);
    }
}

async function populateDecisionEvidence() {
    const select =
        document.getElementById("decisionEvidence");

    if (!select) {
        return;
    }

    try {
        const items =
            await loadDecisionOptions("/innovation/evidence");

        select.innerHTML =
            '<option value="">Select evidence</option>';

        items.forEach(item => {
            const option =
                document.createElement("option");

            option.value = item.id;
            option.textContent = item.title;

            select.appendChild(option);
        });

    } catch (error) {
        console.error("Error loading evidence:", error);
    }
}

async function createDecision(event) {
    event.preventDefault();

    const message =
        document.getElementById("decisionFormMessage");

    const payload = {
        problem_id:
            document.getElementById("decisionProblem").value
                ? Number(
                    document.getElementById("decisionProblem").value
                )
                : null,

        opportunity_id:
            document.getElementById("decisionOpportunity").value
                ? Number(
                    document.getElementById("decisionOpportunity").value
                )
                : null,

        idea_id:
            document.getElementById("decisionIdea").value
                ? Number(
                    document.getElementById("decisionIdea").value
                )
                : null,

        experiment_id:
            document.getElementById("decisionExperiment").value
                ? Number(
                    document.getElementById("decisionExperiment").value
                )
                : null,

        learning_id:
            document.getElementById("decisionLearning").value
                ? Number(
                    document.getElementById("decisionLearning").value
                )
                : null,

        evidence_id:
            document.getElementById("decisionEvidence").value
                ? Number(
                    document.getElementById("decisionEvidence").value
                )
                : null,

        title:
            document.getElementById("decisionTitle").value.trim(),

        decision:
            document.getElementById("decisionDecision").value.trim(),

        rationale:
            document.getElementById("decisionRationale").value.trim()
                || null,

        status:
            document.getElementById("decisionStatus").value,

        decided_by:
            document.getElementById("decisionDecidedBy").value.trim()
                || null
    };

    if (!payload.title || !payload.decision) {
        message.textContent =
            "Please complete the Decision title and Decision fields.";

        return;
    }

    message.textContent = "Creating decision...";

    try {
        const response = await fetch(
            "/innovation/decisions",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                    ...getSPFHeaders()
                },

                body: JSON.stringify(payload)
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Unable to create decision."
            );
        }

        message.textContent =
            "Decision created successfully.";

        document.getElementById("decisionForm").reset();

        setTimeout(() => {
            hideCreateDecisionForm();
        }, 1000);

        if (typeof loadDashboard === "function") {
            await loadDashboard();
        }

    } catch (error) {
        console.error("Error creating decision:", error);

        message.textContent =
            error.message || "Unable to create decision.";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const form =
        document.getElementById("decisionForm");

    if (form) {
        form.addEventListener(
            "submit",
            createDecision
        );
    }
});
</script>
'''

marker = "</body>"

if marker not in html:
    raise SystemExit("Could not find </body> marker.")

html = html.replace(marker, js + "\n" + marker, 1)

path.write_text(html, encoding="utf-8")

print("Decision JavaScript inserted successfully.")