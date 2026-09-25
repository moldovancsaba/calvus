/* Shared TOP3 point-line chart + tooltip layer for the IDBC Salary Guide.
   Loaded as a plain <script> by sap/, berezes/ and expert-pool/ — no build step,
   no modules, matching the rest of this repo. */
(() => {
  const COLOR_MIN = '#a4dd8c';   // vállalatok által kínált bér
  const COLOR_IDBC = '#4ca283';  // IDBC szakértői által javasolt bér
  const COLOR_MAX = '#35715c';   // jelöltek által elvárt bér

  // The texts below carry a sync marker: they come from the IDBCSYNC sheet (data/idbcsync.py rewrites them).
  const LABEL = {
    min: /*sync:SHARED-CHART-MIN*/"Vállalatok által kínált bér",
    idbc: /*sync:SHARED-CHART-IDBC*/"IDBC szakértői által javasolt bér",
    max: /*sync:SHARED-CHART-MAX*/"Jelöltek által elvárt bér",
  };

  // LinkedIn Talent Insight market count per TOP3 position (client, 2026-09): a pill under the
  // role name, and one explanatory footnote under the chart. Rendered only where a row carries
  // the number, so a position the client's list does not cover shows no pill.
  const hufFormat = new Intl.NumberFormat('hu-HU');
  const TALENT_NOTE = /*sync:SHARED-CHART-TALENT-NOTE*/"*Elérhető szakértők száma Magyarországon LinkedIn Talent Insight adatai alapján.";
  const talentText = n => /*sync:SHARED-CHART-TALENT-PILL*/"{n} elérhető jelölt*".replace('{n}', () => hufFormat.format(n));
  const LEGEND_LABEL = /*sync:SHARED-CHART-LEGEND-ARIA*/"Jelmagyarázat";
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

  // Value labels sit centred above their own dot. When two labels would overlap, the later one
  // moves up a row instead of sideways (client, 2026-09-25: "if they are very close, one of them
  // should move up a little, because now they drift far apart"). The earlier approach spread a
  // tight cluster horizontally, which kept the labels readable but could put a label 40–90 px
  // from the dot it names. Now every label stays over its dot; a cluster of three close values
  // uses up to three rows. `charWidth` is measured per layout (Outfit, 2026-09-25: about 5.3 px
  // per character at the wide chart's 10 px, 7.7 px at the compact chart's 13 px), plus room
  // for the hover enlargement. Every page that loads this file (Bérek, SAP, Expert Pool) and both
  // chart layouts use this one function.
  function layoutLabels(points, plotMin, plotMax, charWidth) {
    const gap = 6;
    const placed = [];
    points.forEach(p => {
      p.hw = (p.text.length * charWidth + 8) / 2;
      p.labelX = Math.min(Math.max(p.x, plotMin + p.hw), plotMax - p.hw);
      let tier = 0;
      while (placed.some(q => q.tier === tier && p.labelX - p.hw < q.right + gap && p.labelX + p.hw > q.left - gap)) tier++;
      p.tier = tier;
      placed.push({ left: p.labelX - p.hw, right: p.labelX + p.hw, tier });
    });
  }

  // Narrow layout (client request, 2026-09-16): instead of one wide chart with the role names
  // in a left gutter, stack one block per position — name and sub-label above, a short band
  // chart below — so nothing needs sideways scrolling. All blocks share one domain so the
  // bands stay comparable, and values are abbreviated to millions.
  function renderCompactChart(rows, opts) {
    // Room above the band for up to three label rows (TIER = one 13 px label's full height).
    const W = 340, PLOT_MIN = 10, PLOT_MAX = 330, MID = 66, AXIS_Y = 96, H = 104, TIER = 17;
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
      layoutLabels(points, PLOT_MIN, PLOT_MAX, 8.2);

      let defs = '', body = '';
      body += ticks.map(t => `<line class="grid-line" x1="${xPos(t).toFixed(1)}" y1="${MID - 32}" x2="${xPos(t).toFixed(1)}" y2="${MID + 12}" />`).join('');
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
          `<text class="value-label" x="${p.labelX.toFixed(1)}" y="${MID - 14 - p.tier * TIER}" text-anchor="middle">${escapeHtml(p.text)}</text>` +
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
      <ul class="top3-chart-legend" aria-label="${escapeHtml(LEGEND_LABEL)}">
        <li><span style="background:${COLOR_MIN}"></span>${escapeHtml(LABEL.min)}</li>
        <li><span style="background:${COLOR_IDBC}"></span>${escapeHtml(LABEL.idbc)}</li>
        <li><span style="background:${COLOR_MAX}"></span>${escapeHtml(LABEL.max)}</li>
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
      layoutLabels(points, PLOT_MIN - 40, PLOT_MAX + 40, 5.9);

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
          `<text class="value-label" x="${p.labelX.toFixed(1)}" y="${(y - 16 - p.tier * 13).toFixed(1)}" text-anchor="middle">${escapeHtml(p.text)}</text>` +
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
      <ul class="top3-chart-legend" aria-label="${escapeHtml(LEGEND_LABEL)}">
        <li><span style="background:${COLOR_MIN}"></span>${escapeHtml(LABEL.min)}</li>
        <li><span style="background:${COLOR_IDBC}"></span>${escapeHtml(LABEL.idbc)}</li>
        <li><span style="background:${COLOR_MAX}"></span>${escapeHtml(LABEL.max)}</li>
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
