/* ═══════════════════════════════════════════════
   Simulateur de devis — estimation indicative
   ⚠ TARIFS INDICATIFS À VALIDER AVEC M. GIRARD
   ═══════════════════════════════════════════════ */
(function () {
  'use strict';
  const RATES = {          // € / part, fourchette basse et haute
    choux:   { low: 6.0, high: 8.0, min: 12, label: 'Pièce montée en choux' },
    wedding: { low: 6.5, high: 9.0, min: 10, label: 'Wedding cake' },
    anniv:   { low: 4.5, high: 6.5, min: 4,  label: 'Gâteau d’anniversaire' },
    buffet:  { low: 3.5, high: 5.5, min: 20, label: 'Buffet de desserts' },
  };
  const form = document.getElementById('simu');
  if (!form) return;
  const parts = document.getElementById('parts'), partsOut = document.getElementById('partsOut');
  const low = document.getElementById('priceLow'), high = document.getElementById('priceHigh'), detail = document.getElementById('priceDetail');
  const fmt = (n) => Math.round(n / 5) * 5 + ' €';

  function parfums() { return [...document.querySelectorAll('#parfums input:checked')].map((i) => i.value); }
  document.querySelectorAll('#parfums input').forEach((i) => i.addEventListener('change', () => {
    if (parfums().length > 2) i.checked = false;
  }));

  function compute() {
    const type = form.type.value, r = RATES[type];
    const n = Math.max(r.min, parseInt(parts.value, 10));
    partsOut.textContent = parts.value;
    let optLow = 0, optHigh = 0, opts = [];
    document.querySelectorAll('input[name=opt]:checked').forEach((o) => {
      const p = parseFloat(o.dataset.price);
      optLow += p; optHigh += p * 1.5; opts.push(o.value);
    });
    const tiers = type === 'choux' ? Math.max(1, Math.ceil(n / 25)) : type === 'wedding' ? Math.max(1, Math.ceil(n / 30)) : 1;
    const l = n * r.low + optLow, h = n * r.high + optHigh;
    low.textContent = fmt(l); high.textContent = fmt(h);
    detail.textContent = `${r.label} · ${n} parts` + (tiers > 1 ? ` · environ ${tiers} étages` : '') + (opts.length ? ` · ${opts.join(', ')}` : '');
    return { type: r.label, n, tiers, opts, l, h };
  }
  form.addEventListener('input', compute);
  compute();

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const c = compute();
    const body = [
      `Nom : ${form.nom.value}`, `Téléphone : ${form.tel.value}`,
      `Date de l’événement : ${form.date.value}`, `Lieu : ${form.lieu.value || '—'}`, '',
      `Type : ${c.type}`, `Parts : ${c.n}` + (c.tiers > 1 ? ` (≈ ${c.tiers} étages)` : ''),
      `Parfums : ${parfums().join(', ') || '—'}`, `Options : ${c.opts.join(', ') || '—'}`, '',
      `Estimation indicative du site : ${fmt(c.l)} à ${fmt(c.h)}`,
    ].join('\n');
    window.location.href = 'mailto:yohann.girard63@gmail.com?subject=' + encodeURIComponent(`Demande de devis — ${c.type}, ${c.n} parts`) + '&body=' + encodeURIComponent(body);
    form.classList.add('sent');
  });
})();
