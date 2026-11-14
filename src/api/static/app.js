// FreshGuard AI — Enterprise Conversational Client
// Team SOL CULTURE (Adithya R Kulkarni & Manisha M Kulkarni)

let currentUser = {
    userId: "user_adithya",
    name: "Adithya R Kulkarni",
    email: "adithya@solculture.ai",
    picture: "https://api.dicebear.com/7.x/initials/svg?seed=Adithya"
};

let historyRecords = [];
let activeFilter = "all";
let isIncognito = false;
let isSpeaking = false;

document.addEventListener("DOMContentLoaded", () => {
    initAuth();
    loadSidebarHistory();
    setupEventListeners();
});

// --- AUTHENTICATION ---
function initAuth() {
    const saved = localStorage.getItem("fg_session");
    if (saved) {
        try {
            currentUser = JSON.parse(saved);
        } catch (e) {}
    }
    updateProfileUI();
}

function updateProfileUI() {
    const nameEl = document.getElementById("sidebar-user-name");
    const avatarEl = document.getElementById("sidebar-user-avatar");
    if (nameEl) nameEl.textContent = currentUser.name || "Adithya R Kulkarni";
    if (avatarEl) avatarEl.src = currentUser.picture || `https://api.dicebear.com/7.x/initials/svg?seed=${currentUser.name}`;
}

async function handleGoogleLogin() {
    // If already logged in, prompt sign out
    if (currentUser.userId !== "user_demo" && currentUser.email !== "demo@solculture.ai") {
        if (confirm(`Currently signed in as ${currentUser.name}. Do you want to sign out?`)) {
            currentUser = {
                userId: "user_demo",
                name: "Demo Account",
                email: "demo@solculture.ai",
                picture: "https://api.dicebear.com/7.x/initials/svg?seed=Demo"
            };
            localStorage.setItem("fg_session", JSON.stringify(currentUser));
            updateProfileUI();
            loadSidebarHistory();
            showToast("Signed out");
            return;
        }
    }

    try {
        const res = await fetch("/api/auth/google", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                email: "adithya.kulkarni@gmail.com",
                name: "Adithya R Kulkarni",
                picture: "https://api.dicebear.com/7.x/avataaars/svg?seed=Adithya"
            })
        });
        if (res.ok) {
            const data = await res.json();
            currentUser = {
                userId: data.user_id,
                name: data.name,
                email: data.email,
                picture: data.picture
            };
            localStorage.setItem("fg_session", JSON.stringify(currentUser));
            updateProfileUI();
            loadSidebarHistory();
            showToast(`Welcome back, ${currentUser.name}!`);
        }
    } catch (e) {
        console.error("Auth error", e);
    }
}

// --- SETUP EVENT LISTENERS ---
function setupEventListeners() {
    // Sidebar Toggles
    const sidebar = document.getElementById("sidebar");
    const toggleBtn = document.getElementById("sidebar-toggle-btn");
    const mobileToggleBtn = document.getElementById("mobile-sidebar-toggle");

    if (toggleBtn) {
        toggleBtn.addEventListener("click", () => {
            sidebar.classList.toggle("collapsed");
        });
    }
    if (mobileToggleBtn) {
        mobileToggleBtn.addEventListener("click", () => {
            sidebar.classList.toggle("collapsed");
        });
    }

    // New Audit button
    document.getElementById("new-audit-btn").addEventListener("click", resetToNewAudit);

    // Keyboard shortcut Cmd/Ctrl + K for new audit
    document.addEventListener("keydown", (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
            e.preventDefault();
            resetToNewAudit();
        }
    });

    // Google Auth icon button
    document.getElementById("google-auth-btn").addEventListener("click", handleGoogleLogin);

    // Incognito Toggle
    const incognitoInput = document.getElementById("incognito-toggle");
    const incognitoBanner = document.getElementById("incognito-banner");
    if (incognitoInput) {
        incognitoInput.addEventListener("change", (e) => {
            isIncognito = e.target.checked;
            if (isIncognito) {
                incognitoBanner.classList.remove("hidden");
                showToast("Incognito active: Zero history saved");
            } else {
                incognitoBanner.classList.add("hidden");
            }
        });
    }

    // History Search
    const searchInput = document.getElementById("history-search");
    if (searchInput) {
        searchInput.addEventListener("input", () => {
            renderSidebarHistory(searchInput.value.trim().toLowerCase());
        });
    }

    // History Filter tabs
    document.querySelectorAll(".hist-filter-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".hist-filter-btn").forEach(b => b.classList.remove("active", "text-white", "bg-zinc-800"));
            btn.classList.add("active", "text-white", "bg-zinc-800");
            activeFilter = btn.getAttribute("data-filter");
            renderSidebarHistory();
        });
    });

    // Chat input auto-expand & send
    const chatInput = document.getElementById("chat-input");
    const sendBtn = document.getElementById("send-btn");

    if (chatInput) {
        chatInput.addEventListener("input", () => {
            chatInput.style.height = "auto";
            chatInput.style.height = Math.min(chatInput.scrollHeight, 130) + "px";
        });

        chatInput.addEventListener("keydown", (e) => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSubmit();
            }
        });
    }

    if (sendBtn) sendBtn.addEventListener("click", handleSubmit);

    // Quick chip buttons
    document.querySelectorAll(".quick-chip").forEach(chip => {
        chip.addEventListener("click", () => {
            const prompt = chip.getAttribute("data-prompt");
            if (chatInput) {
                chatInput.value = prompt;
                handleSubmit();
            }
        });
    });

    // Interactive Voice Demo Walkthrough button
    const voiceDemoBtn = document.getElementById("voice-demo-btn");
    if (voiceDemoBtn) voiceDemoBtn.addEventListener("click", runInteractiveVoiceDemo);
}

function resetToNewAudit() {
    document.getElementById("messages-wrapper").innerHTML = "";
    document.getElementById("welcome-state").classList.remove("hidden");
    document.getElementById("current-audit-title").textContent = "New Audit Session";
    const input = document.getElementById("chat-input");
    input.value = "";
    input.style.height = "auto";
    input.focus();
}

// --- SUBMIT VERIFICATION PIPELINE ---
async function handleSubmit() {
    const input = document.getElementById("chat-input");
    const text = input.value.trim();
    if (!text || text.length < 5) {
        showToast("Enter at least 5 characters to verify");
        return;
    }

    // Hide welcome state
    document.getElementById("welcome-state").classList.add("hidden");
    document.getElementById("current-audit-title").textContent = text.substring(0, 32) + "...";

    // 1. Append User Message Bubble
    appendUserBubble(text);
    input.value = "";
    input.style.height = "auto";

    // 2. Show Thinking Indicator
    const thinkingIndicator = document.getElementById("thinking-indicator");
    thinkingIndicator.classList.remove("hidden");
    scrollChatToBottom();

    // Animate thinking stages
    const thinkInterval = animateThinkingSteps();
    const deepSearch = document.getElementById("deep-search-dock").checked ? "advanced" : "basic";

    try {
        const response = await fetch("/api/verify", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                text: text,
                search_depth: deepSearch,
                user_id: currentUser.userId,
                is_incognito: isIncognito
            })
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || "Verification failed");
        }

        const report = await response.json();
        clearInterval(thinkInterval);
        thinkingIndicator.classList.add("hidden");

        // 3. Append FreshGuard Assistant Response Bubble
        appendAssistantBubble(report);

        if (!isIncognito) {
            loadSidebarHistory();
        }
    } catch (err) {
        clearInterval(thinkInterval);
        thinkingIndicator.classList.add("hidden");
        appendErrorBubble(err.message);
    }
}

function animateThinkingSteps() {
    const textEl = document.getElementById("thinking-stage-text");
    const progEl = document.getElementById("thinking-progress");
    const stages = [
        { text: "Deconstructing factual assertions & calculating decay risk...", width: "30%" },
        { text: "Querying Tavily search across live 2026 web ground truth...", width: "60%" },
        { text: "Cross-referencing contradictions via Bifrost Gateway...", width: "85%" },
        { text: "Synthesizing verified output & diff...", width: "95%" }
    ];

    let i = 0;
    const interval = setInterval(() => {
        if (i < stages.length) {
            textEl.textContent = stages[i].text;
            progEl.style.width = stages[i].width;
            i++;
        }
    }, 1200);

    return interval;
}

// --- BUBBLE RENDERING ---
function appendUserBubble(text) {
    const wrapper = document.getElementById("messages-wrapper");
    const bubble = document.createElement("div");
    bubble.className = "flex space-x-3 justify-end text-xs sm:text-sm chat-bubble-animate";
    bubble.innerHTML = `
        <div class="bg-surface-900 border border-zinc-800 text-zinc-100 rounded-2xl rounded-tr-sm px-4 py-3 max-w-xl shadow-sm leading-relaxed whitespace-pre-wrap font-sans">
            ${escapeHtml(text)}
        </div>
        <img src="${currentUser.picture || 'https://api.dicebear.com/7.x/initials/svg?seed=User'}" class="w-7 h-7 rounded-full border border-zinc-700 flex-shrink-0 object-cover mt-0.5">
    `;
    wrapper.appendChild(bubble);
    scrollChatToBottom();
}

function appendAssistantBubble(report) {
    const wrapper = document.getElementById("messages-wrapper");
    const bubble = document.createElement("div");
    bubble.className = "flex space-x-3 text-xs sm:text-sm chat-bubble-animate";

    const score = report.overall_freshness_score;
    let badgeClass = "bg-red-500/10 text-red-400 border-red-500/20";
    let badgeLabel = "Stale Claims Detected";
    if (score >= 80) {
        badgeClass = "bg-emerald-500/10 text-emerald-400 border-emerald-500/20";
        badgeLabel = "Verified Fresh";
    } else if (score >= 50) {
        badgeClass = "bg-amber-500/10 text-amber-400 border-amber-500/20";
        badgeLabel = "Partially Stale";
    }

    // Side-by-Side Diff markup
    let diffOriginal = report.input_text;
    report.claims.forEach(c => {
        if (c.status === "stale" && c.claim && c.claim.text) {
            const target = c.claim.text;
            if (diffOriginal.includes(target)) {
                diffOriginal = diffOriginal.replace(
                    target,
                    `<span class="stale-highlight" title="Outdated: ${escapeHtml(c.stale_delta || c.reasoning)}">${escapeHtml(target)}</span>`
                );
            }
        }
    });

    // Claims markup
    let claimsHtml = "";
    report.claims.forEach((c, idx) => {
        let tag = c.status === "stale" ? '<span class="text-red-400 font-mono text-[10px] font-bold uppercase">Stale</span>' : '<span class="text-emerald-400 font-mono text-[10px] font-bold uppercase">Fresh</span>';
        let correction = c.current_value_correction ? `<div class="text-emerald-400 font-medium text-[11px] pt-1 border-t border-zinc-800">Verified Reality: ${escapeHtml(c.current_value_correction)}</div>` : '';
        let citations = "";
        if (c.evidence && c.evidence.length > 0) {
            const items = c.evidence.map(e => `
                <a href="${e.url}" target="_blank" class="px-2 py-1 rounded bg-surface-950 border border-zinc-800 hover:border-zinc-700 text-[10px] text-zinc-400 hover:text-white truncate block max-w-xs">
                    🔗 ${escapeHtml(e.domain)} — ${escapeHtml(e.title)}
                </a>
            `).join("");
            citations = `<div class="flex flex-wrap gap-1.5 pt-1">${items}</div>`;
        }

        claimsHtml += `
            <div class="p-3 rounded-xl bg-surface-950 border border-zinc-800/80 space-y-1 text-xs">
                <div class="flex items-center justify-between text-[10px] font-mono text-zinc-500 border-b border-zinc-800/60 pb-1">
                    <span>#${idx+1} ${c.claim.category.toUpperCase()} · Volatility: ${Math.round(c.claim.time_volatility_score*100)}%</span>
                    ${tag}
                </div>
                <div class="font-medium text-zinc-200">"${escapeHtml(c.claim.text)}"</div>
                <div class="text-zinc-400 text-[11px]">${escapeHtml(c.reasoning)}</div>
                ${correction}
                ${citations}
            </div>
        `;
    });

    const reportId = `rep_${Date.now()}`;
    window[reportId] = report;

    bubble.innerHTML = `
        <div class="w-7 h-7 rounded-lg bg-zinc-800 border border-zinc-700 flex items-center justify-center flex-shrink-0 text-indigo-400 mt-0.5">
            <i class="fa-solid fa-shield-halved text-xs"></i>
        </div>
        <div class="bg-surface-900 border border-zinc-800 rounded-2xl rounded-tl-sm p-4 sm:p-5 space-y-4 max-w-2xl shadow-sm text-zinc-200">
            <!-- Header Score -->
            <div class="flex items-center justify-between border-b border-zinc-800 pb-3">
                <div class="flex items-center space-x-2.5">
                    <span class="text-xl font-bold font-mono text-white">${score}%</span>
                    <span class="text-[10px] px-2 py-0.5 rounded border ${badgeClass} font-mono uppercase font-bold">${badgeLabel}</span>
                </div>
                <span class="text-[10px] font-mono text-zinc-500">${report.gateway_provider} · ${report.latency_seconds}s</span>
            </div>

            <!-- Executive Summary -->
            <p class="text-xs text-zinc-300 leading-relaxed">${escapeHtml(report.summary)}</p>

            <!-- Side-by-Side Diff -->
            <div class="space-y-2 pt-1">
                <span class="text-[11px] font-semibold text-zinc-400 uppercase tracking-wider block">Side-by-Side Verification</span>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs font-mono">
                    <div class="p-3 rounded-xl bg-surface-950 border border-red-500/20 space-y-1">
                        <span class="text-[10px] font-bold text-red-400 block uppercase">Original (Stale Flagged)</span>
                        <div class="text-zinc-300 font-sans leading-relaxed text-[11px]">${diffOriginal}</div>
                    </div>
                    <div class="p-3 rounded-xl bg-surface-950 border border-emerald-500/25 space-y-1">
                        <span class="text-[10px] font-bold text-emerald-400 block uppercase">Verified (2026 Ground Truth)</span>
                        <div class="text-zinc-100 font-sans leading-relaxed text-[11px]">${escapeHtml(report.updated_text)}</div>
                    </div>
                </div>
            </div>

            <!-- Claims Breakdown Accordion -->
            <div class="space-y-2 pt-2 border-t border-zinc-800/80">
                <span class="text-[11px] font-semibold text-zinc-400 uppercase tracking-wider block">Atomic Claims & Citations (${report.total_claims})</span>
                <div class="space-y-2">${claimsHtml}</div>
            </div>

            <!-- Action Toolbar (Audio, Copy, Export) -->
            <div class="flex flex-wrap items-center justify-between pt-2 border-t border-zinc-800/80 text-xs gap-2">
                <div class="flex items-center space-x-2">
                    <button class="px-2.5 py-1 rounded-lg bg-surface-950 border border-zinc-800 hover:border-zinc-700 text-indigo-300 hover:text-indigo-200 text-xs font-medium flex items-center space-x-1.5 transition-colors" onclick="speakReport('${reportId}')">
                        <i class="fa-solid fa-volume-high text-xs"></i>
                        <span>Listen Voiceover</span>
                    </button>
                    <button class="px-2.5 py-1 rounded-lg bg-surface-950 border border-zinc-800 hover:border-zinc-700 text-zinc-300 hover:text-white text-xs font-medium flex items-center space-x-1.5 transition-colors" onclick="copyVerifiedText('${reportId}')">
                        <i class="fa-regular fa-copy text-xs"></i>
                        <span>Copy Output</span>
                    </button>
                </div>
                <div class="flex items-center space-x-2 text-[10px] font-mono text-zinc-500">
                    <button class="hover:text-zinc-300" onclick="copyJsonReport('${reportId}')">JSON</button>
                    <span>·</span>
                    <button class="hover:text-zinc-300" onclick="exportMarkdown('${reportId}')">Markdown</button>
                </div>
            </div>
        </div>
    `;

    wrapper.appendChild(bubble);
    scrollChatToBottom();
}

function appendErrorBubble(msg) {
    const wrapper = document.getElementById("messages-wrapper");
    const bubble = document.createElement("div");
    bubble.className = "flex space-x-3 text-xs sm:text-sm chat-bubble-animate";
    bubble.innerHTML = `
        <div class="w-7 h-7 rounded-lg bg-red-900/30 border border-red-700/50 flex items-center justify-center flex-shrink-0 text-red-400 mt-0.5">
            <i class="fa-solid fa-triangle-exclamation text-xs"></i>
        </div>
        <div class="bg-surface-900 border border-red-500/20 text-red-300 rounded-2xl rounded-tl-sm p-4 max-w-xl text-xs">
            <strong>Verification Error:</strong> ${escapeHtml(msg)}
        </div>
    `;
    wrapper.appendChild(bubble);
    scrollChatToBottom();
}

function scrollChatToBottom() {
    const stream = document.getElementById("chat-stream");
    stream.scrollTop = stream.scrollHeight;
}

// --- ACTIONS: AUDIO VOICEOVER, COPY, EXPORT ---
window.speakReport = function(reportId) {
    const report = window[reportId];
    if (!report || !('speechSynthesis' in window)) {
        showToast("Audio synthesis not available");
        return;
    }

    if (isSpeaking) {
        window.speechSynthesis.cancel();
        isSpeaking = false;
        showToast("Voiceover stopped");
        return;
    }

    const textToSpeak = `Verification complete. Freshness score: ${report.overall_freshness_score} percent. ${report.summary}. Verified ground truth: ${report.updated_text}`;
    const utterance = new SpeechSynthesisUtterance(textToSpeak);
    utterance.rate = 1.05;
    utterance.onend = () => { isSpeaking = false; };
    window.speechSynthesis.speak(utterance);
    isSpeaking = true;
    showToast("Playing voiceover...");
};

window.copyVerifiedText = function(reportId) {
    const report = window[reportId];
    if (report) {
        navigator.clipboard.writeText(report.updated_text);
        showToast("Verified output copied to clipboard");
    }
};

window.copyJsonReport = function(reportId) {
    const report = window[reportId];
    if (report) {
        navigator.clipboard.writeText(JSON.stringify(report, null, 2));
        showToast("JSON report copied");
    }
};

window.exportMarkdown = function(reportId) {
    const r = window[reportId];
    if (!r) return;
    let md = `# FreshGuard Audit Report\n\n`;
    md += `**Freshness Score:** ${r.overall_freshness_score}%\n`;
    md += `**Summary:** ${r.summary}\n\n`;
    md += `## Original Input\n> ${r.input_text}\n\n`;
    md += `## Verified 2026 Ground Truth\n> ${r.updated_text}\n\n`;
    md += `## Citations\n`;
    r.claims.forEach((c, idx) => {
        md += `\n### Claim ${idx+1}: "${c.claim.text}"\n- Status: ${c.status}\n- Reasoning: ${c.reasoning}\n`;
        if (c.evidence) {
            c.evidence.forEach(e => { md += `  - [${e.title}](${e.url}) (${e.domain})\n`; });
        }
    });

    const blob = new Blob([md], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `freshguard-audit-${Date.now()}.md`;
    a.click();
    URL.revokeObjectURL(url);
    showToast("Downloaded Markdown report");
};

// --- SIDEBAR HISTORY MANAGEMENT ---
async function loadSidebarHistory() {
    try {
        const res = await fetch(`/api/history?user_id=${currentUser.userId}&filter_type=${activeFilter}`);
        if (res.ok) {
            historyRecords = await res.json();
            renderSidebarHistory();
        }
    } catch (e) {
        console.warn("History fetch failed", e);
    }
}

function renderSidebarHistory(searchQuery = "") {
    const listEl = document.getElementById("sidebar-history-list");
    if (!listEl) return;
    listEl.innerHTML = "";

    let filtered = historyRecords;
    if (searchQuery) {
        filtered = filtered.filter(i => (i.input_text || "").toLowerCase().includes(searchQuery));
    }

    if (filtered.length === 0) {
        listEl.innerHTML = `<div class="text-center py-8 text-zinc-500 text-[11px] font-mono">No audits found</div>`;
        return;
    }

    filtered.forEach(item => {
        const row = document.createElement("div");
        row.className = "p-2.5 rounded-xl bg-surface-950 border border-zinc-800/80 hover:border-zinc-700 hover:bg-zinc-800/40 transition-all cursor-pointer space-y-1 group relative";

        const isStale = item.stale_count > 0;
        const badgeColor = isStale ? "text-red-400 bg-red-500/10 border-red-500/20" : "text-emerald-400 bg-emerald-500/10 border-emerald-500/20";
        const dateStr = new Date(item.created_at * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const starIcon = item.is_starred ? "fa-solid fa-star text-amber-400" : "fa-regular fa-star text-zinc-500 hover:text-amber-400";
        const archiveIcon = item.is_archived ? "fa-solid fa-box-open text-indigo-400" : "fa-solid fa-box-archive text-zinc-500 hover:text-indigo-400";

        row.innerHTML = `
            <div class="flex items-center justify-between text-[10px] font-mono">
                <span class="px-1.5 py-0.2 rounded border ${badgeColor}">${item.overall_freshness_score}% Fresh</span>
                <span class="text-zinc-500">${dateStr}</span>
            </div>
            <p class="text-xs text-zinc-300 line-clamp-2 leading-relaxed pr-6 font-sans">${escapeHtml(item.input_text)}</p>

            <!-- Quick Action Icons on hover -->
            <div class="absolute right-2 top-2.5 hidden group-hover:flex items-center space-x-1.5 text-xs bg-surface-950/90 pl-1">
                <button class="p-1 text-zinc-400 hover:text-amber-400" title="Star" onclick="event.stopPropagation(); toggleStar('${item.id}')">
                    <i class="${starIcon}"></i>
                </button>
                <button class="p-1 text-zinc-400 hover:text-indigo-400" title="Archive" onclick="event.stopPropagation(); toggleArchive('${item.id}')">
                    <i class="${archiveIcon}"></i>
                </button>
                <button class="p-1 text-zinc-400 hover:text-red-400" title="Delete" onclick="event.stopPropagation(); deleteHistoryItem('${item.id}')">
                    <i class="fa-regular fa-trash-can"></i>
                </button>
            </div>
        `;

        row.addEventListener("click", () => {
            loadAuditIntoChat(item.id);
        });

        listEl.appendChild(row);
    });
}

async function loadAuditIntoChat(auditId) {
    try {
        const res = await fetch(`/api/history/${auditId}`);
        if (res.ok) {
            const report = await res.json();
            document.getElementById("welcome-state").classList.add("hidden");
            document.getElementById("current-audit-title").textContent = report.input_text.substring(0, 32) + "...";
            document.getElementById("messages-wrapper").innerHTML = "";
            appendUserBubble(report.input_text);
            appendAssistantBubble(report);
            showToast("Loaded past audit record");
        }
    } catch (e) {
        showToast("Error loading audit");
    }
}

window.toggleStar = async function(id) {
    try {
        await fetch(`/api/history/${id}/star?user_id=${currentUser.userId}`, { method: "PUT" });
        loadSidebarHistory();
    } catch (e) {}
};

window.toggleArchive = async function(id) {
    try {
        await fetch(`/api/history/${id}/archive?user_id=${currentUser.userId}`, { method: "PUT" });
        loadSidebarHistory();
    } catch (e) {}
};

window.deleteHistoryItem = async function(id) {
    try {
        await fetch(`/api/history/${id}?user_id=${currentUser.userId}`, { method: "DELETE" });
        loadSidebarHistory();
        showToast("Audit deleted");
    } catch (e) {}
};

// --- INTERACTIVE VOICE DEMO WALKTHROUGH ---
function runInteractiveVoiceDemo() {
    resetToNewAudit();
    const demoPrompt = "OpenAI's flagship GPT-4 costs $30.00 per 1M prompt tokens and $60.00 per 1M completion tokens.";
    const chatInput = document.getElementById("chat-input");

    // Speak introductory narration
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const intro = new SpeechSynthesisUtterance("Welcome to FreshGuard AI by team SOL CULTURE. Let us audit a real-world outdated claim regarding OpenAI GPT-4 pricing.");
        intro.rate = 1.05;
        window.speechSynthesis.speak(intro);
    }

    // Type out prompt smoothly
    let charIdx = 0;
    chatInput.value = "";
    const typeInterval = setInterval(() => {
        if (charIdx < demoPrompt.length) {
            chatInput.value += demoPrompt[charIdx];
            charIdx++;
        } else {
            clearInterval(typeInterval);
            setTimeout(() => {
                handleSubmit();
            }, 800);
        }
    }, 25);
}

function showToast(msg) {
    const toast = document.createElement("div");
    toast.className = "fixed bottom-5 right-5 bg-zinc-800 text-zinc-100 border border-zinc-700 px-3.5 py-2 rounded-xl shadow-xl text-xs font-medium z-50 transition-opacity animate-bounce";
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2500);
}

function escapeHtml(str) {
    if (!str) return "";
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
