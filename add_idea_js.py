from pathlib import Path

path = Path("app/web/innovation.html")

html = path.read_text(encoding="utf-8")

marker = "        function showCreateOpportunityForm() {"

idea_js = r'''
        function showCreateIdeaForm() {
            const form = document.getElementById("createIdeaForm");

            if (form) {
                form.style.display = "flex";
            }

            populateIdeaOpportunities();

            const title = document.getElementById("ideaTitle");

            if (title) {
                title.focus();
            }
        }

        function hideCreateIdeaForm() {
            const form = document.getElementById("createIdeaForm");

            if (form) {
                form.style.display = "none";
            }

            const ideaForm = document.getElementById("ideaForm");

            if (ideaForm) {
                ideaForm.reset();
            }

            const message = document.getElementById("ideaFormMessage");

            if (message) {
                message.textContent = "";
                message.className = "form-message";
            }
        }

        async function populateIdeaOpportunities() {
            const select = document.getElementById("ideaOpportunity");

            if (!select) {
                return;
            }

            try {
                const token = localStorage.getItem("spf_access_token");

                if (!token) {
                    return;
                }

                const response = await fetch("/innovation/opportunities", {
                    headers: {
                        "Authorization": `Bearer ${token}`,
                        "X-Organization-ID": "7"
                    }
                });

                if (!response.ok) {
                    throw new Error("Unable to load opportunities.");
                }

                const opportunities = await response.json();

                select.innerHTML = `
                    <option value="">
                        Select an opportunity (optional)
                    </option>
                `;

                opportunities.forEach((opportunity) => {
                    const option = document.createElement("option");

                    option.value = opportunity.id;
                    option.textContent = opportunity.title;

                    select.appendChild(option);
                });
            } catch (error) {
                console.error("Opportunity loading error:", error);
            }
        }

        async function createIdea() {
            const token = localStorage.getItem("spf_access_token");

            if (!token) {
                throw new Error("Please log in again.");
            }

            const opportunityValue =
                document.getElementById("ideaOpportunity").value;

            const payload = {
                opportunity_id: opportunityValue
                    ? Number(opportunityValue)
                    : null,

                title: document.getElementById("ideaTitle").value.trim(),

                description:
                    document.getElementById("ideaDescription").value.trim(),

                solution_concept:
                    document.getElementById("ideaSolutionConcept").value.trim() || null,

                target_users:
                    document.getElementById("ideaTargetUsers").value.trim() || null,

                value_proposition:
                    document.getElementById("ideaValueProposition").value.trim() || null,

                hypothesis:
                    document.getElementById("ideaHypothesis").value.trim() || null,

                expected_outcome:
                    document.getElementById("ideaExpectedOutcome").value.trim() || null,

                success_conditions:
                    document.getElementById("ideaSuccessConditions").value.trim() || null,

                status:
                    document.getElementById("ideaStatus").value
            };

            if (!payload.title || !payload.description) {
                throw new Error(
                    "Idea title and description are required."
                );
            }

            const response = await fetch("/innovation/ideas", {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                    "X-Organization-ID": "7"
                },

                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.detail || "Unable to create idea."
                );
            }

            return data;
        }

        const ideaForm = document.getElementById("ideaForm");

        if (ideaForm) {
            ideaForm.addEventListener(
                "submit",
                async function (event) {
                    event.preventDefault();

                    const message =
                        document.getElementById("ideaFormMessage");

                    try {
                        if (message) {
                            message.textContent = "Creating idea...";
                            message.className = "form-message";
                        }

                        const idea = await createIdea();

                        console.log(
                            "Idea created:",
                            idea
                        );

                        if (message) {
                            message.textContent =
                                "Idea created successfully.";

                            message.className =
                                "form-message success";
                        }

                        setTimeout(() => {
                            hideCreateIdeaForm();

                            if (typeof loadInnovationData === "function") {
                                loadInnovationData();
                            } else {
                                window.location.reload();
                            }
                        }, 700);

                    } catch (error) {
                        console.error(
                            "Create idea error:",
                            error
                        );

                        if (message) {
                            message.textContent =
                                error.message ||
                                "Unable to create idea.";

                            message.className =
                                "form-message error";
                        }
                    }
                }
            );
        }

'''

if marker not in html:
    raise SystemExit(
        "Opportunity JavaScript marker not found. No changes made."
    )

if "function showCreateIdeaForm()" in html:
    raise SystemExit(
        "Idea JavaScript already exists. No changes made."
    )

html = html.replace(
    marker,
    idea_js + marker,
    1
)

path.write_text(
    html,
    encoding="utf-8"
)

print("Idea JavaScript inserted successfully.")