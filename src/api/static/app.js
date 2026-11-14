// FreshGuard AI — Enterprise Client Application

let currentReport = null;
let currentUser = {
    userId: "user_demo",
    name: "Demo Account",
    email: "demo@freshguard.ai",
    picture: "https://api.dicebear.com/7.x/initials/svg?seed=Demo"
};

document.addEventListener("DOMContentLoaded", () => {
    initGoogleAuth();
    loadHistory();
    setupEventListeners();
});

// --- GOOGLE AUTHENTICATION ---
function initGoogleAuth() {
    const saved = localStorage.getItem("fg_user_session");
    if (saved) {
        try {
            currentUser = JSON.parse(saved);
        } catch (e) {}
    }
    updateAuthUI();
}

function updateAuthUI() {
    const signInBtn = document.getElementById("google-sign-in-btn");
    const profileView = document.getElementById("google-profile-view");
    const avatarImg = document.getElementById("user-avatar");
    const userNameSpan = document.getElementById("user-name");

    const isLoggedIn = currentUser.userId && currentUser.userId !== "user_demo";

    if (isLoggedIn) {
        if (signInBtn) signInBtn.classList.add("hidden");
        if (profileView) profileView.classList.remove("hidden");
        if (avatarImg) avatarImg.src = currentUser.picture || `https://api.dicebear.com/7.x/initials/svg?seed=${currentUser.name}`;
        if (userNameSpan) userNameSpan.textContent = currentUser.name || currentUser.email;
    } else {
        if (signInBtn) signInBtn.classList.remove("hidden");
        if (profileView) profileView.classList.add("hidden");
    }
}

async function handleGoogleSignIn() {
    // Authenticate with Google
    try {
        const res = await fetch("/api/auth/google", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                email: "adithya@gmail.com",
                name: "Adithya",
                picture: "https://api.dicebear.com/7.x/initials/svg?seed=Adithya"
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
            localStorage.setItem("fg_user_session", JSON.stringify(currentUser));
            updateAuthUI();
            loadHistory();
            showToast(`Signed in as ${currentUser.name}`);
        }
    } catch (e) {
        console.error("Sign in error", e);
    }
}

function handleGoogleSignOut() {
    currentUser = {
        userId: "user_demo",
        name: "Demo Account",
        email: "demo@freshguard.ai",
        picture: "https://api.dicebear.com/7.x/initials/svg?seed=Demo"
    };
    localStorage.removeItem("fg_user_session");
    updateAuthUI();
    loadHistory();
    showToast("Signed out");
}

// --- SETUP EVENT LISTENERS ---
function setupEventListeners() {
    const inputEl = document.getElementById("input-text");
    const counterEl = document.getElementById("char-counter");
    if (inputEl && counterEl) {
        inputEl.addEventListener("input", () => {
            counterEl.textContent = `${inputEl.value.length} characters`;
        });

        // Keyboard shortcut: Ctrl+Enter / Cmd+Enter to run verification
        inputEl.addEventListener("keydown", (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
                e.preventDefault();
                runVerification();
            }
        });
    }

    // Buttons
    const verifyBtn = document.getElementById("verify-btn");
    const clearBtn = document.getElementById("clear-btn");
    const copyTextBtn = document.getElementById("copy-text-btn");
    const copyJsonBtn = document.getElementById("copy-json-btn");
    const signInBtn = document.getElementById("google-sign-in-btn");
    const signOutBtn = document.getElementById("google-sign-out-btn");

    if (verifyBtn) verifyBtn.addEventListener("click", runVerification);
    if (signInBtn) signInBtn.addEventListener("click", handleGoogleSignIn);
    if (signOutBtn) signOutBtn.addEventListener("click", handleGoogleSignOut);

    if (clearBtn) {
        clearBtn.addEventListener("click", () => {
            inputEl.value = "";
            counterEl.textContent = "0 characters";
            document.getElementById("results-container").classList.add("hidden");
        });
    }

    if (copyTextBtn) {
        copyTextBtn.addEventListener("click", () => {
            if (currentReport) {
                navigator.clipboard.writeText(currentReport.updated_text);
                showToast("Copied to clipboard");
            }
        });
    }

    if (copyJsonBtn) {
        copyJsonBtn.addEventListener("click", () => {
            if (currentReport) {
                navigator.clipboard.writeText(JSON.stringify(currentReport, null, 2));
                showToast("JSON report copied");
            }
        });
    }

    // History drawer controls
    const openHistoryBtn = document.getElementById("open-history-btn");
    const closeHistoryBtn = document.getElementById("close-history-btn");
    const historyOverlay = document.getElementById("history-drawer-overlay");
    const clearHistoryBtn = document.getElementById("clear-history-btn");

    if (openHistoryBtn) openHistoryBtn.addEventListener("click", openHistoryDrawer);
    if (closeHistoryBtn) closeHistoryBtn.addEventListener("click", closeHistoryDrawer);
    if (historyOverlay) {
        historyOverlay.addEventListener("click", (e) => {
            if (e.target === historyOverlay) closeHistoryDrawer();
        });
    }
    if (clearHistoryBtn) clearHistoryBtn.addEventListener("click", clearHistory);
}

// --- VERIFICATION PIPELINE ---
async function runVerification() {
    const text = document.getElementById("input-text").value.trim();
    if (!text || text.length < 5) {
        showToast("Enter at least 5 characters to verify");
        return;
    }

    const verifyBtn = document.getElementById("verify-btn");
    const verifyBtnText = document.getElementById("verify-btn-text");
    const loadingState = document.getElementById("loading-state");
    const resultsContainer = document.getElementById("results-container");

    verifyBtn.disabled = true;
    verifyBtnText.textContent = "Verifying...";
    loadingState.classList.remove("hidden");
    resultsContainer.classList.add("hidden");

    // Linear progress animation
    const loadInterval = startLoadingAnimation();
    const searchDepth = document.getElementById("deep-search-toggle").checked ? "advanced" : "basic";

    try {
        const response = await fetch("/api/verify", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                text: text,
                search_depth: searchDepth,
                user_id: currentUser.userId
            })
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || "Verification failed");
        }

        const report = await response.json();
        currentReport = report;
        renderResults(report);
        loadHistory();
    } catch (err) {
        alert("Error during verification: " + err.message);
    } finally {
        clearInterval(loadInterval);
        verifyBtn.disabled = false;
        verifyBtnText.textContent = "Verify Freshness";
        loadingState.classList.add("hidden");
    }
}

function startLoadingAnimation() {
    const msgEl = document.getElementById("loading-message");
    const barEl = document.getElementById("loading-bar");

    const messages = [
        { text: "Deconstructing assertions & volatility index...", width: "25%" },
        { text: "Cross-referencing live web consensus via Tavily...", width: "55%" },
        { text: "Evaluating contradictions & freshness score...", width: "80%" },
        { text: "Synthesizing verified output...", width: "95%" }
    ];

    let step = 0;
    barEl.style.width = "10%";

    const interval = setInterval(() => {
        if (step < messages.length) {
            msgEl.textContent = messages[step].text;
            barEl.style.width = messages[step].width;
            step++;
        }
    }, 1200);

    return interval;
}

// --- RENDER RESULTS ---
function renderResults(report) {
    const resultsContainer = document.getElementById("results-container");
    resultsContainer.classList.remove("hidden");

    const score = report.overall_freshness_score;
    const scoreText = document.getElementById("score-text");
    const scoreBadge = document.getElementById("score-badge");

    scoreText.textContent = `${score}%`;

    if (score >= 80) {
        scoreBadge.className = "text-[10px] px-2 py-0.5 rounded font-mono font-medium uppercase bg-emerald-500/10 text-emerald-400 border border-emerald-500/20";
        scoreBadge.textContent = "Verified Fresh";
    } else if (score >= 50) {
        scoreBadge.className = "text-[10px] px-2 py-0.5 rounded font-mono font-medium uppercase bg-amber-500/10 text-amber-400 border border-amber-500/20";
        scoreBadge.textContent = "Partially Stale";
    } else {
        scoreBadge.className = "text-[10px] px-2 py-0.5 rounded font-mono font-medium uppercase bg-red-500/10 text-red-400 border border-red-500/20";
        scoreBadge.textContent = "Stale Claims Detected";
    }

    document.getElementById("summary-text").textContent = report.summary;

    renderDiff(report);
    renderClaims(report.claims);

    resultsContainer.scrollIntoView({ behavior: "smooth", block: "start" });
}

function renderDiff(report) {
    let originalHtml = report.input_text;
    
    report.claims.forEach(c => {
        if (c.status === "stale" && c.claim && c.claim.text) {
            const staleText = c.claim.text;
            if (originalHtml.includes(staleText)) {
                originalHtml = originalHtml.replace(
                    staleText,
                    `<span class="stale-highlight" title="Outdated: ${escapeHtml(c.stale_delta || c.reasoning)}">${escapeHtml(staleText)}</span>`
                );
            }
        }
    });

    document.getElementById("diff-original-box").innerHTML = originalHtml;
    document.getElementById("diff-updated-box").innerHTML = `<span class="text-zinc-100">${escapeHtml(report.updated_text)}</span>`;
}

function renderClaims(claims) {
    const container = document.getElementById("claims-list");
    container.innerHTML = "";

    claims.forEach((item, idx) => {
        const claim = item.claim;
        const card = document.createElement("div");
        card.className = "bg-surface-900 border border-zinc-800 rounded-lg p-4 space-y-2.5 text-xs";

        let statusBadge = "";
        if (item.status === "stale") {
            statusBadge = `<span class="px-2 py-0.5 rounded bg-red-500/10 text-red-400 border border-red-500/20 font-mono text-[10px] uppercase font-medium">Stale</span>`;
        } else if (item.status === "fresh") {
            statusBadge = `<span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono text-[10px] uppercase font-medium">Fresh</span>`;
        } else if (item.status === "evergreen") {
            statusBadge = `<span class="px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20 font-mono text-[10px] uppercase font-medium">Evergreen</span>`;
        } else {
            statusBadge = `<span class="px-2 py-0.5 rounded bg-zinc-800 text-zinc-400 border border-zinc-700 font-mono text-[10px] uppercase font-medium">Unverified</span>`;
        }

        let correctionHtml = "";
        if (item.status === "stale") {
            correctionHtml = `
                <div class="p-3 rounded bg-red-500/5 border border-red-500/20 space-y-1.5 text-xs">
                    <div class="text-red-400 font-medium">Outdated: ${escapeHtml(item.stale_delta || item.reasoning)}</div>
                    ${item.current_value_correction ? `
                        <div class="text-emerald-400 font-medium pt-1 border-t border-red-500/15">Correction: ${escapeHtml(item.current_value_correction)}</div>
                    ` : ""}
                </div>
            `;
        }

        let evidenceHtml = "";
        if (item.evidence && item.evidence.length > 0) {
            const evItems = item.evidence.map(ev => `
                <a href="${ev.url}" target="_blank" class="block p-2 rounded bg-surface-950 border border-zinc-800 hover:border-zinc-700 transition-colors">
                    <div class="flex items-center justify-between text-[11px] text-zinc-300 font-medium mb-0.5">
                        <span class="hover:underline truncate max-w-[260px]">${escapeHtml(ev.title)}</span>
                        <span class="text-zinc-500 text-[10px] font-mono">${escapeHtml(ev.domain)}</span>
                    </div>
                    <p class="text-zinc-500 text-[10px] line-clamp-1">${escapeHtml(ev.snippet)}</p>
                </a>
            `).join("");

            evidenceHtml = `
                <div class="space-y-1.5 pt-1">
                    <span class="text-[10px] font-mono uppercase text-zinc-500 block">Sources (${item.evidence.length}):</span>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">${evItems}</div>
                </div>
            `;
        }

        card.innerHTML = `
            <div class="flex items-center justify-between border-b border-zinc-800/80 pb-2">
                <div class="flex items-center space-x-2">
                    <span class="text-[10px] font-mono text-zinc-500">#${idx+1}</span>
                    <span class="text-[10px] font-mono uppercase px-1.5 py-0.5 rounded bg-surface-950 border border-zinc-800 text-zinc-400">${claim.category}</span>
                    ${statusBadge}
                </div>
                <span class="text-[10px] font-mono text-zinc-500">Volatility: ${Math.round(claim.time_volatility_score * 100)}%</span>
            </div>

            <div class="text-zinc-100 font-medium leading-relaxed">
                "${escapeHtml(claim.text)}"
            </div>

            <p class="text-zinc-400 leading-relaxed bg-surface-950 p-2.5 rounded border border-zinc-800/80">
                ${escapeHtml(item.reasoning)}
            </p>

            ${correctionHtml}
            ${evidenceHtml}
        `;

        container.appendChild(card);
    });
}

// --- HISTORY DRAWER MANAGEMENT ---
async function loadHistory() {
    try {
        const res = await fetch(`/api/history?user_id=${currentUser.userId}`);
        if (res.ok) {
            const items = await res.json();
            const badge = document.getElementById("history-badge");
            const countText = document.getElementById("history-count-text");
            if (badge) badge.textContent = items.length;
            if (countText) countText.textContent = `${items.length} items`;
            renderHistoryItems(items);
        }
    } catch (e) {
        console.warn("Could not load history", e);
    }
}

function renderHistoryItems(items) {
    const container = document.getElementById("history-items-container");
    if (!container) return;
    container.innerHTML = "";

    if (!items || items.length === 0) {
        container.innerHTML = `<div class="text-center py-8 text-zinc-500 text-xs font-mono">No previous records</div>`;
        return;
    }

    items.forEach(item => {
        const row = document.createElement("div");
        row.className = "p-2.5 rounded-lg bg-surface-900 border border-zinc-800 hover:border-zinc-700 transition-colors cursor-pointer space-y-1";
        
        const isStale = item.stale_count > 0;
        const badgeColor = isStale ? "text-red-400 bg-red-500/10 border-red-500/20" : "text-emerald-400 bg-emerald-500/10 border-emerald-500/20";
        const dateStr = new Date(item.created_at * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        row.innerHTML = `
            <div class="flex items-center justify-between text-[10px] font-mono">
                <span class="px-1.5 py-0.2 rounded border ${badgeColor}">${item.overall_freshness_score}% Fresh</span>
                <span class="text-zinc-500">${dateStr}</span>
            </div>
            <p class="text-xs text-zinc-300 line-clamp-2 leading-relaxed">${escapeHtml(item.input_text)}</p>
        `;

        row.addEventListener("click", () => {
            loadHistoryDetail(item.id);
            closeHistoryDrawer();
        });

        container.appendChild(row);
    });
}

async function loadHistoryDetail(historyId) {
    try {
        const res = await fetch(`/api/history/${historyId}`);
        if (res.ok) {
            const report = await res.json();
            currentReport = report;
            document.getElementById("input-text").value = report.input_text;
            renderResults(report);
            showToast("Loaded past record");
        }
    } catch (e) {
        showToast("Failed to load item");
    }
}

function openHistoryDrawer() {
    const overlay = document.getElementById("history-drawer-overlay");
    const drawer = document.getElementById("history-drawer");
    overlay.classList.remove("hidden");
    setTimeout(() => {
        drawer.classList.remove("translate-x-full");
    }, 10);
}

function closeHistoryDrawer() {
    const overlay = document.getElementById("history-drawer-overlay");
    const drawer = document.getElementById("history-drawer");
    drawer.classList.add("translate-x-full");
    setTimeout(() => {
        overlay.classList.add("hidden");
    }, 250);
}

async function clearHistory() {
    try {
        await fetch(`/api/history?user_id=${currentUser.userId}`, { method: "DELETE" });
        loadHistory();
        showToast("History cleared");
    } catch (e) {
        showToast("Error clearing history");
    }
}

function showToast(msg) {
    const toast = document.createElement("div");
    toast.className = "fixed bottom-5 right-5 bg-zinc-800 text-zinc-100 border border-zinc-700 px-3.5 py-2 rounded-lg shadow-lg text-xs font-medium z-50 transition-opacity";
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2000);
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
