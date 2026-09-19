from pathlib import Path

path = Path("app/web/innovation.html")

html = path.read_text(encoding="utf-8")

marker = "        function showCreateIdeaForm() {"

experiment_js = r'''
        function showCreateExperimentForm() {
            const form = document.getElementById("createExperimentForm");

            if (form) {
                form.style.display = "flex";
            }

            populateExperimentIdeas();

            const title = document.getElementById("experimentTitle");

            if (title) {
                title.focus();
            }
        }

        function hideCreateExperimentForm() {
            const form = document.getElementById("createExperimentForm");

            if (form) {
                form.style.display = "none";
            }

            const experimentForm =
                document.getElementById("experimentForm");

            if (experimentForm) {
                experimentForm.reset();
            }

            const message =
                document.getElementById("experimentFormMessage");

            if (message) {
                message.textContent = "";
                message.className = "form-message";
            }
        }

        async function populateExperimentIdeas() {
            const select =
                document.getElementById("experimentIdea");

            if (!select) {
                return;
            }

            try {
                const token =
                    localStorage.getItem("spf_access_token");

                if (!token) {
                    return;
                }

                const response = await fetch(
                    "/innovation/ideas",
                    {
                        headers: {
                            "Authorization": `Bearer ${token}`,
                            "X-Organization-ID": "7"
                        }
                    }
                );

                if (!response.ok) {
                    throw new Error(
                        "Unable to load ideas."
                    );
                }

                const ideas = await response.json();

                select.innerHTML = `
                    <option value="">
                        Select an idea
                    </option>
                `;

                ideas.forEach((idea) => {
                    const option =
                        document.createElement("option");

                    option.value = idea.id;
                    option.textContent = idea.title;

                    select.appendChild(option);
                });

            } catch (error) {
                console.error(
                    "Idea loading error:",
                    error
                );
            }
        }

        async function createExperiment() {
            const token =
                localStorage.getItem("spf_access_token");

            if (!token) {
                throw new Error(
                    "Please log in again."
                );
            }

            const payload = {
                idea_id: Number(
                    document.getElementById(
                        "experimentIdea"
                    ).value
                ),

                title:
                    document.getElementById(
                        "experimentTitle"
                    ).value.trim(),

                objective:
                    document.getElementById(
                        "experimentObjective"
                    ).value.trim(),

                hypothesis:
                    document.getElementById(
                        "experimentHypothesis"
                    ).value.trim(),

                uncertainty:
                    document.getElementById(
                        "experimentUncertainty"
                    ).value.trim() || null,

                assumptions:
                    document.getElementById(
                        "experimentAssumptions"
                    ).value.trim() || null,

                methodology:
                    document.getElementById(
                        "experimentMethodology"
                    ).value.trim(),

                success_criteria:
                    document.getElementById(
                        "experimentSuccessCriteria"
                    ).value.trim(),

                failure_criteria:
                    document.getElementById(
                        "experimentFailureCriteria"
                    ).value.trim() || null,

                status:
                    document.getElementById(
                        "experimentStatus"
                    ).value
            };

            if (!payload.idea_id) {
                throw new Error(
                    "Please select an idea."
                );
            }

            if (
                !payload.title ||
                !payload.objective ||
                !payload.hypothesis ||
                !payload.methodology ||
                !payload.success_criteria
            ) {
                throw new Error(
                    "Please complete all required experiment fields."
                );
            }

            const response = await fetch(
                "/innovation/experiments",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",

                        "Authorization":
                            `Bearer ${token}`,

                        "X-Organization-ID":
                            "7"
                    },

                    body: JSON.stringify(payload)
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.detail ||
                    "Unable to create experiment."
                );
            }

            return data;
        }

        const experimentForm =
            document.getElementById(
                "experimentForm"
            );

        if (experimentForm) {
            experimentForm.addEventListener(
                "submit",
                async function (event) {
                    event.preventDefault();

                    const message =
                        document.getElementById(
                            "experimentFormMessage"
                        );

                    try {
                        if (message) {
                            message.textContent =
                                "Creating experiment...";

                            message.className =
                                "form-message";
                        }

                        const experiment =
                            await createExperiment();

                        console.log(
                            "Experiment created:",
                            experiment
                        );

                        if (message) {
                            message.textContent =
                                "Experiment created successfully.";

                            message.className =
                                "form-message success";
                        }

                        setTimeout(() => {
                            hideCreateExperimentForm();

                            if (
                                typeof loadInnovationData ===
                                "function"
                            ) {
                                loadInnovationData();
                            } else {
                                window.location.reload();
                            }
                        }, 700);

                    } catch (error) {
                        console.error(
                            "Create experiment error:",
                            error
                        );

                        if (message) {
                            message.textContent =
                                error.message ||
                                "Unable to create experiment.";

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
        "Idea JavaScript marker not found. No changes made."
    )

if "function showCreateExperimentForm()" in html:
    raise SystemExit(
        "Experiment JavaScript already exists. No changes made."
    )

html = html.replace(
    marker,
    experiment_js + marker,
    1
)

path.write_text(
    html,
    encoding="utf-8"
)

print(
    "Experiment JavaScript inserted successfully."
)