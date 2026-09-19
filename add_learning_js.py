from pathlib import Path

path = Path("app/web/innovation.html")
html = path.read_text(encoding="utf-8")

if "async function createLearning()" in html:
    print("Learning JavaScript already exists.")
    raise SystemExit

js = r'''
<script>
        function showCreateLearningForm() {
            const form = document.getElementById("createLearningForm");

            if (form) {
                form.style.display = "flex";
                populateLearningExperiments();
            }
        }

        function hideCreateLearningForm() {
            const form = document.getElementById("createLearningForm");

            if (form) {
                form.style.display = "none";
            }

            const learningForm =
                document.getElementById("learningForm");

            if (learningForm) {
                learningForm.reset();
            }

            const message =
                document.getElementById("learningFormMessage");

            if (message) {
                message.textContent = "";
            }
        }

        async function populateLearningExperiments() {
            const select =
                document.getElementById("learningExperiment");

            if (!select) {
                return;
            }

            const token = localStorage.getItem("spf_access_token");

            if (!token) {
                return;
            }

            try {
                const response = await fetch(
                    "/innovation/experiments",
                    {
                        headers: {
                            "Authorization": `Bearer ${token}`,
                            "X-Organization-ID": "7"
                        }
                    }
                );

                if (!response.ok) {
                    throw new Error(
                        "Unable to load experiments."
                    );
                }

                const experiments = await response.json();

                select.innerHTML =
                    '<option value="">Select experiment</option>';

                experiments.forEach((experiment) => {
                    const option =
                        document.createElement("option");

                    option.value = experiment.id;
                    option.textContent = experiment.title;

                    select.appendChild(option);
                });

            } catch (error) {
                console.error(
                    "Error loading experiments:",
                    error
                );
            }
        }

        async function createLearning() {
            const token =
                localStorage.getItem("spf_access_token");

            if (!token) {
                throw new Error(
                    "Please log in before creating a learning."
                );
            }

            const experimentId =
                document.getElementById(
                    "learningExperiment"
                ).value;

            const title =
                document.getElementById(
                    "learningTitle"
                ).value.trim();

            const description =
                document.getElementById(
                    "learningDescription"
                ).value.trim();

            const learningType =
                document.getElementById(
                    "learningType"
                ).value;

            const confidence =
                document.getElementById(
                    "learningConfidence"
                ).value;

            const status =
                document.getElementById(
                    "learningStatus"
                ).value;

            if (!title) {
                throw new Error(
                    "Learning title is required."
                );
            }

            if (!description) {
                throw new Error(
                    "Learning description is required."
                );
            }

            if (!learningType) {
                throw new Error(
                    "Learning type is required."
                );
            }

            const payload = {
                title: title,
                description: description,
                learning_type: learningType,
                confidence: confidence || null,
                status: status
            };

            if (experimentId) {
                payload.experiment_id =
                    Number(experimentId);
            }

            const response = await fetch(
                "/innovation/learnings",
                {
                    method: "POST",
                    headers: {
                        "Authorization":
                            `Bearer ${token}`,
                        "X-Organization-ID": "7",
                        "Content-Type":
                            "application/json"
                    },
                    body: JSON.stringify(payload)
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.detail ||
                    "Unable to create learning."
                );
            }

            return data;
        }

        const learningForm =
            document.getElementById("learningForm");

        if (learningForm) {
            learningForm.addEventListener(
                "submit",
                async function (event) {
                    event.preventDefault();

                    const message =
                        document.getElementById(
                            "learningFormMessage"
                        );

                    if (message) {
                        message.textContent =
                            "Creating learning...";
                    }

                    try {
                        const learning =
                            await createLearning();

                        if (message) {
                            message.textContent =
                                "Learning created successfully.";
                        }

                        console.log(
                            "Learning created:",
                            learning
                        );

                        setTimeout(() => {
                            hideCreateLearningForm();

                            if (
                                typeof loadDashboard ===
                                "function"
                            ) {
                                loadDashboard();
                            }
                        }, 700);

                    } catch (error) {
                        console.error(
                            "Learning creation failed:",
                            error
                        );

                        if (message) {
                            message.textContent =
                                error.message;
                        }
                    }
                }
            );
        }
</script>
'''

marker = "</body>"

if marker not in html:
    raise SystemExit("Could not find </body> marker.")

html = html.replace(marker, js + "\n" + marker, 1)

path.write_text(html, encoding="utf-8")

print("Learning JavaScript inserted successfully.")