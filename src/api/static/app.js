// FreshGuard AI — Real-Time Fact Verification & Temporal Obsolescence Engine
// Team SOL CULTURE: Adithya R Kulkarni & Manisha M Kulkarni

let historyRecords = [];
let activeFilter = "all";
let isIncognito = false;
let isSpeaking = false;
const DEFAULT_USER_ID = "user_default";

document.addEventListener("DOMContentLoaded", () => {
    loadSidebarHistory();
    setupEventListeners();
});

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
    const newBtn = document.getElementById("new-audit-btn");
    if (newBtn) {
        newBtn.addEventListener("click", resetToNewAudit);
    }

    // Clear feed button
    const clearBtn = document.getElementById("clear-feed-btn");
    if (clearBtn) {
        clearBtn.addEventListener("click", resetToNewAudit);
    }

    // Keyboard shortcut Cmd/Ctrl + K for new audit
    document.addEventListener("keydown", (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
            e.preventDefault();
            resetToNewAudit();
        }
    });

    // Incognito Toggle
    const incognitoInput = document.getElementById("incognito-toggle");
    const incognitoBanner = document.getElementById("incognito-banner");
    if (incognitoInput) {
        incognitoInput.addEventListener("change", (e) => {
            isIncognito = e.target.checked;
            if (isIncognito) {
                incognitoBanner.classList.remove("hidden");
                showToast("Incognito active: Zero storage mode");
            } else {
                incognitoBanner.classList.add("hidden");
                showToast("Standard mode: History enabled");
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
            document.querySelectorAll(".hist-filter-btn").forEach(b => {
                b.classList.remove("active", "text-white");
                b.classList.add("text-zinc-400");
            });
            btn.classList.add("active", "text-white");
            btn.classList.remove("text-zinc-400");
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
            chatInput.style.height = Math.min(chatInput.scrollHeight, 140) + "px";
        });

        chatInput.addEventListener("keydown", (e) => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                submitAudit();
            }
        });
    }

    if (sendBtn) {
        sendBtn.addEventListener("click", submitAudit);
    }

    // Quick Chip Click Handlers
    document.querySelectorAll(".quick-chip").forEach(chip => {
        chip.addEventListener("click", () => {
            const prompt = chip.getAttribute("data-prompt");
            if (chatInput && prompt) {
                chatInput.value = prompt;
                chatInput.style.height = "auto";
                chatInput.style.height = Math.min(chatInput.scrollHeight, 140) + "px";
                submitAudit();
            }
        });
    });
}

// --- SUBMIT AUDIT VERIFICATION ---
async function submitAudit() {
    const chatInput = document.getElementById("chat-input");
    const sendBtn = document.getElementById("send-btn");
    const thinkingIndicator = document.getElementById("thinking-indicator");
    const welcomeState = document.getElementById("welcome-state");

    const text = chatInput ? chatInput.value.trim() : "";
    if (!text || text.length < 5) {
        showToast("Please enter at least 5 characters to audit.");
        return;
    }

    // Hide welcome state
    if (welcomeState) {
        welcomeState.classList.add("hidden");
    }

    // 1. Append User Query Bubble
    appendUserBubble(text);

    // Reset input
    chatInput.value = "";
    chatInput.style.height = "auto";
    if (sendBtn) sendBtn.disabled = true;

    // Show Thinking Indicator
    thinkingIndicator.classList.remove("hidden");
    const thinkInterval = animateThinkingSteps();
    scrollChatToBottom();

    // 2. Dispatch verification request to FastAPI
    try {
        const isDeep = document.getElementById("deep-search-dock") ? document.getElementById("deep-search-dock").checked : true;
        
        const response = await fetch("/api/verify", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                text: text,
                search_depth: isDeep ? "advanced" : "basic",
                is_incognito: isIncognito,
                user_id: DEFAULT_USER_ID
            })
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || "Audit verification failed.");
        }

        const report = await response.json();
        clearInterval(thinkInterval);
        thinkingIndicator.classList.add("hidden");

        // 3. Append Decrypted FreshGuard Response Bubble
        appendDecryptedAssistantBubble(report);

        // Update Title
        const titleEl = document.getElementById("current-audit-title");
        if (titleEl) {
            titleEl.textContent = text.length > 35 ? text.substring(0, 35) + "..." : text;
        }

        if (!isIncognito) {
            loadSidebarHistory();
        }
    } catch (err) {
        clearInterval(thinkInterval);
        thinkingIndicator.classList.add("hidden");
        appendErrorBubble(err.message);
    } finally {
        if (sendBtn) sendBtn.disabled = false;
    }
}

// --- THINKING PROGRESS ANIMATOR ---
function animateThinkingSteps() {
    const textEl = document.getElementById("thinking-stage-text");
    const progEl = document.getElementById("thinking-progress");
    const stages = [
        { text: "Deconstructing atomic claims & calculating decay risk...", width: "25%" },
        { text: "Scanning live 2026 web evidence via Tavily...", width: "55%" },
        { text: "Cross-referencing contradictions via Bifrost Gateway...", width: "80%" },
        { text: "Synthesizing truth decryption & key takeaways...", width: "95%" }
    ];

    let i = 0;
    const interval = setInterval(() => {
        if (i < stages.length) {
            if (textEl) textEl.textContent = stages[i].text;
            if (progEl) progEl.style.width = stages[i].width;
            i++;
        }
    }, 1100);

    return interval;
}

// --- USER MESSAGE BUBBLE ---
function appendUserBubble(text) {
    const wrapper = document.getElementById("messages-wrapper");
    const bubble = document.createElement("div");
    bubble.className = "flex space-x-3 justify-end text-xs sm:text-sm chat-bubble-animate";
    bubble.innerHTML = `
        <div class="bg-surface-900 border border-white/10 text-zinc-100 rounded-2xl rounded-tr-sm px-4 py-3 max-w-xl shadow-lg leading-relaxed whitespace-pre-wrap font-sans">
            ${escapeHtml(text)}
        </div>
        <div class="w-8 h-8 rounded-xl bg-gradient-to-tr from-cyan-500 to-indigo-600 flex items-center justify-center text-white text-xs font-bold flex-shrink-0 shadow-md mt-0.5">
            You
        </div>
    `;
    wrapper.appendChild(bubble);
    scrollChatToBottom();
}

// --- DECRYPTED ASSISTANT AUDIT BUBBLE (EASY COMPREHENSION) ---
function appendDecryptedAssistantBubble(report) {
    const wrapper = document.getElementById("messages-wrapper");
    const bubble = document.createElement("div");
    bubble.className = "flex space-x-3 text-xs sm:text-sm chat-bubble-animate";

    const score = Math.round(report.overall_freshness_score);
    const staleClaims = report.claims.filter(c => c.status === "stale");
    const freshClaims = report.claims.filter(c => c.status === "fresh" || c.status === "evergreen");
    const unverifiedClaims = report.claims.filter(c => c.status === "unverified");

    // Verdict Badge & Colors
    let verdictHeadline = "";
    let verdictBg = "";
    let verdictBorder = "";
    let scoreColor = "";

    if (staleClaims.length > 0) {
        verdictHeadline = `🚨 CRITICAL STALENESS: ${staleClaims.length} Outdated Claim${staleClaims.length > 1 ? 's' : ''} Detected`;
        verdictBg = "bg-rose-500/10";
        verdictBorder = "border-rose-500/30";
        scoreColor = "text-rose-400";
    } else if (unverifiedClaims.length > 0) {
        verdictHeadline = `⚠️ PARTIAL CONFIDENCE: Insufficient 2026 Live Web Sources`;
        verdictBg = "bg-amber-500/10";
        verdictBorder = "border-amber-500/30";
        scoreColor = "text-amber-400";
    } else {
        verdictHeadline = `✅ 100% VERIFIED FRESH: Accurate & Current for 2026`;
        verdictBg = "bg-emerald-500/10";
        verdictBorder = "border-emerald-500/30";
        scoreColor = "text-emerald-400";
    }

    // 1. "WHAT'S WRONG WITH YOUR INFORMATION" (Instant Decryption)
    let whatsWrongHtml = "";
    if (staleClaims.length > 0) {
        whatsWrongHtml = `
            <div class="space-y-2.5">
                <div class="flex items-center space-x-2 text-rose-400 font-bold uppercase tracking-wider text-[11px]">
                    <i class="fa-solid fa-triangle-exclamation"></i>
                    <span>What is Wrong or Outdated in Your Statement</span>
                </div>
                <div class="space-y-2">
                    ${staleClaims.map((c, i) => `
                        <div class="flaw-card rounded-xl p-3 space-y-2">
                            <div class="flex items-start justify-between">
                                <div class="space-y-1">
                                    <div class="text-[10px] font-mono font-bold text-rose-400 flex items-center space-x-1.5">
                                        <span class="w-1.5 h-1.5 rounded-full bg-rose-400"></span>
                                        <span>FLAW #${i+1} · ${c.claim.category.toUpperCase()} (Decay Volatility: ${Math.round(c.claim.time_volatility_score * 100)}%)</span>
                                    </div>
                                    <div class="text-zinc-300 font-medium text-xs leading-snug">
                                        ❌ <strong class="text-rose-300 line-through">"${escapeHtml(c.claim.text)}"</strong>
                                    </div>
                                </div>
                            </div>

                            <div class="bg-surface-950/80 rounded-lg p-2.5 border border-white/5 space-y-1 text-xs">
                                <div class="text-emerald-400 font-semibold text-[11px] flex items-center space-x-1.5">
                                    <i class="fa-solid fa-arrow-right text-[10px]"></i>
                                    <span>Verified 2026 Ground Truth:</span>
                                </div>
                                <div class="text-zinc-100 font-sans pl-3 border-l-2 border-emerald-500/50">
                                    ${escapeHtml(c.current_value_correction || c.reasoning)}
                                </div>
                            </div>

                            ${c.evidence && c.evidence.length > 0 ? `
                                <div class="pt-1 flex items-center space-x-2 text-[10px] text-zinc-400">
                                    <span class="text-zinc-500">Live Citation:</span>
                                    <a href="${c.evidence[0].url}" target="_blank" class="text-cyan-400 hover:underline truncate max-w-xs font-mono">
                                        🔗 ${escapeHtml(c.evidence[0].domain)} — "${escapeHtml(c.evidence[0].title)}"
                                    </a>
                                </div>
                            ` : ''}
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    } else {
        whatsWrongHtml = `
            <div class="verified-card rounded-xl p-3.5 space-y-1.5 text-xs">
                <div class="flex items-center space-x-2 text-emerald-400 font-bold uppercase tracking-wider text-[11px]">
                    <i class="fa-solid fa-circle-check"></i>
                    <span>No Temporal Flaws Detected</span>
                </div>
                <p class="text-zinc-300 leading-relaxed text-[11px]">
                    Every atomic statement was cross-verified against live 2026 web sources via Tavily. Zero contradictions or temporal obsolescence found.
                </p>
            </div>
        `;
    }

    // 2. Side-by-Side Diff markup
    let diffOriginal = escapeHtml(report.input_text);
    staleClaims.forEach(c => {
        if (c.claim && c.claim.text) {
            const rawTarget = c.claim.text;
            const escTarget = escapeHtml(rawTarget);
            if (diffOriginal.includes(escTarget)) {
                diffOriginal = diffOriginal.replace(
                    escTarget,
                    `<span class="stale-highlight" title="Outdated: ${escapeHtml(c.current_value_correction || c.reasoning)}">${escTarget}</span>`
                );
            }
        }
    });

    const reportId = `rep_${Date.now()}`;
    window[reportId] = report;

    bubble.innerHTML = `
        <!-- High-Tech FreshGuard Avatar -->
        <div class="w-8 h-8 rounded-xl bg-surface-900 border border-cyan-500/30 flex items-center justify-center flex-shrink-0 shadow-md p-1 mt-0.5">
            <svg class="w-6 h-6" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 5L31 9.5V18C31 25.5 26.2 32.2 20 35C13.8 32.2 9 25.5 9 18V9.5L20 5Z" fill="#0d101a" stroke="#06b6d4" stroke-width="2"/>
                <path d="M16 19.5L18.8 22.3L24.5 16.5" stroke="#10b981" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>

        <!-- Assistant Main Card -->
        <div class="bg-surface-900/95 border border-white/10 rounded-2xl rounded-tl-sm p-4 sm:p-5 space-y-4 max-w-3xl shadow-xl text-zinc-200">
            
            <!-- Verdict Header Banner -->
            <div class="p-3.5 rounded-xl ${verdictBg} border ${verdictBorder} flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div class="space-y-1">
                    <div class="text-xs sm:text-sm font-extrabold ${scoreColor} tracking-tight">
                        ${verdictHeadline}
                    </div>
                    <p class="text-[11px] text-zinc-300 leading-snug">
                        ${escapeHtml(report.summary)}
                    </p>
                </div>

                <!-- Circular Score Indicator -->
                <div class="flex items-center space-x-3 flex-shrink-0">
                    <div class="text-right">
                        <div class="text-2xl font-black font-mono ${scoreColor}">${score}%</div>
                        <div class="text-[9px] font-mono text-zinc-400 uppercase">Freshness Score</div>
                    </div>
                </div>
            </div>

            <!-- Instant Decryption Section: What is Wrong -->
            ${whatsWrongHtml}

            <!-- Verified 2026 Output (Ready to Copy) -->
            <div class="space-y-1.5 pt-1">
                <div class="flex items-center justify-between">
                    <span class="text-[11px] font-bold text-cyan-400 uppercase tracking-wider flex items-center space-x-1.5">
                        <i class="fa-solid fa-sparkles"></i>
                        <span>Verified 2026 Replacement Answer</span>
                    </span>
                    <button class="px-2 py-1 rounded bg-white/5 hover:bg-white/10 text-cyan-300 hover:text-cyan-200 text-[11px] font-medium flex items-center space-x-1 transition-colors" onclick="copyVerifiedText('${reportId}')">
                        <i class="fa-regular fa-copy text-[10px]"></i>
                        <span>Copy Answer</span>
                    </button>
                </div>
                <div class="p-3 rounded-xl bg-surface-950 border border-cyan-500/20 text-zinc-100 font-sans leading-relaxed text-xs sm:text-[13px] shadow-inner select-text">
                    ${escapeHtml(report.updated_text)}
                </div>
            </div>

            <!-- Tabs Switcher for Deep Dive: Diff & Citations -->
            <div class="pt-2 border-t border-white/5 space-y-3">
                <div class="flex items-center space-x-2 text-[11px] font-medium text-zinc-400">
                    <button class="px-2.5 py-1 rounded-lg bg-white/10 text-white font-semibold tab-btn active" onclick="switchReportTab('${reportId}', 'diff', this)">
                        Visual Diff
                    </button>
                    <button class="px-2.5 py-1 rounded-lg hover:text-white tab-btn" onclick="switchReportTab('${reportId}', 'sources', this)">
                        Live Citations (${report.claims.reduce((acc, c) => acc + (c.evidence ? c.evidence.length : 0), 0)})
                    </button>
                    <button class="px-2.5 py-1 rounded-lg hover:text-white tab-btn" onclick="switchReportTab('${reportId}', 'telemetry', this)">
                        Telemetry
                    </button>
                </div>

                <!-- Tab Content 1: Visual Diff (Default) -->
                <div id="tab-diff-${reportId}" class="tab-pane">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                        <div class="p-3 rounded-xl bg-surface-950 border border-rose-500/20 space-y-1.5">
                            <span class="text-[10px] font-bold text-rose-400 uppercase tracking-wider flex items-center space-x-1">
                                <i class="fa-solid fa-clock-rotate-left"></i>
                                <span>Original (With Stale Claims Flagged)</span>
                            </span>
                            <div class="text-zinc-300 leading-relaxed text-[11px] font-sans">${diffOriginal}</div>
                        </div>

                        <div class="p-3 rounded-xl bg-surface-950 border border-emerald-500/25 space-y-1.5">
                            <span class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider flex items-center space-x-1">
                                <i class="fa-solid fa-shield-check"></i>
                                <span>Corrected (2026 Live Reality)</span>
                            </span>
                            <div class="text-zinc-100 leading-relaxed text-[11px] font-sans">${escapeHtml(report.updated_text)}</div>
                        </div>
                    </div>
                </div>

                <!-- Tab Content 2: Live Citations (Hidden initially) -->
                <div id="tab-sources-${reportId}" class="tab-pane hidden space-y-2">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                        ${report.claims.flatMap(c => c.evidence || []).map(ev => `
                            <a href="${ev.url}" target="_blank" class="p-2.5 rounded-xl bg-surface-950 border border-white/5 hover:border-cyan-500/40 transition-all block group">
                                <div class="text-[11px] font-semibold text-cyan-300 group-hover:underline truncate">${escapeHtml(ev.title || ev.domain)}</div>
                                <div class="text-[10px] font-mono text-zinc-500 truncate">${escapeHtml(ev.url)}</div>
                                <p class="text-[10px] text-zinc-400 line-clamp-2 mt-1 leading-snug">${escapeHtml(ev.snippet)}</p>
                            </a>
                        `).join('')}
                    </div>
                </div>

                <!-- Tab Content 3: Telemetry (Hidden initially) -->
                <div id="tab-telemetry-${reportId}" class="tab-pane hidden">
                    <div class="p-3 rounded-xl bg-surface-950 border border-white/5 text-[11px] font-mono space-y-1 text-zinc-400">
                        <div>Latency: <span class="text-white">${report.latency_seconds}s</span></div>
                        <div>Gateway: <span class="text-white">${report.gateway_provider}</span></div>
                        <div>Model: <span class="text-white">${report.model_name}</span></div>
                        <div>Total Claims Extracted: <span class="text-white">${report.total_claims}</span></div>
                    </div>
                </div>
            </div>

            <!-- Bottom Action Toolbar -->
            <div class="flex flex-wrap items-center justify-between pt-2 border-t border-white/5 text-xs gap-2">
                <div class="flex items-center space-x-2">
                    <!-- Audio Voiceover Button with Animated Waveform -->
                    <button id="audio-btn-${reportId}" class="px-3 py-1.5 rounded-xl bg-cyan-500/10 hover:bg-cyan-500/20 border border-cyan-500/30 text-cyan-300 hover:text-cyan-200 text-xs font-semibold flex items-center space-x-2 transition-all" onclick="toggleVoiceover('${reportId}')">
                        <i class="fa-solid fa-volume-high text-xs"></i>
                        <span>Listen Audio Briefing</span>
                        <div id="wave-${reportId}" class="hidden flex items-center space-x-0.5 ml-1">
                            <span class="wave-bar"></span>
                            <span class="wave-bar"></span>
                            <span class="wave-bar"></span>
                            <span class="wave-bar"></span>
                        </div>
                    </button>

                    <button class="px-2.5 py-1.5 rounded-xl bg-white/5 hover:bg-white/10 text-zinc-300 hover:text-white text-xs font-medium flex items-center space-x-1.5 transition-colors" onclick="copyVerifiedText('${reportId}')">
                        <i class="fa-regular fa-copy text-xs"></i>
                        <span>Copy</span>
                    </button>
                </div>

                <div class="flex items-center space-x-2 text-[10px] font-mono text-zinc-500">
                    <button class="hover:text-zinc-300 transition-colors" onclick="copyJsonReport('${reportId}')">JSON</button>
                    <span>·</span>
                    <button class="hover:text-zinc-300 transition-colors" onclick="exportMarkdown('${reportId}')">Markdown</button>
                </div>
            </div>

        </div>
    `;

    wrapper.appendChild(bubble);
    scrollChatToBottom();
}

// --- TAB SWITCHER FOR REPORT CARD ---
window.switchReportTab = function(reportId, tabName, btn) {
    const parent = btn.closest('.space-y-4') || btn.parentElement.parentElement;
    parent.querySelectorAll('.tab-btn').forEach(b => {
        b.classList.remove('bg-white/10', 'text-white', 'font-semibold');
        b.classList.add('text-zinc-400');
    });
    btn.classList.add('bg-white/10', 'text-white', 'font-semibold');
    btn.classList.remove('text-zinc-400');

    parent.querySelectorAll('.tab-pane').forEach(p => p.classList.add('hidden'));
    const target = parent.querySelector(`#tab-${tabName}-${reportId}`);
    if (target) {
        target.classList.remove('hidden');
    }
};

// --- AUDIO VOICEOVER NARRATION ---
window.toggleVoiceover = function(reportId) {
    const report = window[reportId];
    if (!report || !('speechSynthesis' in window)) {
        showToast("Speech synthesis not supported in this browser.");
        return;
    }

    const wave = document.getElementById(`wave-${reportId}`);

    if (isSpeaking) {
        window.speechSynthesis.cancel();
        isSpeaking = false;
        if (wave) wave.classList.add("hidden");
        showToast("Audio stopped");
        return;
    }

    // Build plain English briefing for instant audio comprehension
    let briefing = `FreshGuard audit complete. Freshness score: ${Math.round(report.overall_freshness_score)} percent. `;
    const staleClaims = report.claims.filter(c => c.status === "stale");
    if (staleClaims.length > 0) {
        briefing += `Warning: Found ${staleClaims.length} outdated claim. `;
        staleClaims.forEach((c, idx) => {
            briefing += `Point ${idx + 1}: The claim "${c.claim.text}" is outdated. Current 2026 reality is: ${c.current_value_correction || c.reasoning}. `;
        });
    } else {
        briefing += `All assertions verified accurate against 2026 live web sources. `;
    }

    const utterance = new SpeechSynthesisUtterance(briefing);
    utterance.rate = 1.05;
    utterance.pitch = 1.0;

    utterance.onstart = () => {
        isSpeaking = true;
        if (wave) wave.classList.remove("hidden");
    };

    utterance.onend = () => {
        isSpeaking = false;
        if (wave) wave.classList.add("hidden");
    };

    utterance.onerror = () => {
        isSpeaking = false;
        if (wave) wave.classList.add("hidden");
    };

    window.speechSynthesis.speak(utterance);
    showToast("Playing audio briefing...");
};

// --- ERROR BUBBLE ---
function appendErrorBubble(msg) {
    const wrapper = document.getElementById("messages-wrapper");
    const bubble = document.createElement("div");
    bubble.className = "flex space-x-3 text-xs sm:text-sm chat-bubble-animate";
    bubble.innerHTML = `
        <div class="w-8 h-8 rounded-xl bg-rose-900/30 border border-rose-500/40 flex items-center justify-center flex-shrink-0 text-rose-400 mt-0.5">
            <i class="fa-solid fa-triangle-exclamation text-xs"></i>
        </div>
        <div class="bg-surface-900 border border-rose-500/30 text-rose-200 rounded-2xl rounded-tl-sm p-4 max-w-xl text-xs space-y-1">
            <strong class="font-bold text-rose-400 block">Verification Request Failed:</strong>
            <p>${escapeHtml(msg)}</p>
        </div>
    `;
    wrapper.appendChild(bubble);
    scrollChatToBottom();
}

function scrollChatToBottom() {
    const stream = document.getElementById("chat-stream");
    if (stream) {
        stream.scrollTop = stream.scrollHeight;
    }
}

// --- NEW AUDIT RESET ---
function resetToNewAudit() {
    const messages = document.getElementById("messages-wrapper");
    const welcome = document.getElementById("welcome-state");
    const titleEl = document.getElementById("current-audit-title");
    const chatInput = document.getElementById("chat-input");

    if (window.speechSynthesis) {
        window.speechSynthesis.cancel();
        isSpeaking = false;
    }

    if (messages) messages.innerHTML = "";
    if (welcome) welcome.classList.remove("hidden");
    if (titleEl) titleEl.textContent = "Live Verification Terminal";
    if (chatInput) {
        chatInput.value = "";
        chatInput.focus();
    }
    showToast("Started new audit session");
}

// --- COPY & EXPORT UTILITIES ---
window.copyVerifiedText = function(reportId) {
    const report = window[reportId];
    if (!report) return;
    navigator.clipboard.writeText(report.updated_text).then(() => {
        showToast("Copied verified answer to clipboard!");
    });
};

window.copyJsonReport = function(reportId) {
    const report = window[reportId];
    if (!report) return;
    navigator.clipboard.writeText(JSON.stringify(report, null, 2)).then(() => {
        showToast("Copied full JSON report to clipboard!");
    });
};

window.exportMarkdown = function(reportId) {
    const report = window[reportId];
    if (!report) return;

    let md = `# FreshGuard AI Verification Report\n\n`;
    md += `**Overall Freshness Score:** ${Math.round(report.overall_freshness_score)}%\n`;
    md += `**Summary:** ${report.summary}\n\n`;
    md += `## Verified 2026 Ground Truth\n${report.updated_text}\n\n`;
    md += `## Claims Breakdown\n`;
    report.claims.forEach((c, idx) => {
        md += `### ${idx+1}. ${c.claim.text}\n`;
        md += `- **Status:** ${c.status.toUpperCase()}\n`;
        md += `- **Category:** ${c.claim.category}\n`;
        md += `- **Reasoning:** ${c.reasoning}\n`;
        if (c.current_value_correction) {
            md += `- **2026 Correction:** ${c.current_value_correction}\n`;
        }
        md += `\n`;
    });
    md += `---\n*Generated by FreshGuard AI — Team SOL CULTURE (Adithya R Kulkarni & Manisha M Kulkarni)*\n`;

    const blob = new Blob([md], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `FreshGuard_Audit_${Date.now()}.md`;
    a.click();
    URL.revokeObjectURL(url);
    showToast("Downloaded Markdown audit report");
};

// --- SIDEBAR HISTORY MANAGEMENT ---
async function loadSidebarHistory() {
    try {
        const res = await fetch(`/api/history?user_id=${DEFAULT_USER_ID}&filter_type=all`);
        if (res.ok) {
            historyRecords = await res.json();
            renderSidebarHistory();
        }
    } catch (e) {
        console.error("Failed to load history", e);
    }
}

function renderSidebarHistory(searchQuery = "") {
    const container = document.getElementById("sidebar-history-list");
    if (!container) return;

    let filtered = historyRecords;

    if (activeFilter === "starred") {
        filtered = filtered.filter(item => item.is_starred);
    } else if (activeFilter === "archived") {
        filtered = filtered.filter(item => item.is_archived);
    } else if (activeFilter === "active") {
        filtered = filtered.filter(item => !item.is_archived);
    }

    if (searchQuery) {
        filtered = filtered.filter(item => 
            (item.input_text && item.input_text.toLowerCase().includes(searchQuery)) ||
            (item.summary && item.summary.toLowerCase().includes(searchQuery))
        );
    }

    if (filtered.length === 0) {
        container.innerHTML = `
            <div class="text-center py-8 text-zinc-500 space-y-1">
                <i class="fa-regular fa-folder-open text-base"></i>
                <p class="text-[11px]">No audits found</p>
            </div>
        `;
        return;
    }

    container.innerHTML = filtered.map(item => {
        const score = Math.round(item.overall_freshness_score);
        let scoreDot = "bg-rose-400";
        if (score >= 80) scoreDot = "bg-emerald-400";
        else if (score >= 50) scoreDot = "bg-amber-400";

        const textPreview = item.input_text.length > 36 ? item.input_text.substring(0, 36) + "..." : item.input_text;

        return `
            <div class="group relative flex items-center justify-between p-2 rounded-xl hover:bg-white/5 transition-all cursor-pointer border border-transparent hover:border-white/5" onclick="loadHistoryItem('${item.id}')">
                <div class="flex items-center space-x-2 overflow-hidden pr-2">
                    <span class="w-2 h-2 rounded-full ${scoreDot} flex-shrink-0"></span>
                    <span class="text-xs text-zinc-300 group-hover:text-white truncate">${escapeHtml(textPreview)}</span>
                </div>

                <div class="flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0" onclick="event.stopPropagation()">
                    <button class="p-1 hover:text-amber-400 transition-colors" title="Star" onclick="toggleStarItem('${item.id}')">
                        <i class="fa-${item.is_starred ? 'solid' : 'regular'} fa-star text-[10px] ${item.is_starred ? 'text-amber-400' : 'text-zinc-500'}"></i>
                    </button>
                    <button class="p-1 hover:text-cyan-400 transition-colors" title="Archive" onclick="toggleArchiveItem('${item.id}')">
                        <i class="fa-solid fa-box-archive text-[10px] ${item.is_archived ? 'text-cyan-400' : 'text-zinc-500'}"></i>
                    </button>
                    <button class="p-1 hover:text-rose-400 transition-colors" title="Delete" onclick="deleteHistoryItem('${item.id}')">
                        <i class="fa-regular fa-trash-can text-[10px] text-zinc-500 hover:text-rose-400"></i>
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

async function loadHistoryItem(historyId) {
    try {
        const res = await fetch(`/api/history/${historyId}`);
        if (res.ok) {
            const report = await res.json();
            const welcome = document.getElementById("welcome-state");
            const wrapper = document.getElementById("messages-wrapper");
            if (welcome) welcome.classList.add("hidden");
            if (wrapper) wrapper.innerHTML = "";

            appendUserBubble(report.input_text);
            appendDecryptedAssistantBubble(report);

            const titleEl = document.getElementById("current-audit-title");
            if (titleEl) {
                titleEl.textContent = report.input_text.substring(0, 35) + "...";
            }
        }
    } catch (e) {
        showToast("Failed to load historical audit");
    }
}

async function toggleStarItem(historyId) {
    try {
        await fetch(`/api/history/${historyId}/star?user_id=${DEFAULT_USER_ID}`, { method: "PUT" });
        loadSidebarHistory();
    } catch (e) {
        console.error(e);
    }
}

async function toggleArchiveItem(historyId) {
    try {
        await fetch(`/api/history/${historyId}/archive?user_id=${DEFAULT_USER_ID}`, { method: "PUT" });
        loadSidebarHistory();
    } catch (e) {
        console.error(e);
    }
}

async function deleteHistoryItem(historyId) {
    try {
        await fetch(`/api/history/${historyId}?user_id=${DEFAULT_USER_ID}`, { method: "DELETE" });
        loadSidebarHistory();
        showToast("Deleted audit record");
    } catch (e) {
        console.error(e);
    }
}

// --- UTILITIES ---
function showToast(msg) {
    const toast = document.getElementById("toast");
    const toastText = document.getElementById("toast-text");
    if (!toast || !toastText) return;

    toastText.textContent = msg;
    toast.classList.remove("translate-y-[-100px]", "opacity-0");
    toast.classList.add("translate-y-0", "opacity-100");

    setTimeout(() => {
        toast.classList.remove("translate-y-0", "opacity-100");
        toast.classList.add("translate-y-[-100px]", "opacity-0");
    }, 2800);
}

function escapeHtml(str) {
    if (!str) return "";
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
