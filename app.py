<div style="max-width:1000px; margin:0 auto; padding:20px; font-family:Arial, sans-serif;">
  <h2 style="margin-bottom:6px;">TMK Lesson Plan Builder</h2>
  <p style="margin-top:0; margin-bottom:16px;">
    Paste copied planner text from the TMK Workroom, then build and print a formal lesson plan.
  </p>

  <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:12px;">
    <div>
      <label for="lessonTitle" style="display:block; font-weight:bold; margin-bottom:4px;">Lesson title</label>
      <input id="lessonTitle" type="text" placeholder="e.g. TMK Lesson Plan"
        style="width:100%; padding:10px; border:1px solid #bfbfbf; border-radius:4px; box-sizing:border-box;">
    </div>
    <div>
      <label for="lessonDate" style="display:block; font-weight:bold; margin-bottom:4px;">Date</label>
      <input id="lessonDate" type="text" placeholder="e.g. 5 April 2026"
        style="width:100%; padding:10px; border:1px solid #bfbfbf; border-radius:4px; box-sizing:border-box;">
    </div>
    <div>
      <label for="lessonClass" style="display:block; font-weight:bold; margin-bottom:4px;">Class / group</label>
      <input id="lessonClass" type="text" placeholder="e.g. Year 4 intervention"
        style="width:100%; padding:10px; border:1px solid #bfbfbf; border-radius:4px; box-sizing:border-box;">
    </div>
    <div>
      <label for="lessonDurationOverride" style="display:block; font-weight:bold; margin-bottom:4px;">Override lesson length (optional)</label>
      <input id="lessonDurationOverride" type="text" placeholder="Leave blank to use copied planner value"
        style="width:100%; padding:10px; border:1px solid #bfbfbf; border-radius:4px; box-sizing:border-box;">
    </div>
  </div>

  <label for="lessonText" style="display:block; font-weight:bold; margin-bottom:4px;">Paste TMK planner text</label>
  <textarea id="lessonText" placeholder="Paste copied text from the Streamlit app here..."
    style="width:100%; min-height:300px; padding:12px; border:1px solid #bfbfbf; border-radius:4px; box-sizing:border-box; line-height:1.4; resize:vertical;"></textarea>

  <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:12px;">
    <div>
      <label for="teacherNotes" style="display:block; font-weight:bold; margin-bottom:4px;">Teacher notes</label>
      <textarea id="teacherNotes" placeholder="Add reminders, follow-up points, resources needed..."
        style="width:100%; min-height:100px; padding:10px; border:1px solid #bfbfbf; border-radius:4px; box-sizing:border-box; resize:vertical;"></textarea>
    </div>
    <div>
      <label for="assessmentNextSteps" style="display:block; font-weight:bold; margin-bottom:4px;">Assessment / next steps</label>
      <textarea id="assessmentNextSteps" placeholder="What will you look for? What comes next?"
        style="width:100%; min-height:100px; padding:10px; border:1px solid #bfbfbf; border-radius:4px; box-sizing:border-box; resize:vertical;"></textarea>
    </div>
  </div>

  <div style="margin-top:14px; display:flex; gap:10px; flex-wrap:wrap;">
    <button onclick="buildPlan()" style="padding:10px 16px; border:none; border-radius:4px; cursor:pointer;">Build lesson plan</button>
    <button onclick="window.print()" style="padding:10px 16px; border:none; border-radius:4px; cursor:pointer;">Print</button>
    <button onclick="clearPlan()" style="padding:10px 16px; border:none; border-radius:4px; cursor:pointer;">Clear</button>
  </div>

  <hr style="margin:22px 0;">

  <div id="printArea" style="background:#fff; border:1px solid #d0d0d0; padding:20px; border-radius:4px;">
    <h3 style="margin-top:0;">Preview</h3>
    <p style="margin-bottom:0; color:#666;">Your formal lesson plan will appear here.</p>
  </div>
</div>

<script>
function escapeHtml(text) {
  return (text || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function normalize(raw) {
  return raw.replace(/\r\n/g, "\n").replace(/\r/g, "\n").trim();
}

function getSection(raw, heading, nextHeadings) {
  const h = heading.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const next = nextHeadings.map(x => x.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join("|");
  const regex = new RegExp(h + "\\s*([\\s\\S]*?)(?=\\n(?:" + next + ")\\b|$)", "i");
  const match = raw.match(regex);
  return match ? match[1].trim() : "";
}

function getLineAfterHeading(raw, heading, nextHeadings) {
  const section = getSection(raw, heading, nextHeadings);
  if (!section) return "";
  const lines = section.split("\n").map(x => x.trim()).filter(Boolean);
  return lines.length ? lines[0] : "";
}

function getOpenStageSequence(raw, nextHeadings) {
  const regex = /([A-Za-z0-9×+\-–—()\/ ]+?)\s+sequence\s*/i;
  const lines = raw.split("\n");
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (regex.test(line)) {
      const heading = line;
      const next = nextHeadings.map(x => x.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join("|");
      const escapedHeading = heading.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const sectionRegex = new RegExp(escapedHeading + "\\s*([\\s\\S]*?)(?=\\n(?:" + next + ")\\b|$)", "i");
      const match = raw.match(sectionRegex);
      return {
        heading: heading,
        body: match ? match[1].trim() : ""
      };
    }
  }
  return {
    heading: "Stage sequence",
    body: ""
  };
}

function textToParagraphs(text) {
  if (!text || !text.trim()) return "<p class='compact-p' style='margin:0;'>—</p>";

  const lines = text
    .split(/\n+/)
    .map(x => x.trim())
    .filter(Boolean);

  return lines.map(line =>
    "<p class='compact-p'>" + escapeHtml(line) + "</p>"
  ).join("");
}

function linesToBullets(text) {
  if (!text || !text.trim()) return "<p class='compact-p' style='margin:0;'>—</p>";

  const items = text
    .split(/\n+/)
    .map(x => x.trim())
    .filter(Boolean);

  return "<ul class='compact-list'>" +
    items.map(item =>
      "<li>" + escapeHtml(item.replace(/^[-•]\s*/, "")) + "</li>"
    ).join("") +
    "</ul>";
}

function numberedToList(text) {
  if (!text || !text.trim()) return "<p class='compact-p' style='margin:0;'>—</p>";

  const items = text
    .split(/\n+/)
    .map(x => x.trim())
    .filter(Boolean);

  return "<ol class='compact-list compact-ol'>" +
    items.map(item =>
      "<li>" + escapeHtml(item.replace(/^\d+\.\s*/, "")) + "</li>"
    ).join("") +
    "</ol>";
}

function extractLabeledGroups(text, labels) {
  if (!text || !text.trim()) return "";
  const escaped = labels.map(l => l.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
  const regex = new RegExp("(^|\\n)(" + escaped.join("|") + ")\\s*\\n([\\s\\S]*?)(?=\\n(?:" + escaped.join("|") + ")\\s*\\n|$)", "g");
  const groups = [];
  let match;
  while ((match = regex.exec(text)) !== null) {
    groups.push({
      label: match[2].trim(),
      body: match[3].trim()
    });
  }
  return groups;
}

function renderGroupedBlocks(groups) {
  if (!groups || !groups.length) return "<p class='compact-p' style='margin:0;'>—</p>";
  return groups.map(group => `
    <div class="lesson-section inner-box">
      <div class="inner-box-heading"><strong>${escapeHtml(group.label)}</strong></div>
      <div class="inner-box-body">${linesToBullets(group.body)}</div>
    </div>
  `).join("");
}

function renderPatternBlocks(text) {
  if (!text || !text.trim()) return "<p class='compact-p' style='margin:0;'>—</p>";
  const blocks = text.split(/\n\s*\n/).map(x => x.trim()).filter(Boolean);
  return blocks.map(block => {
    const lines = block.split("\n").map(x => x.trim()).filter(Boolean);
    const title = lines[0] || "";
    const body = lines.slice(1).join(" ");
    return `
      <div class="lesson-section inner-box">
        <div class="inner-box-heading"><strong>${escapeHtml(title)}</strong></div>
        <div class="inner-box-body">${body ? "<p class='compact-p'>" + escapeHtml(body) + "</p>" : "<p class='compact-p' style='margin:0;'>—</p>"}</div>
      </div>
    `;
  }).join("");
}

function renderSceBlock(title, body) {
  return `
    <div class="lesson-section sce-box">
      <div class="inner-box-heading"><strong>${escapeHtml(title)}</strong></div>
      <div class="inner-box-body">${textToParagraphs(body)}</div>
    </div>
  `;
}

function buildPlan() {
  const raw = normalize(document.getElementById("lessonText").value);
  const customTitle = document.getElementById("lessonTitle").value.trim();
  const lessonDate = document.getElementById("lessonDate").value.trim();
  const lessonClass = document.getElementById("lessonClass").value.trim();
  const durationOverride = document.getElementById("lessonDurationOverride").value.trim();
  const teacherNotes = document.getElementById("teacherNotes").value.trim();
  const assessmentNextSteps = document.getElementById("assessmentNextSteps").value.trim();
  const printArea = document.getElementById("printArea");

  if (!raw) {
    printArea.innerHTML = "<h3 style='margin-top:0;'>Preview</h3><p>Please paste your planner text first.</p>";
    return;
  }

  const headings = [
    "Selected product",
    "Structural dependency reminder",
    "Lesson aim",
    "Suggested lesson length",
    "TMK stage patterns to use in this lesson",
    "Explanation sequence",
    "Teacher model",
    "Teacher explanation sentence",
    "Inverse connection",
    "Check for understanding",
    "Teach now vocabulary",
    "Teacher prompt bank",
    "Introduce if needed",
    "Example questions",
    "Delay vocabulary",
    "Support / Core / Extension",
    "Teaching warning",
    "Teacher quick summary"
  ];

  const selectedProduct = getLineAfterHeading(raw, "Selected product", headings.filter(h => h !== "Selected product"));
  const structuralDependency = getSection(raw, "Structural dependency reminder", headings.filter(h => h !== "Structural dependency reminder"));
  const lessonAim = getSection(raw, "Lesson aim", headings.filter(h => h !== "Lesson aim"));
  const suggestedLessonLength = getSection(raw, "Suggested lesson length", headings.filter(h => h !== "Suggested lesson length"));
  const patterns = getSection(raw, "TMK stage patterns to use in this lesson", headings.filter(h => h !== "TMK stage patterns to use in this lesson"));
  const stageSequence = getOpenStageSequence(raw, headings);
  const explanationSequence = getSection(raw, "Explanation sequence", headings.filter(h => h !== "Explanation sequence"));
  const teacherModel = getSection(raw, "Teacher model", headings.filter(h => h !== "Teacher model"));
  const teacherExplanationSentence = getSection(raw, "Teacher explanation sentence", headings.filter(h => h !== "Teacher explanation sentence"));
  const inverseConnection = getSection(raw, "Inverse connection", headings.filter(h => h !== "Inverse connection"));
  const checkForUnderstanding = getSection(raw, "Check for understanding", headings.filter(h => h !== "Check for understanding"));
  const teachNowVocabulary = getSection(raw, "Teach now vocabulary", headings.filter(h => h !== "Teach now vocabulary"));
  const teacherPromptBank = getSection(raw, "Teacher prompt bank", headings.filter(h => h !== "Teacher prompt bank"));
  const introduceIfNeeded = getSection(raw, "Introduce if needed", headings.filter(h => h !== "Introduce if needed"));
  const exampleQuestions = getSection(raw, "Example questions", headings.filter(h => h !== "Example questions"));
  const delayVocabulary = getSection(raw, "Delay vocabulary", headings.filter(h => h !== "Delay vocabulary"));
  const supportCoreExtension = getSection(raw, "Support / Core / Extension", headings.filter(h => h !== "Support / Core / Extension"));
  const teachingWarning = getSection(raw, "Teaching warning", headings.filter(h => h !== "Teaching warning"));
  const teacherQuickSummary = getSection(raw, "Teacher quick summary", headings.filter(h => h !== "Teacher quick summary"));

  const promptGroups = extractLabeledGroups(teacherPromptBank, [
    "Entry prompts",
    "Pattern prompts",
    "Inverse prompts",
    "Extension prompts"
  ]);

  const questionGroups = extractLabeledGroups(exampleQuestions, [
    "Build the product",
    "Quantifier-build and digit-sum",
    "Rise/fall and sequence",
    "Inverse questions",
    "Explain"
  ]);

  const sceGroups = extractLabeledGroups(supportCoreExtension, [
    "Support",
    "Core",
    "Extension"
  ]);

  const finalDuration = durationOverride || suggestedLessonLength || "—";
  const finalTitle = customTitle || "TMK Lesson Plan";

  printArea.innerHTML = `
    <div class="formal-plan">
      <div class="lesson-section plan-title">
        <h1>${escapeHtml(finalTitle)}</h1>
        <div class="plan-subtitle">Formal teacher lesson plan</div>
      </div>

      <table class="lesson-section meta-table">
        <tr>
          <td><strong>Date</strong><br>${escapeHtml(lessonDate) || "—"}</td>
          <td><strong>Class / group</strong><br>${escapeHtml(lessonClass) || "—"}</td>
          <td><strong>Duration</strong><br>${escapeHtml(finalDuration) || "—"}</td>
          <td><strong>Selected product</strong><br>${escapeHtml(selectedProduct) || "—"}</td>
        </tr>
      </table>

      <div class="lesson-section outer-section">
        <div class="outer-heading"><strong>Structural dependency reminder</strong></div>
        <div class="outer-body">${textToParagraphs(structuralDependency)}</div>
      </div>

      <div class="lesson-section outer-section">
        <div class="outer-heading"><strong>Lesson aim</strong></div>
        <div class="outer-body">${textToParagraphs(lessonAim)}</div>
      </div>

      <div class="lesson-section outer-section">
        <div class="outer-heading"><strong>TMK stage patterns to use in this lesson</strong></div>
        <div class="outer-body">${renderPatternBlocks(patterns)}</div>
      </div>

      <div class="lesson-section outer-section">
        <div class="outer-heading"><strong>${escapeHtml(stageSequence.heading || "Stage sequence")}</strong></div>
        <div class="outer-body">${textToParagraphs(stageSequence.body)}</div>
      </div>

      <div class="lesson-section outer-section">
        <div class="outer-heading"><strong>Explanation sequence</strong></div>
        <div class="outer-body">${numberedToList(explanationSequence)}</div>
      </div>

      <div class="two-col">
        <div class="lesson-section outer-section outer-section-no-bottom-right">
          <div class="outer-heading"><strong>Teacher model</strong></div>
          <div class="outer-body">${linesToBullets(teacherModel)}</div>
        </div>
        <div class="lesson-section outer-section">
          <div class="outer-heading"><strong>Teacher explanation sentence</strong></div>
          <div class="outer-body">${textToParagraphs(teacherExplanationSentence)}</div>
        </div>
      </div>

      <div class="lesson-section outer-section">
        <div class="outer-heading"><strong>Inverse connection</strong></div>
        <div class="outer-body">${linesToBullets(inverseConnection)}</div>
      </div>

      <div class="lesson-section outer-section">
        <div class="outer-heading"><strong>Check for understanding</strong></div>
        <div class="outer-body">${textToParagraphs(checkForUnderstanding)}</div>
      </div>

      <div class="two-col">
        <div class="lesson-section outer-section outer-section-no-bottom-right">
          <div class="outer-heading"><strong>Teach now vocabulary</strong></div>
          <div class="outer-body">${linesToBullets(teachNowVocabulary)}</div>
        </div>
        <div class="lesson-section outer-section">
          <div class="outer-heading"><strong>Introduce if needed</strong></div>
          <div class="outer-body">${linesToBullets(introduceIfNeeded)}</div>
        </div>
      </div>

      <div class="lesson-section outer-section">
        <div class="outer-heading"><strong>Teacher prompt bank</strong></div>
        <div class="outer-body">${renderGroupedBlocks(promptGroups)}</div>
      </div>

      <div class="lesson-section outer-section">
        <div class="outer-heading"><strong>Example questions</strong></div>
        <div class="outer-body">${renderGroupedBlocks(questionGroups)}</div>
      </div>

      <div class="lesson-section outer-section">
        <div class="outer-heading"><strong>Delay vocabulary</strong></div>
        <div class="outer-body">${linesToBullets(delayVocabulary)}</div>
      </div>

      <div class="lesson-section outer-section">
        <div class="outer-heading"><strong>Support / Core / Extension</strong></div>
        <div class="outer-body">
          <div class="three-col">
            ${sceGroups && sceGroups.length ? sceGroups.map(group => renderSceBlock(group.label, group.body)).join("") : renderSceBlock("Support", "") + renderSceBlock("Core", "") + renderSceBlock("Extension", "")}
          </div>
        </div>
      </div>

      <div class="lesson-section outer-section">
        <div class="outer-heading"><strong>Teaching warning</strong></div>
        <div class="outer-body">${textToParagraphs(teachingWarning)}</div>
      </div>

      <div class="lesson-section outer-section">
        <div class="outer-heading"><strong>Teacher quick summary</strong></div>
        <div class="outer-body">${textToParagraphs(teacherQuickSummary)}</div>
      </div>

      <div class="two-col">
        <div class="lesson-section outer-section outer-section-no-bottom-right">
          <div class="outer-heading"><strong>Teacher notes</strong></div>
          <div class="outer-body notes-box">${textToParagraphs(teacherNotes)}</div>
        </div>
        <div class="lesson-section outer-section">
          <div class="outer-heading"><strong>Assessment / next steps</strong></div>
          <div class="outer-body notes-box">${textToParagraphs(assessmentNextSteps)}</div>
        </div>
      </div>
    </div>
  `;
}

function clearPlan() {
  document.getElementById("lessonTitle").value = "";
  document.getElementById("lessonDate").value = "";
  document.getElementById("lessonClass").value = "";
  document.getElementById("lessonDurationOverride").value = "";
  document.getElementById("lessonText").value = "";
  document.getElementById("teacherNotes").value = "";
  document.getElementById("assessmentNextSteps").value = "";
  document.getElementById("printArea").innerHTML = "<h3 style='margin-top:0;'>Preview</h3><p style='margin-bottom:0; color:#666;'>Your formal lesson plan will appear here.</p>";
}
</script>

<style>
.formal-plan {
  border: 1.5px solid #222;
  color: #222;
  background: #fff;
}

.plan-title {
  padding: 12px 14px;
  border-bottom: 1px solid #222;
}

.plan-title h1 {
  margin: 0 0 4px 0;
  font-size: 24px;
  line-height: 1.15;
}

.plan-subtitle {
  font-size: 12px;
  line-height: 1.2;
}

.meta-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}

.meta-table td {
  border-right: 1px solid #222;
  border-bottom: 1px solid #222;
  padding: 8px 10px;
  vertical-align: top;
  font-size: 12px;
  line-height: 1.25;
}

.meta-table td:last-child {
  border-right: none;
}

.outer-section {
  border-bottom: 1px solid #222;
}

.outer-section-no-bottom-right {
  border-right: 1px solid #222;
}

.outer-heading {
  padding: 7px 9px;
  background: #f4f4f4;
  border-bottom: 1px solid #222;
  font-size: 12px;
  line-height: 1.2;
}

.outer-body {
  padding: 8px 10px;
  font-size: 12px;
  line-height: 1.3;
}

.inner-box {
  border: 1px solid #222;
  margin-bottom: 8px;
}

.inner-box-heading {
  padding: 6px 8px;
  background: #f7f7f7;
  border-bottom: 1px solid #222;
  font-size: 12px;
  line-height: 1.2;
}

.inner-box-body {
  padding: 8px;
  font-size: 12px;
  line-height: 1.3;
}

.sce-box {
  border: 1px solid #222;
  min-height: 100px;
}

.two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
}

.three-col {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 8px;
}

.compact-p {
  margin: 3px 0;
  line-height: 1.28;
  font-size: 12px;
}

.compact-list {
  margin: 3px 0;
  padding-left: 18px;
  font-size: 12px;
  line-height: 1.28;
}

.compact-list li {
  margin-bottom: 3px;
}

.compact-ol {
  padding-left: 20px;
}

.notes-box {
  min-height: 90px;
}

.lesson-section {
  break-inside: avoid;
  page-break-inside: avoid;
}

@media (max-width: 800px) {
  .two-col,
  .three-col {
    grid-template-columns: 1fr !important;
  }

  .outer-section-no-bottom-right {
    border-right: none;
  }
}

@page {
  size: A4;
  margin: 10mm;
}

@media print {
  body * {
    visibility: hidden;
  }

  #printArea, #printArea * {
    visibility: visible;
  }

  #printArea {
    position: absolute;
    left: 0;
    top: 0;
    width: 100% !important;
    max-width: 100% !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
    background: #fff !important;
    box-shadow: none !important;
  }

  .formal-plan {
    border: 1.2px solid #222;
  }

  table, tr, td, th,
  ul, ol,
  .lesson-section,
  .inner-box,
  .sce-box {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
  }

  h1, h2, h3, h4 {
    page-break-after: avoid !important;
    break-after: avoid !important;
  }

  .compact-p,
  .compact-list,
  .compact-list li,
  .outer-body,
  .inner-box-body,
  .meta-table td {
    font-size: 11px !important;
    line-height: 1.22 !important;
  }

  .outer-heading,
  .inner-box-heading,
  .plan-subtitle {
    font-size: 11px !important;
  }

  .plan-title h1 {
    font-size: 20px !important;
  }
}
</style>
