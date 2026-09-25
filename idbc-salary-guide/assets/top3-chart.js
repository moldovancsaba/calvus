/* Shared TOP3 point-line chart + tooltip layer for the IDBC Salary Guide.
   Loaded as a plain <script> by sap/, berezes/ and expert-pool/ — no build step,
   no modules, matching the rest of this repo. */
(() => {
  const COLOR_MIN = '#a5df8f';   // vállalatok által kínált bér
  const COLOR_IDBC = '#55aa8b';  // IDBC szakértői által javasolt bér
  const COLOR_MAX = '#245d54';   // jelöltek által elvárt bér

  const LABEL = {
    min: 'Vállalatok által kínált bér',
    idbc: 'IDBC szakértői által javasolt bér',
    max: 'Jelöltek által elvárt bér',
  };

  // LinkedIn Talent Insight market count per TOP3 position (client, 2026-09): a pill under the
  // role name, and one explanatory footnote under the chart. Rendered only where a row carries
  // the number, so a position the client's list does not cover shows no pill.
  const hufFormat = new Intl.NumberFormat('hu-HU');
  const TALENT_NOTE = '*Elérhető szakértők száma Magyarországon LinkedIn Talent Insight adatai alapján.';
  const talentText = n => `${hufFormat.format(n)} elérhető jelölt*`;
  const fmtHuf = n => (n === null || n === undefined) ? '–' : hufFormat.format(n) + ' Ft';

  // Compact millions for the narrow layout: 1 250 000 -> "1,25M", 1 300 000 -> "1,3M".
  // Hungarian decimal comma, trailing zeros trimmed.
  function fmtMillions(n) {
    if (n === null || n === undefined) return '–';
    const m = n / 1e6;
    const s = (Math.round(m * 100) / 100).toString().replace('.', ',');
    return s + 'M';
  }

  const escapeHtml = s => String(s).replace(/[&<>"']/g, c => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
  ));

  // Axis domain that brackets the data on round numbers, ~4 steps wide.
  // Does not force a 0 baseline: salary bands sit far from zero and would
  // otherwise collapse into the right-hand edge of the plot.
  function niceDomain(values) {
    const lo = Math.min(...values);
    const hi = Math.max(...values);
    const span = (hi - lo) || Math.max(hi * 0.2, 1);
    const rawStep = span / 4;
    const mag = Math.pow(10, Math.floor(Math.log10(rawStep)));
    const step = [1, 2, 2.5, 5, 10].map(m => m * mag).find(s => s >= rawStep) || 10 * mag;
    return { min: Math.floor(lo / step) * step, max: Math.ceil(hi / step) * step, step };
  }

  // Value labels sit above their dot. When two dots are close the labels would collide, so
  // they need nudging apart — but nudging with a single left-to-right cascade (the original
  // approach) anchors the whole run on the leftmost dot and only ever pushes right, so a
  // tight cluster of 3 close values drifts its 2nd and 3rd labels well clear of their own
  // dots (client, 2026-09-25: "when the amounts are close together, the amounts skew" —
  // confirmed live: a label could land 90px+ from the dot it names). Fixed with a min/max
  // cascade: run the same left-to-right push, then a mirrored right-to-left push, and average
  // the two per point. For points with room to spare both cascades already equal the natural
  // x, so nothing changes; for a colliding run this centers the whole group on its natural
  // midpoint instead of dragging it rightward. Same fix reaches both chart layouts (this and
  // the mobile "compact" one below) and every page that loads this file (Bérek, SAP, Expert
  // Pool), since they all call this one function.
  // ponytail: proportional-width estimate, not real text measurement — good
  // enough for tabular HUF strings at one fixed font size. Measure with
  // getComputedTextLength if the label font or content ever varies.
  function layoutLabels(points, plotMin, plotMax) {
    const halfWidth = p => (p.text.length * 5.6 + 8) / 2;
    const gap = 6;
    points.forEach(p => { p.hw = halfWidth(p); });

    const n = points.length;
    const minLayout = new Array(n);
    let prevRight = -Infinity;
    points.forEach((p, i) => {
      minLayout[i] = Math.max(p.x, prevRight + gap + p.hw);
      prevRight = minLayout[i] + p.hw;
    });
    const maxLayout = new Array(n);
    let nextLeft = Infinity;
    for (let i = n - 1; i >= 0; i--) {
      maxLayout[i] = Math.min(points[i].x, nextLeft - gap - points[i].hw);
      nextLeft = maxLayout[i] - points[i].hw;
    }
    points.forEach((p, i) => { p.labelX = (minLayout[i] + maxLayout[i]) / 2; });

    // Keep the now-evenly-spaced group inside the plot bounds as one block.
    const first = points[0], last = points[n - 1];
    const leftOvershoot = plotMin - (first.labelX - first.hw);
    if (leftOvershoot > 0) points.forEach(p => { p.labelX += leftOvershoot; });
    const rightOvershoot = (last.labelX + last.hw) - plotMax;
    if (rightOvershoot > 0) points.forEach(p => { p.labelX -= rightOvershoot; });
  }

  // Narrow layout (client request, 2026-09-16): instead of one wide chart with the role names
  // in a left gutter, stack one block per position — name and sub-label above, a short band
  // chart below — so nothing needs sideways scrolling. All blocks share one domain so the
  // bands stay comparable, and values are abbreviated to millions.
  function renderCompactChart(rows, opts) {
    const W = 340, PLOT_MIN = 10, PLOT_MAX = 330, MID = 46, AXIS_Y = 76, H = 84;
    const values = rows.flatMap(r => [r.min, r.max, r.idbc].filter(v => v != null));
    const domain = niceDomain(values);
    const xPos = v => PLOT_MIN + ((v - domain.min) / (domain.max - domain.min)) * (PLOT_MAX - PLOT_MIN);
    const ticks = [];
    for (let t = domain.min; t <= domain.max + 1; t += domain.step) ticks.push(t);

    const blocks = rows.map((r, i) => {
      const uid = `t3c-${opts.idPrefix || 'chart'}-${i}`;
      const points = [
        { key: 'min', value: r.min, color: COLOR_MIN },
        { key: 'idbc', value: r.idbc, color: COLOR_IDBC },
        { key: 'max', value: r.max, color: COLOR_MAX },
      ].filter(p => p.value != null);
      points.forEach(p => { p.x = xPos(p.value); p.text = fmtMillions(p.value); });
      points.sort((a, b) => a.x - b.x);
      layoutLabels(points, PLOT_MIN, PLOT_MAX);

      let defs = '', body = '';
      body += ticks.map(t => `<line class="grid-line" x1="${xPos(t).toFixed(1)}" y1="14" x2="${xPos(t).toFixed(1)}" y2="${MID + 12}" />`).join('');
      // Every chart carries its own value scale (client request, 2026-09-16).
      body += ticks.map(t => `<text class="axis-label" x="${xPos(t).toFixed(1)}" y="${AXIS_Y}" text-anchor="middle">${escapeHtml(fmtMillions(t))}</text>`).join('');
      body += `<line class="row-line" x1="${PLOT_MIN}" y1="${MID}" x2="${PLOT_MAX}" y2="${MID}" />`;
      const first = points[0], last = points[points.length - 1];
      if (last.x - first.x > 0.5) {
        const stops = points.map(p => `<stop offset="${(((p.x - first.x) / (last.x - first.x)) * 100).toFixed(2)}%" stop-color="${p.color}" />`).join('');
        defs += `<linearGradient id="${uid}" gradientUnits="userSpaceOnUse" x1="${first.x.toFixed(1)}" y1="${MID}" x2="${last.x.toFixed(1)}" y2="${MID}">${stops}</linearGradient>`;
        body += `<line class="salary-connector" x1="${first.x.toFixed(1)}" y1="${MID}" x2="${last.x.toFixed(1)}" y2="${MID}" stroke="url(#${uid})" />`;
      }
      points.forEach(p => {
        const tip = `${r.pozicio} – ${LABEL[p.key]}: ${fmtHuf(p.value)}`;
        body += `<g class="salary-point" role="img" tabindex="0" aria-label="${escapeHtml(tip)}" data-tooltip="${escapeHtml(tip)}">` +
          `<text class="value-label" x="${p.labelX.toFixed(1)}" y="${MID - 14}" text-anchor="middle">${escapeHtml(p.text)}</text>` +
          `<circle class="salary-dot" cx="${p.x.toFixed(1)}" cy="${MID}" r="6" fill="${p.color}" />` +
          `</g>`;
      });

      const sub = r.szint || '';
      return `
        <div class="top3-compact-row">
          <p class="top3-compact-name">${escapeHtml(r.pozicio)}</p>
          ${sub ? `<p class="top3-compact-sub">${escapeHtml(sub)}</p>` : ''}
          ${r.linkedin != null ? `<p class="talent-pill">${escapeHtml(talentText(r.linkedin))}</p>` : ''}
          <svg class="top3-chart top3-chart-compact" viewBox="0 0 ${W} ${H}" role="img"
               aria-label="${escapeHtml(`${r.pozicio}: ${LABEL.min} ${fmtHuf(r.min)}, ${LABEL.idbc} ${fmtHuf(r.idbc)}, ${LABEL.max} ${fmtHuf(r.max)}`)}">
            <defs>${defs}</defs>${body}
          </svg>
        </div>`;
    }).join('');

    return `
      <ul class="top3-chart-legend" aria-label="Jelmagyarázat">
        <li><span style="background:${COLOR_MIN}"></span>${LABEL.min}</li>
        <li><span style="background:${COLOR_IDBC}"></span>${LABEL.idbc}</li>
        <li><span style="background:${COLOR_MAX}"></span>${LABEL.max}</li>
      </ul>
      <div class="top3-compact">${blocks}</div>
      ${talentNote(rows)}`;
  }

  const talentNote = rows => rows.some(r => r.linkedin != null)
    ? `<p class="talent-note">${escapeHtml(TALENT_NOTE)}</p>` : '';

  function renderTop3Chart(rows, options) {
    const opts = options || {};
    if (!rows || !rows.length) {
      return `<p class="no-data">${escapeHtml(opts.emptyText || 'Nincs kiemelt (TOP3) pozíció.')}</p>`;
    }
    const compact = opts.compact !== undefined
      ? opts.compact
      : (typeof window !== 'undefined' && window.matchMedia
          ? window.matchMedia('(max-width: 700px)').matches : false);
    if (compact) return renderCompactChart(rows, opts);

    const hasTalent = rows.some(r => r.linkedin != null);
    // The plot's left edge has to clear the row-label text (position name, 14px/900-weight, set
    // at x=0) or a dot landing at the domain minimum sits on top of it — confirmed live: "Supply
    // Chain / Order Management Specialist" measures ~298px at this font, wider than the old fixed
    // 280px gutter, so its lowest-value dot covered the label's last few letters (2026-09-25).
    // 7px/char is a safe estimate for this font (real longest label above measured ~6.8px/char).
    const W = 1080, PLOT_MIN = Math.max(280, Math.max(...rows.map(r => r.pozicio.length * 7)) + 20), PLOT_MAX = 1020, TOP = 42, ROW_H = hasTalent ? 104 : 74;
    const rowY = i => TOP + 44 + i * ROW_H;
    const gridBottom = rowY(rows.length - 1) + 44;
    const axisY = gridBottom + 36;
    const H = axisY + 46; // matches the mockup's breathing room below the axis

    const values = rows.flatMap(r => [r.min, r.max, r.idbc].filter(v => v != null));
    const domain = niceDomain(values);
    const xPos = v => PLOT_MIN + ((v - domain.min) / (domain.max - domain.min)) * (PLOT_MAX - PLOT_MIN);

    const ticks = [];
    for (let t = domain.min; t <= domain.max + 1; t += domain.step) ticks.push(t);

    let defs = '';
    let body = '';

    rows.forEach((r, i) => {
      const y = rowY(i);
      const uid = `t3-${opts.idPrefix || 'chart'}-${i}`;

      const points = [
        { key: 'min', value: r.min, color: COLOR_MIN },
        { key: 'idbc', value: r.idbc, color: COLOR_IDBC },
        { key: 'max', value: r.max, color: COLOR_MAX },
      ].filter(p => p.value != null);

      points.forEach(p => {
        p.x = xPos(p.value);
        p.text = fmtHuf(p.value);
      });
      points.sort((a, b) => a.x - b.x);
      layoutLabels(points, PLOT_MIN - 40, PLOT_MAX + 40);

      body += `<line class="row-line" x1="${PLOT_MIN}" y1="${y}" x2="${PLOT_MAX}" y2="${y}" />`;

      // Continuous gradient along the band: offered → recommended → expected.
      const first = points[0], last = points[points.length - 1];
      if (last.x - first.x > 0.5) {
        const stops = points.map(p => {
          const offset = ((p.x - first.x) / (last.x - first.x)) * 100;
          return `<stop offset="${offset.toFixed(2)}%" stop-color="${p.color}" />`;
        }).join('');
        defs += `<linearGradient id="${uid}" gradientUnits="userSpaceOnUse" x1="${first.x.toFixed(1)}" y1="${y}" x2="${last.x.toFixed(1)}" y2="${y}">${stops}</linearGradient>`;
        body += `<line class="salary-connector" x1="${first.x.toFixed(1)}" y1="${y}" x2="${last.x.toFixed(1)}" y2="${y}" stroke="url(#${uid})" />`;
      }

      const sub = r.szint || '';
      body += `<text class="role-label" x="0" y="${(y - (sub ? 4 : -5)).toFixed(1)}">${escapeHtml(r.pozicio)}</text>`;
      if (sub) body += `<text class="role-sub" x="0" y="${(y + 13).toFixed(1)}">${escapeHtml(sub)}</text>`;
      if (r.linkedin != null) {
        const txt = talentText(r.linkedin);
        const pw = txt.length * 6.4 + 20;
        body += `<g class="talent-pill-svg"><rect x="0" y="${(y + 22).toFixed(1)}" width="${pw.toFixed(0)}" height="24" rx="8" />` +
          `<text x="10" y="${(y + 38).toFixed(1)}">${escapeHtml(txt)}</text></g>`;
      }

      points.forEach(p => {
        const tip = `${r.pozicio} – ${LABEL[p.key]}: ${p.text}`;
        body += `<g class="salary-point" role="img" tabindex="0" aria-label="${escapeHtml(tip)}" data-tooltip="${escapeHtml(tip)}">` +
          `<text class="value-label" x="${p.labelX.toFixed(1)}" y="${(y - 16).toFixed(1)}" text-anchor="middle">${escapeHtml(p.text)}</text>` +
          `<circle class="salary-dot" cx="${p.x.toFixed(1)}" cy="${y}" r="7" fill="${p.color}" />` +
          `</g>`;
      });
    });

    let axis = '';
    ticks.forEach(t => {
      const gx = xPos(t);
      axis += `<line class="grid-line" x1="${gx.toFixed(1)}" y1="${TOP}" x2="${gx.toFixed(1)}" y2="${gridBottom}" />`;
      axis += `<text class="axis-label" x="${gx.toFixed(1)}" y="${axisY}" text-anchor="middle">${escapeHtml(fmtHuf(t))}</text>`;
    });

    const summary = rows.map(r => `${r.pozicio}: ${fmtHuf(r.min)} – ${fmtHuf(r.max)}`).join('; ');

    return `
      <ul class="top3-chart-legend" aria-label="Jelmagyarázat">
        <li><span style="background:${COLOR_MIN}"></span>${LABEL.min}</li>
        <li><span style="background:${COLOR_IDBC}"></span>${LABEL.idbc}</li>
        <li><span style="background:${COLOR_MAX}"></span>${LABEL.max}</li>
      </ul>
      <div class="top3-chart-scroll">
        <svg class="top3-chart" viewBox="0 0 ${W} ${H}" role="group" aria-label="${escapeHtml((opts.chartLabel || 'TOP 3 pozíció havi bérértékei') + '. ' + summary)}">
          <defs>${defs}</defs>
          ${axis}
          ${body}
        </svg>
      </div>
      ${talentNote(rows)}`;
  }

  // Cursor-following tooltip for any [data-tooltip] element inside `root`.
  // Idempotent: calling it again on the same root re-binds nothing extra.
  function attachTooltip(root) {
    const scope = root || document;
    let tooltip = document.querySelector('.chart-tooltip');
    if (!tooltip) {
      tooltip = document.createElement('div');
      tooltip.className = 'chart-tooltip';
      tooltip.setAttribute('role', 'tooltip');
      document.body.appendChild(tooltip);
    }

    const show = (el, clientX, clientY) => {
      tooltip.textContent = el.dataset.tooltip || '';
      tooltip.classList.add('is-visible');

      const gap = 14;
      const rect = tooltip.getBoundingClientRect();
      let left = clientX + gap;
      let top = clientY - rect.height - gap;
      if (left + rect.width > window.innerWidth - 10) left = clientX - rect.width - gap;
      if (top < 10) top = clientY + gap;

      tooltip.style.left = `${Math.max(10, left)}px`;
      tooltip.style.top = `${Math.max(10, top)}px`;
    };

    const hide = () => tooltip.classList.remove('is-visible');

    // A re-render replaces the elements the tooltip was anchored to, so start clean.
    hide();

    scope.querySelectorAll('[data-tooltip]').forEach(el => {
      if (el.dataset.tooltipBound) return;
      el.dataset.tooltipBound = '1';
      el.addEventListener('mouseenter', e => show(el, e.clientX, e.clientY));
      el.addEventListener('mousemove', e => show(el, e.clientX, e.clientY));
      el.addEventListener('mouseleave', hide);
      el.addEventListener('focus', () => {
        const r = el.getBoundingClientRect();
        show(el, r.left + r.width / 2, r.top);
      });
      el.addEventListener('blur', hide);
    });

    return hide;
  }

  window.IDBCChart = { renderTop3Chart, attachTooltip, fmtHuf, fmtMillions, escapeHtml, LABEL, TALENT_NOTE, COLOR_MIN, COLOR_IDBC, COLOR_MAX };
})();
