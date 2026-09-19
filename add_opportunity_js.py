from pathlib import Path

path = Path("app/web/innovation.html")
html = path.read_text(encoding="utf-8")

if "async function createOpportunity()" in html:
    print("Opportunity JavaScript already exists.")
    raise SystemExit(0)

script = r"""
        function showCreateOpportunityForm() {
            const form = document.getElementById(
                "createOpportunityForm"
            );

            if (!form) {
                return;
            }

            form.style.display = "block";

            populateOpportunityProblems();

            const title = document.getElementById(
                "opportunityTitle"
            );

            if (title) {
                title.focus();
            }
        }


        function hideCreateOpportunityForm() {
            const form = document.getElementById(
                "createOpportunityForm"
            );

            if (form) {
                form.style.display = "none";
            }

            const opportunityForm = document.getElementById(
                "opportunityForm"
            );

            if (opportunityForm) {
                opportunityForm.reset();
            }

            const message = document.getElementById(
                "opportunityFormMessage"
            );

            if (message) {
                message.textContent = "";
                message.className = "form-message";
            }
        }


        function populateOpportunityProblems() {
            const select = document.getElementById(
                "opportunityProblem"
            );

            if (!select) {
                return;
            }

            const problems = window.spfProblems || [];

            select.innerHTML = "";

            const placeholder = document.createElement(
                "option"
            );

            placeholder.value = "";
            placeholder.textContent = "Select a problem";

            select.appendChild(placeholder);

            problems.forEach(function (problem) {
                const option = document.createElement(
                    "option"
                );

                option.value = problem.id;
                option.textContent =
                    problem.title || "Untitled problem";

                select.appendChild(option);
            });
        }


        async function createOpportunity() {
            const token = localStorage.getItem(
                "spf_access_token"
            );

            const organizationId =
                localStorage.getItem(
                    "spf_organization_id"
                ) || "7";

            if (!token) {
                throw new Error(
                    "You are not logged in."
                );
            }

            const problemId =
                document.getElementById(
                    "opportunityProblem"
                ).value;

            const title =
                document.getElementById(
                    "opportunityTitle"
                ).value.trim();

            const description =
                document.getElementById(
                    "opportunityDescription"
                ).value.trim();

            if (!title || !description) {
                throw new Error(
                    "Opportunity title and description are required."
                );
            }

            const payload = {
                problem_id: problemId
                    ? Number(problemId)
                    : null,

                title: title,

                description: description,

                thesis:
                    document.getElementById(
                        "opportunityThesis"
                    ).value.trim() || null,

                target_users:
                    document.getElementById(
                        "opportunityTargetUsers"
                    ).value.trim() || null,

                value_proposition:
                    document.getElementById(
                        "opportunityValue"
                    ).value.trim() || null,

                potential_outcome:
                    document.getElementById(
                        "opportunityOutcome"
                    ).value.trim() || null,

                technology_leverage:
                    document.getElementById(
                        "opportunityTechnology"
                    ).value.trim() || null,

                strategic_relevance:
                    document.getElementById(
                        "opportunityRelevance"
                    ).value || null,

                timing:
                    document.getElementById(
                        "opportunityTiming"
                    ).value.trim() || null,

                status:
                    document.getElementById(
                        "opportunityStatus"
                    ).value || "discovered"
            };

            const response = await fetch(
                "/innovation/opportunities",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",

                        "Authorization":
                            "Bearer " + token,

                        "X-Organization-ID":
                            organizationId
                    },

                    body: JSON.stringify(payload)
                }
            );

            if (!response.ok) {
                let detail =
                    "Unable to create opportunity.";

                try {
                    const error =
                        await response.json();

                    detail =
                        error.detail || detail;
                } catch (error) {
                    // Keep default error message.
                }

                throw new Error(detail);
            }

            return await response.json();
        }


        const opportunityForm =
            document.getElementById(
                "opportunityForm"
            );

        if (opportunityForm) {
            opportunityForm.addEventListener(
                "submit",
                async function (event) {
                    event.preventDefault();

                    const message =
                        document.getElementById(
                            "opportunityFormMessage"
                        );

                    if (message) {
                        message.textContent =
                            "Creating opportunity...";
                        message.className =
                            "form-message";
                    }

                    try {
                        const opportunity =
                            await createOpportunity();

                        console.log(
                            "Opportunity created:",
                            opportunity
                        );

                        if (message) {
                            message.textContent =
                                "Opportunity created successfully.";
                            message.className =
                                "form-message success";
                        }

                        await loadDashboard();

                        setTimeout(function () {
                            hideCreateOpportunityForm();
                        }, 800);

                    } catch (error) {
                        console.error(
                            "Create opportunity error:",
                            error
                        );

                        if (message) {
                            message.textContent =
                                error.message ||
                                "Unable to create opportunity.";
                            message.className =
                                "form-message error";
                        }
                    }
                }
            );
        }

"""

marker = "</body>"

if marker not in html:
    print("ERROR: </body> marker not found.")
    raise SystemExit(1)

html = html.replace(
    marker,
    "<script>\n" + script + "    </script>\n\n" + marker,
    1
)

path.write_text(html, encoding="utf-8")

print("Opportunity JavaScript inserted successfully.")