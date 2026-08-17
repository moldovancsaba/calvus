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

  const hufFormat = new Intl.NumberFormat('hu-HU');
  const fmtHuf = n => (n === null || n === undefined) ? '–' : hufFormat.format(n) + ' Ft';

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

  // Value labels sit above their dot. When two dots are close the labels would
  // collide, so nudge them apart left-to-right, then slide the whole row back
  // if the last one overshot the plot.
  // ponytail: proportional-width estimate, not real text measurement — good
  // enough for tabular HUF strings at one fixed font size. Measure with
  // getComputedTextLength if the label font or content ever varies.
  function layoutLabels(points, plotMin, plotMax) {
    const halfWidth = p => (p.text.length * 5.6 + 8) / 2;
    let prevRight = -Infinity;
    points.forEach(p => {
      const hw = halfWidth(p);
      p.labelX = Math.max(p.x, prevRight + 6 + hw);
      prevRight = p.labelX + hw;
    });
    const last = points[points.length - 1];
    const overshoot = (last.labelX + halfWidth(last)) - plotMax;
    if (overshoot > 0) {
      const first = points[0];
      const headroom = (first.labelX - halfWidth(first)) - plotMin;
      const shift = Math.min(overshoot, Math.max(0, headroom));
      points.forEach(p => { p.labelX -= shift; });
    }
  }

  function renderTop3Chart(rows, options) {
    const opts = options || {};
    if (!rows || !rows.length) {
      return `<p class="no-data">${escapeHtml(opts.emptyText || 'Nincs kiemelt (TOP3) pozíció.')}</p>`;
    }

    const W = 1080, PLOT_MIN = 280, PLOT_MAX = 1020, TOP = 42, ROW_H = 74;
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

      const sub = [r.terulet, r.szint].filter(Boolean).join(' · ');
      body += `<text class="role-label" x="0" y="${(y - (sub ? 4 : -5)).toFixed(1)}">${escapeHtml(r.pozicio)}</text>`;
      if (sub) body += `<text class="role-sub" x="0" y="${(y + 13).toFixed(1)}">${escapeHtml(sub)}</text>`;

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
      </div>`;
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

  window.IDBCChart = { renderTop3Chart, attachTooltip, fmtHuf, escapeHtml, LABEL, COLOR_MIN, COLOR_IDBC, COLOR_MAX };
})();
