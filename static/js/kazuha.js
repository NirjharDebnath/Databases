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

async function readApiResponse(response) {
    const contentType = response.headers.get("content-type") || "";
    const body = await response.text();
    let payload;

    if (contentType.includes("application/json")) {
        try {
            payload = JSON.parse(body);
        } catch {
            throw new Error(`The server returned invalid JSON (HTTP ${response.status}).`);
        }
    } else {
        throw new Error(
            `The API returned HTML instead of JSON (HTTP ${response.status}). ` +
            "Start the application with run_web.sh, not a static web server."
        );
    }

    if (!response.ok) {
        const error = new Error(payload.error || `API request failed (HTTP ${response.status}).`);
        error.name = "ApiError";
        throw error;
    }

    return payload;
}

async function streamQueryResponse(response, onEvent) {
    if (!response.ok) {
        await readApiResponse(response);
        throw new Error(`Query request failed (HTTP ${response.status}).`);
    }

    const contentType = response.headers.get("content-type") || "";
    if (!contentType.includes("application/x-ndjson")) {
        throw new Error("The query API returned an unsupported response format.");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    const processLines = (text) => {
        buffer += text;
        const lines = buffer.split("\n");
        buffer = lines.pop();
        lines.filter(Boolean).forEach(line => onEvent(JSON.parse(line)));
    };

    while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        processLines(decoder.decode(value, { stream: true }));
    }
    processLines(decoder.decode());
    if (buffer.trim()) onEvent(JSON.parse(buffer));
}

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
        schemaCache = await readApiResponse(res);
        
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
        const samples = await readApiResponse(res);
        renderShowcaseCards(samples);
    } catch (err) {
        console.error("Failed to load showcase queries:", err);
    }
}

/* ==========================================================================
   4. MONACO-STYLE SQL STUDIO (SYNTAX HIGHLIGHTING, TABS, GUTTER, AUTOCOMPLETE)
   ========================================================================== */

// SQL Vocabulary Sets for Highlighting
const SQL_KEYWORDS_SET = new Set([
    "SELECT", "FROM", "WHERE", "INNER", "LEFT", "RIGHT", "FULL", "CROSS", "JOIN",
    "ON", "GROUP", "BY", "ORDER", "HAVING", "LIMIT", "OFFSET", "WITH", "RECURSIVE",
    "AS", "UNION", "ALL", "EXCEPT", "INTERSECT", "DISTINCT", "CASE", "WHEN", "THEN",
    "ELSE", "END", "IS", "NULL", "NOT", "IN", "LIKE", "GLOB", "BETWEEN", "EXISTS",
    "AND", "OR", "DESC", "ASC", "PRAGMA", "EXPLAIN", "QUERY", "PLAN", "VALUES",
    "INSERT", "INTO", "UPDATE", "SET", "DELETE", "DROP", "ALTER", "CREATE", "TABLE",
    "VIEW", "INDEX", "TRIGGER", "DEFAULT", "CHECK", "UNIQUE", "PRIMARY", "KEY",
    "FOREIGN", "REFERENCES", "CASCADE", "COLLATE", "AUTOINCREMENT"
]);

const SQL_FUNCTIONS_SET = new Set([
    "COUNT", "SUM", "AVG", "ROUND", "MIN", "MAX", "DENSE_RANK", "RANK", "ROW_NUMBER",
    "OVER", "PARTITION", "COALESCE", "NULLIF", "SUBSTR", "LENGTH", "UPPER", "LOWER",
    "TRIM", "LTRIM", "RTRIM", "INSTR", "CAST", "TYPEOF", "IFNULL", "TOTAL", "ABS",
    "RANDOM", "HEX", "PRINTF", "CHAR", "UNICODE", "DATE", "TIME", "DATETIME",
    "STRFTIME", "JULIANDAY"
]);

const SQL_TABLES_SET = new Set(["characters", "weapons", "artifact_sets", "character_builds"]);

const SQL_COLUMNS_SET = new Set([
    "character_id", "name", "rarity", "vision", "weapon_type", "region", "base_hp",
    "base_atk", "base_def", "talent_priority", "release_patch", "weapon_id",
    "sub_stat_type", "sub_stat_value", "is_craftable", "signature_character_id",
    "artifact_set_id", "domain_name", "two_piece_bonus", "four_piece_bonus",
    "build_id", "build_name", "role", "recommended_weapon_id", "recommended_artifact_id",
    "sands_stat", "goblet_stat", "circlet_stat", "tier_rating"
]);

const SQL_TOKEN_REGEX = /(\/\*[\s\S]*?\*\/|--[^\n]*)|('(?:[^'\\]|\\.)*'|"(?:[^"\\]|\\.)*")|(\b\d+(?:\.\d+)?\b)|(\b[a-zA-Z_][a-zA-Z0-9_]*\b)|([=!<>+\-*\/%|]+)|([(),;])/g;

function highlightSQL(code) {
    if (!code) return "";
    let result = "";
    let lastIndex = 0;
    let match;
    SQL_TOKEN_REGEX.lastIndex = 0;
    while ((match = SQL_TOKEN_REGEX.exec(code)) !== null) {
        if (match.index > lastIndex) {
            result += escapeHtml(code.slice(lastIndex, match.index));
        }
        const [full, comment, str, num, word, op, punct] = match;
        if (comment) {
            result += `<span class="tok-comment">${escapeHtml(comment)}</span>`;
        } else if (str) {
            result += `<span class="tok-string">${escapeHtml(str)}</span>`;
        } else if (num) {
            result += `<span class="tok-number">${escapeHtml(num)}</span>`;
        } else if (word) {
            const upper = word.toUpperCase();
            const lower = word.toLowerCase();
            if (SQL_KEYWORDS_SET.has(upper)) {
                result += `<span class="tok-keyword">${escapeHtml(word)}</span>`;
            } else if (SQL_FUNCTIONS_SET.has(upper)) {
                result += `<span class="tok-function">${escapeHtml(word)}</span>`;
            } else if (SQL_TABLES_SET.has(lower)) {
                result += `<span class="tok-table">${escapeHtml(word)}</span>`;
            } else if (SQL_COLUMNS_SET.has(lower)) {
                result += `<span class="tok-column">${escapeHtml(word)}</span>`;
            } else {
                result += `<span class="tok-ident">${escapeHtml(word)}</span>`;
            }
        } else if (op) {
            result += `<span class="tok-op">${escapeHtml(op)}</span>`;
        } else if (punct) {
            result += `<span class="tok-punct">${escapeHtml(punct)}</span>`;
        }
        lastIndex = match.index + full.length;
    }
    if (lastIndex < code.length) {
        result += escapeHtml(code.slice(lastIndex));
    }
    if (code.endsWith("\n")) {
        result += " "; // Prevent pre height collapse on trailing empty line
    }
    return result;
}

// Query Tabs State
let editorTabs = [
    {
        id: 1,
        title: "Query 1",
        content: `-- Type your SELECT query here...
-- IntelliSense autocomplete triggers automatically as you type!
SELECT name, vision, region, base_atk
FROM characters
WHERE rarity = 5
ORDER BY base_atk DESC
LIMIT 8;`
    }
];
let activeEditorTabId = 1;
let nextEditorTabId = 2;

function renderEditorTabs() {
    const list = document.getElementById("query-tabs-list");
    if (!list) return;
    list.innerHTML = "";

    editorTabs.forEach(tab => {
        const tabEl = document.createElement("div");
        tabEl.className = `query-tab ${tab.id === activeEditorTabId ? "active" : ""}`;
        tabEl.innerHTML = `
            <span class="query-tab-leaf">🍁</span>
            <span class="query-tab-title" title="Double-click to rename">${escapeHtml(tab.title)}</span>
            ${editorTabs.length > 1 ? `<span class="query-tab-close" title="Close Tab">×</span>` : ""}
        `;

        // Switch Tab
        tabEl.addEventListener("click", (e) => {
            if (e.target.classList.contains("query-tab-close")) return;
            switchEditorTab(tab.id);
        });

        // Close Tab
        const closeBtn = tabEl.querySelector(".query-tab-close");
        if (closeBtn) {
            closeBtn.addEventListener("click", (e) => {
                e.stopPropagation();
                closeEditorTab(tab.id);
            });
        }

        // Rename Tab on Double Click
        const titleEl = tabEl.querySelector(".query-tab-title");
        titleEl.addEventListener("dblclick", (e) => {
            e.stopPropagation();
            const newTitle = prompt("Rename Query Tab:", tab.title);
            if (newTitle && newTitle.trim()) {
                tab.title = newTitle.trim();
                renderEditorTabs();
            }
        });

        list.appendChild(tabEl);
    });
}

function switchEditorTab(tabId) {
    if (tabId === activeEditorTabId) return;
    const textarea = document.getElementById("sql-input");
    const currentTab = editorTabs.find(t => t.id === activeEditorTabId);
    if (currentTab) currentTab.content = textarea.value;

    activeEditorTabId = tabId;
    const targetTab = editorTabs.find(t => t.id === tabId);
    if (targetTab) {
        textarea.value = targetTab.content;
    }
    renderEditorTabs();
    onEditorContentChanged();
    textarea.focus();
}

function createNewEditorTab(initialContent = "", title = "") {
    const textarea = document.getElementById("sql-input");
    const currentTab = editorTabs.find(t => t.id === activeEditorTabId);
    if (currentTab) currentTab.content = textarea.value;

    const newId = nextEditorTabId++;
    const newTab = {
        id: newId,
        title: title || `Query ${newId}`,
        content: initialContent || `-- New Query Scratchpad\nSELECT * FROM characters LIMIT 10;\n`
    };
    editorTabs.push(newTab);
    activeEditorTabId = newId;
    textarea.value = newTab.content;
    renderEditorTabs();
    onEditorContentChanged();
    textarea.focus();
}

function closeEditorTab(tabId) {
    if (editorTabs.length <= 1) return;
    const idx = editorTabs.findIndex(t => t.id === tabId);
    if (idx === -1) return;

    editorTabs.splice(idx, 1);
    if (activeEditorTabId === tabId) {
        const nextActive = editorTabs[Math.max(0, idx - 1)];
        activeEditorTabId = nextActive.id;
        document.getElementById("sql-input").value = nextActive.content;
    }
    renderEditorTabs();
    onEditorContentChanged();
}

function onEditorContentChanged() {
    const textarea = document.getElementById("sql-input");
    const codeEl = document.getElementById("monaco-code");
    if (!textarea || !codeEl) return;

    const code = textarea.value;
    
    // 1. Update active tab memory
    const curTab = editorTabs.find(t => t.id === activeEditorTabId);
    if (curTab) curTab.content = code;

    // 2. Syntax Highlight
    codeEl.innerHTML = highlightSQL(code);

    // 3. Update cursor, gutter, status bar
    updateCursorStatus();
}

function updateGutter(lineCount, activeLineIndex) {
    const gutterLines = document.getElementById("gutter-lines");
    if (!gutterLines) return;

    if (gutterLines.children.length !== lineCount) {
        let html = "";
        for (let i = 1; i <= lineCount; i++) {
            html += `<div class="gutter-line ${i === activeLineIndex ? "active" : ""}" data-line="${i}">${i}</div>`;
        }
        gutterLines.innerHTML = html;
    } else {
        const children = gutterLines.children;
        for (let i = 0; i < children.length; i++) {
            children[i].classList.toggle("active", (i + 1) === activeLineIndex);
        }
    }
}

function updateActiveLineHighlight(lineNumber) {
    const activeLineBar = document.getElementById("monaco-active-line");
    if (!activeLineBar) return;
    const lineHeight = 22; // Must match CSS line-height
    const top = (lineNumber - 1) * lineHeight + 10; // 10px padding-top
    activeLineBar.style.top = `${top}px`;
}

function updateCursorStatus() {
    const textarea = document.getElementById("sql-input");
    if (!textarea) return;

    const val = textarea.value;
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;

    // Line and Column
    const textUpToCursor = val.substring(0, start);
    const lines = textUpToCursor.split("\n");
    const lineNum = lines.length;
    const colNum = lines[lines.length - 1].length + 1;

    const posEl = document.getElementById("editor-pos-indicator");
    if (posEl) posEl.textContent = `Ln ${lineNum}, Col ${colNum}`;

    // Selection Indicator
    const selEl = document.getElementById("editor-selection-indicator");
    if (selEl) {
        if (start !== end) {
            selEl.textContent = `(${Math.abs(end - start)} selected)`;
            selEl.style.display = "inline";
        } else {
            selEl.style.display = "none";
        }
    }

    // Total Lines Indicator
    const totalLines = val.split("\n").length;
    const linesEl = document.getElementById("editor-lines-indicator");
    if (linesEl) linesEl.textContent = `${totalLines} line${totalLines === 1 ? "" : "s"}`;

    // Sync Gutter & Active Line
    updateGutter(totalLines, lineNum);
    updateActiveLineHighlight(lineNum);
}

function setEditorContent(sql) {
    const textarea = document.getElementById("sql-input");
    if (!textarea) return;
    textarea.value = sql;
    onEditorContentChanged();
}

function initSqlEditorAutocomplete() {
    const textarea = document.getElementById("sql-input");
    const acBox = document.getElementById("autocomplete-box");
    const acList = document.getElementById("autocomplete-list");
    const highlightLayer = document.getElementById("monaco-highlight-layer");
    const gutter = document.getElementById("monaco-gutter");
    const addTabBtn = document.getElementById("new-query-tab-btn");

    if (addTabBtn) {
        addTabBtn.addEventListener("click", () => createNewEditorTab());
    }

    renderEditorTabs();
    onEditorContentChanged();

    // Synchronize scrolling between textarea, highlight layer, and gutter
    textarea.addEventListener("scroll", () => {
        if (highlightLayer) {
            highlightLayer.scrollTop = textarea.scrollTop;
            highlightLayer.scrollLeft = textarea.scrollLeft;
        }
        if (gutter) {
            gutter.scrollTop = textarea.scrollTop;
        }
    });

    textarea.addEventListener("input", handleEditorInput);
    textarea.addEventListener("keyup", handleEditorKeyup);
    textarea.addEventListener("click", () => {
        hideAutocomplete();
        updateCursorStatus();
    });
    textarea.addEventListener("select", updateCursorStatus);

    function handleEditorInput() {
        onEditorContentChanged();
        const { token } = getCaretContext();
        if (token.length >= 1) {
            showAutocomplete(token);
        } else {
            hideAutocomplete();
        }
    }

    function handleEditorKeyup(e) {
        if (["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown", "Home", "End"].includes(e.key)) {
            updateCursorStatus();
        }
    }

    function getCaretContext() {
        const pos = textarea.selectionStart;
        const text = textarea.value.substring(0, pos);
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

            let matchedTable = null;
            if (schemaCache) {
                if (schemaCache[qualifier]) {
                    matchedTable = qualifier;
                } else {
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
        SQL_KEYWORDS.forEach(kw => pool.push({ text: kw, insertText: kw + " ", kind: "keyword", detail: "Keyword" }));
        SQL_FUNCTIONS.forEach(fn => pool.push({ text: fn, insertText: fn, kind: "function", detail: "Function" }));

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
            const aPrefix = a.text.toLowerCase().startsWith(tLower);
            const bPrefix = b.text.toLowerCase().startsWith(tLower);
            if (aPrefix && !bPrefix) return -1;
            if (!aPrefix && bPrefix) return 1;
            return a.text.localeCompare(b.text);
        });
    }

    function showAutocomplete(token) {
        currentAutocompleteMatches = buildCandidates(token);
        if (currentAutocompleteMatches.length === 0) {
            hideAutocomplete();
            return;
        }

        activeAutocompleteIndex = 0;
        renderAutocompleteList();

        const caretCoords = getCaretCoordinates(textarea, textarea.selectionStart);
        acBox.style.left = `${Math.min(caretCoords.left + 14, textarea.clientWidth - 320)}px`;
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

    textarea.addEventListener("keydown", (e) => {
        // 1. Run Query: Ctrl+Enter or Cmd+Enter
        if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
            e.preventDefault();
            executeCurrentQuery();
            return;
        }

        // 2. New Tab: Ctrl+Alt+N
        if ((e.ctrlKey || e.metaKey) && e.altKey && (e.key === "n" || e.key === "N")) {
            e.preventDefault();
            createNewEditorTab();
            return;
        }

        // 3. Toggle Comment: Ctrl+/ or Cmd+/
        if ((e.ctrlKey || e.metaKey) && e.key === "/") {
            e.preventDefault();
            toggleComment();
            return;
        }

        // 4. Manual Autocomplete trigger: Ctrl+Space
        if ((e.ctrlKey || e.metaKey) && e.key === " ") {
            e.preventDefault();
            const { token } = getCaretContext();
            showAutocomplete(token || "");
            return;
        }

        // 5. Autocomplete Navigation when open
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

        // 6. TAB KEY INDENTATION & UNINDENTATION (4 Spaces)
        if (e.key === "Tab") {
            e.preventDefault();
            handleTabIndentation(e.shiftKey);
            return;
        }

        // 7. ENTER KEY AUTO-INDENT
        if (e.key === "Enter" && !e.ctrlKey && !e.metaKey && acBox.style.display === "none") {
            e.preventDefault();
            handleEnterAutoIndent();
            return;
        }

        // 8. AUTO-CLOSE BRACKETS & QUOTES
        const PAIRS = { "(": ")", "[": "]", "{": "}", "'": "'", '"': '"' };
        if (PAIRS[e.key] && !e.ctrlKey && !e.metaKey && !e.altKey) {
            const start = textarea.selectionStart;
            const end = textarea.selectionEnd;
            const val = textarea.value;
            if (start !== end) {
                e.preventDefault();
                const selected = val.substring(start, end);
                textarea.setRangeText(e.key + selected + PAIRS[e.key], start, end, "end");
                textarea.selectionStart = start + 1;
                textarea.selectionEnd = end + 1;
                onEditorContentChanged();
                return;
            } else {
                if (val[start] === e.key && (e.key === "'" || e.key === '"')) {
                    e.preventDefault();
                    textarea.selectionStart = textarea.selectionEnd = start + 1;
                    updateCursorStatus();
                    return;
                }
                e.preventDefault();
                textarea.setRangeText(e.key + PAIRS[e.key], start, end, "end");
                textarea.selectionStart = textarea.selectionEnd = start + 1;
                onEditorContentChanged();
                return;
            }
        }

        // 9. BACKSPACE PAIR DELETION
        if (e.key === "Backspace" && textarea.selectionStart === textarea.selectionEnd) {
            const pos = textarea.selectionStart;
            const val = textarea.value;
            const prevChar = val[pos - 1];
            const nextChar = val[pos];
            if (
                (prevChar === "(" && nextChar === ")") ||
                (prevChar === "[" && nextChar === "]") ||
                (prevChar === "{" && nextChar === "}") ||
                (prevChar === "'" && nextChar === "'") ||
                (prevChar === '"' && nextChar === '"')
            ) {
                e.preventDefault();
                textarea.setRangeText("", pos - 1, pos + 1, "end");
                onEditorContentChanged();
                return;
            }
        }
    });

    function handleTabIndentation(isShift) {
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        const val = textarea.value;

        if (start === end) {
            if (isShift) {
                // Unindent current line
                const lineStart = val.lastIndexOf("\n", start - 1) + 1;
                const linePrefix = val.substring(lineStart, lineStart + 4);
                let removeCount = 0;
                while (removeCount < 4 && linePrefix[removeCount] === " ") {
                    removeCount++;
                }
                if (removeCount > 0) {
                    textarea.setRangeText("", lineStart, lineStart + removeCount, "end");
                    textarea.selectionStart = textarea.selectionEnd = Math.max(lineStart, start - removeCount);
                }
            } else {
                // Insert 4 spaces at cursor
                textarea.setRangeText("    ", start, end, "end");
            }
        } else {
            // Multi-line selection indent/unindent
            const lineStart = val.lastIndexOf("\n", start - 1) + 1;
            let lineEnd = val.indexOf("\n", end);
            if (lineEnd === -1) lineEnd = val.length;

            const selectedText = val.substring(lineStart, lineEnd);
            const lines = selectedText.split("\n");

            if (isShift) {
                const unindented = lines.map(l => {
                    let c = 0;
                    while (c < 4 && l[c] === " ") c++;
                    return l.substring(c);
                });
                const repl = unindented.join("\n");
                textarea.setRangeText(repl, lineStart, lineEnd, "select");
            } else {
                const indented = lines.map(l => "    " + l);
                const repl = indented.join("\n");
                textarea.setRangeText(repl, lineStart, lineEnd, "select");
            }
        }
        onEditorContentChanged();
    }

    function handleEnterAutoIndent() {
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        const val = textarea.value;

        const lineStart = val.lastIndexOf("\n", start - 1) + 1;
        const currentLine = val.substring(lineStart, start);
        const match = currentLine.match(/^[ \t]+/);
        let indent = match ? match[0] : "";

        if (currentLine.trim().endsWith("(") || currentLine.trim().endsWith("[")) {
            indent += "    ";
        }

        textarea.setRangeText("\n" + indent, start, end, "end");
        onEditorContentChanged();
    }

    function toggleComment() {
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        const val = textarea.value;

        const lineStart = val.lastIndexOf("\n", start - 1) + 1;
        let lineEnd = val.indexOf("\n", end);
        if (lineEnd === -1) lineEnd = val.length;

        const lines = val.substring(lineStart, lineEnd).split("\n");
        const allCommented = lines.every(l => l.trimStart().startsWith("--"));

        const toggled = lines.map(l => {
            if (allCommented) {
                return l.replace(/^(\s*)--\s?/, "$1");
            } else {
                return l.replace(/^(\s*)/, "$1-- ");
            }
        });

        const repl = toggled.join("\n");
        textarea.setRangeText(repl, lineStart, lineEnd, "select");
        onEditorContentChanged();
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
        onEditorContentChanged();
        textarea.focus();
    }

    function hideAutocomplete() {
        acBox.style.display = "none";
    }

    function getCaretCoordinates(element, position) {
        const text = element.value.substring(0, position);
        const lines = text.split("\n");
        const lineNumber = lines.length;
        const currentLine = lines[lines.length - 1];
        
        const left = Math.min(currentLine.length * 8.1 + 14, element.clientWidth - 320);
        const top = Math.min((lineNumber - 1) * 22 + 10, element.clientHeight - 40);
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
        setEditorContent("");
        sqlInput.focus();
    });

    formatBtn.addEventListener("click", () => {
        let code = sqlInput.value.trim();
        if (!code) return;

        // Structured SQL Beautifier with 4-space indentation
        const clauses = ["SELECT", "FROM", "WHERE", "INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "CROSS JOIN", "JOIN", "GROUP BY", "ORDER BY", "HAVING", "LIMIT", "OFFSET", "WITH"];
        clauses.forEach(cl => {
            const regex = new RegExp(`\\b${cl}\\b`, "gi");
            code = code.replace(regex, `\n${cl.toUpperCase()}`);
        });

        const lines = code.split("\n").map(l => l.trim()).filter(l => l.length > 0);
        let formatted = "";
        let inClause = false;

        lines.forEach(line => {
            const upper = line.toUpperCase();
            if (
                upper.startsWith("SELECT") || upper.startsWith("FROM") ||
                upper.startsWith("WHERE") || upper.startsWith("GROUP BY") ||
                upper.startsWith("ORDER BY") || upper.startsWith("HAVING") ||
                upper.startsWith("LIMIT") || upper.startsWith("WITH") ||
                upper.startsWith("JOIN") || upper.startsWith("INNER JOIN") ||
                upper.startsWith("LEFT JOIN")
            ) {
                inClause = false;
                formatted += line + "\n";
            } else {
                formatted += "    " + line + "\n";
            }
        });

        setEditorContent(formatted.trim());
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
        let completed = false;
        await streamQueryResponse(response, (event) => {
            if (event.type === "start") {
                queryResultsCache = { columns: event.columns, rows: [] };
                beginStreamingResults(event.columns);
                resultActions.style.display = "none";
            } else if (event.type === "rows") {
                for (let i = 0; i < event.rows.length; i++) {
                    queryResultsCache.rows.push(event.rows[i]);
                }
                appendStreamingRows(event.rows);
                statusBadge.textContent = `Receiving ${streamingRowCount.toLocaleString()} rows...`;
            } else if (event.type === "complete") {
                completed = true;
                finishStreamingResults(event);
                const badgeExtra = event.truncated ? " (capped)" : "";
                statusBadge.textContent = `✓ ${event.count.toLocaleString()} rows${badgeExtra} (${event.execution_time_ms} ms)`;
                statusBadge.className = event.truncated ? "status-badge warning" : "status-badge success";
                resultActions.style.display = "flex";
            } else if (event.type === "error") {
                throw new Error(event.error);
            }
        });
        if (!completed) {
            throw new Error("The query stream ended before all results were received.");
        }
    } catch (err) {
        statusBadge.textContent = err.name === "ApiError" ? "Query Error" : (err.message.includes("Timeout") ? "Timeout" : "Query Error");
        statusBadge.className = "status-badge error";
        resultActions.style.display = "none";
        resultsContainer.innerHTML = `
            <div class="error-banner">
                <div class="error-title">Query Execution Notice</div>
                <div class="error-message">${escapeHtml(err.message || "Unable to contact the SQL API.")}</div>
            </div>
        `;
    }
}

const MAX_DOM_ROWS = 1000;
let streamingTableBody = null;
let streamingRowCount = 0;
let renderedRowCount = 0;

function beginStreamingResults(columns) {
    streamingRowCount = 0;
    renderedRowCount = 0;
    const container = document.getElementById("results-container");
    let header = "";
    columns.forEach(col => {
        header += `<th>${escapeHtml(col)}</th>`;
    });
    container.innerHTML = `
        <div class="table-scroll">
            <table class="data-table" id="data-table">
                <thead><tr>${header}</tr></thead>
                <tbody></tbody>
            </table>
        </div>
    `;
    streamingTableBody = container.querySelector("tbody");
}

function appendStreamingRows(rows) {
    if (!streamingTableBody) return;
    const fragment = document.createDocumentFragment();
    rows.forEach(row => {
        // Protect client DOM: only create real DOM nodes up to MAX_DOM_ROWS
        if (renderedRowCount < MAX_DOM_ROWS) {
            const tr = document.createElement("tr");
            row.forEach(value => {
                const td = document.createElement("td");
                if (value === null) {
                    td.innerHTML = '<span class="null-cell">NULL</span>';
                } else {
                    td.textContent = String(value);
                }
                tr.appendChild(td);
            });
            fragment.appendChild(tr);
            renderedRowCount++;
        }
        streamingRowCount++;
    });
    if (fragment.childNodes.length > 0) {
        streamingTableBody.appendChild(fragment);
    }
}

function finishStreamingResults(event) {
    const count = typeof event === "object" ? event.count : event;
    const isTruncated = typeof event === "object" && event.truncated;
    const warning = typeof event === "object" ? event.warning : null;

    const container = document.getElementById("results-container");
    if (count === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-leaf">🍃</div>
                <h3>Zero Rows Returned</h3>
                <p>The query executed successfully, but no matching records were found.</p>
            </div>
        `;
    } else {
        if (isTruncated || renderedRowCount < count) {
            const notice = document.createElement("div");
            notice.className = "results-notice-banner";
            let msg = "";
            if (isTruncated) {
                msg += `⚠️ <strong>Server Limit Reached:</strong> ${escapeHtml(warning || `Results capped at ${event.max_rows} rows.`)}<br>`;
            }
            if (renderedRowCount < count) {
                msg += `Showing first <strong>${renderedRowCount.toLocaleString()}</strong> of <strong>${count.toLocaleString()}</strong> rows in browser memory. Complete data is exportable below via CSV/JSON.`;
            }
            notice.innerHTML = msg;
            container.insertBefore(notice, container.firstChild);
        }
    }
    streamingTableBody = null;
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
            setEditorContent(sql);
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
            setEditorContent(item.query);
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
            if (snippet.startsWith("SELECT")) {
                setEditorContent(snippet);
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
    onEditorContentChanged();
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
