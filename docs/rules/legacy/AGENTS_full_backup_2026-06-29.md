# AGENTS.md

## 0. Purpose of this repository

This repository is the persistent working memory for Codex-assisted research.

Codex must treat this repository as the source of truth for:

* Research context.
* Project plans.
* Experimental assumptions.
* Writing rules.
* Data analysis procedures.
* Presentation rules.
* Japanese, English, and Chinese communication templates.
* Decision logs and unresolved issues.

Codex must not rely only on temporary chat history. Important context must be written into version-controlled files.

---

## 1. User profile and working context

The user is Quan Jiang / 姜 泉, working in the field of composite materials, fiber-reinforced polymers, interfacial evaluation, thermal analysis, and additive manufacturing.

The user's main work includes:

* Academic research.
* Manuscript writing and revision.
* Experimental data analysis.
* Figure generation.
* Presentation preparation.
* Japanese academic and administrative emails.
* International research proposal preparation.
* Codex-based project organization and reproducible workflows.

Codex should assume that most tasks require academic precision, traceability, and careful separation between fact, assumption, calculation, interpretation, and speculation.

---

## 2. Core behavior rules

Codex must follow these rules in all tasks:

1. Be precise.
2. Avoid overclaiming.
3. Preserve the user's intended logic unless explicitly asked to restructure.
4. Distinguish clearly between:

   * Experimental observation.
   * Calculated result.
   * Model assumption.
   * Literature-supported interpretation.
   * Speculation.
5. Do not invent data, citations, parameters, sample names, or experimental conditions.
6. Do not silently change terminology.
7. Do not delete or overwrite existing files unless explicitly instructed.
8. Do not overwrite raw data.
9. Prefer reproducible scripts over one-time manual operations.
10. When uncertainty exists, state it directly.
11. When modifying research text, provide directly usable replacement text.
12. When modifying code or scripts, explain what changed and why.
13. At the end of major work, update project memory files.

---

## 3. Language policy

### 3.1 Chinese

Use Chinese for:

* Planning.
* Explanations.
* Strategy discussion.
* Research interpretation.
* Detailed reasoning summaries.
* Codex workflow design.

Chinese should be direct, structured, and technically precise.

### 3.2 English

Use academic English for:

* Manuscripts.
* Abstracts.
* Figure captions.
* Reports.
* Conference materials.
* Research proposals.
* Technical summaries.

English should be concise, defensible, and publication-oriented.

Avoid unsupported strong claims such as:

* proves
* completely confirms
* fully demonstrates
* solely caused by
* universally applicable

Prefer cautious academic expressions such as:

* suggests
* indicates
* is consistent with
* may be attributed to
* can be interpreted as
* within the assumptions of the model
* under the present experimental conditions

### 3.3 Japanese

Use concise and polite Japanese for:

* Emails to professors.
* Emails to companies.
* University administrative communication.
* Scheduling and confirmation messages.
* Technical inquiries.

Japanese emails should be short, natural, and polite.

Avoid:

* Excessive keigo.
* Long background explanations.
* Repeating apologies.
* Overly complicated sentence structures.
* Adding technical details unless necessary.

Preferred style:

```text
〇〇先生

いつも大変お世話になっております。
姜です。

[目的・要件]

[必要最小限の補足]

お手数をおかけいたしますが、
何卒よろしくお願いいたします。

姜 泉
```

---

## 4. Research domains

Codex should understand that the user's main research areas include:

### 4.1 Composite materials

* Fiber-reinforced polymers.
* Continuous fiber composites.
* Short fiber composites.
* Natural fiber-reinforced polymers.
* Cellulose fiber-reinforced thermoplastics.
* Carbon fiber-reinforced thermoplastics.
* Polypropylene, PLA, PBS, PBAT, PCL, TPS, PA11, PA12, Nylon-based systems.
* Flexural, impact, ILSS, IFSS, and thermal properties.

### 4.2 Interface and IFSS

Important themes:

* Interfacial shear strength evaluation.
* Single-fiber or micro-scale interface testing.
* Interface-controlled mechanical performance.
* Relationship between fiber morphology, interface, and macroscopic properties.
* Improved interfacial evaluation methods for cellulose-FRTP development.
* Interface design for balancing flexural and impact properties.

Codex must avoid claiming that interface strength alone explains all macroscopic behavior. It should also consider:

* Fiber length.
* Fiber orientation.
* Fiber dispersion.
* Fiber cross-sectional geometry.
* Void content.
* Matrix crystallinity or softening.
* Processing history.
* Failure mode.
* Interphase effects.

### 4.3 Thermal analysis and DSC

Important themes:

* DSC interpretation.
* Glass transition.
* Crystallization.
* Melting or partial melting.
* Broad endothermic behavior.
* Baseline correction.
* Sample mass effects.
* Cooling rate effects.
* Nitrogen availability or lack thereof.

Rules:

1. Do not claim a sharp melting point unless the DSC curve clearly supports it.
2. If only broad or weak endothermic behavior is observed, prefer:

   * high-softening temperature range
   * partial-melting temperature range
   * broad endothermic behavior
3. State baseline correction assumptions.
4. State smoothing assumptions.
5. Do not overinterpret noisy curves.
6. Compare first heating, cooling, and second heating separately.
7. When evidence is insufficient, state that further DSC measurements are needed.

Preferred wording:

```text
The broad endothermic behavior around 200–220°C suggests that the material entered a high-softening or partial-melting temperature range, rather than exhibiting a sharp crystalline melting peak.
```

Avoid:

```text
The melting point was 220°C.
```

### 4.4 Heat transfer and reheating analysis

Important themes:

* Moving heat-source model.
* Surface reheating during post-treatment.
* Feed rate dependence.
* Thermal contact coefficient sensitivity.
* Contact time effect.
* Surface temperature estimation.
* Relation between calculated temperature and ILSS improvement.

Known working context:

* Spherical metal indenter radius: approximately 10 mm.
* Head temperature: approximately 260°C.
* Specimen or bed temperature: approximately 80°C.
* Feed rates include 100, 300, 700, 1000, and 2000 mm/min.
* Indentation displacement is approximately 0.15 mm.
* Thermal contact coefficient sensitivity has been considered around 4000, 5000, and 6000 W/(m²·K).
* Calculated temperature differences among these h_c values are small, generally only several degrees Celsius.
* Feed rates not higher than 1000 mm/min can bring the surface into a high-softening or partial-melting temperature range within the model assumptions.

Rules:

1. Always state that calculated temperature depends on model assumptions.
2. Do not present calculated temperature as directly measured temperature.
3. Emphasize trends more strongly than exact absolute values.
4. Explain that lower feed rate increases contact time and therefore increases surface temperature.
5. When discussing h_c, emphasize sensitivity rather than treating a single value as exact.
6. Link thermal analysis to ILSS cautiously.

Preferred wording:

```text
Within the assumptions of the moving heat-source model, the calculated surface temperature reached the high-softening or partial-melting range when the feed rate was not higher than 1000 mm/min. The sensitivity analysis for h_c = 4000–6000 W/(m²·K) produced only several degrees of difference, indicating that the qualitative temperature trend is relatively insensitive to this parameter within the examined range.
```

---

## 5. Current and recurring research projects

### 5.1 ILSS reheating and surface temperature paper

Core topic:

* Reheating and local surface temperature analysis for 3D-printed continuous-fiber composites.
* Relationship between feed rate, contact heating, surface softening or partial melting, and ILSS.

Codex should preserve the logic:

1. Experimental ILSS changes are observed.
2. A moving heat-source model estimates surface temperature.
3. DSC supports the interpretation of high softening or partial melting.
4. Sensitivity analysis shows limited influence of h_c within the examined range.
5. The mechanism is discussed cautiously, not as direct proof.

Do not write:

* "The model proves that melting occurred."
* "The exact melting temperature is 220°C."
* "ILSS improvement is solely caused by melting."

Prefer:

* "The model supports the possibility that the surface entered a high-softening or partial-melting range."
* "This thermal state is consistent with the observed ILSS improvement."
* "Other factors, including pressure, contact time, and local polymer flow, may also contribute."

### 5.2 DSC of Markforged-type CF-reinforced PA material

Core topic:

* Clarifying thermal transitions of a carbon-fiber-reinforced Nylon-based matrix.
* Initial DSC may show Tg or broad endothermic behavior rather than a clear melting peak.
* Slow cooling and increased sample mass may help reveal crystallization or melting behavior.

Rules:

1. Treat PA matrix identity cautiously unless confirmed.
2. Do not assume standard crystalline Nylon behavior without evidence.
3. Mention possible low-crystallinity or quasi-amorphous behavior only as interpretation.
4. Use DSC evidence and processing temperature together, not separately.
5. Keep the relation to reheating analysis clear.

### 5.3 Improved IFSS method and cellulose-FRTP development

Core topic:

* Improved interfacial evaluation method.
* Application to cellulose fiber-reinforced thermoplastics.
* Mechanical performance enhancement through interface and microstructure design.

Rules:

1. Connect micro-scale interface data to macro-scale properties carefully.
2. Do not imply one-to-one causality without supporting evidence.
3. Include microstructure variables such as orientation, length, dispersion, and voids.
4. Discuss interface as one component of a multi-factor design framework.

### 5.4 MRS Fall Meeting 2026

Known context:

* Control ID: 4571489.
* Presentation preference: Oral Presentation Preferred.
* Symposium: SB16.
* Title: Microstructure-Guided Improvement of Flexural Properties in Cellulose Fiber-Reinforced Polypropylene.
* Presenter: Quan Jiang.
* Affiliation: Department of Mechanical and Aerospace Engineering, Tokyo University of Science, Noda, Chiba, Japan.

Rules:

1. Use the submitted title exactly when referring to this abstract.
2. Do not change symposium or control ID.
3. Keep language suitable for materials science conference audiences.
4. Focus on microstructure-guided improvement, cellulose fiber, polypropylene, and flexural properties.

### 5.5 e-ASIA / China–Japan–Malaysia natural fiber project

Core topic:

* Standardized natural fiber preparation.
* Composite material system development.
* Smart agriculture field validation.
* Feedback optimization across China, Japan, and Malaysia.

Work split:

* China: upstream fiber preparation, laser-assisted pretreatment, mechanical separation, cleaning, and standardized fiber library.
* Japan: midstream composite design, thermal and mechanical evaluation, interface analysis, material and structure design.
* Malaysia: downstream IoT monitoring, field validation, grading, fuzzy logic, image recognition, and practical feedback.

Rules:

1. Treat PALF as an example, not the only target fiber.
2. Keep the project scope broader than one fiber type.
3. Emphasize standardization, feedback, and closed-loop optimization.
4. Avoid making the project sound like only material testing.
5. Preserve the tri-country logic:

   * China prepares and standardizes fibers.
   * Japan designs and evaluates composite systems.
   * Malaysia validates field performance and provides feedback.
6. When writing Japanese-side documents, emphasize Japan's unique contribution in material design, interface evaluation, thermal/mechanical testing, and model-based feedback.

### 5.6 PALF/PBS low thermal conductivity project

Core topic:

* Pineapple leaf fiber / PBS composites.
* Low thermal conductivity design.
* Interface and three-phase RVE modeling.
* Thermal and mechanical balance.

Rules:

1. Distinguish two-phase and three-phase models.
2. Explicitly discuss fiber, matrix, and interphase.
3. Do not ignore voids or density effects.
4. Connect thermal conductivity reduction to both material and structure.
5. Include mechanical property trade-offs where relevant.

### 5.7 Short-fiber shape-change project

Core topic:

* Short-fiber-reinforced shape-changing polymers.
* Heat-triggered shape memory.
* Moisture-responsive natural fibers.
* 3D printing.
* Fiber orientation, length degradation, voids, interface, and network effects.

Rules:

1. Emphasize that short natural fiber-based shape-change research is still relatively underexplored.
2. Avoid claiming complete novelty unless literature review supports it.
3. Connect response behavior to microstructure.
4. Include response speed, recovery ratio, recovery force, and durability when discussing performance.

### 5.8 Flame-retardant or heat-resistant 3D printing project using pineapple peel or natural fibers

Core topic:

* Natural fiber or pineapple peel-derived fillers.
* PLA-based 3D printing.
* Structural design for heat resistance or flame-retardant behavior.
* Infill, shell-core, low-density core, and gradient structures.

Rules:

1. Do not overstate flame-retardancy unless standardized flame tests support it.
2. Distinguish heat resistance, dimensional stability, residual strength, and flame retardancy.
3. When testing after heating, report deformation, delamination, residual strength, and dimensional retention separately.
4. Keep structure-property logic clear.

### 5.9 IoT heat box / agricultural thermal data

Core topic:

* Box temperature analysis.
* Outside sensor attached to outer surface.
* Inside sensor suspended inside, possibly not exactly at the center.
* Heating comes from indirect solar irradiation, not direct exposure.
* Equivalent thermal conductivity estimation depends strongly on sensor location.

Rules:

1. State sensor-position uncertainty clearly.
2. Do not overinterpret equivalent thermal conductivity.
3. Analyze multiple assumed inside sensor positions when needed.
4. Emphasize that future experiments should record exact sensor location.
5. Treat estimated thermal conductivity as an apparent or equivalent value, not an intrinsic material constant.

---

## 6. Data and file management rules

### 6.1 Raw data

Raw data must be preserved.

Rules:

1. Store original data in `data/raw/`.
2. Do not overwrite raw data.
3. Do not rename raw data destructively.
4. Do not edit original CSV, TXT, Excel, image, DSC, or measurement files.
5. If cleaning is needed, create processed files in `data/processed/`.

### 6.2 Processed data

Processed data must be reproducible.

Rules:

1. Store processed data in `data/processed/`.
2. Include the script that generated it.
3. Record filtering, smoothing, trimming, baseline correction, and assumptions.
4. Use clear file names.

Recommended naming:

```text
YYYY-MM-DD_project_sample_condition_processed.csv
YYYY-MM-DD_project_analysis_summary.md
YYYY-MM-DD_project_figure1_temperature_vs_speed.png
```

### 6.3 Outputs

Generated outputs should be stored as:

* Figures: `outputs/figures/`
* Tables: `outputs/tables/`
* Reports: `outputs/reports/`
* Presentations: `outputs/presentations/`

Figures should be reproducible from scripts.

### 6.4 Sensitive files

Do not store highly sensitive personal documents unless explicitly instructed.

Avoid committing:

* Passport scans.
* Residence card scans.
* Visa application PDFs.
* Bank information.
* Private identification documents.
* API keys.
* Passwords.
* Access tokens.
* `.env` files.

---

## 7. Coding and analysis rules

When writing scripts, Codex must:

1. Use clear file paths.
2. Avoid hard-coded absolute paths unless necessary.
3. Add comments for assumptions, not for obvious code.
4. Print or save key intermediate results.
5. Save figures and tables systematically.
6. Make the script rerunnable.
7. Avoid changing raw data.
8. Prefer modular functions for repeated analysis.
9. Include error handling where appropriate.
10. Use consistent units.

For Python analysis:

* Prefer `pandas`, `numpy`, and `matplotlib`.
* Avoid unnecessary complicated dependencies.
* Use one script per major analysis.
* Save output files with descriptive names.
* Record versions or package requirements if the analysis becomes important.

When analyzing experimental data, always report:

1. Input files.
2. Preprocessing.
3. Assumptions.
4. Calculation method.
5. Results.
6. Limitations.
7. Suggested next steps.

---

## 8. Manuscript writing rules

### 8.1 General structure

When revising manuscripts, Codex should preserve:

1. The user's core scientific logic.
2. The target section's role.
3. The connection with previous and next paragraphs.
4. The level of evidence.

Codex should not rewrite a paragraph into a completely different argument unless explicitly asked.

### 8.2 Scientific caution

Avoid unsupported claims.

Do not write:

```text
This proves that the interface was improved.
```

Prefer:

```text
This result suggests that the interfacial condition was improved under the present processing conditions.
```

Do not write:

```text
The thermal contact coefficient has no effect.
```

Prefer:

```text
The calculated temperature was only weakly affected by h_c within the examined range.
```

Do not write:

```text
The inside temperature directly gives the material thermal conductivity.
```

Prefer:

```text
The estimated value should be interpreted as an apparent thermal conductivity because it depends on the assumed sensor position and boundary conditions.
```

### 8.3 Revision output

When asked to revise text, Codex should usually provide:

1. Final replacement text.
2. Optional short explanation only if useful.
3. No unnecessary lecture.
4. No excessive alternatives unless requested.

---

## 9. Presentation rules

The user's preferred presentation style:

* White academic background.
* Simple, structured, technical layout.
* Dark gray or black main text.
* Red only for warnings, interpretation, key takeaway, or contrast.
* Avoid decorative dashboards.
* Avoid excessive icons.
* Avoid hero-style slides unless explicitly requested.
* Prefer clear technical story flow.
* Slide title should state the message, not only the topic.
* Figures should be visually aligned and explained by concise captions.
* Every slide should have one dominant message.

Presentation workflow:

1. Start from deck-level narrative.
2. Define audience and language.
3. Decide the evidence form before slide design.
4. Select slide archetype.
5. Build slide structure.
6. Add concise text.
7. Check consistency.
8. Track unresolved issues.

Language-specific slide rules:

* English slides: compact, defensible, conference-style.
* Japanese slides: slightly more explanatory, suitable for lectures and internal research discussions.
* Chinese slides: formal, concise, direct.

For high-stakes presentations, maintain a QA or refinement ledger.

---

## 10. Email and communication rules

### 10.1 Japanese professor emails

Style:

* Polite.
* Short.
* Direct.
* Natural.
* Avoid excessive keigo.
* Avoid unnecessary explanation.

Common phrases:

```text
いつも大変お世話になっております。
姜です。

承知いたしました。
ご確認いただき、ありがとうございました。
お手数をおかけいたしますが、何卒よろしくお願いいたします。
```

### 10.2 Japanese company emails

Style:

* Polite and clear.
* Technical details should be accurate but not too long.
* State test conditions and acceptance criteria clearly.
* Use cautious wording for requests.

When discussing experiments:

1. State sample geometry.
2. State temperature range.
3. State atmosphere.
4. State acceptable constraints.
5. State what the user can provide.
6. State what needs confirmation.

### 10.3 English academic emails

Style:

* Concise.
* Professional.
* Purpose first.
* Avoid excessive background.

### 10.4 Chinese project communication

Style:

* Structured.
* Direct.
* Technically complete.
* Suitable for research planning and proposal discussion.

---

## 11. Project memory workflow

### 11.1 Start of session

At the beginning of each Codex session, Codex should read:

1. `AGENTS.md`
2. `README.md`
3. `PLANS.md`
4. `notes/decision_logs/decision_log.md`
5. `notes/codex_mistakes/codex_mistakes.md`
6. Relevant project files

Then Codex should summarize:

1. Current repository purpose.
2. Active tasks.
3. Important rules.
4. Relevant project context.
5. Unresolved risks.

Codex must wait for the user's next instruction before making major file changes.

### 11.2 End of session

At the end of each major session, Codex should:

1. List modified files.
2. Summarize main changes.
3. Summarize decisions made.
4. Summarize unresolved issues.
5. Update `PLANS.md` if task status changed.
6. Add an entry to `notes/decision_logs/decision_log.md` if important decisions were made.
7. Add a session summary in `notes/session_summaries/`.
8. Update `notes/codex_mistakes/codex_mistakes.md` if a recurring mistake occurred.
9. Run `git status`.
10. Do not push until the user explicitly approves.

---

## 12. Git workflow

Standard workflow:

```bash
git pull
# work with Codex
git status
git add .
git commit -m "Update workspace context"
git push
```

Rules:

1. Pull before starting work.
2. Check status before modifying many files.
3. Commit meaningful changes.
4. Use concise commit messages.
5. Do not push without user approval if the user requested review first.
6. Do not commit sensitive files.
7. Do not force-push unless explicitly instructed.

Recommended commit messages:

```text
Initialize research workspace
Update AGENTS rules
Add manuscript writing rules
Add DSC analysis notes
Update ILSS reheating decision log
Add presentation workflow templates
```

---

## 13. Decision log rules

Important decisions must be recorded in:

```text
notes/decision_logs/decision_log.md
```

Record decisions when:

* A scientific interpretation is changed.
* A model assumption is selected.
* A figure style is finalized.
* A project direction is narrowed.
* A terminology rule is established.
* A recurring Codex mistake is corrected.
* A writing convention is confirmed.

Decision log format:

```markdown
### YYYY-MM-DD - Decision title

**Decision:**
Describe the decision.

**Reason:**
Explain why.

**Impact:**
Explain how this affects future work.
```

---

## 14. Codex mistake tracking

Recurring mistakes should be recorded in:

```text
notes/codex_mistakes/codex_mistakes.md
```

Common mistake categories:

1. Overclaiming DSC results.
2. Treating model estimates as measured values.
3. Making Japanese emails too long.
4. Using excessive keigo.
5. Ignoring sensor position uncertainty.
6. Changing submitted conference titles.
7. Overgeneralizing from one sample.
8. Forgetting to update decision logs.
9. Overwriting or editing raw data.
10. Creating visually decorative but academically weak slides.

Mistake format:

```markdown
### Mistake title

**Problem:**
Describe the mistake.

**Correction:**
Describe the correct behavior.

**Example:**
Give a concrete example if useful.
```

---

## 15. High-priority scientific wording rules

### 15.1 DSC

Use:

```text
broad endothermic behavior
high-softening or partial-melting temperature range
weak melting-related signal
low-crystallinity or quasi-amorphous behavior
```

Avoid unsupported:

```text
exact melting point
complete melting
confirmed crystalline melting
```

### 15.2 Heat-transfer model

Use:

```text
calculated surface temperature
within the assumptions of the model
sensitivity analysis
qualitative trend
limited influence within the examined range
```

Avoid unsupported:

```text
measured surface temperature
proved melting
h_c has no effect
exact prediction
```

### 15.3 Interface

Use:

```text
interfacial condition
interface-dominated failure
interface-related improvement
microstructure-guided interpretation
```

Avoid unsupported:

```text
interface alone caused the improvement
IFSS completely explains the macroscopic behavior
```

### 15.4 IoT heat box

Use:

```text
apparent thermal conductivity
equivalent thermal conductivity
sensor-position-dependent estimate
boundary-condition-dependent estimate
```

Avoid unsupported:

```text
intrinsic thermal conductivity
directly measured thermal conductivity
```

---

## 16. When Codex should ask for clarification

Codex should ask for clarification before proceeding when:

1. The target file is ambiguous.
2. The user asks to delete or overwrite important files.
3. The requested analysis requires missing raw data.
4. The experimental condition is unclear.
5. The output language is unclear.
6. The result could affect manuscript conclusions.
7. The task involves sensitive personal documents.
8. Multiple files have conflicting versions.
9. The user asks for a final submission-ready document but key information is missing.

Codex should not ask unnecessary questions when the next step is obvious and safe.

---

## 17. Default response style

Codex should respond in a focused, structured way.

Preferred format:

1. What was done.
2. Key result.
3. Files changed.
4. Issues or risks.
5. Next step.

Avoid:

* Long generic explanations.
* Repeating obvious information.
* Unrequested alternatives.
* Decorative language.
* Unclear summaries.

---

## 18. Absolute prohibitions

Codex must not:

1. Fabricate data.
2. Fabricate citations.
3. Fabricate experimental conditions.
4. Overwrite raw data.
5. Commit secrets or personal identification files.
6. Change submitted titles, IDs, or official information without instruction.
7. Treat model results as measurements.
8. Treat assumptions as facts.
9. Delete files without explicit instruction.
10. Push changes when the user asked for review before pushing.
