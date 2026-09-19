from pathlib import Path

path = Path("app/web/innovation.html")

html = path.read_text(encoding="utf-8")

marker = """                        <!-- CREATE IDEA -->"""

experiment_form = """                        <!-- CREATE EXPERIMENT -->
                        <div class="section-actions" style="margin-top: 18px;">
                            <button
                                type="button"
                                class="primary-button"
                                onclick="showCreateExperimentForm()"
                            >
                                + Create Experiment
                            </button>
                        </div>

                        <div
                            id="createExperimentForm"
                            class="modal-overlay"
                            style="display: none;"
                        >
                            <div class="modal-card">
                                <div class="modal-header">
                                    <div>
                                        <h3>Create a New Experiment</h3>
                                        <p>
                                            Turn an idea into a structured test
                                            that can generate evidence and learning.
                                        </p>
                                    </div>

                                    <button
                                        type="button"
                                        class="modal-close"
                                        onclick="hideCreateExperimentForm()"
                                    >
                                        ×
                                    </button>
                                </div>

                                <form id="experimentForm">
                                    <div class="form-group">
                                        <label for="experimentIdea">
                                            Idea
                                        </label>
                                        <select id="experimentIdea" required>
                                            <option value="">
                                                Select an idea
                                            </option>
                                        </select>
                                    </div>

                                    <div class="form-group">
                                        <label for="experimentTitle">
                                            Experiment title
                                        </label>
                                        <input
                                            id="experimentTitle"
                                            type="text"
                                            required
                                            placeholder="Give the experiment a clear name..."
                                        >
                                    </div>

                                    <div class="form-group">
                                        <label for="experimentObjective">
                                            Objective
                                        </label>
                                        <textarea
                                            id="experimentObjective"
                                            rows="3"
                                            required
                                            placeholder="What are we trying to learn?"
                                        ></textarea>
                                    </div>

                                    <div class="form-group">
                                        <label for="experimentHypothesis">
                                            Hypothesis
                                        </label>
                                        <textarea
                                            id="experimentHypothesis"
                                            rows="3"
                                            required
                                            placeholder="What do we believe will happen?"
                                        ></textarea>
                                    </div>

                                    <div class="form-group">
                                        <label for="experimentUncertainty">
                                            Key uncertainty
                                        </label>
                                        <textarea
                                            id="experimentUncertainty"
                                            rows="3"
                                            placeholder="What are we most uncertain about?"
                                        ></textarea>
                                    </div>

                                    <div class="form-group">
                                        <label for="experimentAssumptions">
                                            Assumptions
                                        </label>
                                        <textarea
                                            id="experimentAssumptions"
                                            rows="3"
                                            placeholder="What assumptions are we making?"
                                        ></textarea>
                                    </div>

                                    <div class="form-group">
                                        <label for="experimentMethodology">
                                            Methodology
                                        </label>
                                        <textarea
                                            id="experimentMethodology"
                                            rows="4"
                                            required
                                            placeholder="How will we conduct the experiment?"
                                        ></textarea>
                                    </div>

                                    <div class="form-group">
                                        <label for="experimentSuccessCriteria">
                                            Success criteria
                                        </label>
                                        <textarea
                                            id="experimentSuccessCriteria"
                                            rows="3"
                                            required
                                            placeholder="What result would indicate success?"
                                        ></textarea>
                                    </div>

                                    <div class="form-group">
                                        <label for="experimentFailureCriteria">
                                            Failure criteria
                                        </label>
                                        <textarea
                                            id="experimentFailureCriteria"
                                            rows="3"
                                            placeholder="What result would indicate that the hypothesis is not supported?"
                                        ></textarea>
                                    </div>

                                    <div class="form-group">
                                        <label for="experimentStatus">
                                            Status
                                        </label>
                                        <select id="experimentStatus">
                                            <option value="draft">Draft</option>
                                            <option value="planned">Planned</option>
                                            <option value="running">Running</option>
                                            <option value="completed">Completed</option>
                                            <option value="cancelled">Cancelled</option>
                                        </select>
                                    </div>

                                    <div
                                        id="experimentFormMessage"
                                        class="form-message"
                                    ></div>

                                    <div class="modal-actions">
                                        <button
                                            type="button"
                                            class="secondary-button"
                                            onclick="hideCreateExperimentForm()"
                                        >
                                            Cancel
                                        </button>

                                        <button
                                            type="submit"
                                            class="primary-button"
                                        >
                                            Create Experiment
                                        </button>
                                    </div>
                                </form>
                            </div>
                        </div>

"""

if marker not in html:
    raise SystemExit(
        "Idea marker not found. No changes made."
    )

if "id=\"createExperimentForm\"" in html:
    raise SystemExit(
        "Create Experiment form already exists. No changes made."
    )

html = html.replace(
    marker,
    experiment_form + marker,
    1
)

path.write_text(
    html,
    encoding="utf-8"
)

print("Create Experiment form inserted successfully.")