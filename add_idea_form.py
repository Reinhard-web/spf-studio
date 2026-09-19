from pathlib import Path

path = Path("app/web/innovation.html")

html = path.read_text(encoding="utf-8")

marker = """                        <!-- CREATE OPPORTUNITY -->"""

idea_form = """                        <!-- CREATE IDEA -->
                        <div class="section-actions" style="margin-top: 18px;">
                            <button
                                type="button"
                                class="primary-button"
                                onclick="showCreateIdeaForm()"
                            >
                                + Create Idea
                            </button>
                        </div>

                        <div
                            id="createIdeaForm"
                            class="modal-overlay"
                            style="display: none;"
                        >
                            <div class="modal-card">
                                <div class="modal-header">
                                    <div>
                                        <h3>Create a New Idea</h3>
                                        <p>
                                            Turn an opportunity into a concrete solution concept
                                            that can be tested.
                                        </p>
                                    </div>

                                    <button
                                        type="button"
                                        class="modal-close"
                                        onclick="hideCreateIdeaForm()"
                                    >
                                        ×
                                    </button>
                                </div>

                                <form id="ideaForm">
                                    <div class="form-group">
                                        <label for="ideaOpportunity">
                                            Opportunity
                                        </label>
                                        <select id="ideaOpportunity">
                                            <option value="">
                                                Select an opportunity (optional)
                                            </option>
                                        </select>
                                    </div>

                                    <div class="form-group">
                                        <label for="ideaTitle">
                                            Idea title
                                        </label>
                                        <input
                                            id="ideaTitle"
                                            type="text"
                                            required
                                            placeholder="Give the idea a clear name..."
                                        >
                                    </div>

                                    <div class="form-group">
                                        <label for="ideaDescription">
                                            Description
                                        </label>
                                        <textarea
                                            id="ideaDescription"
                                            rows="4"
                                            required
                                            placeholder="Describe the idea..."
                                        ></textarea>
                                    </div>

                                    <div class="form-group">
                                        <label for="ideaSolutionConcept">
                                            Solution concept
                                        </label>
                                        <textarea
                                            id="ideaSolutionConcept"
                                            rows="3"
                                            placeholder="How would the solution work?"
                                        ></textarea>
                                    </div>

                                    <div class="form-group">
                                        <label for="ideaTargetUsers">
                                            Target users
                                        </label>
                                        <input
                                            id="ideaTargetUsers"
                                            type="text"
                                            placeholder="Who would use or benefit from this?"
                                        >
                                    </div>

                                    <div class="form-group">
                                        <label for="ideaValueProposition">
                                            Value proposition
                                        </label>
                                        <textarea
                                            id="ideaValueProposition"
                                            rows="3"
                                            placeholder="What value would this create?"
                                        ></textarea>
                                    </div>

                                    <div class="form-group">
                                        <label for="ideaHypothesis">
                                            Hypothesis
                                        </label>
                                        <textarea
                                            id="ideaHypothesis"
                                            rows="3"
                                            placeholder="What do we believe will happen if this idea is tested?"
                                        ></textarea>
                                    </div>

                                    <div class="form-group">
                                        <label for="ideaExpectedOutcome">
                                            Expected outcome
                                        </label>
                                        <textarea
                                            id="ideaExpectedOutcome"
                                            rows="3"
                                            placeholder="What result do we expect from testing this idea?"
                                        ></textarea>
                                    </div>

                                    <div class="form-group">
                                        <label for="ideaSuccessConditions">
                                            Success conditions
                                        </label>
                                        <textarea
                                            id="ideaSuccessConditions"
                                            rows="3"
                                            placeholder="What conditions would indicate that the idea is worth pursuing?"
                                        ></textarea>
                                    </div>

                                    <div class="form-group">
                                        <label for="ideaStatus">
                                            Status
                                        </label>
                                        <select id="ideaStatus">
                                            <option value="draft">Draft</option>
                                            <option value="active">Active</option>
                                            <option value="testing">Testing</option>
                                            <option value="validated">Validated</option>
                                            <option value="rejected">Rejected</option>
                                        </select>
                                    </div>

                                    <div
                                        id="ideaFormMessage"
                                        class="form-message"
                                    ></div>

                                    <div class="modal-actions">
                                        <button
                                            type="button"
                                            class="secondary-button"
                                            onclick="hideCreateIdeaForm()"
                                        >
                                            Cancel
                                        </button>

                                        <button
                                            type="submit"
                                            class="primary-button"
                                        >
                                            Create Idea
                                        </button>
                                    </div>
                                </form>
                            </div>
                        </div>

"""

if marker not in html:
    raise SystemExit("Opportunity marker not found. No changes made.")

if "id=\"createIdeaForm\"" in html:
    raise SystemExit("Create Idea form already exists. No changes made.")

html = html.replace(marker, idea_form + marker, 1)

path.write_text(html, encoding="utf-8")

print("Create Idea form inserted successfully.")