/* gameformative — the few behaviours the pages need; every page works without this file. */
(function () {
  var root = document.documentElement;

  // Theme: system preference by default; the toggle stores the reader's choice on this device.
  function stored() { try { return localStorage.getItem("gf-theme"); } catch (e) { return null; } }
  function isDark() {
    var t = root.getAttribute("data-theme");
    if (t) return t === "dark";
    return window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches;
  }
  function label() {
    document.querySelectorAll("[data-theme-toggle]").forEach(function (b) {
      var dark = isDark();
      b.setAttribute("aria-pressed", dark ? "true" : "false");
      b.setAttribute("aria-label", dark ? "Switch to light theme" : "Switch to dark theme");
    });
  }
  var s = stored(); if (s === "dark" || s === "light") root.setAttribute("data-theme", s);
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-theme-toggle]");
    if (!b) return;
    var next = isDark() ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try { localStorage.setItem("gf-theme", next); } catch (err) {}
    label();
  });
  label();

  // "More" sheet (phone tab bar and desktop menu)
  var sheet = document.getElementById("gf-more");
  var opener = null;
  function openSheet(btn) { opener = btn; sheet.hidden = false; btn.setAttribute("aria-expanded", "true"); var f = sheet.querySelector("a,button"); if (f) f.focus(); }
  function closeSheet() { sheet.hidden = true; if (opener) { opener.setAttribute("aria-expanded", "false"); opener.focus(); } }
  document.addEventListener("click", function (e) {
    var o = e.target.closest("[data-sheet-open]"); if (o && sheet) { openSheet(o); return; }
    if (e.target.closest("[data-sheet-close]") || e.target === sheet) closeSheet();
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && sheet && !sheet.hidden) closeSheet(); });

  // Share: the native share sheet where available, and copy-link; the plain links need no script
  document.querySelectorAll("[data-share]").forEach(function (box) {
    var url = box.dataset.url, title = box.dataset.title, status = box.querySelector("[data-share-status]");
    var nat = box.querySelector("[data-share-native]");
    if (nat && navigator.share) {
      nat.hidden = false; box.classList.add("has-native");
      nat.addEventListener("click", function () { navigator.share({ title: title, url: url }).catch(function () {}); });
    }
    var copy = box.querySelector("[data-copy]");
    if (copy) copy.addEventListener("click", function () {
      function done(ok) { status.textContent = ok ? "Link copied" : "Copy failed — select the address bar instead"; copy.textContent = ok ? "Link copied" : "Copy link"; setTimeout(function () { copy.textContent = "Copy link"; }, 2500); }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(function () { done(true); }, function () { done(false); });
      else done(false);
    });
  });

  // Sortable tables: a button in each sortable header; numbers sort high→low first.
  document.querySelectorAll("table[data-sortable]").forEach(function (table) {
    var body = table.tBodies[0];
    table.querySelectorAll("th[data-key]").forEach(function (th, _) {
      var btn = th.querySelector(".gf-sort"); if (!btn) return;
      btn.addEventListener("click", function () {
        var idx = Array.prototype.indexOf.call(th.parentNode.children, th);
        var asc = th.getAttribute("aria-sort") === "descending";
        table.querySelectorAll("th[aria-sort]").forEach(function (h) { h.removeAttribute("aria-sort"); });
        th.setAttribute("aria-sort", asc ? "ascending" : "descending");
        var rows = Array.prototype.slice.call(body.rows);
        rows.sort(function (a, b) {
          var x = a.children[idx].dataset.v, y = b.children[idx].dataset.v;
          var nx = parseFloat(x), ny = parseFloat(y);
          var r = (isNaN(nx) || isNaN(ny)) ? String(x).localeCompare(String(y)) : nx - ny;
          return asc ? r : -r;
        });
        rows.forEach(function (r) { body.appendChild(r); });
        var live = document.getElementById(table.dataset.live); if (live) live.textContent = "Sorted by " + btn.textContent.trim() + (asc ? ", lowest first" : ", highest first");
      });
    });
  });

  // Overall / Home / Away views of a league table (three tables, one shown)
  document.querySelectorAll("[data-views]").forEach(function (box) {
    var btns = box.querySelectorAll("[data-view]");
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        btns.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
        box.querySelectorAll("[data-panel]").forEach(function (p) { p.hidden = p.dataset.panel !== b.dataset.view; });
      });
    });
  });

  // Phones: "All columns" shows the columns a compact table hides
  document.querySelectorAll("[data-cols]").forEach(function (b) {
    b.addEventListener("click", function () {
      var box = b.closest("[data-views]"); var on = !box.classList.contains("is-full");
      box.classList.toggle("is-full", on); b.setAttribute("aria-pressed", on ? "true" : "false");
    });
  });

  // League filter on the scores page
  document.querySelectorAll("[data-filter]").forEach(function (box) {
    var btns = box.querySelectorAll("[data-league]");
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        btns.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
        document.querySelectorAll("[data-league-block]").forEach(function (blk) {
          blk.hidden = !(b.dataset.league === "all" || blk.dataset.leagueBlock === b.dataset.league);
        });
      });
    });
  });

  // "Load more" on the analysis index (the footer stays reachable — no infinite scroll)
  document.querySelectorAll("[data-loadmore]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var hidden = document.querySelectorAll("[data-more][hidden]");
      for (var i = 0; i < Math.min(+btn.dataset.loadmore, hidden.length); i++) hidden[i].hidden = false;
      var first = hidden[0] && hidden[0].querySelector("a, h2"); if (first && first.focus) first.setAttribute("tabindex", "-1"), first.focus();
      if (!document.querySelector("[data-more][hidden]")) btn.hidden = true;
    });
  });
})();
