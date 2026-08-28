/* ═══════════════════════════════════════════════
   MAISON ROSALIE — moteur de scroll
   Lenis (scroll natif lissé) + GSAP ScrollTrigger + DisplaceGL
   ═══════════════════════════════════════════════ */
(function () {
  'use strict';

  const html = document.documentElement;
  html.classList.add('js');

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = window.matchMedia('(hover:hover) and (pointer:fine)').matches;
  const rand = gsap.utils.random;

  gsap.registerPlugin(ScrollTrigger);
  gsap.defaults({ ease: 'power3.out' });

  /* ---------- 1. Lenis ---------- */
  let lenis = null;
  if (!reduced) {
    html.classList.add('lenis-active');
    lenis = new Lenis({ lerp: 0.085, wheelMultiplier: 1, syncTouch: false });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add((t) => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
  }
  // vidéos HD/SD hors héros (le héros choisit via son script inline)
  document.querySelectorAll('video[data-src-hd]').forEach((v) => { if (!v.getAttribute('src')) v.src = (window.innerWidth > 760 || window.devicePixelRatio > 2) ? v.dataset.srcHd : v.dataset.srcSd; });
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener('click', (e) => {
      const id = a.getAttribute('href');
      if (id.length < 2) return;
      const el = document.querySelector(id);
      if (!el) return;
      e.preventDefault();
      closeMenu();
      lenis ? lenis.scrollTo(el, { duration: 1.8 }) : el.scrollIntoView({ behavior: 'smooth' });
    });
  });

  /* ---------- 2. Découpes ---------- */
  function splitLetters(el) {
    const words = el.textContent.split(/(\s+)/);
    el.textContent = '';
    let i = 0;
    words.forEach((w) => {
      if (!w.trim()) { el.appendChild(document.createTextNode(' ')); return; }
      const wd = document.createElement('span');
      wd.className = 'wd';
      [...w].forEach((c) => {
        const s = document.createElement('span');
        s.className = 'ch';
        s.textContent = c;
        s.style.setProperty('--i', i++);
        wd.appendChild(s);
      });
      el.appendChild(wd);
    });
  }
  function splitWords(el) {
    const words = el.textContent.split(/(\s+)/);
    el.textContent = '';
    words.forEach((w) => {
      if (!w.trim()) { el.appendChild(document.createTextNode(w)); return; }
      const s = document.createElement('span');
      s.className = 'sw';
      s.textContent = w;
      el.appendChild(s);
    });
  }
  document.querySelectorAll('[data-letters]').forEach(splitLetters);
  document.querySelectorAll('[data-scrub-words]').forEach(splitWords);

  /* ---------- 2b. Formulaire de commande → e-mail ---------- */
  const form = document.getElementById('orderForm');
  if (form) form.addEventListener('submit', (e) => {
    e.preventDefault();
    const f = new FormData(form);
    const body = `Nom : ${f.get('nom')}\nTéléphone : ${f.get('tel')}\nDate souhaitée : ${f.get('date')}\n\n${f.get('msg')}`;
    window.location.href = 'mailto:yohann.girard63@gmail.com?subject=' + encodeURIComponent('Demande de commande — site') + '&body=' + encodeURIComponent(body);
    form.classList.add('sent');
  });

  /* ---------- 3. Menu mobile ---------- */
  const menu = document.getElementById('menu');
  function closeMenu() { menu.classList.remove('open'); document.body.classList.remove('menu-open'); }
  document.getElementById('burger').addEventListener('click', () => {
    menu.classList.toggle('open');
    document.body.classList.toggle('menu-open');
  });

  /* ---------- 4. Loader → intro ---------- */
  function intro() {
    if (reduced) {
      gsap.set('.hero__title .ch', { y: 0 });
      gsap.set('.hero__actions,.hero__meta', { clipPath: 'inset(0 0 0% 0)' });
      return;
    }
    const count = { v: 0 }, el = document.getElementById('loadCount');
    const tl = gsap.timeline({ onComplete: () => { buildHeroScroll(); heroSentences(); } });
    tl.to('.loader__mark .ch', { y: '0%', duration: 1, stagger: .035, ease: 'power4.out' }, 0)
      .to(count, { v: 100, duration: 1.6, ease: 'power2.inOut', onUpdate: () => (el.textContent = String(Math.round(count.v)).padStart(2, '0')) }, 0)
      .to('.loader__mark .ch', { y: '-110%', duration: .7, stagger: .02, ease: 'power3.in' }, 1.4)
      .to('.loader__sub, .loader__count', { opacity: 0, duration: .4 }, 1.6)
      .to('#loader', { yPercent: -100, borderRadius: '0 0 50% 50% / 0 0 12% 12%', duration: 1.1, ease: 'expo.inOut' }, 1.85)
      .set('#loader', { display: 'none' })
      .from('.hero__cell', { yPercent: 100, duration: 1.3, stagger: .12, ease: 'expo.out' }, 2.0)
      .fromTo('.hero__video', { scale: 1.3 }, { scale: 1, duration: 2.4, ease: 'expo.out', stagger: .1 }, 2.0)
      .from('.nav', { y: -40, opacity: 0, duration: .8 }, 2.4)
      .from('.hero__eyebrow .ch', { y: 14, opacity: 0, stagger: .012, duration: .6 }, 2.4)
      .to('.hero__eyebrow i', { scaleX: 1, duration: .6 }, 2.6)
      .to('.hero__title .ch', { y: '0%', duration: 1.1, stagger: { each: .03, from: 'start' }, ease: 'power4.out' }, 2.5)
      .to('.hero__actions, .hero__meta', { clipPath: 'inset(0 0 0% 0)', duration: .9, stagger: .1 }, 3.2)
      .from('.hero__scroll', { opacity: 0, y: 10, duration: .6 }, 3.6);
  }
  // Phrases une par une, calées sur la boucle de la vidéo : la séquence repart à chaque tour
  function heroSentences() {
    const video = document.getElementById('heroVideo'), lines = gsap.utils.toArray('.hero__lines p');
    if (!lines.length) return;
    let seq = null;
    const build = () => {
      const dur = (video && video.duration && isFinite(video.duration)) ? video.duration : 8.6;
      const slot = dur / lines.length;
      seq = gsap.timeline({ repeat: -1 });
      lines.forEach((l, i) => {
        seq.fromTo(l, { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: .55, ease: 'power3.out' }, i * slot)
           .to(l, { opacity: 0, y: -10, duration: .4, ease: 'power2.in' }, (i + 1) * slot - .4);
      });
    };
    build();
    if (video) {
      let last = 0;
      video.addEventListener('timeupdate', () => { if (video.currentTime < last - .5) seq.restart(); last = video.currentTime; });
      video.addEventListener('loadedmetadata', () => { seq.kill(); build(); });
    }
  }
  // Créée APRÈS l'intro : sinon la timeline de scroll mémorise les lettres encore cachées
  function buildHeroScroll() {
    if (!document.querySelector('.hero-wrap')) return;
    const tl = gsap.timeline({ scrollTrigger: { trigger: '.hero-wrap', start: 'top top', end: 'bottom bottom', scrub: .6 } });
    tl.fromTo('.hero__cell--mid .hero__video', { scale: 1 }, { scale: 1.18, ease: 'none', duration: 1 }, 0)
      .fromTo('.hero__cell:not(.hero__cell--mid) .hero__video', { scale: 1.08, yPercent: 4 }, { scale: 1.08, yPercent: -4, ease: 'none', duration: 1 }, 0)
      .to('.hero__veil', { opacity: .4, duration: 1 }, 0)
      .to('.hero__text', { y: -90, opacity: 0, ease: 'power1.in', duration: .55 }, 0)
      .to('.hero__scroll', { opacity: 0, duration: .3 }, 0);
  }
  function introSub() {
    const first = document.querySelector('main > section:first-child');
    if (!first) return;
    const tl = gsap.timeline();
    tl.from('.nav', { y: -30, opacity: 0, duration: .8 }, 0);
    if (first.querySelector('[data-hero-img]')) tl.from(first.querySelector('[data-hero-img]'), { scale: 1.2, duration: 1.8, ease: 'expo.out' }, 0);
    [...first.querySelectorAll('[data-letters]')].filter((el) => { const m = el.closest('[data-mslide]'); return !m || m === first.querySelector('[data-mslide]'); }).forEach((el, i) => {
      tl.to(el.querySelectorAll('.ch'), { y: '0%', rotateX: 0, duration: 1.1, stagger: .025, ease: 'power4.out' }, .2 + i * .15);
    });
    tl.to(first.querySelectorAll('[data-reveal]'), { opacity: 1, y: 0, duration: .9, stagger: .12 }, .6);
    // les data-reveal du hero ne doivent pas être repris par le trigger générique
    first.querySelectorAll('[data-reveal]').forEach((el) => el.removeAttribute('data-reveal'));
  }
  window.addEventListener('load', document.getElementById('loader') ? intro : introSub);

  /* ---------- 5. Curseur + boutons magnétiques ---------- */
  if (fine && !reduced) {
    const cur = document.querySelector('.cursor');
    const label = cur.querySelector('.cursor__label');
    const xDot = gsap.quickTo('.cursor__dot', 'x', { duration: .12 }), yDot = gsap.quickTo('.cursor__dot', 'y', { duration: .12 });
    const xRing = gsap.quickTo('.cursor__ring', 'x', { duration: .4, ease: 'power3' }), yRing = gsap.quickTo('.cursor__ring', 'y', { duration: .4, ease: 'power3' });
    window.addEventListener('pointermove', (e) => { xDot(e.clientX); yDot(e.clientY); xRing(e.clientX); yRing(e.clientY); });
    document.querySelectorAll('[data-cursor]').forEach((el) => {
      el.addEventListener('pointerenter', () => { label.textContent = el.dataset.cursor; cur.classList.add('is-label'); });
      el.addEventListener('pointerleave', () => cur.classList.remove('is-label'));
    });
    document.querySelectorAll('[data-magnet]').forEach((el) => {
      const mx = gsap.quickTo(el, 'x', { duration: .5, ease: 'power3' }), my = gsap.quickTo(el, 'y', { duration: .5, ease: 'power3' });
      el.addEventListener('pointermove', (e) => {
        const r = el.getBoundingClientRect();
        mx((e.clientX - r.left - r.width / 2) * .35); my((e.clientY - r.top - r.height / 2) * .35);
      });
      el.addEventListener('pointerleave', () => { mx(0); my(0); });
    });
  }

  if (reduced) return; // tout ce qui suit est du mouvement

  /* ---------- 6b. Hero des pages secondaires ---------- */
  if (document.querySelector('.page-hero')) {
    gsap.to('[data-hero-img]', { yPercent: 22, scale: 1.12, ease: 'none', scrollTrigger: { trigger: '.page-hero', start: 'top top', end: 'bottom top', scrub: true } });
    gsap.to('.page-hero__content', { yPercent: 30, opacity: 0, ease: 'none', scrollTrigger: { trigger: '.page-hero', start: '30% top', end: 'bottom top', scrub: true } });
    gsap.to('.page-hero__ghost', { xPercent: 12, yPercent: -20, ease: 'none', scrollTrigger: { trigger: '.page-hero', start: 'top top', end: 'bottom top', scrub: true } });
  }

  if (document.querySelector('.video-hero')) {
    gsap.to('.video-hero__video', { yPercent: 20, scale: 1.15, ease: 'none', scrollTrigger: { trigger: '.video-hero', start: 'top top', end: 'bottom top', scrub: true } });
    gsap.to('.video-hero__content', { yPercent: 40, opacity: 0, ease: 'none', scrollTrigger: { trigger: '.video-hero', start: '20% top', end: 'bottom top', scrub: true } });
  }
  if (document.getElementById('howLine')) gsap.to('#howLine', { scaleX: 1, ease: 'none', scrollTrigger: { trigger: '.how', start: 'top 70%', end: 'bottom 60%', scrub: true } });

  /* ---------- 6b2. Carte : colonne d'images qui défile sans fin ---------- */
  document.querySelectorAll('[data-vmarquee]').forEach((wrap) => {
    const row = wrap.children[0];
    const run = () => {
      const h = row.offsetHeight;
      gsap.killTweensOf(wrap);
      gsap.to(wrap, { y: -h, duration: h / 40, ease: 'none', repeat: -1, modifiers: { y: (y) => (parseFloat(y) % h) + 'px' } });
    };
    const imgs = wrap.querySelectorAll('img');
    let left = imgs.length;
    imgs.forEach((im) => { if (im.complete) { if (!--left) run(); } else im.addEventListener('load', () => { if (!--left) run(); }); });
    // le scroll accélère la colonne
    gsap.to(wrap, { y: '-=300', ease: 'none', scrollTrigger: { trigger: '.split-hero', start: 'top top', end: 'bottom top', scrub: 1 } });
  });

  /* ---------- 6b3. Mariages : cartes qui s'empilent ---------- */
  const scards = gsap.utils.toArray('.scard');
  scards.forEach((c, i) => {
    const next = scards[i + 1];
    if (next) gsap.to(c, { scale: .92 - (scards.length - i - 1) * .02, filter: 'brightness(.55)', ease: 'none', scrollTrigger: { trigger: next, start: 'top 90%', end: 'top 30%', scrub: true } });
  });

  /* ---------- 6b4. Maison : journée à l'atelier, horloge pinnée ---------- */
  (function day() {
    const pin = document.querySelector('.day__pin');
    if (!pin) return;
    const moments = gsap.utils.toArray('.day__moment'), dots = gsap.utils.toArray('.day__dots i');
    const times = ['4 h 30', '6 h', '9 h', '12 h 30', '15 h'], angles = [135, 180, 270, 375, 450]; // degrés depuis minuit
    const hand = document.getElementById('clockHand'), glow = document.getElementById('clockGlow'), label = document.getElementById('clockTime');
    const tickBox = document.getElementById('clockTicks');
    for (let i = 0; i < 12; i++) tickBox.insertAdjacentHTML('beforeend', `<u style="transform:rotate(${i * 30}deg)"></u>`);
    let cur = -1;
    const show = (i) => { if (i === cur) return; cur = i; moments.forEach((m, k) => m.classList.toggle('is-on', k === i)); dots.forEach((d, k) => d.classList.toggle('on', k === i)); label.textContent = times[i]; };
    show(0);
    ScrollTrigger.create({
      trigger: '.day', start: 'top top', end: '+=' + (moments.length * 80) + '%', pin: pin, scrub: true, refreshPriority: 1,
      onUpdate: (st) => {
        const p = st.progress * (moments.length - 1), i = Math.round(p), a = i < moments.length - 1 ? angles[Math.floor(p)] + (angles[Math.ceil(p)] - angles[Math.floor(p)]) * (p - Math.floor(p)) : angles[angles.length - 1];
        hand.style.transform = `rotate(${a}deg)`;
        glow.style.setProperty('--a', (30 + st.progress * 320) + 'deg');
        show(i);
      },
    });
  })();

  /* ---------- 6b5. Mariages : points 01-03 qui apparaissent sur la vidéo ---------- */
  (function mhero() {
    const pin = document.querySelector('.mhero__pin');
    if (!pin) return;
    const slides = gsap.utils.toArray('[data-mslide]');
    gsap.set(slides.slice(1), { autoAlpha: 0 });
    const tl = gsap.timeline({ scrollTrigger: { trigger: '.mhero', start: 'top top', end: '+=350%', pin: pin, scrub: .6, refreshPriority: 1 } });
    tl.fromTo('.mhero__video', { scale: 1 }, { scale: 1.12, ease: 'none', duration: 3.6 }, 0)
      .to('#mBar', { scaleX: 1, ease: 'none', duration: 3.6 }, 0)
      .to(slides[0], { autoAlpha: 0, y: -60, duration: .3 }, .5);
    let t = .75;
    slides.slice(1).forEach((sl, k) => {
      tl.set(sl, { autoAlpha: 1 }, t)
        .fromTo(sl.querySelectorAll('.ch'), { y: '110%', rotateX: -60 }, { y: '0%', rotateX: 0, duration: .28, stagger: .012, ease: 'power3.out' }, t)
        .fromTo(sl.querySelector('.mhero__num'), { xPercent: 25, autoAlpha: 0 }, { xPercent: 0, autoAlpha: .9, duration: .3 }, t)
        .fromTo(sl.querySelector('.mhero__p'), { y: 24, autoAlpha: 0 }, { y: 0, autoAlpha: 1, duration: .25 }, t + .08);
      if (k < 2) tl.to(sl, { autoAlpha: 0, y: -50, duration: .25 }, t + .72);
      t += .95;
    });
  })();

  /* ---------- 6c. Saisons : panneaux à recouvrement ---------- */
  const panels = gsap.utils.toArray('[data-panel]');
  panels.forEach((pn, i) => {
    const next = panels[i + 1];
    gsap.fromTo(pn.querySelector('[data-panel-img]'), { yPercent: -10 }, { yPercent: 10, ease: 'none', scrollTrigger: { trigger: pn, start: 'top bottom', end: 'bottom top', scrub: true } });
    gsap.from(pn.querySelectorAll('.panel__title .ch'), { y: '110%', rotateX: -60, duration: 1, stagger: .03, ease: 'power4.out', scrollTrigger: { trigger: pn, start: 'top 60%', once: true } });
    gsap.from(pn.querySelectorAll('.panel__lead, .panel__list li, .panel .link'), { y: 30, opacity: 0, duration: .9, stagger: .08, scrollTrigger: { trigger: pn, start: 'top 55%', once: true } });
    gsap.fromTo(pn.querySelector('.panel__ghost'), { xPercent: -8 }, { xPercent: 8, ease: 'none', scrollTrigger: { trigger: pn, start: 'top bottom', end: 'bottom top', scrub: true } });
    if (next) gsap.to(pn.querySelector('.panel__inner'), { scale: .9, opacity: .25, filter: 'blur(6px)', ease: 'none', scrollTrigger: { trigger: next, start: 'top bottom', end: 'top top', scrub: true } });
  });

  /* ---------- 6d. Frise (à-propos) + horaires (contact) ---------- */
  if (document.getElementById('tlLine')) gsap.to('#tlLine', { scaleY: 1, ease: 'none', scrollTrigger: { trigger: '.timeline__list', start: 'top 70%', end: 'bottom 60%', scrub: true } });
  const openNow = document.getElementById('openNow');
  if (openNow) {
    const d = new Date(), day = d.getDay(), m = d.getHours() * 60 + d.getMinutes();
    const slots = { 0: [[540, 750]], 2: [[540, 750], [900, 1110]], 3: [[540, 750], [900, 1110]], 4: [[540, 750], [900, 1110]], 5: [[540, 750], [900, 1110]], 6: [[540, 810]] };
    const open = (slots[day] || []).some(([a, b]) => m >= a && m < b);
    openNow.innerHTML = open ? '<i class="on"></i> Ouvert en ce moment' : '<i></i> Fermé en ce moment' + (day === 1 ? ' — réouverture mardi 9 h' : '');
  }

  /* ---------- 7. Primitives génériques ---------- */
  document.querySelectorAll('[data-speed]').forEach((el) => {
    const s = parseFloat(el.dataset.speed);
    gsap.fromTo(el, { yPercent: s * 40 }, { yPercent: s * -40, ease: 'none', scrollTrigger: { trigger: el.closest('section'), start: 'top bottom', end: 'bottom top', scrub: true } });
  });
  document.querySelectorAll('[data-parallax-img]').forEach((img) => {
    gsap.fromTo(img, { yPercent: -8, scale: 1.18 }, { yPercent: 8, scale: 1.18, ease: 'none', scrollTrigger: { trigger: img.closest('figure'), start: 'top bottom', end: 'bottom top', scrub: true } });
  });
  document.querySelectorAll('[data-reveal]').forEach((el) => {
    gsap.to(el, { opacity: 1, y: 0, duration: 1.1, scrollTrigger: { trigger: el, start: 'top 88%', once: true } });
  });
  document.querySelectorAll('[data-reveal-clip]').forEach((el) => {
    const media = el.querySelector('img,video');
    const tl = gsap.timeline({ scrollTrigger: { trigger: el, start: 'top 85%', once: true } });
    tl.to(el, { clipPath: 'inset(0% 0 0% 0 round 6px)', duration: 1.4, ease: 'expo.out' });
    if (media && !media.hasAttribute('data-parallax-img')) tl.to(media, { scale: 1, duration: 1.7, ease: 'expo.out' }, 0);
  });
  // titres en lettres (hors héros, signature, galerie : pilotés ailleurs)
  document.querySelectorAll('.h2[data-letters], .legal h2[data-letters]').forEach((el) => {
    gsap.from(el.querySelectorAll('.ch'), { y: '110%', rotateX: -60, duration: 1.1, stagger: .025, ease: 'power4.out', scrollTrigger: { trigger: el, start: 'top 85%', once: true } });
  });
  document.querySelectorAll('[data-scrub-words]').forEach((el) => {
    gsap.to(el.querySelectorAll('.sw'), { opacity: 1, stagger: .05, ease: 'none', scrollTrigger: { trigger: el, start: 'top 80%', end: 'bottom 50%', scrub: .5 } });
  });
  document.querySelectorAll('[data-3d]').forEach((el) => {
    const n = el.querySelector('.step__n');
    const fromRight = el.classList.contains('step--right');
    gsap.fromTo(el, { rotateX: -35, z: -300, y: 120, opacity: 0, transformOrigin: '50% 100%' }, { rotateX: 0, z: 0, y: 0, opacity: 1, ease: 'none', scrollTrigger: { trigger: el, start: 'top 95%', end: 'center 55%', scrub: .5 } });
    gsap.to(el, { opacity: 0, y: -80, rotateX: 18, z: -200, ease: 'none', scrollTrigger: { trigger: el, start: 'center 30%', end: 'bottom 5%', scrub: .5 } });
    if (n) gsap.fromTo(n, { xPercent: fromRight ? 40 : -40 }, { xPercent: fromRight ? -10 : 10, ease: 'none', scrollTrigger: { trigger: el, start: 'top bottom', end: 'bottom top', scrub: true } });
  });
  if (fine) document.querySelectorAll('[data-tilt]').forEach((el) => {
    const inner = el.querySelector('.tilt__inner');
    const rx = gsap.quickTo(inner, 'rotateX', { duration: .7, ease: 'power3' }), ry = gsap.quickTo(inner, 'rotateY', { duration: .7, ease: 'power3' });
    el.addEventListener('pointermove', (e) => {
      const r = el.getBoundingClientRect();
      rx(-((e.clientY - r.top) / r.height - .5) * 18); ry(((e.clientX - r.left) / r.width - .5) * 18);
    });
    el.addEventListener('pointerleave', () => { rx(0); ry(0); });
  });
  document.querySelectorAll('[data-marquee]').forEach((row) => {
    const w = row.children[0].offsetWidth;
    const dir = parseFloat(row.dataset.dir || 1);
    gsap.to(row, { x: -w * dir, duration: w / 50, ease: 'none', repeat: -1, modifiers: { x: (x) => ((parseFloat(x) % w) - (dir < 0 ? w : 0)) + 'px' } });
  });
  document.querySelectorAll('[data-count]').forEach((el) => {
    const n = { v: 0 }, t = parseInt(el.dataset.count, 10);
    gsap.to(n, { v: t, duration: 2, ease: 'power3.out', onUpdate: () => (el.textContent = Math.round(n.v)), scrollTrigger: { trigger: el, start: 'top 85%', once: true } });
  });

  // Note Google : 0,0 → 4,9, étoiles qui se remplissent, métiers qui éclosent
  (function facts() {
    const note = document.querySelector('.fact__note');
    if (!note) return;
    const stars = document.querySelector('.fact__stars'), tags = document.querySelectorAll('.fact__tags i');
    ScrollTrigger.create({
      trigger: note, start: 'top 88%', once: true,
      onEnter: () => {
        const o = { v: 0 };
        gsap.to(o, { v: 4.9, duration: 2, ease: 'power3.out', onUpdate: () => (note.textContent = o.v.toFixed(1).replace('.', ',')) });
        if (stars) gsap.fromTo(stars, { '--p': '0%' }, { '--p': '98%', duration: 2, ease: 'power3.out' });
        if (tags.length) gsap.from(tags, { scale: 0, opacity: 0, duration: .6, stagger: .12, ease: 'back.out(2)', delay: .3 });
      },
    });
  })();

  /* ---------- 8. Manifeste : lignes en contre-sens + images qui s'ouvrent ---------- */
  document.querySelectorAll('.mani__line').forEach((line) => {
    const s = parseFloat(line.dataset.shift) * (window.innerWidth <= 760 ? 7 : 14);
    gsap.fromTo(line, { xPercent: s }, { xPercent: -s, ease: 'none', scrollTrigger: { trigger: '.mani__lines', start: 'top bottom', end: 'bottom top', scrub: true } });
    gsap.to(line.querySelectorAll('.mani__inline'), { scaleX: 1, ease: 'power2.out', scrollTrigger: { trigger: line, start: 'top 80%', end: 'top 35%', scrub: .5 } });
  });

  /* ---------- 9. Atelier : zoom vidéo + ligne qui se trace ---------- */
  if (document.querySelector('.atelier')) gsap.fromTo('.atelier__video', { scale: 1 }, { scale: 1.35, ease: 'none', scrollTrigger: { trigger: '.atelier', start: 'top top', end: 'bottom bottom', scrub: true } });
  if (document.getElementById('aLine')) gsap.to('#aLine', { scaleY: 1, ease: 'none', scrollTrigger: { trigger: '.atelier', start: 'top top', end: 'bottom bottom', scrub: true } });

  /* ---------- 10. Signature : déformation WebGL + textes ---------- */
  (function signature() {
    const canvas = document.getElementById('sigCanvas');
    if (!canvas) return;
    const slides = [...document.querySelectorAll('.sig__slide')];
    const gl = new DisplaceGL(canvas, ['img/sig-1.webp', 'img/sig-2.webp', 'img/sig-3.webp']);
    // révélation en iris : la section s'ouvre en cercle sur la précédente
    if (window.innerWidth > 760) gsap.fromTo('.sig__pin', { clipPath: 'circle(9% at 50% 86%)' }, { clipPath: 'circle(142% at 50% 50%)', ease: 'power2.inOut', immediateRender: true, scrollTrigger: { trigger: '.signature', start: 'top 30%', end: 'top top', scrub: .5 } });
    if (!gl.ok) document.querySelector('.signature').classList.add('no-gl');
    let active = 0;
    function activate(i) {
      if (i === active) return;
      const old = slides[active];
      old.classList.remove('is-active');
      old.classList.add('is-leaving');
      setTimeout(() => old.classList.remove('is-leaving'), 900);
      slides[i].classList.add('is-active');
      active = i;
    }
    ScrollTrigger.create({
      trigger: '.signature', start: 'top top', end: '+=' + (slides.length * 100) + '%', pin: '.sig__pin', pinSpacing: true, scrub: true,
      refreshPriority: 1,
      onUpdate: (st) => {
        const p = st.progress * (slides.length - 1);
        if (gl.ok) gl.progress = p;
        activate(Math.round(p));
        document.getElementById('sBar').style.transform = `scaleY(${st.progress})`;
      },
    });
    // lettres fantômes : chacune à sa profondeur
    document.querySelectorAll('.sig__ghost span').forEach((s, i) => {
      gsap.fromTo(s, { y: (i % 2 ? 1 : -1) * 160, z: -300 + i * 60, rotateY: -20 }, { y: (i % 2 ? -1 : 1) * 160, z: 200 - i * 60, rotateY: 20, ease: 'none', scrollTrigger: { trigger: '.signature', start: 'top top', end: 'bottom bottom', scrub: true } });
    });
    window.addEventListener('resize', () => gl.ok && gl.resize());
  })();

  /* ---------- 11. Galerie : éventail depuis la pile ---------- */
  (function gallery() {
    const items = gsap.utils.toArray('.gal__item');
    if (!items.length) return;
    const tl = gsap.timeline({ scrollTrigger: { trigger: '.galerie', start: 'top top', end: '+=220%', pin: '.gal__pin', scrub: .8, refreshPriority: 1 } });
    items.forEach((it, i) => {
      const x = parseFloat(it.style.getPropertyValue('--x')), y = parseFloat(it.style.getPropertyValue('--y'));
      tl.fromTo(it,
        { x: () => -x * window.innerWidth / 100, y: () => -y * window.innerHeight / 100, rotate: (i - 3) * 4, scale: .55, z: -i * 60 },
        { x: 0, y: 0, rotate: 0, scale: 1, z: 0, ease: 'power2.inOut', duration: 1 },
        i * .06);
    });
    tl.to(items, { scale: .82, z: -250, opacity: .55, ease: 'power2.inOut', duration: .6, stagger: { each: .02, from: 'center' } }, 1.1)
      .to('.gal__title .ch', { y: '0%', duration: .5, stagger: .02, ease: 'power3.out' }, 1.25)
      .to('.gal__head .eyebrow', { opacity: 1, duration: .3 }, 1.35);
  })();

  /* ---------- 12. Vitrine horizontale pinnée (desktop) ---------- */
  ScrollTrigger.matchMedia({
    '(min-width: 761px)': () => {
      const track = document.getElementById('track');
      if (!track) return;
      const cards = gsap.utils.toArray('.card');
      const dist = () => track.scrollWidth - window.innerWidth + parseFloat(getComputedStyle(track.parentElement).paddingLeft);
      // le pin dure un écran de plus : l'atelier vient recouvrir la vitrine encore épinglée
      ScrollTrigger.create({ trigger: '.vitrine', start: 'top top', end: () => '+=' + (dist() * 1.2 + window.innerHeight), pin: true, anticipatePin: 1, invalidateOnRefresh: true, refreshPriority: 1 });
      gsap.to('.vitrine__pin', { scale: .96, filter: 'brightness(.6)', ease: 'power2.in', scrollTrigger: { trigger: '.atelier', start: 'top 80%', end: 'top top', scrub: .5 } });
      const tween = gsap.to(track, {
        x: () => -dist(), ease: 'none',
        scrollTrigger: {
          trigger: '.vitrine', start: 'top top', end: () => '+=' + dist() * 1.2, scrub: 1, invalidateOnRefresh: true,
          onUpdate: (st) => {
            document.getElementById('vCur').textContent = String(Math.min(7, Math.floor(st.progress * 7.4) + 1)).padStart(2, '0');
            document.getElementById('vBar').style.transform = `scaleX(${st.progress})`;
          },
        },
      });
      gsap.to('.vitrine__ghost', { xPercent: -45, ease: 'none', scrollTrigger: { trigger: '.vitrine', start: 'top top', end: () => '+=' + dist() * 1.2, scrub: 1 } });
      cards.forEach((c) => {
        const img = c.querySelector('.card__img img');
        gsap.set(c, { rotateY: 42, z: -500, scale: .82, opacity: .35 });
        gsap.to(c, { keyframes: [{ rotateY: 0, z: 0, scale: 1, opacity: 1 }, { rotateY: -42, z: -500, scale: .82, opacity: .35 }], ease: 'none', scrollTrigger: { trigger: c, containerAnimation: tween, start: 'left right', end: 'right left', scrub: true } });
        if (img) gsap.fromTo(img, { xPercent: -6 }, { xPercent: 6, ease: 'none', scrollTrigger: { trigger: c, containerAnimation: tween, start: 'left right', end: 'right left', scrub: true } });
      });
    },
  });

  /* ---------- 13. Footer : nom géant qui monte ---------- */
  if (document.querySelector('.footer__giant')) gsap.fromTo('.footer__giant', { scale: .6, yPercent: 30, opacity: .3 }, { scale: 1, yPercent: 0, opacity: 1, ease: 'none', scrollTrigger: { trigger: '.footer', start: 'top bottom', end: 'top 30%', scrub: true } });

  // les pins doivent être calculés avant les triggers situés plus bas dans la page
  ScrollTrigger.sort();
  window.addEventListener('load', () => ScrollTrigger.refresh());
  let rt; window.addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(() => ScrollTrigger.refresh(), 200); });
})();
