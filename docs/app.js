const sample = [
  { first: "Ava Example", position: "Senior Product Manager", company: "Example Labs", url: "https://example.invalid/ava" },
  { first: "Noah Example", position: "Machine Learning Engineer", company: "Example AI", url: "" },
  { first: "Mina Example", position: "Technical Recruiter", company: "Example Talent", url: "https://example.invalid/mina" },
  { first: "Omid Example", position: "Backend Software Engineer", company: "Example Systems", url: "https://example.invalid/omid" },
  { first: "Sara Example", position: "Community Founder", company: "Example Studio", url: "" }
];
const categoryPoints = { Product: 5, "Developer": 4, "AI / Data": 4, "HR / Recruiter": 3, Other: 1 };
const recommendations = { Product: "Prioritize outreach", "AI / Data": "Prioritize outreach", Developer: "Explore collaboration", "HR / Recruiter": "Keep warm", Other: "Review manually" };
function categorizeTitle(value) {
  const title = String(value ?? "").trim().toLowerCase();
  if (!title) return "Other";
  if (["hr", "recruiter", "talent", "people", "human resources"].some(k => title.includes(k))) return "HR / Recruiter";
  if (["machine learning", "deep learning", "data scientist", "data analyst", "data engineer", "ai engineer", "ml engineer", "artificial intelligence"].some(k => title.includes(k)) || /^(ai |ml |data )/.test(title)) return "AI / Data";
  if (["product manager", "head of product", "product owner", "product lead", "product"].some(k => title.includes(k)) || title === "pm") return "Product";
  if (["developer", "engineer", "cto", "backend", "frontend", "fullstack", "full stack", "software", "programmer"].some(k => title.includes(k))) return "Developer";
  return "Other";
}
function analyze(records) {
  return records.map(record => {
    const category = categorizeTitle(record.position);
    const score = (categoryPoints[category] || 1) + [record.company, record.position, record.url].filter(x => String(x || "").trim()).length;
    return { ...record, category, score, priority: score >= 7 ? "High" : score >= 5 ? "Medium" : "Low", recommendation: recommendations[category] || "Review manually" };
  });
}
if (typeof module !== "undefined") module.exports = { categorizeTitle, analyze, sample };
if (typeof document !== "undefined") {
  const rows = analyze(sample), body = document.querySelector("#records"), search = document.querySelector("#search"), category = document.querySelector("#category"), priority = document.querySelector("#priority"), count = document.querySelector("#result-count"), empty = document.querySelector("#empty"), insights = document.querySelector("#insights");
  const groups = [...new Set(rows.map(r => r.category))].sort();
  for (const group of groups) { const option = document.createElement("option"); option.value = group; option.textContent = group; category.append(option); }
  document.querySelector("#total-count").textContent = rows.length;
  document.querySelector("#category-count").textContent = groups.length;
  function render() {
    const query = search.value.trim().toLocaleLowerCase();
    const visible = rows.filter(r => [r.first, r.position, r.company].join(" ").toLocaleLowerCase().includes(query) && (category.value === "all" || r.category === category.value) && (priority.value === "all" || r.priority === priority.value));
    body.replaceChildren();
    for (const r of visible) {
      const tr = document.createElement("tr");
      const person = document.createElement("td"); const name = document.createElement("span"); name.className = "person"; name.textContent = r.first; const title = document.createElement("small"); title.textContent = r.position; person.append(name, title);
      const group = document.createElement("td"); const badge = document.createElement("span"); badge.className = "group"; badge.textContent = r.category; group.append(badge);
      const rec = document.createElement("td"); rec.className = "recommendation"; rec.textContent = r.recommendation;
      const score = document.createElement("td"); score.className = "score"; score.textContent = `${r.score} / 8`;
      const band = document.createElement("td"); const label = document.createElement("span"); label.className = `band ${r.priority.toLowerCase()}`; label.textContent = r.priority; const note = document.createElement("small"); note.className = "review-note"; note.textContent = "Human review required"; band.append(label, note);
      tr.append(person, group, rec, score, band); body.append(tr);
    }
    count.textContent = `${visible.length} ${visible.length === 1 ? "record" : "records"}`; empty.hidden = visible.length > 0;
    const tally = groups.map(g => `${g}: ${visible.filter(r => r.category === g).length}`).filter(x => !x.endsWith(": 0"));
    insights.replaceChildren(...(tally.length ? tally : ["No groups in this view"]).map(text => { const chip = document.createElement("span"); chip.className = "insight-chip"; chip.textContent = text; return chip; }));
  }
  [search, category, priority].forEach(control => control.addEventListener("input", render));
  document.querySelector("#reset").addEventListener("click", () => { search.value = ""; category.value = "all"; priority.value = "all"; render(); search.focus(); });
  render();
}

