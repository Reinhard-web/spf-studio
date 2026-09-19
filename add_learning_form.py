from pathlib import Path

path = Path("app/web/innovation.html")
html = path.read_text(encoding="utf-8")

marker = "<!-- CREATE EXPERIMENT -->"

if "id=\"createLearningForm\"" in html:
    print("Create Learning form already exists.")
    raise SystemExit

form = r'''
<!-- CREATE LEARNING -->
<div
    id="createLearningForm"
    class="modal-overlay"
    style="display: none;"
>
    <div class="modal-card">
        <div class="modal-header">
            <div>
                <h2>Create Learning</h2>
                <p>Capture what the experiment has taught us.</p>
            </div>

            <button
                type="button"
                class="modal-close"
                onclick="hideCreateLearningForm()"
            >
                ×
            </button>
        </div>

        <form id="learningForm">

            <div class="form-group">
                <label for="learningExperiment">
                    Experiment
                </label>

                <select
                    id="learningExperiment"
                    name="experiment_id"
                >
                    <option value="">
                        Select experiment
                    </option>
                </select>
            </div>

            <div class="form-group">
                <label for="learningTitle">
                    Learning title
                </label>

                <input
                    type="text"
                    id="learningTitle"
                    name="title"
                    placeholder="What did we learn?"
                    required
                >
            </div>

            <div class="form-group">
                <label for="learningDescription">
                    Description
                </label>

                <textarea
                    id="learningDescription"
                    name="description"
                    rows="5"
                    placeholder="Describe the learning and what it means."
                    required
                ></textarea>
            </div>

            <div class="form-group">
                <label for="learningType">
                    Learning type
                </label>

                <select
                    id="learningType"
                    name="learning_type"
                    required
                >
                    <option value="">
                        Select learning type
                    </option>
                    <option value="customer">Customer</option>
                    <option value="product">Product</option>
                    <option value="market">Market</option>
                    <option value="technical">Technical</option>
                    <option value="operational">Operational</option>
                    <option value="business">Business</option>
                    <option value="other">Other</option>
                </select>
            </div>

            <div class="form-group">
                <label for="learningConfidence">
                    Confidence
                </label>

                <select
                    id="learningConfidence"
                    name="confidence"
                >
                    <option value="">
                        Select confidence
                    </option>
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                </select>
            </div>

            <div class="form-group">
                <label for="learningStatus">
                    Status
                </label>

                <select
                    id="learningStatus"
                    name="status"
                >
                    <option value="active">
                        Active
                    </option>
                    <option value="archived">
                        Archived
                    </option>
                </select>
            </div>

            <div
                id="learningFormMessage"
                class="form-message"
            ></div>

            <div class="modal-actions">
                <button
                    type="button"
                    class="btn btn-secondary"
                    onclick="hideCreateLearningForm()"
                >
                    Cancel
                </button>

                <button
                    type="submit"
                    class="btn btn-primary"
                >
                    Create Learning
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

print("Create Learning form inserted successfully.")