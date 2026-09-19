from pathlib import Path

path = Path("app/web/innovation.html")
html = path.read_text(encoding="utf-8")

marker = "<!-- CREATE LEARNING -->"

if 'id="createEvidenceForm"' in html:
    print("Create Evidence form already exists.")
    raise SystemExit

form = r'''
<!-- CREATE EVIDENCE -->
<div
    id="createEvidenceForm"
    class="modal-overlay"
    style="display: none;"
>
    <div class="modal-card">

        <div class="modal-header">
            <div>
                <h2>Create Evidence</h2>
                <p>Capture concrete evidence from the experiment.</p>
            </div>

            <button
                type="button"
                class="modal-close"
                onclick="hideCreateEvidenceForm()"
            >
                ×
            </button>
        </div>

        <form id="evidenceForm">

            <div class="form-group">
                <label for="evidenceExperiment">
                    Experiment
                </label>

                <select
                    id="evidenceExperiment"
                    name="experiment_id"
                >
                    <option value="">
                        Select experiment
                    </option>
                </select>
            </div>

            <div class="form-group">
                <label for="evidenceTitle">
                    Evidence title
                </label>

                <input
                    type="text"
                    id="evidenceTitle"
                    name="title"
                    placeholder="What evidence was observed?"
                    required
                >
            </div>

            <div class="form-group">
                <label for="evidenceDescription">
                    Description
                </label>

                <textarea
                    id="evidenceDescription"
                    name="description"
                    rows="5"
                    placeholder="Describe the evidence and what was observed."
                    required
                ></textarea>
            </div>

            <div class="form-group">
                <label for="evidenceType">
                    Evidence type
                </label>

                <select
                    id="evidenceType"
                    name="evidence_type"
                    required
                >
                    <option value="">
                        Select evidence type
                    </option>
                    <option value="observation">
                        Observation
                    </option>
                    <option value="customer_feedback">
                        Customer feedback
                    </option>
                    <option value="interview">
                        Interview
                    </option>
                    <option value="usage_data">
                        Usage data
                    </option>
                    <option value="test_result">
                        Test result
                    </option>
                    <option value="survey">
                        Survey
                    </option>
                    <option value="document">
                        Document
                    </option>
                    <option value="other">
                        Other
                    </option>
                </select>
            </div>

            <div class="form-group">
                <label for="evidenceSourceType">
                    Source type
                </label>

                <select
                    id="evidenceSourceType"
                    name="source_type"
                >
                    <option value="">
                        Select source type
                    </option>
                    <option value="customer">
                        Customer
                    </option>
                    <option value="team">
                        Internal team
                    </option>
                    <option value="experiment">
                        Experiment
                    </option>
                    <option value="analytics">
                        Analytics
                    </option>
                    <option value="survey">
                        Survey
                    </option>
                    <option value="document">
                        Document
                    </option>
                    <option value="other">
                        Other
                    </option>
                </select>
            </div>

            <div class="form-group">
                <label for="evidenceSourceReference">
                    Source reference
                </label>

                <input
                    type="text"
                    id="evidenceSourceReference"
                    name="source_reference"
                    placeholder="Interview ID, document, URL, note, etc."
                >
            </div>

            <div class="form-group">
                <label for="evidenceObservedAt">
                    Observed at
                </label>

                <input
                    type="datetime-local"
                    id="evidenceObservedAt"
                    name="observed_at"
                >
            </div>

            <div class="form-group">
                <label for="evidenceStatus">
                    Status
                </label>

                <select
                    id="evidenceStatus"
                    name="status"
                >
                    <option value="observed">
                        Observed
                    </option>
                    <option value="verified">
                        Verified
                    </option>
                    <option value="disputed">
                        Disputed
                    </option>
                    <option value="archived">
                        Archived
                    </option>
                </select>
            </div>

            <div
                id="evidenceFormMessage"
                class="form-message"
            ></div>

            <div class="modal-actions">

                <button
                    type="button"
                    class="btn btn-secondary"
                    onclick="hideCreateEvidenceForm()"
                >
                    Cancel
                </button>

                <button
                    type="submit"
                    class="btn btn-primary"
                >
                    Create Evidence
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

print("Create Evidence form inserted successfully.")