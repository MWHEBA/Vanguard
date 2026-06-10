/**
 * Rich Text Editor
 * يشوف كل textarea عليها data-rich-editor="true" ويحوّلها لـ editor بسيط
 * بيستخدم الـ CSS classes الموجودة في dashboard.css
 */

(function () {
  "use strict";

  // الأزرار اللي هتظهر في الـ toolbar
  const TOOLBAR_ACTIONS = [
    { cmd: "bold",                label: "B",   title: "Bold",          style: "font-weight:700" },
    { cmd: "italic",              label: "I",   title: "Italic",        style: "font-style:italic" },
    { cmd: "underline",           label: "U",   title: "Underline",     style: "text-decoration:underline" },
    { sep: true },
    { cmd: "insertUnorderedList", label: "≡",   title: "Bullet list" },
    { cmd: "insertOrderedList",   label: "1.",  title: "Numbered list" },
    { sep: true },
    { cmd: "justifyLeft",         label: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="17" y1="10" x2="3" y2="10"></line><line x1="21" y1="6" x2="3" y2="6"></line><line x1="21" y1="14" x2="3" y2="14"></line><line x1="17" y1="18" x2="3" y2="18"></line></svg>`,   title: "Align left" },
    { cmd: "justifyCenter",       label: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="21" y1="6" x2="3" y2="6"></line><line x1="18" y1="10" x2="6" y2="10"></line><line x1="21" y1="14" x2="3" y2="14"></line><line x1="18" y1="18" x2="6" y2="18"></line></svg>`,   title: "Align center" },
    { cmd: "justifyRight",        label: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="21" y1="6" x2="3" y2="6"></line><line x1="21" y1="10" x2="9" y2="10"></line><line x1="21" y1="14" x2="3" y2="14"></line><line x1="21" y1="18" x2="9" y2="18"></line></svg>`,   title: "Align right" },
    { cmd: "justifyFull",         label: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="21" y1="6" x2="3" y2="6"></line><line x1="21" y1="10" x2="3" y2="10"></line><line x1="21" y1="14" x2="3" y2="14"></line><line x1="21" y1="18" x2="3" y2="18"></line></svg>`,   title: "Justify" },
    { sep: true },
    { cmd: "h2",                  label: "H2",  title: "Heading 2",     isBlock: true },
    { cmd: "h3",                  label: "H3",  title: "Heading 3",     isBlock: true },
    { cmd: "p",                   label: "¶",   title: "Paragraph",     isBlock: true },
    { sep: true },
    { cmd: "createLink",          label: "🔗",  title: "Insert link",   isLink: true },
    { cmd: "unlink",              label: "✂",   title: "Remove link" },
    { sep: true },
    { cmd: "removeFormat",        label: "✕",   title: "Clear formatting" },
  ];

  /**
   * يبني الـ editor ويربطه بالـ textarea الأصلي
   */
  function buildEditor(textarea) {
    // إخفاء الـ textarea الأصلي
    textarea.style.display = "none";

    // Container رئيسي - rich-text-container موجود في CSS
    const container = document.createElement("div");
    container.className = "rich-text-container";

    // Toolbar - rich-text-toolbar موجود في CSS
    const toolbar = document.createElement("div");
    toolbar.className = "rich-text-toolbar";
    toolbar.setAttribute("role", "toolbar");
    toolbar.setAttribute("aria-label", "Text formatting");

    // بناء مجموعات الأزرار
    let currentGroup = null;

    TOOLBAR_ACTIONS.forEach((action) => {
      if (action.sep) {
        currentGroup = null;
        return;
      }

      if (!currentGroup) {
        currentGroup = document.createElement("div");
        currentGroup.className = "toolbar-group";
        toolbar.appendChild(currentGroup);
      }

      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "toolbar-btn";
      btn.dataset.cmd = action.cmd;
      btn.title = action.title;
      btn.setAttribute("aria-label", action.title);

      const inner = document.createElement("span");
      inner.style.display = "inline-flex";
      inner.style.alignItems = "center";
      inner.style.justifyContent = "center";
      if (action.label.trim().startsWith("<svg")) {
        inner.innerHTML = action.label;
      } else {
        inner.textContent = action.label;
      }
      if (action.style) inner.setAttribute("style", action.style);
      btn.appendChild(inner);

      currentGroup.appendChild(btn);
    });

    // Editable area - rich-text-editor موجود في CSS
    const editable = document.createElement("div");
    editable.className = "rich-text-editor";
    editable.contentEditable = "true";
    editable.setAttribute("role", "textbox");
    editable.setAttribute("aria-multiline", "true");
    editable.setAttribute(
      "aria-label",
      textarea.getAttribute("aria-label") || "Rich text content"
    );

    // Max chars
    const maxChars = parseInt(textarea.dataset.maxChars, 10) || 0;

    // نحمّل المحتوى الأصلي من الـ textarea
    const rawValue = textarea.value.trim();
    if (rawValue) {
      if (rawValue.startsWith("<")) {
        editable.innerHTML = rawValue;
      } else {
        editable.innerHTML = "<p>" + escapeHtml(rawValue) + "</p>";
      }
    } else {
      editable.innerHTML = "<p><br></p>";
    }

    // Footer للعداد (لو في maxChars)
    let footer = null;
    let charCountEl = null;
    if (maxChars > 0) {
      footer = document.createElement("div");
      footer.className = "rich-text-footer";

      const limitLabel = document.createElement("span");
      limitLabel.className = "char-limit-label";
      limitLabel.textContent = "Characters: ";

      charCountEl = document.createElement("span");
      charCountEl.className = "char-count";

      footer.appendChild(limitLabel);
      footer.appendChild(charCountEl);
    }

    // نجمّع الكل
    container.appendChild(toolbar);
    container.appendChild(editable);
    if (footer) container.appendChild(footer);

    textarea.parentNode.insertBefore(container, textarea.nextSibling);

    // ربط الأحداث
    bindToolbar(toolbar, editable, textarea);
    bindEditable(editable, textarea, maxChars, footer, charCountEl);

    updateCounter(editable, maxChars, footer, charCountEl);
    updateActiveButtons(toolbar, editable);
  }

  /**
   * ربط الـ toolbar بالـ editable area
   */
  function bindToolbar(toolbar, editable, textarea) {
    toolbar.addEventListener("mousedown", function (e) {
      const btn = e.target.closest(".toolbar-btn");
      if (!btn) return;
      e.preventDefault(); // نحافظ على الـ selection

      const cmd = btn.dataset.cmd;
      editable.focus();

      const blockCmds = ["h2", "h3", "p"];
      if (blockCmds.includes(cmd)) {
        document.execCommand("formatBlock", false, cmd);
        syncToTextarea(editable, textarea);
        updateActiveButtons(toolbar, editable);
        return;
      }

      if (cmd === "createLink") {
        const url = prompt("Enter URL:");
        if (url) {
          document.execCommand("createLink", false, url);
        }
        syncToTextarea(editable, textarea);
        updateActiveButtons(toolbar, editable);
        return;
      }

      document.execCommand(cmd, false, null);
      syncToTextarea(editable, textarea);
      updateActiveButtons(toolbar, editable);
    });
  }

  /**
   * ربط الـ editable area - مزامنة المحتوى مع الـ textarea
   */
  function bindEditable(editable, textarea, maxChars, footer, charCountEl) {
    editable.addEventListener("input", function () {
      if (maxChars > 0) {
        const text = editable.innerText || "";
        if (text.length > maxChars) {
          document.execCommand("undo");
          return;
        }
      }
      syncToTextarea(editable, textarea);
      updateCounter(editable, maxChars, footer, charCountEl);
    });

    editable.addEventListener("keyup", function () {
      const toolbar = editable.closest(".rich-text-container").querySelector(".rich-text-toolbar");
      updateActiveButtons(toolbar, editable);
    });

    editable.addEventListener("mouseup", function () {
      const toolbar = editable.closest(".rich-text-container").querySelector(".rich-text-toolbar");
      updateActiveButtons(toolbar, editable);
    });

    // منع paste HTML - نقبل text فقط
    editable.addEventListener("paste", function (e) {
      e.preventDefault();
      const text = (e.clipboardData || window.clipboardData).getData("text/plain");
      document.execCommand("insertText", false, text);
    });
  }

  /**
   * مزامنة المحتوى من editable إلى textarea
   */
  function syncToTextarea(editable, textarea) {
    textarea.value = editable.innerHTML;
  }

  /**
   * تحديث حالة الأزرار (active/inactive)
   */
  function updateActiveButtons(toolbar, editable) {
    const stateCmds = ["bold", "italic", "underline", "insertUnorderedList", "insertOrderedList", "justifyLeft", "justifyCenter", "justifyRight", "justifyFull"];
    stateCmds.forEach((cmd) => {
      const btn = toolbar.querySelector(`[data-cmd="${cmd}"]`);
      if (!btn) return;
      try {
        btn.classList.toggle("is-active", document.queryCommandState(cmd));
      } catch (_) {}
    });

    // تحديث block format buttons
    try {
      const blockVal = document.queryCommandValue("formatBlock").toLowerCase();
      ["h2", "h3", "p"].forEach((tag) => {
        const btn = toolbar.querySelector(`[data-cmd="${tag}"]`);
        if (!btn) return;
        btn.classList.toggle("is-active", blockVal === tag);
      });
    } catch (_) {}
  }

  /**
   * تحديث عداد الأحرف
   */
  function updateCounter(editable, maxChars, footer, charCountEl) {
    if (!footer || !charCountEl || !maxChars) return;
    const len = (editable.innerText || "").replace(/\n$/, "").length;
    charCountEl.textContent = len + " / " + maxChars;

    footer.classList.remove("near-limit", "at-limit");
    if (len >= maxChars) {
      footer.classList.add("at-limit");
    } else if (len >= maxChars * 0.85) {
      footer.classList.add("near-limit");
    }
  }

  /**
   * Escape HTML للنصوص العادية
   */
  function escapeHtml(str) {
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\n/g, "<br>");
  }

  /**
   * تشغيل الـ editor على كل الـ textareas المناسبة
   */
  function init() {
    document.querySelectorAll("textarea[data-rich-editor]").forEach(buildEditor);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
