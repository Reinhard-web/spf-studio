from pathlib import Path

path = Path("app/web/innovation.html")
html = path.read_text(encoding="utf-8")

marker = """                        <!-- PROBLEM LIST -->"""

if "id=\"createOpportunityForm\"" in html:
    print("Create Opportunity form already exists.")
    raise SystemExit(0)

insert = r"""
                        <!-- CREATE OPPORTUNITY -->

                        <div class="problem-create-bar">
                            <button
                                type="button"
                                class="problem-create-button"
                                onclick="showCreateOpportunityForm()"
                            >
                                + Create Opportunity
                            </button>
                        </div>

                        <div
                            id="createOpportunityForm"
                            class="create-problem-form"
                            style="display: none;"
                        >

                            <div class="create-problem-header">
                                <div>
                                    <h3>Create a New Opportunity</h3>
                                    <p>
                                        Turn a meaningful problem into a
                                        potential opportunity worth exploring.
                                    </p>
                                </div>

                                <button
                                    type="button"
                                    class="create-problem-close"
                                    onclick="hideCreateOpportunityForm()"
                                >
                                    ×
                                </button>
                            </div>

                            <form id="opportunityForm">

                                <div class="form-field">
                                    <label for="opportunityProblem">
                                        Related problem
                                    </label>

                                    <select
                                        id="opportunityProblem"
                                        name="problem_id"
                                    >
                                        <option value="">
                                            Select a problem
                                        </option>
                                    </select>
                                </div>

                                <div class="form-field">
                                    <label for="opportunityTitle">
                                        Opportunity title
                                    </label>

                                    <input
                                        type="text"
                                        id="opportunityTitle"
                                        name="title"
                                        placeholder="e.g. Simple customer follow-up management for small businesses"
                                        required
                                    >
                                </div>

                                <div class="form-field">
                                    <label for="opportunityDescription">
                                        Description
                                    </label>

                                    <textarea
                                        id="opportunityDescription"
                                        name="description"
                                        rows="5"
                                        placeholder="Describe the opportunity and what could be created or improved..."
                                        required
                                    ></textarea>
                                </div>

                                <div class="form-field">
                                    <label for="opportunityThesis">
                                        Opportunity thesis
                                    </label>

                                    <textarea
                                        id="opportunityThesis"
                                        name="thesis"
                                        rows="3"
                                        placeholder="Why do we believe this opportunity is worth exploring?"
                                    ></textarea>
                                </div>

                                <div class="form-field">
                                    <label for="opportunityTargetUsers">
                                        Target users
                                    </label>

                                    <textarea
                                        id="opportunityTargetUsers"
                                        name="target_users"
                                        rows="3"
                                        placeholder="Who could benefit from this opportunity?"
                                    ></textarea>
                                </div>

                                <div class="form-field">
                                    <label for="opportunityValue">
                                        Value proposition
                                    </label>

                                    <textarea
                                        id="opportunityValue"
                                        name="value_proposition"
                                        rows="3"
                                        placeholder="What value could this opportunity create?"
                                    ></textarea>
                                </div>

                                <div class="form-field">
                                    <label for="opportunityOutcome">
                                        Potential outcome
                                    </label>

                                    <textarea
                                        id="opportunityOutcome"
                                        name="potential_outcome"
                                        rows="3"
                                        placeholder="What could success or improvement look like?"
                                    ></textarea>
                                </div>

                                <div class="form-row">

                                    <div class="form-field">
                                        <label for="opportunityTechnology">
                                            Technology leverage
                                        </label>

                                        <input
                                            type="text"
                                            id="opportunityTechnology"
                                            name="technology_leverage"
                                            placeholder="e.g. AI, automation, workflow software"
                                        >
                                    </div>

                                    <div class="form-field">
                                        <label for="opportunityTiming">
                                            Timing
                                        </label>

                                        <input
                                            type="text"
                                            id="opportunityTiming"
                                            name="timing"
                                            placeholder="e.g. Now, next 6 months"
                                        >
                                    </div>

                                </div>

                                <div class="form-row">

                                    <div class="form-field">
                                        <label for="opportunityRelevance">
                                            Strategic relevance
                                        </label>

                                        <select
                                            id="opportunityRelevance"
                                            name="strategic_relevance"
                                        >
                                            <option value="">
                                                Not assessed
                                            </option>

                                            <option value="low">
                                                Low
                                            </option>

                                            <option value="medium">
                                                Medium
                                            </option>

                                            <option value="high">
                                                High
                                            </option>
                                        </select>
                                    </div>

                                    <div class="form-field">
                                        <label for="opportunityStatus">
                                            Status
                                        </label>

                                        <select
                                            id="opportunityStatus"
                                            name="status"
                                        >
                                            <option value="discovered">
                                                Discovered
                                            </option>

                                            <option value="exploring">
                                                Exploring
                                            </option>

                                            <option value="active">
                                                Active
                                            </option>

                                            <option value="validated">
                                                Validated
                                            </option>
                                        </select>
                                    </div>

                                </div>

                                <div
                                    id="opportunityFormMessage"
                                    class="form-message"
                                ></div>

                                <div class="create-problem-actions">

                                    <button
                                        type="button"
                                        class="secondary-button"
                                        onclick="hideCreateOpportunityForm()"
                                    >
                                        Cancel
                                    </button>

                                    <button
                                        type="submit"
                                        class="primary-button"
                                    >
                                        Create Opportunity
                                    </button>

                                </div>

                            </form>

                        </div>

"""

if marker not in html:
    print("ERROR: insertion point not found.")
    raise SystemExit(1)

html = html.replace(marker, insert + marker, 1)

path.write_text(html, encoding="utf-8")

print("Create Opportunity form inserted successfully.")