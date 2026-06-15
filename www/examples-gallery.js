(function () {
  "use strict";

  const TEST_SUMMARY = {
    pytest: "50 passed · 2 skipped",
    runSh: "27/27 PASS",
    testedAt: "2026-06-14",
  };

  const EXAMPLES = [
    { id: "01_quickstart_local", num: "01", category: "tutorial", title: "Local quickstart", desc: "URI Tree generation and validation without Docker.", cmd: "bash examples/01_quickstart_local/run.sh", uris: [], office: null },
    { id: "02_uri3_scan_http", num: "02", category: "agents", title: "HTTP agent scan", desc: "Health, capabilities, agent-card via uri3.", cmd: "uri3 scan http://localhost:8101", uris: ["http://"], office: "Site / API monitor" },
    { id: "03_ssh_remote_agent", num: "03", category: "agents", title: "Agent via Docker + SSH", desc: "Remote testenv: deploy, scan, container logs.", cmd: "make docker-testenv-up && uri3 scan ssh", uris: ["ssh://", "docker://"], office: null },
    { id: "04_nl2a_weather_map", num: "04", category: "agents", title: "NL → weather agent", desc: "Domain Pack + contract from NL prompt.", cmd: "bash examples/04_nl2a_weather_map/run.sh", uris: [], office: null },
    { id: "05_meta_repair", num: "05", category: "agents", title: "Agent contract repair", desc: "meta_agent repair on broken YAML.", cmd: "python -m meta_agent.cli repair examples/05_meta_repair/broken_agent.yaml", uris: [], office: null },
    { id: "06_orders_agent", num: "06", category: "agents", title: "Orders agent contract", desc: "YAML pattern — validation without runtime.", cmd: "python -m generator.validate examples/06_orders_agent", uris: [], office: "E-commerce · orders" },
    { id: "07_invoices_agent", num: "07", category: "agents", title: "Invoices agent prompt", desc: "NL → invoices_agent contract plan.", cmd: 'python -m meta_agent.cli plan "$(cat examples/07_invoices_agent/create_invoices_agent_prompt.txt)"', uris: [], office: "Office · invoices" },
    { id: "08_evolution", num: "08", category: "agents", title: "Evolution proposals", desc: "Validate auto-evolution proposals.", cmd: "make evolution-check", uris: [], office: null },
    { id: "09_run_agent_hypervisor", num: "09", category: "agents", title: "Agent lifecycle", desc: "run → supervise → stop via hypervisor.", cmd: "bash examples/09_run_agent_hypervisor/run.sh", uris: ["local://", "http://"], office: "Office process registry" },
    { id: "10_browser_operator", num: "10", category: "operator", title: "Browser (mock)", desc: "Open URL, read DOM, assert OK.", cmd: "bash examples/10_browser_operator/run.sh", uris: ["browser://"], office: "Portal · download web report" },
    { id: "11_playwright_browser", num: "11", category: "operator", title: "Playwright (real browser)", desc: "Chromium — login, click, extract.", cmd: "bash examples/11_playwright_browser/run.sh", uris: ["browser://"], office: "Online bank · portal form" },
    { id: "12_android_operator", num: "12", category: "operator", title: "Android (ADB / mock)", desc: "Screenshot, UI dump, tap — 2FA token.", cmd: "bash examples/12_android_operator/run.sh", uris: ["android://"], office: "Mobile token on phone" },
    { id: "13_pcwin_operator", num: "13", category: "operator", title: "Windows UIA (mock / UIA)", desc: "Focus ERP window, click controls.", cmd: "bash examples/13_pcwin_operator/run.sh", uris: ["pcwin://"], office: "Subiekt · ERP windows" },
    { id: "14_uri2ops_serve", num: "14", category: "operator", title: "uri2ops HTTP daemon", desc: "A2A + MCP + operation registry on :8791.", cmd: "bash examples/14_uri2ops_serve/run.sh", uris: ["browser://"], office: null },
    { id: "13_nl2uri_multi_uri_graph", num: "13", category: "workflow", title: "nl2uri — all modes", desc: "single / list / tree / task / graph from one NL prompt.", cmd: "bash examples/13_nl2uri_multi_uri_graph/run.sh", uris: ["browser://", "dom://"], office: "Office sentence → URI plan" },
    { id: "14_workflow_executor_mock", num: "14", category: "workflow", title: "Workflow executor", desc: "validate → plan → dry-run → approve.", cmd: "bash examples/14_workflow_executor_mock/run.sh", uris: ["browser://", "assertion://"], office: "Chain: portal → invoice → bank" },
    { id: "15_compact_uri_flow", num: "15", category: "workflow", title: "Compact URI flow", desc: "Short YAML → expand → run-flow.", cmd: "bash examples/15_compact_uri_flow/run.sh", uris: ["agent://", "browser://"], office: null },
    { id: "15_playwright_browser", num: "15", category: "workflow", title: "uri3 + Playwright", desc: "Workflow with a real browser.", cmd: "uri3 run-workflow examples/14_workflow_executor_mock/task_graph.yaml --approve --browser playwright", uris: ["browser://"], office: null },
    { id: "16_llm_graph_planner", num: "16", category: "workflow", title: "LLM graph planner", desc: "NL → workflow graph (rules / LLM).", cmd: "bash examples/16_llm_graph_planner/run.sh", uris: [], office: null },
    { id: "17_flow_vs_graph", num: "17", category: "workflow", title: "Flow vs graph", desc: "Compact flow vs expanded graph.", cmd: "bash examples/17_flow_vs_graph/run.sh", uris: [], office: null },
    { id: "18_llm_flow_planner", num: "18", category: "workflow", title: "LLM flow planner", desc: "NL → compact flow → run-flow.", cmd: "bash examples/18_llm_flow_planner/run.sh", uris: [], office: null },
    { id: "20_touri_capabilities", num: "20", category: "touri", title: "New capability (touri)", desc: "Manifest YAML → validate → call.", cmd: "bash examples/20_touri_capabilities/run.sh", uris: ["weather://", "echo://"], office: "Custom URI without full nl2a" },
    { id: "21_touri_voice", num: "21", category: "touri", title: "Voice → URI", desc: "STT / TTS / voice command as capability.", cmd: "bash examples/21_touri_voice/run.sh", uris: ["stt://", "voice://"], office: "Dictate office tasks" },
    { id: "22_markpact_weather", num: "22", category: "touri", title: "Markpact → touri", desc: "Capability and flow in Markdown.", cmd: "bash examples/22_markpact_weather/run.sh", uris: ["markpact://", "weather://"], office: null },
    { id: "23_nl_to_agent_tutorial", num: "23", category: "tutorial", title: "Tutorial NL → HTTP agent", desc: "From natural language to a working URL.", cmd: "bash examples/23_nl_to_agent_tutorial/run.sh", uris: ["browser://", "agent://"], office: "Full onboarding path" },
    { id: "30_golden_path", num: "30", category: "tutorial", title: "Golden path (15 min)", desc: "Agent → observe → diagnose → dashboard.", cmd: "bash examples/30_golden_path/run.sh", uris: [], office: "First day with Taskinity" },
    { id: "31_office_day", num: "31", category: "office", title: "Marta's office day", desc: "Supplier portal, ERP invoices, bank checkpoint and Android token in mock-first mode.", cmd: "bash examples/31_office_day/run.sh", uris: ["browser://", "pcwin://", "android://"], office: "Office · portal → invoices → bank → Android" },
  ];

  const CATEGORY_LABELS = {
    all: "All",
    agents: "Agents",
    operator: "Operator (Web · Android · Windows)",
    workflow: "Workflow",
    office: "Office",
    touri: "Touri / capability",
    tutorial: "Tutorial",
  };

  const OFFICE_CHAINS = [
    {
      title: "Download report from portal",
      steps: ["31_office_day", "10_browser_operator", "11_playwright_browser"],
      chat: "Go to the supplier portal and download the CSV report",
    },
    {
      title: "Invoice in ERP",
      steps: ["31_office_day", "07_invoices_agent", "13_pcwin_operator", "09_run_agent_hypervisor"],
      chat: "Issue yesterday's invoices and show a preview",
    },
    {
      title: "Bank + Android token",
      steps: ["11_playwright_browser", "12_android_operator", "31_office_day"],
      chat: "Prepare transfers and stop before 2FA",
    },
    {
      title: "From sentence to HTTP agent",
      steps: ["23_nl_to_agent_tutorial", "30_golden_path", "04_nl2a_weather_map"],
      chat: "Generate an agent and check health in the browser",
    },
  ];

  const gridEl = document.getElementById("examples-grid");
  const filterEl = document.getElementById("examples-filter");
  const chainsEl = document.getElementById("office-chains");
  const summaryEl = document.getElementById("test-summary");

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function findExample(id) {
    return EXAMPLES.find((e) => e.id === id);
  }

  function renderSummary() {
    if (!summaryEl) return;
    summaryEl.innerHTML = `
      <div class="examples-status-item ok"><strong>${escapeHtml(TEST_SUMMARY.runSh)}</strong> scripts/test-all-examples.sh</div>
      <div class="examples-status-item ok"><strong>${escapeHtml(TEST_SUMMARY.pytest)}</strong> pytest tests/examples</div>
      <div class="examples-status-item muted">Last run: ${escapeHtml(TEST_SUMMARY.testedAt)}</div>`;
  }

  function renderFilters() {
    if (!filterEl) return;
    filterEl.innerHTML = Object.entries(CATEGORY_LABELS)
      .map(
        ([key, label], i) =>
          `<button type="button" class="examples-filter-btn${i === 0 ? " is-active" : ""}" data-filter="${key}">${escapeHtml(label)}</button>`
      )
      .join("");
    filterEl.addEventListener("click", (ev) => {
      const btn = ev.target.closest(".examples-filter-btn");
      if (!btn) return;
      filterEl.querySelectorAll(".examples-filter-btn").forEach((b) => b.classList.remove("is-active"));
      btn.classList.add("is-active");
      renderGrid(btn.dataset.filter || "all");
    });
  }

  function renderGrid(filter) {
    if (!gridEl) return;
    const items = filter === "all" ? EXAMPLES : EXAMPLES.filter((e) => e.category === filter);
    gridEl.innerHTML = items
      .map(
        (ex) => `
      <article class="example-card" data-category="${escapeHtml(ex.category)}">
        <div class="example-card-head">
          <span class="example-num">ex ${escapeHtml(ex.num)}</span>
          <span class="example-pass" title="PASS in CI">✓ PASS</span>
        </div>
        <h3>${escapeHtml(ex.title)}</h3>
        <p class="example-desc">${escapeHtml(ex.desc)}</p>
        ${ex.office ? `<p class="example-office">Office: ${escapeHtml(ex.office)}</p>` : ""}
        ${ex.uris.length ? `<div class="example-uris">${ex.uris.map((u) => `<code>${escapeHtml(u)}</code>`).join("")}</div>` : ""}
        <pre class="integration-snippet example-cmd">${escapeHtml(ex.cmd)}</pre>
        <div class="example-card-foot">
          <button type="button" class="btn btn-ghost example-copy" data-cmd="${escapeHtml(ex.cmd)}">Copy command</button>
          <span class="example-path">examples/${escapeHtml(ex.id)}/</span>
        </div>
      </article>`
      )
      .join("");
  }

  function renderOfficeChains() {
    if (!chainsEl) return;
    chainsEl.innerHTML = OFFICE_CHAINS.map(
      (chain) => `
      <article class="office-chain-card">
        <h3>${escapeHtml(chain.title)}</h3>
        <blockquote class="office-chat-quote">${escapeHtml(chain.chat)}</blockquote>
        <ol class="office-flow">
          ${chain.steps
            .map((id) => {
              const ex = findExample(id);
              return ex ? `<li><strong>${escapeHtml(ex.title)}</strong> — <code>examples/${escapeHtml(ex.id)}/</code></li>` : "";
            })
            .join("")}
        </ol>
      </article>`
    ).join("");
  }

  document.addEventListener("click", (ev) => {
    const btn = ev.target.closest(".example-copy");
    if (!btn) return;
    const cmd = btn.dataset.cmd || "";
    navigator.clipboard.writeText(cmd).then(
      () => {
        const prev = btn.textContent;
        btn.textContent = "Copied!";
        setTimeout(() => {
          btn.textContent = prev;
        }, 1200);
      },
      () => {
        btn.textContent = "Copy failed";
      }
    );
  });

  renderSummary();
  renderFilters();
  renderGrid("all");
  renderOfficeChains();
})();
