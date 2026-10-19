/* MOTIF Lab site script (vanilla, bundled by Hugo js.Build). Everything degrades: without JS the pages are complete and static.
   Modules: nav toggle · reveal-on-scroll · count-up · "Latest" rotation · hero signal wall. All motion respects prefers-reduced-motion. */
(() => {
  const html = document.documentElement;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  html.classList.add('js'); if (reduced) html.classList.add('reduced');
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => Array.from(r.querySelectorAll(s));

  // ---- nav toggle (the CSS-only checkbox stays as the no-JS fallback)
  const btn = $('.nav-btn'), nav = $('#site-nav');
  if (btn && nav) {
    btn.hidden = false;
    const set = (open) => { nav.classList.toggle('is-open', open); btn.setAttribute('aria-expanded', String(open)); };
    btn.addEventListener('click', () => set(!nav.classList.contains('is-open')));
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && nav.classList.contains('is-open')) { set(false); btn.focus(); } });
    document.addEventListener('click', (e) => { if (nav.classList.contains('is-open') && !nav.contains(e.target) && e.target !== btn) set(false); });
  }

  // ---- reveal on scroll
  const revealed = $$('.reveal');
  if (revealed.length) {
    if (reduced || !('IntersectionObserver' in window)) revealed.forEach((el) => el.classList.add('on'));
    else { const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('on'); io.unobserve(e.target); } }), { threshold: 0.12 }); revealed.forEach((el) => io.observe(el)); }
  }

  // ---- count-up for headline numbers (<data class="num" value> inside [data-countup])
  const nums = $$('[data-countup] data.num');
  if (nums.length && !reduced && 'IntersectionObserver' in window) {
    const fmt = (v, dec) => new Intl.NumberFormat('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec }).format(v);
    const io2 = new IntersectionObserver((es) => es.forEach((e) => {
      if (!e.isIntersecting) return; io2.unobserve(e.target); const el = e.target, target = parseFloat(el.getAttribute('value'));
      const text = el.firstChild && el.firstChild.nodeType === 3 ? el.firstChild : null; if (!text || !isFinite(target)) return;
      const orig = text.nodeValue, m = orig.match(/^[\d,]*\.?(\d*)/), dec = m && m[1] ? m[1].length : 0, suffix = orig.replace(/^[\d,.]+/, '');
      const t0 = performance.now(), dur = 1200;
      const step = (now) => { const p = Math.min(1, (now - t0) / dur), k = 1 - Math.pow(1 - p, 3); text.nodeValue = fmt(target * k, dec) + suffix; if (p < 1) requestAnimationFrame(step); else text.nodeValue = orig; };
      requestAnimationFrame(step);
    }), { threshold: 0.4 });
    nums.forEach((el) => io2.observe(el));
  }

  // ---- "Latest" rotation in the hero (all items are in the DOM; one shown at a time on wide screens)
  const list = $('.latest-list');
  if (list) {
    const items = $$('.latest-item', list), ctl = $('.latest-ctl'), dots = ctl ? $$('[data-go]', ctl) : [], bar = ctl ? $('.latest-bar', ctl) : null;
    let i = 0, timer = null, userTouched = false;
    const wide = () => matchMedia('(min-width: 768px)').matches;
    const show = (n, announce) => { i = (n + items.length) % items.length; items.forEach((el, k) => { el.hidden = wide() && k !== i; }); dots.forEach((d, k) => d.setAttribute('aria-current', k === i ? 'true' : 'false')); if (announce) list.setAttribute('aria-live', 'polite'); if (bar) { bar.classList.remove('run'); void bar.offsetWidth; if (!reduced && !userTouched) bar.classList.add('run'); } };
    const stop = () => { if (timer) { clearInterval(timer); timer = null; } if (bar) bar.classList.remove('run'); };
    const start = () => { stop(); if (reduced || userTouched || !wide() || items.length < 2 || document.hidden) return; timer = setInterval(() => show(i + 1, false), parseInt(list.dataset.rotate || '6000', 10)); if (bar) bar.classList.add('run'); };
    if (items.length > 1 && ctl) { ctl.hidden = false; }
    show(0, false); start();
    if (ctl) { $('[data-prev]', ctl)?.addEventListener('click', () => { userTouched = true; stop(); show(i - 1, true); }); $('[data-next]', ctl)?.addEventListener('click', () => { userTouched = true; stop(); show(i + 1, true); }); dots.forEach((d) => d.addEventListener('click', () => { userTouched = true; stop(); show(parseInt(d.dataset.go, 10), true); })); }
    const host = list.closest('.hero-latest') || list;
    host.addEventListener('mouseenter', stop); host.addEventListener('mouseleave', start); host.addEventListener('focusin', stop); host.addEventListener('focusout', start);
    document.addEventListener('visibilitychange', () => (document.hidden ? stop() : start()));
    matchMedia('(min-width: 768px)').addEventListener('change', () => { show(i, false); start(); });
  }

  // ---- hero signal wall: real production-vehicle traces drawn as a scrolling background
  const cv = $('[data-hero-canvas]');
  if (cv && !reduced && cv.getContext) {
    const ctx = cv.getContext('2d'); let clips = null, ci = 0, t = 22 * 0.6, last = 0, fade = 0, running = false, visible = true, W = 0, H = 0, dpr = 1;
    const WINDOW = 22; // seconds visible across the width
    const resize = () => { dpr = Math.min(1.5, window.devicePixelRatio || 1); const r = cv.getBoundingClientRect(); W = Math.max(1, Math.round(r.width)); H = Math.max(1, Math.round(r.height)); cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr); ctx.setTransform(dpr, 0, 0, dpr, 0, 0); };
    const range = (a) => { let lo = Infinity, hi = -Infinity; for (const v of a) if (v != null) { if (v < lo) lo = v; if (v > hi) hi = v; } if (!isFinite(lo)) { lo = 0; hi = 1; } if (hi - lo < 1e-6) hi = lo + 1; return [lo, hi]; };
    const LANES = [['speed', 'rgba(207,196,147,.80)', 2], ['steer', 'rgba(159,212,184,.70)', 1.5], ['lane', 'rgba(255,255,255,.45)', 1.2], ['brake', 'rgba(255,255,255,.45)', 1.2], ['gas', 'rgba(159,212,184,.40)', 1]];
    const draw = (now) => {
      if (!running) return; const dt = Math.min(0.05, (now - last) / 1000 || 0); last = now; t += dt;
      const clip = clips[ci], dur = clip.n / clip.hz; if (t > dur + 1) { ci = (ci + 1) % clips.length; t = WINDOW * 0.6; fade = 1; }
      ctx.clearRect(0, 0, W, H); const alpha = fade > 0 ? Math.max(0, 1 - fade) : 1; if (fade > 0) fade = Math.max(0, fade - dt);
      const lanes = LANES.filter((l) => clip.series[l[0]]); const laneH = H / Math.max(1, lanes.length);
      lanes.forEach(([key, color, lw], li) => {
        const a = clip.series[key], [lo, hi] = clip._r[key] || (clip._r[key] = range(a)); const y0 = li * laneH + laneH * 0.15, y1 = (li + 1) * laneH - laneH * 0.15;
        ctx.beginPath(); ctx.strokeStyle = color; ctx.lineWidth = lw; ctx.globalAlpha = alpha; let pen = false;
        for (let k = 0; k < a.length; k++) { const ts = k / clip.hz, x = W - (t - ts) / WINDOW * W; if (x < -4 || x > W + 4) continue; const v = a[k]; if (v == null) { pen = false; continue; } const y = y1 - (v - lo) / (hi - lo) * (y1 - y0); if (pen) ctx.lineTo(x, y); else { ctx.moveTo(x, y); pen = true; } }
        ctx.stroke();
      });
      ctx.globalAlpha = alpha * 0.9; ctx.strokeStyle = 'rgba(183,159,77,.9)'; ctx.fillStyle = 'rgba(207,196,147,.95)'; ctx.font = '600 11px Inter, system-ui, sans-serif'; ctx.lineWidth = 1;
      for (const ev of clip.events) { const x = W - (t - (ev.t - (clip.t0 || 0))) / WINDOW * W; if (x < 0 || x > W) continue; ctx.setLineDash([3, 4]); ctx.beginPath(); ctx.moveTo(x + .5, 0); ctx.lineTo(x + .5, H); ctx.stroke(); ctx.setLineDash([]); if (x < W - 140) ctx.fillText(ev.label.slice(0, 32), x + 6, 14); }
      ctx.globalAlpha = 1; requestAnimationFrame(draw);
    };
    const start = () => { if (running || !clips || !visible || document.hidden) return; running = true; last = performance.now(); requestAnimationFrame(draw); };
    const stop = () => { running = false; };
    fetch(cv.dataset.src, { credentials: 'same-origin' }).then((r) => r.json()).then((d) => { clips = d.clips.map((c) => Object.assign({ _r: {} }, c)); clips.forEach((c) => { if (c.events.length) { const t0 = c.events[0].t - (c.n / c.hz) * 0.25; c.t0 = Math.max(0, Math.min(t0, c.events[0].t)); } }); resize(); cv.classList.add('is-live'); start(); }).catch(() => {});
    new ResizeObserver(resize).observe(cv);
    new IntersectionObserver((es) => { visible = es[0].isIntersecting; visible ? start() : stop(); }).observe(cv);
    document.addEventListener('visibilitychange', () => (document.hidden ? stop() : start()));
    const hero = cv.closest('.hero'); if (hero) { let ticking = false; addEventListener('scroll', () => { if (ticking) return; ticking = true; requestAnimationFrame(() => { cv.style.setProperty('--py', Math.round(scrollY * 0.25) + 'px'); ticking = false; }); }, { passive: true }); }
  }
})();
