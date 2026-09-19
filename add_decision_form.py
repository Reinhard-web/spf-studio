from pathlib import Path

path = Path("app/web/innovation.html")
html = path.read_text(encoding="utf-8")

marker = "<!-- CREATE EVIDENCE -->"

if 'id="createDecisionForm"' in html:
    print("Create Decision form already exists.")
    raise SystemExit

form = r'''
<!-- CREATE DECISION -->
<div
    id="createDecisionForm"
    class="modal-overlay"
    style="display: none;"
>
    <div class="modal-card">

        <div class="modal-header">
            <div>
                <h2>Create Decision</h2>
                <p>Record the decision reached from the innovation evidence.</p>
            </div>

            <button
                type="button"
                class="modal-close"
                onclick="hideCreateDecisionForm()"
            >
                ×
            </button>
        </div>

        <form id="decisionForm">

            <div class="form-group">
                <label for="decisionProblem">
                    Problem
                </label>

                <select id="decisionProblem">
                    <option value="">
                        Select problem
                    </option>
                </select>
            </div>

            <div class="form-group">
                <label for="decisionOpportunity">
                    Opportunity
                </label>

                <select id="decisionOpportunity">
                    <option value="">
                        Select opportunity
                    </option>
                </select>
            </div>

            <div class="form-group">
                <label for="decisionIdea">
                    Idea
                </label>

                <select id="decisionIdea">
                    <option value="">
                        Select idea
                    </option>
                </select>
            </div>

            <div class="form-group">
                <label for="decisionExperiment">
                    Experiment
                </label>

                <select id="decisionExperiment">
                    <option value="">
                        Select experiment
                    </option>
                </select>
            </div>

            <div class="form-group">
                <label for="decisionLearning">
                    Learning
                </label>

                <select id="decisionLearning">
                    <option value="">
                        Select learning
                    </option>
                </select>
            </div>

            <div class="form-group">
                <label for="decisionEvidence">
                    Evidence
                </label>

                <select id="decisionEvidence">
                    <option value="">
                        Select evidence
                    </option>
                </select>
            </div>

            <div class="form-group">
                <label for="decisionTitle">
                    Decision title
                </label>

                <input
                    type="text"
                    id="decisionTitle"
                    placeholder="What decision was reached?"
                    required
                >
            </div>

            <div class="form-group">
                <label for="decisionDecision">
                    Decision
                </label>

                <textarea
                    id="decisionDecision"
                    rows="4"
                    placeholder="What should happen next?"
                    required
                ></textarea>
            </div>

            <div class="form-group">
                <label for="decisionRationale">
                    Rationale
                </label>

                <textarea
                    id="decisionRationale"
                    rows="5"
                    placeholder="Why was this decision made?"
                ></textarea>
            </div>

            <div class="form-group">
                <label for="decisionStatus">
                    Status
                </label>

                <select id="decisionStatus">
                    <option value="active">
                        Active
                    </option>
                    <option value="draft">
                        Draft
                    </option>
                    <option value="superseded">
                        Superseded
                    </option>
                    <option value="archived">
                        Archived
                    </option>
                </select>
            </div>

            <div class="form-group">
                <label for="decisionDecidedBy">
                    Decided by
                </label>

                <input
                    type="text"
                    id="decisionDecidedBy"
                    placeholder="Person or team making the decision"
                >
            </div>

            <div
                id="decisionFormMessage"
                class="form-message"
            ></div>

            <div class="modal-actions">

                <button
                    type="button"
                    class="btn btn-secondary"
                    onclick="hideCreateDecisionForm()"
                >
                    Cancel
                </button>

                <button
                    type="submit"
                    class="btn btn-primary"
                >
                    Create Decision
                </button>

            </div>

        </form>
    </div>
</div>

'''

if marker not in html:
    raise SystemExit(f"Marker not found: {marker}")

html = html.replace(marker, form + marker, 1)

path.write_text(html, encoding="utf-8")

print("Create Decision form inserted successfully.")