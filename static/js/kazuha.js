/**
 * kazuha.js
 * Kaedehara Kazuha SQL Sanctuary Client Application
 * Features:
 * 1. Client-Side VS Code-like SQL IntelliSense Autocomplete (Pure JS, No AI)
 * 2. Interactive Canvas Maple Leaves Physics Animation
 * 3. Query Execution, Table Rendering, CSV/JSON Exports
 * 4. Dynamic Schema Explorer & Visual ER Architecture
 * 5. Kazuha's Master SQL Anthology Showcase
 */

// Global State
let schemaCache = null;
let activeAutocompleteIndex = 0;
let currentAutocompleteMatches = [];
let queryResultsCache = { columns: [], rows: [] };

// Default Keywords & Functions
const SQL_KEYWORDS = [
    "SELECT", "FROM", "WHERE", "JOIN", "INNER JOIN", "LEFT JOIN", "ON",
    "GROUP BY", "ORDER BY", "HAVING", "LIMIT", "OFFSET", "WITH", "AS",
    "OVER", "PARTITION BY", "ROW_NUMBER()", "RANK()", "DENSE_RANK()",
    "CASE", "WHEN", "THEN", "ELSE", "END", "AND", "OR", "NOT",
    "LIKE", "IN", "BETWEEN", "IS NULL", "IS NOT NULL", "DISTINCT", "DESC", "ASC"
];

const SQL_FUNCTIONS = [
    "COUNT(*)", "AVG()", "SUM()", "MIN()", "MAX()", "ROUND()", "COALESCE()",
    "ROW_NUMBER() OVER ()", "RANK() OVER ()", "DENSE_RANK() OVER ()"
];

// Initialize on DOM Ready
document.addEventListener("DOMContentLoaded", () => {
    initNavigationTabs();
    initMapleLeavesCanvas();
    fetchSchemaMetadata();
    fetchShowcaseQueries();
    initSqlEditorAutocomplete();
    initQueryExecution();
    initSnippetsRibbon();
});

/* ==========================================================================
   1. NAVIGATION TABS
   ========================================================================== */
function initNavigationTabs() {
    const tabButtons = document.querySelectorAll(".tab-btn");
    tabButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const targetId = btn.getAttribute("data-tab");
            
            tabButtons.forEach(b => b.classList.remove("active"));
            document.querySelectorAll(".tab-pane").forEach(pane => pane.classList.remove("active"));

            btn.classList.add("active");
            const targetPane = document.getElementById(targetId);
            if (targetPane) targetPane.classList.add("active");
        });
    });
}

/* ==========================================================================
   2. MAPLE LEAVES PARTICLE SIMULATION (CANVAS)
   ========================================================================== */
function initMapleLeavesCanvas() {
    const canvas = document.getElementById("maple-canvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;

    window.addEventListener("resize", () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    });

    let leavesEnabled = true;
    const toggleBtn = document.getElementById("toggle-leaves-btn");
    if (toggleBtn) {
        toggleBtn.addEventListener("click", () => {
            leavesEnabled = !leavesEnabled;
            toggleBtn.style.opacity = leavesEnabled ? "1" : "0.4";
            if (!leavesEnabled) ctx.clearRect(0, 0, width, height);
        });
    }

    const leafColors = [
        "rgba(211, 62, 56, 0.75)",   // Maple Red
        "rgba(235, 87, 87, 0.7)",    // Crimson
        "rgba(229, 169, 83, 0.75)",  // Autumn Gold
        "rgba(242, 201, 125, 0.65)", // Warm Amber
        "rgba(184, 45, 39, 0.8)"     // Deep Rust Red
    ];

    class Leaf {
        constructor() {
            this.reset(true);
        }

        reset(initial = false) {
            this.x = Math.random() * width;
            this.y = initial ? Math.random() * height : -30;
            this.size = 9 + Math.random() * 12;
            this.speedY = 0.8 + Math.random() * 1.4;
            this.speedX = -0.5 + Math.random() * 1.5;
            this.angle = Math.random() * Math.PI * 2;
            this.rotationSpeed = (Math.random() - 0.5) * 0.03;
            this.oscillationSpeed = 0.02 + Math.random() * 0.03;
            this.color = leafColors[Math.floor(Math.random() * leafColors.length)];
        }

        update() {
            this.y += this.speedY;
            this.x += this.speedX + Math.sin(this.y * this.oscillationSpeed) * 0.8;
            this.angle += this.rotationSpeed;

            if (this.y > height + 40 || this.x < -40 || this.x > width + 40) {
                this.reset();
            }
        }

        draw() {
            ctx.save();
            ctx.translate(this.x, this.y);
            ctx.rotate(this.angle);

            ctx.fillStyle = this.color;
            ctx.beginPath();
            // Stylized 3-point maple silhouette
            const s = this.size;
            ctx.moveTo(0, -s);
            ctx.bezierCurveTo(s * 0.8, -s * 0.5, s * 0.9, s * 0.3, 0, s);
            ctx.bezierCurveTo(-s * 0.9, s * 0.3, -s * 0.8, -s * 0.5, 0, -s);
            ctx.fill();

            ctx.restore();
        }
    }

    const leaves = Array.from({ length: 32 }, () => new Leaf());

    function renderLeaves() {
        if (leavesEnabled) {
            ctx.clearRect(0, 0, width, height);
            leaves.forEach(leaf => {
                leaf.update();
                leaf.draw();
            });
        }
        requestAnimationFrame(renderLeaves);
    }
    renderLeaves();
}

/* ==========================================================================
   3. SCHEMA & SHOWCASE API INTEGRATION
   ========================================================================== */
async function fetchSchemaMetadata() {
    try {
        const res = await fetch("/api/schema");
        schemaCache = await res.json();
        
        // Update header badges
        if (schemaCache.characters) document.getElementById("stat-chars").textContent = schemaCache.characters.row_count;
        if (schemaCache.weapons) document.getElementById("stat-weapons").textContent = schemaCache.weapons.row_count;
        if (schemaCache.artifact_sets) document.getElementById("stat-artifacts").textContent = schemaCache.artifact_sets.row_count;
        if (schemaCache.character_builds) document.getElementById("stat-builds").textContent = schemaCache.character_builds.row_count;

        // Update ER node row badges
        document.getElementById("er-count-characters").textContent = `${schemaCache.characters.row_count} rows`;
        document.getElementById("er-count-weapons").textContent = `${schemaCache.weapons.row_count} rows`;
        document.getElementById("er-count-artifacts").textContent = `${schemaCache.artifact_sets.row_count} rows`;
        document.getElementById("er-count-builds").textContent = `${schemaCache.character_builds.row_count} rows`;

        renderSchemaExplorer();
    } catch (err) {
        console.error("Failed to load schema metadata:", err);
    }
}

async function fetchShowcaseQueries() {
    try {
        const res = await fetch("/api/samples");
        const samples = await res.json();
        renderShowcaseCards(samples);
    } catch (err) {
        console.error("Failed to load showcase queries:", err);
    }
}

/* ==========================================================================
   4. CLIENT-SIDE INTELLISENSE AUTOCOMPLETE (PURE JS, NO AI)
   ========================================================================== */
function initSqlEditorAutocomplete() {
    const textarea = document.getElementById("sql-input");
    const acBox = document.getElementById("autocomplete-box");
    const acList = document.getElementById("autocomplete-list");

    textarea.addEventListener("input", handleEditorInput);
    textarea.addEventListener("keydown", handleEditorKeydown);
    textarea.addEventListener("click", () => hideAutocomplete());

    function getCaretContext() {
        const pos = textarea.selectionStart;
        const text = textarea.value.substring(0, pos);
        
        // Extract word/token directly before cursor (supports characters like alphanumeric and dot)
        const match = text.match(/([a-zA-Z0-9_\.]+)$/);
        return {
            token: match ? match[1] : "",
            startPos: match ? pos - match[1].length : pos,
            endPos: pos
        };
    }

    function buildCandidates(token) {
        let pool = [];

        // Check if token has dot access (e.g. `characters.`)
        if (token.includes(".")) {
            const parts = token.split(".");
            const qualifier = parts[0].toLowerCase();
            const colPrefix = parts.slice(1).join(".").toLowerCase();

            // Find matching table in schema
            let matchedTable = null;
            if (schemaCache) {
                if (schemaCache[qualifier]) {
                    matchedTable = qualifier;
                } else {
                    // Check table alias shorthand (c -> characters, w -> weapons, a -> artifact_sets, cb -> character_builds)
                    const aliasMap = {
                        "c": "characters",
                        "w": "weapons",
                        "a": "artifact_sets",
                        "cb": "character_builds"
                    };
                    if (aliasMap[qualifier]) matchedTable = aliasMap[qualifier];
                }
            }

            if (matchedTable && schemaCache[matchedTable]) {
                schemaCache[matchedTable].columns.forEach(col => {
                    pool.push({
                        text: col.name,
                        insertText: col.name,
                        kind: "column",
                        detail: `${matchedTable}.${col.name} (${col.type})`
                    });
                });
            }

            return pool.filter(item => item.text.toLowerCase().startsWith(colPrefix));
        }

        // Standard candidates pool
        // 1. Keywords
        SQL_KEYWORDS.forEach(kw => pool.push({ text: kw, insertText: kw + " ", kind: "keyword", detail: "Keyword" }));
        
        // 2. Functions
        SQL_FUNCTIONS.forEach(fn => pool.push({ text: fn, insertText: fn, kind: "function", detail: "Function" }));

        // 3. Tables & Columns from Schema
        if (schemaCache) {
            Object.keys(schemaCache).forEach(tbl => {
                pool.push({ text: tbl, insertText: tbl + " ", kind: "table", detail: `Table (${schemaCache[tbl].row_count} rows)` });
                schemaCache[tbl].columns.forEach(col => {
                    pool.push({ text: col.name, insertText: col.name, kind: "column", detail: `Column of ${tbl}` });
                });
            });
        }

        const tLower = token.toLowerCase();
        return pool.filter(item => item.text.toLowerCase().includes(tLower)).sort((a, b) => {
            // Rank exact prefix matches higher
            const aPrefix = a.text.toLowerCase().startsWith(tLower);
            const bPrefix = b.text.toLowerCase().startsWith(tLower);
            if (aPrefix && !bPrefix) return -1;
            if (!aPrefix && bPrefix) return 1;
            return a.text.localeCompare(b.text);
        });
    }

    function handleEditorInput() {
        const { token } = getCaretContext();
        if (token.length >= 1) {
            showAutocomplete(token);
        } else {
            hideAutocomplete();
        }
    }

    function showAutocomplete(token) {
        currentAutocompleteMatches = buildCandidates(token);
        if (currentAutocompleteMatches.length === 0) {
            hideAutocomplete();
            return;
        }

        activeAutocompleteIndex = 0;
        renderAutocompleteList();

        // Position autocomplete dropdown neatly under current line
        const caretCoords = getCaretCoordinates(textarea, textarea.selectionStart);
        acBox.style.left = `${Math.min(caretCoords.left + 16, textarea.clientWidth - 300)}px`;
        acBox.style.top = `${caretCoords.top + 24}px`;
        acBox.style.display = "flex";
    }

    function renderAutocompleteList() {
        acList.innerHTML = "";
        currentAutocompleteMatches.slice(0, 15).forEach((item, index) => {
            const li = document.createElement("li");
            li.className = `autocomplete-item ${index === activeAutocompleteIndex ? "active" : ""}`;
            
            let icon = "🔑";
            if (item.kind === "table") icon = "🗄️";
            if (item.kind === "column") icon = "📋";
            if (item.kind === "function") icon = "⚙️";

            li.innerHTML = `
                <div class="ac-match-left">
                    <span class="ac-icon">${icon}</span>
                    <span class="ac-text">${item.text}</span>
                </div>
                <span class="ac-kind ${item.kind}">${item.detail}</span>
            `;

            li.addEventListener("mousedown", (e) => {
                e.preventDefault();
                insertSelectedCandidate(item);
            });

            acList.appendChild(li);
        });
    }

    function handleEditorKeydown(e) {
        // Ctrl+Enter to Run
        if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
            e.preventDefault();
            executeCurrentQuery();
            return;
        }

        // Ctrl+Space to manually trigger autocomplete
        if ((e.ctrlKey || e.metaKey) && e.key === " ") {
            e.preventDefault();
            const { token } = getCaretContext();
            showAutocomplete(token || "");
            return;
        }

        if (acBox.style.display !== "none") {
            if (e.key === "ArrowDown") {
                e.preventDefault();
                activeAutocompleteIndex = (activeAutocompleteIndex + 1) % Math.min(currentAutocompleteMatches.length, 15);
                updateActiveAutocompleteItem();
                return;
            }
            if (e.key === "ArrowUp") {
                e.preventDefault();
                activeAutocompleteIndex = (activeAutocompleteIndex - 1 + Math.min(currentAutocompleteMatches.length, 15)) % Math.min(currentAutocompleteMatches.length, 15);
                updateActiveAutocompleteItem();
                return;
            }
            if (e.key === "Enter" || e.key === "Tab") {
                if (currentAutocompleteMatches.length > 0) {
                    e.preventDefault();
                    insertSelectedCandidate(currentAutocompleteMatches[activeAutocompleteIndex]);
                    return;
                }
            }
            if (e.key === "Escape") {
                hideAutocomplete();
                return;
            }
        }
    }

    function updateActiveAutocompleteItem() {
        const items = acList.querySelectorAll(".autocomplete-item");
        items.forEach((item, idx) => {
            item.classList.toggle("active", idx === activeAutocompleteIndex);
            if (idx === activeAutocompleteIndex) {
                item.scrollIntoView({ block: "nearest" });
            }
        });
    }

    function insertSelectedCandidate(candidate) {
        if (!candidate) return;
        const { token, startPos, endPos } = getCaretContext();

        let textToInsert = candidate.insertText || candidate.text;
        
        // If token had qualifier dot, insert only after dot
        if (token.includes(".")) {
            const dotIdx = token.lastIndexOf(".");
            const realStart = startPos + dotIdx + 1;
            textarea.value = textarea.value.substring(0, realStart) + textToInsert + textarea.value.substring(endPos);
            textarea.selectionStart = textarea.selectionEnd = realStart + textToInsert.length;
        } else {
            textarea.value = textarea.value.substring(0, startPos) + textToInsert + textarea.value.substring(endPos);
            textarea.selectionStart = textarea.selectionEnd = startPos + textToInsert.length;
        }

        hideAutocomplete();
        textarea.focus();
    }

    function hideAutocomplete() {
        acBox.style.display = "none";
    }

    // Helper to estimate cursor coordinates inside textarea
    function getCaretCoordinates(element, position) {
        const text = element.value.substring(0, position);
        const lines = text.split("\n");
        const lineNumber = lines.length;
        const currentLine = lines[lines.length - 1];
        
        // Character width ~8.4px at 14px Fira Code, line height 21px
        const left = Math.min(currentLine.length * 8.4 + 16, element.clientWidth - 200);
        const top = Math.min((lineNumber - 1) * 21 + 16, element.clientHeight - 40);
        return { left, top };
    }
}

/* ==========================================================================
   5. QUERY EXECUTION & RESULTS RENDERING
   ========================================================================== */
function initQueryExecution() {
    const runBtn = document.getElementById("run-btn");
    const clearBtn = document.getElementById("clear-btn");
    const formatBtn = document.getElementById("format-btn");
    const sqlInput = document.getElementById("sql-input");
    const filterInput = document.getElementById("filter-results-input");

    runBtn.addEventListener("click", executeCurrentQuery);
    clearBtn.addEventListener("click", () => {
        sqlInput.value = "";
        sqlInput.focus();
    });
    formatBtn.addEventListener("click", () => {
        // Simple beautifier for SQL
        let val = sqlInput.value.trim();
        const keywords = ["SELECT", "FROM", "WHERE", "INNER JOIN", "LEFT JOIN", "JOIN", "GROUP BY", "ORDER BY", "HAVING", "LIMIT", "WITH"];
        keywords.forEach(kw => {
            const re = new RegExp(`\\b${kw}\\b`, "gi");
            val = val.replace(re, `\n${kw}`);
        });
        sqlInput.value = val.trim();
    });

    filterInput.addEventListener("input", () => {
        filterResultsTable(filterInput.value.toLowerCase());
    });

    // Exports
    document.getElementById("copy-sql-btn").addEventListener("click", () => {
        navigator.clipboard.writeText(sqlInput.value);
        alert("SQL query copied to clipboard!");
    });

    document.getElementById("download-csv-btn").addEventListener("click", exportResultsToCSV);
    document.getElementById("download-json-btn").addEventListener("click", exportResultsToJSON);
}

async function executeCurrentQuery() {
    const sqlInput = document.getElementById("sql-input");
    const statusBadge = document.getElementById("status-badge");
    const resultsContainer = document.getElementById("results-container");
    const resultActions = document.getElementById("result-actions");

    const query = sqlInput.value.trim();
    if (!query) {
        alert("Please enter a SQL query to execute.");
        return;
    }

    statusBadge.textContent = "Executing...";
    statusBadge.className = "status-badge running";

    try {
        const response = await fetch("/api/query", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query })
        });
        const result = await response.json();

        if (result.success) {
            statusBadge.textContent = `✓ ${result.count} rows (${result.execution_time_ms} ms)`;
            statusBadge.className = "status-badge success";
            queryResultsCache = { columns: result.columns, rows: result.rows };
            resultActions.style.display = "flex";
            renderResultsTable(result.columns, result.rows);
        } else {
            statusBadge.textContent = "Query Error";
            statusBadge.className = "status-badge error";
            resultActions.style.display = "none";
            resultsContainer.innerHTML = `
                <div class="error-banner">
                    <div class="error-title">🍁 Wind Disruption: SQLite Operational Error</div>
                    <div class="error-message">${escapeHtml(result.error)}</div>
                </div>
            `;
        }
    } catch (err) {
        statusBadge.textContent = "Network Error";
        statusBadge.className = "status-badge error";
        resultsContainer.innerHTML = `
            <div class="error-banner">
                <div class="error-title">Connection Error</div>
                <div class="error-message">${err.message}</div>
            </div>
        `;
    }
}

function renderResultsTable(columns, rows) {
    const container = document.getElementById("results-container");
    if (!rows || rows.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-leaf">🍃</div>
                <h3>Zero Rows Returned</h3>
                <p>The query executed successfully, but no matching records were found.</p>
            </div>
        `;
        return;
    }

    let html = `<table class="data-table" id="data-table"><thead><tr>`;
    columns.forEach(col => {
        html += `<th>${escapeHtml(col)}</th>`;
    });
    html += `</tr></thead><tbody>`;

    rows.forEach(row => {
        html += `<tr>`;
        row.forEach(val => {
            if (val === null) {
                html += `<td><span class="null-cell">NULL</span></td>`;
            } else {
                html += `<td>${escapeHtml(String(val))}</td>`;
            }
        });
        html += `</tr>`;
    });

    html += `</tbody></table>`;
    container.innerHTML = html;
}

function filterResultsTable(term) {
    const table = document.getElementById("data-table");
    if (!table) return;
    const trs = table.querySelectorAll("tbody tr");
    trs.forEach(tr => {
        const text = tr.textContent.toLowerCase();
        tr.style.display = text.includes(term) ? "" : "none";
    });
}

function exportResultsToCSV() {
    if (!queryResultsCache.rows.length) return;
    let csv = queryResultsCache.columns.join(",") + "\n";
    queryResultsCache.rows.forEach(row => {
        csv += row.map(v => v === null ? "" : `"${String(v).replace(/"/g, '""')}"`).join(",") + "\n";
    });

    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `kazuha_sql_export_${Date.now()}.csv`;
    a.click();
}

function exportResultsToJSON() {
    if (!queryResultsCache.rows.length) return;
    const jsonArr = queryResultsCache.rows.map(row => {
        let obj = {};
        queryResultsCache.columns.forEach((c, idx) => {
            obj[c] = row[idx];
        });
        return obj;
    });

    const blob = new Blob([JSON.stringify(jsonArr, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `kazuha_sql_export_${Date.now()}.json`;
    a.click();
}

/* ==========================================================================
   6. SCHEMA EXPLORER & PREVIEWS
   ========================================================================== */
function renderSchemaExplorer() {
    const container = document.getElementById("schema-accordion");
    if (!container || !schemaCache) return;
    container.innerHTML = "";

    const tableIcons = {
        "characters": "👤",
        "weapons": "🗡️",
        "artifact_sets": "🌸",
        "character_builds": "⚔️"
    };

    Object.keys(schemaCache).forEach((tableName, idx) => {
        const info = schemaCache[tableName];
        const card = document.createElement("div");
        card.className = "schema-table-card";

        let colsHtml = "";
        info.columns.forEach(col => {
            let badge = `<span class="badge ${col.is_pk ? 'pk-badge' : 'req-badge'}">${col.is_pk ? 'PK' : col.notnull ? 'REQ' : ''}</span>`;
            if (!col.is_pk && !col.notnull) badge = "";

            colsHtml += `
                <div class="schema-col-item" data-col="${col.name}" title="Click to insert column into editor">
                    <span>${col.name} ${badge}</span>
                    <span class="col-type">${col.type}</span>
                </div>
            `;
        });

        card.innerHTML = `
            <div class="schema-table-header">
                <div class="schema-title-left">
                    <span>${tableIcons[tableName] || '📁'}</span>
                    <span class="schema-tbl-name">${tableName}</span>
                    <span class="schema-tbl-pill">${info.row_count} rows</span>
                </div>
                <div>
                    <button class="secondary-btn preview-btn" data-table="${tableName}">Preview 10 Rows</button>
                    <span class="accordion-arrow">▼</span>
                </div>
            </div>
            <div class="schema-table-body ${idx === 0 ? 'open' : ''}">
                <div class="schema-cols-grid">${colsHtml}</div>
            </div>
        `;

        // Toggle Accordion
        const header = card.querySelector(".schema-table-header");
        const body = card.querySelector(".schema-table-body");
        header.addEventListener("click", (e) => {
            if (e.target.classList.contains("preview-btn")) return;
            body.classList.toggle("open");
        });

        // Quick Preview
        card.querySelector(".preview-btn").addEventListener("click", (e) => {
            e.stopPropagation();
            const sql = `SELECT * FROM ${tableName} LIMIT 10;`;
            document.getElementById("sql-input").value = sql;
            // Switch to console tab
            document.querySelector('[data-tab="tab-query"]').click();
            executeCurrentQuery();
        });

        // Click to insert column
        card.querySelectorAll(".schema-col-item").forEach(item => {
            item.addEventListener("click", () => {
                const col = item.getAttribute("data-col");
                insertTextIntoEditor(col);
            });
        });

        container.appendChild(card);
    });

    // Schema filter
    const searchInput = document.getElementById("schema-filter");
    if (searchInput) {
        searchInput.addEventListener("input", () => {
            const term = searchInput.value.toLowerCase();
            document.querySelectorAll(".schema-table-card").forEach(card => {
                const text = card.textContent.toLowerCase();
                card.style.display = text.includes(term) ? "" : "none";
            });
        });
    }
}

/* ==========================================================================
   7. SHOWCASE ANTHOLOGY CARDS
   ========================================================================== */
function renderShowcaseCards(samples) {
    const grid = document.getElementById("showcase-grid");
    if (!grid) return;
    grid.innerHTML = "";

    samples.forEach(item => {
        const card = document.createElement("div");
        card.className = "showcase-card";
        card.innerHTML = `
            <div class="showcase-top">
                <div class="showcase-category">${item.category}</div>
                <h4>${item.title}</h4>
                <p>${item.description}</p>
            </div>
            <pre class="showcase-code-preview"><code>${escapeHtml(item.query)}</code></pre>
            <button class="showcase-load-btn">Load in Editor & Run ▶</button>
        `;

        card.querySelector(".showcase-load-btn").addEventListener("click", () => {
            document.getElementById("sql-input").value = item.query;
            document.querySelector('[data-tab="tab-query"]').click();
            executeCurrentQuery();
        });

        grid.appendChild(card);
    });
}

/* ==========================================================================
   8. QUICK SNIPPETS RIBBON
   ========================================================================== */
function initSnippetsRibbon() {
    document.querySelectorAll(".snippet-tag").forEach(tag => {
        tag.addEventListener("click", () => {
            const snippet = tag.getAttribute("data-insert");
            const textarea = document.getElementById("sql-input");
            if (snippet.startsWith("SELECT")) {
                textarea.value = snippet;
                executeCurrentQuery();
            } else {
                insertTextIntoEditor(" " + snippet + " ");
            }
        });
    });
}

function insertTextIntoEditor(text) {
    const textarea = document.getElementById("sql-input");
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    textarea.value = textarea.value.substring(0, start) + text + textarea.value.substring(end);
    textarea.selectionStart = textarea.selectionEnd = start + text.length;
    textarea.focus();
}

function escapeHtml(string) {
    if (!string) return "";
    return String(string)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
