const API = "";

const QUICK_PROMPTS = [
  {
    label: "WWW · CSV report",
    prompt:
      "Wejdź na stronę dostawcy, pobierz raport CSV za ten miesiąc i zapisz w rozliczeniach.",
  },
  {
    label: "Portal · ZUS form",
    prompt:
      "Zaloguj się do portalu klienta, uzupełnij formularz ZUS i wyślij — najpierw pokaż podgląd.",
  },
  {
    label: "Subiekt · ERP window",
    prompt: "Otwórz Subiekta, wklej dane z Excela do faktury i zapisz jako szkic.",
  },
  {
    label: "Invoices · WooCommerce",
    prompt:
      "Wystaw faktury za zamówienia z WooCommerce, pokaż listę do akceptacji i wyślij tylko zatwierdzone.",
  },
  {
    label: "Bank · batch transfer",
    prompt: "Przygotuj przelewy do dostawców z listy — zatrzymaj się przed autoryzacją.",
  },
  {
    label: "Android · 2FA token",
    prompt: "Bank czeka na potwierdzenie w aplikacji — pokaż mi ekran telefonu.",
  },
];

const INTRO_MARKDOWN =
  "## Taskinity Chat\n\n" +
  "NL → URI → result in one view. Pick a quick prompt or type your own command.\n\n" +
  "Paste **one command per line** for batch planning:\n\n" +
  "```bash\n" +
  "pokaż proces agenta weather-map-agent.local\n" +
  "zdiagnozuj agenta invoices-agent.local\n" +
  "rob rzuty ekranów stron softreck.com prototypowanie.pl www co 5 minut do folderu usera ~/images/\n" +
  "```";

const conversationLog = [];
let isBusy = false;

const messagesEl = document.getElementById("messages");
const form = document.getElementById("chat-form");
const promptEl = document.getElementById("prompt");
const dryRunEl = document.getElementById("dry-run");
const speakSummaryEl = document.getElementById("speak-summary");
const sendBtn = document.getElementById("send-btn");
const statusPill = document.getElementById("status-pill");
const apiDetail = document.getElementById("api-detail");
const refreshBtn = document.getElementById("refresh-btn");
const copyChatBtn = document.getElementById("copy-chat-btn");
const clearChatBtn = document.getElementById("clear-chat-btn");
const quickPromptsEl = document.getElementById("quick-prompts");
const agentListEl = document.getElementById("agent-list");
const eventListEl = document.getElementById("event-list");
const micBtn = document.getElementById("mic-btn");
const voiceEngineEl = document.getElementById("voice-engine");

let eventStream = null;
let mediaRecorder = null;
let mediaChunks = [];

if (window.marked) {
  marked.setOptions({ breaks: true, gfm: true });
}

function renderMarkdown(text) {
  if (window.marked && window.DOMPurify) {
    const raw = marked.parse(text || "");
    return DOMPurify.sanitize(raw, { USE_PROFILES: { html: true } });
  }
  return renderBasicMarkdown(text || "");
}

function renderBasicMarkdown(text) {
  const blocks = [];
  const pattern = /```(\w+)?\n([\s\S]*?)```/g;
  let lastIndex = 0;
  let match;

  while ((match = pattern.exec(text)) !== null) {
    if (match.index > lastIndex) {
      blocks.push(renderBasicText(text.slice(lastIndex, match.index)));
    }
    blocks.push(`<pre><code>${escapeHtml(match[2].trim())}</code></pre>`);
    lastIndex = pattern.lastIndex;
  }
  if (lastIndex < text.length) {
    blocks.push(renderBasicText(text.slice(lastIndex)));
  }
  return blocks.join("");
}

function renderBasicText(text) {
  return text
    .split(/\n{2,}/)
    .map((paragraph) => {
      const lines = paragraph.trim().split("\n");
      if (!paragraph.trim()) return "";
      if (lines[0].startsWith("## ")) {
        return `<h2>${inlineMarkdown(lines[0].slice(3))}</h2>`;
      }
      if (lines.every((line) => line.startsWith("- "))) {
        return `<ul>${lines.map((line) => `<li>${inlineMarkdown(line.slice(2))}</li>`).join("")}</ul>`;
      }
      return `<p>${inlineMarkdown(lines.join("\n")).replace(/\n/g, "<br>")}</p>`;
    })
    .join("");
}

function inlineMarkdown(text) {
  return escapeHtml(text)
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
}

function extractUri(text) {
  const match = text.match(/([a-z][a-z0-9+.-]*:\/\/[^\s`'")\]:]+(?:\/[^\s`'")\]]*)?)/i);
  return match ? match[1].replace(/[.,;]+$/, "") : null;
}

function extractUriFromCode(text) {
  const trimmed = (text || "").trim();
  if (!trimmed) return null;
  const direct = trimmed.match(/^([a-z][a-z0-9+.-]*:\/\/[^\s`'")\]:]+(?:\/[^\s`'")\]]*)?)/i);
  if (direct) return direct[1].replace(/[.,;]+$/, "");
  for (const line of trimmed.split("\n")) {
    const candidate = line.trim();
    const uri = extractUri(candidate);
    if (uri && (candidate === uri || candidate.endsWith(uri))) return uri;
  }
  return extractUri(trimmed);
}

function extractUrisFromCodeBlocks(root) {
  const uris = [];
  root.querySelectorAll("pre > code, code.uri-link").forEach((codeEl) => {
    const uri = extractUriFromCode(codeEl.textContent || "");
    if (uri) uris.push(uri);
  });
  return uris;
}

function collectUris(data) {
  if (!data || typeof data !== "object") return [];
  const uris = [];
  if (Array.isArray(data.actions)) {
    data.actions.forEach((action) => {
      uris.push(...collectUris(action));
    });
  }
  for (const key of ["planned_uris", "uris"]) {
    if (Array.isArray(data[key])) uris.push(...data[key]);
  }
  if (typeof data.uri === "string") uris.push(data.uri);
  if (Array.isArray(data.actions)) {
    data.actions.forEach((action) => {
      if (action && typeof action.uri === "string") uris.push(action.uri);
    });
  }
  return [...new Set(uris.filter((uri) => typeof uri === "string" && uri.includes("://")))];
}

function looksLikeUri(text) {
  return /[a-z][a-z0-9+.-]*:\/\//i.test(text.trim());
}

function htmlToPlainText(html) {
  const div = document.createElement("div");
  div.innerHTML = html;
  return (div.innerText || div.textContent || "").trim();
}

function buildConversationMarkdown() {
  const lines = ["# Taskinity Chat", ""];
  conversationLog.forEach((entry) => {
    lines.push(`## ${entry.role === "user" ? "You" : "Assistant"}`);
    lines.push("");
    lines.push(entry.text);
    lines.push("");
  });
  return lines.join("\n").trim();
}

async function copyToClipboard(text) {
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(text);
    return;
  }
  const area = document.createElement("textarea");
  area.value = text;
  area.setAttribute("readonly", "");
  area.style.position = "fixed";
  area.style.left = "-9999px";
  document.body.appendChild(area);
  area.select();
  document.execCommand("copy");
  document.body.removeChild(area);
}

function flashButtonFeedback(button, okLabel = "Copied") {
  if (!button) return;
  const original = button.textContent;
  button.textContent = okLabel;
  button.disabled = true;
  window.setTimeout(() => {
    button.textContent = original;
    button.disabled = false;
  }, 1400);
}

async function copyConversation() {
  const markdown = buildConversationMarkdown();
  if (!markdown || conversationLog.length === 0) {
    flashButtonFeedback(copyChatBtn, "Nothing to copy");
    return;
  }
  try {
    await copyToClipboard(markdown);
    flashButtonFeedback(copyChatBtn);
  } catch (err) {
    flashButtonFeedback(copyChatBtn, "Copy failed");
    console.error(err);
  }
}

function appendMessage(role, bodyHtml, { text, error = false, uris = [] } = {}) {
  const bodyText = text ?? htmlToPlainText(bodyHtml);
  conversationLog.push({ role, text: bodyText });
  const wrap = document.createElement("article");
  wrap.className = `msg msg--${role}${error ? " msg--error" : ""}`;
  wrap.innerHTML = `
    <div class="msg-role">${role === "user" ? "You" : "Assistant"}</div>
    <div class="msg-body">${bodyHtml}</div>
  `;
  messagesEl.appendChild(wrap);
  enhanceBlocks(wrap);
  appendUriActions(wrap, uris);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return wrap;
}

function enhanceBlocks(root) {
  root.querySelectorAll("pre > code").forEach((codeEl) => {
    const text = codeEl.textContent || "";
    const uri = extractUriFromCode(text);
    const actions = document.createElement("div");
    actions.className = "block-actions";

    const copyBtn = document.createElement("button");
    copyBtn.type = "button";
    copyBtn.textContent = "Copy";
    copyBtn.addEventListener("click", async () => {
      try {
        await copyToClipboard(text.trim());
        flashButtonFeedback(copyBtn);
      } catch (err) {
        console.error(err);
      }
    });
    actions.appendChild(copyBtn);

    if (uri) {
      actions.appendChild(actionButton("Preview URI", () => previewUri(uri)));
      actions.appendChild(
        actionButton("Dry-run URI", () => callUri(uri, { dryRun: true })),
      );
      actions.appendChild(
        actionButton("Run real", () => callUri(uri, { approved: true, dryRun: false })),
      );
    }

    codeEl.parentElement?.insertAdjacentElement("afterend", actions);
  });
}

function appendPlanActions(root, askResult) {
  const data = askResult?.data || {};
  const uris = collectUris(data);
  if (!uris.length) return;

  const actions = document.createElement("div");
  actions.className = "plan-actions";
  actions.appendChild(
    actionButton("Run plan (dry-run)", () => runPlan(uris, { dryRun: true, approved: false })),
  );
  actions.appendChild(
    actionButton("Run plan (approve)", () =>
      runPlan(uris, { dryRun: false, approved: true }),
    ),
  );
  uris.slice(0, 4).forEach((uri) => {
    actions.appendChild(actionButton(shortUri(uri), () => previewUri(uri), "uri-chip"));
  });
  root.appendChild(actions);
}

function planRunPayload(uris, { dryRun = true, approved = false } = {}) {
  return {
    planned_uris: uris,
    dry_run: dryRun,
    approved,
    policy: "dev",
    stop_on_error: true,
    auto_repair: true,
    retry_after_repair: true,
    speak_summary: Boolean(speakSummaryEl?.checked),
  };
}

async function runPlan(uris, { dryRun = true, approved = false } = {}) {
  if (isBusy || !uris.length) return;
  setBusy(true);
  appendMessage(
    "user",
    `<p>Run plan (${uris.length} URI, ${approved ? "approve" : "dry-run"})</p>`,
    { text: `Run plan (${uris.length} URI)` },
  );
  try {
    const result = await apiFetch("/api/plan/run", {
      method: "POST",
      body: JSON.stringify(planRunPayload(uris, { dryRun, approved })),
    });
    const md = result.message_markdown || "```json\n" + JSON.stringify(result, null, 2) + "\n```";
    appendMessage("assistant", renderMarkdown(md), {
      uris: collectUris(result),
      text: md,
    });
    for (const step of result.results || []) {
      if (step.message_markdown) {
        appendMessage("assistant", renderMarkdown(step.message_markdown), {
          uris: collectUris(step),
          text: step.message_markdown,
        });
      }
    }
    if (result.speech) {
      await playSpeechResult(result.speech);
    }
    await loadSystemState();
  } catch (err) {
    appendMessage("assistant", `<p><strong>Plan run error</strong></p><p>${escapeHtml(String(err))}</p>`, {
      error: true,
    });
  } finally {
    setBusy(false);
  }
}

function renderEvents(events) {
  if (!events.length) {
    eventListEl.className = "list list--empty";
    eventListEl.textContent = "brak zdarzeń";
    return;
  }
  eventListEl.className = "list";
  eventListEl.innerHTML = "";
  events.slice(0, 8).forEach((event) => {
    const item = document.createElement("button");
    item.type = "button";
    item.className = "list-item";
    const summary = event.summary || event.status || "";
    const badge = event.level ? `${event.level} · ` : "";
    item.innerHTML = `<strong>${escapeHtml(event.type)}</strong><span>${escapeHtml(badge + (event.agent_id || summary || event.uri || ""))}</span>`;
    const targetUri = event.view_uri || event.uri;
    if (targetUri && String(targetUri).includes("://")) {
      item.addEventListener("click", () => callUri(targetUri));
    }
    eventListEl.appendChild(item);
  });
}

function startEventStream() {
  if (eventStream || typeof EventSource === "undefined") return;
  try {
    eventStream = new EventSource(`${API}/api/events/stream?limit=12&interval_s=8`);
    eventStream.onmessage = (message) => {
      try {
        const payload = JSON.parse(message.data);
        renderEvents(payload.events || []);
      } catch (_err) {
        // Ignore malformed SSE payloads.
      }
    };
    eventStream.onerror = () => {
      if (eventStream) {
        eventStream.close();
        eventStream = null;
      }
    };
  } catch (_err) {
    eventStream = null;
  }
}

function appendUriActions(root, uris) {
  const uniqueUris = [...new Set([...(uris || []), ...extractUrisFromCodeBlocks(root)])];
  if (!uniqueUris.length) return;

  const actions = document.createElement("div");
  actions.className = "uri-actions";
  uniqueUris.slice(0, 6).forEach((uri) => {
    const group = document.createElement("div");
    group.className = "uri-action-group";
    group.appendChild(actionButton(shortUri(uri), () => previewUri(uri), "uri-chip"));
    group.appendChild(actionButton("Dry-run", () => callUri(uri, { dryRun: true })));
    group.appendChild(actionButton("Run real", () => callUri(uri, { approved: true, dryRun: false })));
    actions.appendChild(group);
  });
  root.appendChild(actions);
}

function actionButton(label, handler, className = "") {
  const button = document.createElement("button");
  button.type = "button";
  button.className = className;
  button.textContent = label;
  button.addEventListener("click", handler);
  return button;
}

function shortUri(uri) {
  return uri.length > 46 ? `${uri.slice(0, 43)}...` : uri;
}

async function apiFetch(path, options = {}) {
  const res = await fetch(`${API}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const payload = await res.json().catch(() => ({}));
  if (!res.ok) {
    const detail = payload.detail || payload.error || res.statusText;
    throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
  }
  return payload;
}

async function checkHealth({ silent = false } = {}) {
  try {
    const health = await apiFetch("/health");
    statusPill.textContent = `${health.agent} · OK`;
    statusPill.className = "pill pill--ok";
    apiDetail.textContent = `${health.version || "dev"} · ${API || "same-origin"}`;
    return health;
  } catch (err) {
    statusPill.textContent = "brak API";
    statusPill.className = "pill pill--warn";
    apiDetail.textContent = "offline";
    if (!silent) {
      appendMessage(
        "assistant",
        `<p>Brak połączenia z API. Uruchom serwer:</p><pre><code>urish www serve</code></pre><p>${escapeHtml(String(err))}</p>`,
        { error: true },
      );
    }
    return null;
  }
}

async function loadSystemState() {
  await checkHealth({ silent: true });
  await Promise.all([loadAgents(), loadEvents()]);
}

async function loadAgents() {
  try {
    const payload = await apiFetch("/api/agents");
    const agents = payload.agents || [];
    if (!agents.length) {
      agentListEl.className = "list list--empty";
      agentListEl.textContent = "brak wpisów";
      return;
    }
    agentListEl.className = "list";
    agentListEl.innerHTML = "";
    agents.slice(0, 6).forEach((agent) => {
      const item = document.createElement("button");
      item.type = "button";
      item.className = "list-item";
      item.innerHTML = `<strong>${escapeHtml(agent.id)}</strong><span>${escapeHtml(agent.status || "unknown")}</span>`;
      item.addEventListener("click", () => callUri(agent.view_uri || `view://process/agent/${agent.id}/latest`));
      agentListEl.appendChild(item);
    });
  } catch (err) {
    agentListEl.className = "list list--empty";
    agentListEl.textContent = "API niedostępne";
  }
}

async function loadEvents() {
  try {
    const payload = await apiFetch("/api/events?limit=12");
    renderEvents(payload.events || []);
  } catch (err) {
    eventListEl.className = "list list--empty";
    eventListEl.textContent = "API niedostępne";
  }
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

async function askPrompt(text) {
  return apiFetch("/api/ask", {
    method: "POST",
    body: JSON.stringify({
      prompt: text,
      dry_run: dryRunEl.checked,
      llm: false,
    }),
  });
}

async function previewUri(uri) {
  if (isBusy) return;
  appendMessage("user", `<p>Preview <code>${escapeHtml(uri)}</code></p>`, {
    text: `Preview \`${uri}\``,
  });
  setBusy(true);
  try {
    const result = await apiFetch("/api/uri/preview", {
      method: "POST",
      body: JSON.stringify({
        uri,
        dry_run: true,
        policy: "dev",
      }),
    });
    appendMessage("assistant", renderMarkdown(formatPreviewMarkdown(result)), {
      uris: [uri],
      text: formatPreviewMarkdown(result),
    });
  } catch (err) {
    appendMessage("assistant", `<p><strong>Preview error</strong></p><p>${escapeHtml(String(err))}</p>`, {
      error: true,
    });
  } finally {
    setBusy(false);
  }
}

function formatPreviewMarkdown(result) {
  const approval = result.requires_approval ? "yes" : "no";
  const dryRunAllowed = result.dry_run_allowed ? "allowed" : "blocked";
  const execute = result.execute_allowed_with_approval ? "yes" : "no";
  const mode = dryRunEl.checked ? "dry-run (checkbox on)" : "real execution (checkbox off)";
  return [
    "## URI preview",
    `URI: \`${result.uri}\``,
    `Mode: **${mode}** · dry-run policy: **${dryRunAllowed}** · requires approval: **${approval}** · execute after approval: **${execute}**`,
    "",
    "```json",
    JSON.stringify(result, null, 2),
    "```",
  ].join("\n");
}

async function callUri(uri, { approved = false, echoUser = true, dryRun = null } = {}) {
  if (isBusy) return;
  if (echoUser) {
    appendMessage("user", `<p><code>${escapeHtml(uri)}</code></p>`, { text: `\`${uri}\`` });
  }
  setBusy(true);
  try {
    const result = await apiFetch("/api/uri/call", {
      method: "POST",
      body: JSON.stringify({
        uri,
        dry_run: dryRun === null ? dryRunEl.checked && !approved : dryRun,
        approved,
        policy: "dev",
      }),
    });
    const md = result.message_markdown || "```json\n" + JSON.stringify(result, null, 2) + "\n```";
    appendMessage("assistant", renderMarkdown(md), { uris: collectUris(result.data), text: md });
    await loadSystemState();
  } catch (err) {
    appendMessage("assistant", `<p><strong>URI error</strong></p><p>${escapeHtml(String(err))}</p>`, {
      error: true,
    });
  } finally {
    setBusy(false);
  }
}

function setBusy(busy) {
  isBusy = busy;
  sendBtn.disabled = busy;
  promptEl.disabled = busy;
  refreshBtn.disabled = busy;
  if (copyChatBtn) copyChatBtn.disabled = busy;
  if (clearChatBtn) clearChatBtn.disabled = busy;
  if (micBtn) micBtn.disabled = busy;
}

async function speakText(text) {
  if (!text?.trim()) return null;
  return apiFetch("/api/voice/speak", {
    method: "POST",
    body: JSON.stringify({ text: text.trim().slice(0, 500), voice: "mock", play: true }),
  });
}

async function playSpeechResult(speech) {
  if (!speech) return;
  const playback = speech.playback;
  if (playback?.url) {
    try {
      const audio = new Audio(playback.url);
      await audio.play();
      return;
    } catch (_err) {
      // Fall through to speak API retry.
    }
  }
  if (speech.text) {
    await speakText(speech.text);
  }
}

function markdownToSpeechText(markdown) {
  return String(markdown || "")
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/`([^`]+)`/g, "$1")
    .replace(/[#>*_\[\]()]/g, " ")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 400);
}

async function maybeSpeakAssistantReply(markdown) {
  if (!speakSummaryEl?.checked) return;
  const text = markdownToSpeechText(markdown);
  if (!text) return;
  try {
    await speakText(text);
  } catch (err) {
    console.warn("speak result failed", err);
  }
}

async function blobToBase64(blob) {
  const buffer = await blob.arrayBuffer();
  const bytes = new Uint8Array(buffer);
  let binary = "";
  bytes.forEach((byte) => {
    binary += String.fromCharCode(byte);
  });
  return btoa(binary);
}

async function transcribeAudioBlob(blob, mimeType) {
  const engine = voiceEngineEl?.value || "auto";
  const payload = { mime_type: mimeType, language: "pl" };
  if (engine === "mock") {
    payload.text = promptEl.value.trim() || "otwórz Chrome i sprawdź health agenta";
    payload.engine = "mock";
  } else {
    payload.audio_base64 = await blobToBase64(blob);
    payload.engine = engine === "whisper" ? "auto" : engine;
  }
  return apiFetch("/api/voice/transcribe", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

async function toggleVoiceCapture() {
  if (isBusy) return;
  if (mediaRecorder && mediaRecorder.state === "recording") {
    mediaRecorder.stop();
    return;
  }
  if (!navigator.mediaDevices?.getUserMedia) {
    appendMessage(
      "assistant",
      "<p><strong>Voice unavailable</strong></p><p>Browser does not expose microphone APIs.</p>",
      { error: true },
    );
    return;
  }
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaChunks = [];
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.ondataavailable = (event) => {
      if (event.data?.size) mediaChunks.push(event.data);
    };
    mediaRecorder.onstop = async () => {
      micBtn?.classList.remove("is-recording");
      stream.getTracks().forEach((track) => track.stop());
      if (!mediaChunks.length) return;
      const blob = new Blob(mediaChunks, { type: mediaRecorder.mimeType || "audio/webm" });
      setBusy(true);
      try {
        const result = await transcribeAudioBlob(blob, blob.type);
        const text = result.transcript?.text || "";
        if (!text) throw new Error("Empty transcript");
        promptEl.value = text;
        appendMessage("assistant", `<p>Transcript: ${escapeHtml(text)}</p>`, { text });
        form.requestSubmit();
      } catch (err) {
        appendMessage(
          "assistant",
          `<p><strong>Voice error</strong></p><p>${escapeHtml(String(err))}</p>`,
          { error: true },
        );
      } finally {
        setBusy(false);
        mediaRecorder = null;
        mediaChunks = [];
      }
    };
    mediaRecorder.start();
    micBtn?.classList.add("is-recording");
  } catch (err) {
    appendMessage(
      "assistant",
      `<p><strong>Microphone blocked</strong></p><p>${escapeHtml(String(err))}</p>`,
      { error: true },
    );
  }
}

async function handleSubmit(event) {
  event.preventDefault();
  if (isBusy) return;
  const text = promptEl.value.trim();
  if (!text) return;

  appendMessage("user", `<p>${escapeHtml(text)}</p>`, { text });
  promptEl.value = "";

  if (looksLikeUri(text)) {
    const uri = extractUri(text) || text.trim();
    await callUri(uri, { echoUser: false });
    return;
  }

  setBusy(true);
  try {
    const result = await askPrompt(text);
    const md = result.message_markdown || "_No response._";
    const wrap = appendMessage("assistant", renderMarkdown(md), {
      uris: collectUris(result.data),
      text: md,
    });
    appendPlanActions(wrap, result);
    await maybeSpeakAssistantReply(md);
  } catch (err) {
    appendMessage("assistant", `<p><strong>Ask error</strong></p><p>${escapeHtml(String(err))}</p>`, {
      error: true,
    });
  } finally {
    setBusy(false);
  }
}

function resetConversation() {
  conversationLog.length = 0;
  messagesEl.innerHTML = "";
  appendMessage("assistant", renderMarkdown(INTRO_MARKDOWN), { text: INTRO_MARKDOWN });
}

function renderQuickPrompts() {
  quickPromptsEl.innerHTML = "";
  QUICK_PROMPTS.forEach((item) => {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = item.label;
    button.dataset.prompt = item.prompt;
    button.addEventListener("click", () => {
      promptEl.value = item.prompt;
      promptEl.focus();
    });
    quickPromptsEl.appendChild(button);
  });
}

form.addEventListener("submit", handleSubmit);
refreshBtn.addEventListener("click", () => loadSystemState());
micBtn?.addEventListener("click", toggleVoiceCapture);
copyChatBtn?.addEventListener("click", () => copyConversation());
clearChatBtn?.addEventListener("click", resetConversation);
promptEl.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) {
    event.preventDefault();
    form.requestSubmit();
  }
});

renderQuickPrompts();
resetConversation();
loadSystemState();
startEventStream();

const CHAT_PROMPT_KEY = "taskinity.chatPrompt";
try {
  const pendingPrompt = localStorage.getItem(CHAT_PROMPT_KEY);
  if (pendingPrompt) {
    localStorage.removeItem(CHAT_PROMPT_KEY);
    promptEl.value = pendingPrompt;
    promptEl.focus();
  }
} catch (_err) {
  // Ignore blocked storage.
}
