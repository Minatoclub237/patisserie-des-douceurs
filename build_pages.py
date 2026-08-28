# -*- coding: utf-8 -*-
"""Génère les pages secondaires (header/footer communs, un mécanisme propre par page).
   python build_pages.py  → carte, mariages, saisons, a-propos, contact, mentions-legales
   + met à jour la nav d'index.html."""
import os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))

MAPS = 'https://www.google.com/maps/place/La+P%C3%A2tisserie+Des+Douceurs/@45.7500017,3.1126129,17z/data=!3m1!4b1!4m6!3m5!1s0x47f71c6318a7c699:0xd2ce1351e3a34133!8m2!3d45.7500017!4d3.1126129!16s%2Fg%2F11g0hn_td8'
IG = 'https://www.instagram.com/lapatisseriedesdouceurs/'
FB = 'https://www.facebook.com/p/La-p%C3%A2tisserie-des-douceurs-100042399776991/'
TEL = 'tel:+33668932419'
MAIL = 'yohann.girard63@gmail.com'

NAV_LINKS = [('carte.html', 'La carte'), ('mariages.html', 'Mariages'), ('saisons.html', 'Saisons'), ('a-propos.html', 'La maison'), ('contact.html', 'Contact')]

def head(title, desc, body_class=''):
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="img/hero.webp">
<meta property="og:locale" content="fr_FR">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%23120A0D'/%3E%3Ccircle cx='16' cy='17' r='8' fill='%23E48C9D'/%3E%3Ccircle cx='13' cy='13' r='2.2' fill='%23C4364F'/%3E%3Ccircle cx='19' cy='13' r='2.2' fill='%23C4364F'/%3E%3Ccircle cx='16' cy='10' r='2.2' fill='%23C4364F'/%3E%3C/svg%3E">
<link rel="preload" href="fonts/urbanist-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="vendor/lenis.css">
<link rel="stylesheet" href="styles.css">
<link rel="stylesheet" href="pages.css">
</head>
<body class="sub {body_class}">

<div class="grain" aria-hidden="true"></div>
<div class="cursor" aria-hidden="true"><span class="cursor__dot"></span><span class="cursor__ring"><span class="cursor__label"></span></span></div>
'''

def nav(current):
    links = ''.join(f'<a href="{h}"{" aria-current=page" if h == current else ""}>{l}</a>' for h, l in NAV_LINKS)
    return f'''<header class="nav" id="nav">
  <button class="nav__burger" id="burger" aria-label="Menu"><i></i><i></i></button>
  <a class="nav__logo" href="index.html" aria-label="Pâtisserie des Douceurs">
    <img class="nav__logo-img" src="img/logo.webp" alt="Pâtisserie des Douceurs">
  </a>
  <nav class="nav__links">{links}</nav>
  <a class="btn btn--pill" href="{TEL}" data-cursor="Appeler" data-magnet>06 68 93 24 19</a>
</header>
<div class="menu" id="menu">
  <a href="index.html">Accueil</a>{links}
</div>
'''

FOOTER = f'''<footer class="footer footer--page">
  <img class="footer__logo" src="img/logo.webp" alt="Pâtisserie des Douceurs">
  <div class="footer__cols">
    <div><b>La Pâtisserie Des Douceurs</b><br>7 rue des Ramacles<br>63170 Aubière</div>
    <div>Mar – Ven · 9 h – 12 h 30 &amp; 15 h – 18 h 30<br>Sam · 9 h – 13 h 30 · Dim · 9 h – 12 h 30<br>Fermé le lundi</div>
    <div><a href="{TEL}">06 68 93 24 19</a><br><a href="mailto:{MAIL}">{MAIL}</a><br><a href="{IG}" target="_blank" rel="noopener"><svg class="ig-ico" viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="2.5" y="2.5" width="19" height="19" rx="5.5" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4.2" stroke="currentColor" stroke-width="1.8"/><circle cx="17.4" cy="6.6" r="1.4" fill="currentColor"/></svg>Instagram</a> · <a href="{FB}" target="_blank" rel="noopener">Facebook</a></div>
    <div><a href="index.html">Accueil</a><br><a href="carte.html">La carte</a><br><a href="mariages.html">Mariages &amp; événements</a><br><a href="saisons.html">Saisons</a><br><a href="a-propos.html">La maison</a><br><a href="contact.html">Contact</a></div>
  </div>
  <div class="footer__row">
    <span>© 2026 La Pâtisserie Des Douceurs · Yohann Girard, entrepreneur individuel · SIRET 833 167 109 00010</span>
    <span><a href="mentions-legales.html">Mentions légales · CGV · Confidentialité</a></span>
  </div>
</footer>
'''

def tail(extra_js=''):
    return f'''
<script src="vendor/gsap.min.js"></script>
<script src="vendor/ScrollTrigger.min.js"></script>
<script src="vendor/lenis.min.js"></script>
<script src="main.js"></script>
{extra_js}
</body>
</html>
'''

# ═══════════════════════════ CARTE ═══════════════════════════
FAMILIES = [
  ('patisserie', 'Pâtisserie', '01', 'img/carte-5.webp', 'img/cake-2.webp',
   'Entremets, tartes et créations sucrées, fabriqués chaque matin à l’atelier. Sur commande pour les grandes tailles.',
   [('Entremets de la maison', 'Mousses légères, biscuits moelleux, glaçage velours — 4, 6 ou 8 parts'),
    ('Tarte aux myrtilles', 'La tarte que les habitués réservent d’avance'),
    ('Forêt-noire', 'Chocolat, cerise, chantilly — le classique, avec justesse'),
    ('Tartes de saison', 'Fruits du moment sur pâte sucrée fine'),
    ('Gâteaux d’anniversaire', 'Personnalisés, possibles sous 24 h — <a href="mariages.html">voir la page commande</a>'),
    ('Pièces individuelles', 'La vitrine du jour, différente chaque semaine')]),
  ('chocolat', 'Chocolats & confiserie', '02', 'img/carte-3.webp', 'img/cake-3.webp',
   'Bonbons de chocolat, tablettes, confiseries — « un superbe chocolatier », disent les avis.',
   [('Bonbons de chocolat', 'Ganaches et pralinés, vendus au poids ou en coffret'),
    ('Tablettes', 'Noir, lait, aux éclats'),
    ('Confiseries', 'Pâtes de fruits, caramels, guimauves — selon la saison'),
    ('Coffrets cadeaux', 'Composés en boutique, à offrir')]),
  ('glaces', 'Glaces artisanales', '03', 'img/carte-4.webp', 'img/berries.webp',
   'Glaces et sorbets fabriqués sur place à la belle saison, avec les fruits du moment.',
   [('Sorbets aux fruits', 'Fruits frais, sans arôme'),
    ('Crèmes glacées', 'Vanille, chocolat, caramel… selon le jour'),
    ('Desserts glacés', 'Sur commande, pour les grandes tablées d’été')]),
  ('pain', 'Pain au levain & tradition', '04', 'img/carte-2.webp', 'img/croissant.webp',
   'Baguettes de tradition et pains au levain, à base de farines soigneusement sélectionnées.',
   [('Baguette de tradition', 'Croûte fine, mie crème, cuite plusieurs fois par jour'),
    ('Pain au levain', 'Fermentation lente, farines sélectionnées'),
    ('Pains spéciaux', 'Selon les jours — demandez en boutique')]),
]

def carte():
    fam_nav = ''.join(f'<a href="#{k}">{n}</a>' for k, n, *_ in FAMILIES)
    col_imgs = ['img/carte-5.webp', 'img/carte-3.webp', 'img/carte-4.webp', 'img/carte-2.webp', 'img/carte-1.webp', 'img/gal-6.webp']
    col = ''.join(f'<img src="{i}" alt="" loading="eager">' for i in col_imgs)
    blocks = ''
    for i, (k, n, num, img1, img2, lead, items) in enumerate(FAMILIES):
        lis = ''.join(f'<li data-reveal><h3>{t}</h3><p>{d}</p><b>Prix en boutique</b></li>' for t, d in items)
        blocks += f'''
<section class="fam{" fam--alt" if i % 2 else ""}" id="{k}">
  <div class="fam__visual">
    <figure class="fam__fig" data-reveal-clip><img src="{img1}" alt="" loading="lazy" data-parallax-img></figure>
    <figure class="fam__small" data-speed="-0.35" data-reveal-clip><img src="{img2}" alt="" loading="lazy"></figure>
    <span class="fam__num" data-speed="0.25" aria-hidden="true">{num}</span>
  </div>
  <div class="fam__text">
    <p class="eyebrow" data-reveal>{num} — Famille</p>
    <h2 class="h2" data-letters>{n}</h2>
    <p class="fam__lead" data-scrub-words>{lead}</p>
    <ul class="fam__list">{lis}</ul>
  </div>
</section>'''
    return (head('La carte — La Pâtisserie Des Douceurs, Aubière', 'Pâtisserie, chocolats, glaces artisanales et pain au levain : toute la carte de La Pâtisserie Des Douceurs à Aubière.', 'p-carte')
        + nav('carte.html')
        + f'''<main id="top">
<section class="split-hero">
  <div class="split-hero__text">
    <p class="eyebrow" data-reveal>La carte</p>
    <h1 class="split-hero__title" data-letters>Tout est fait ici</h1>
    <p class="split-hero__lead" data-reveal>Quatre familles, une seule adresse. Les prix sont affichés en boutique ; tout se commande au 06 68 93 24 19.</p>
    <nav class="split-hero__nav" data-reveal>{fam_nav}</nav>
  </div>
  <div class="split-hero__col" aria-hidden="true">
    <div class="vmarquee" data-vmarquee><div class="vmarquee__row">{col}</div><div class="vmarquee__row">{col}</div></div>
  </div>
</section>
{blocks}
<section class="phone-band">
  <p class="eyebrow" data-reveal>Une envie précise ? Un seul numéro</p>
  <a class="phone-band__num" href="{TEL}" data-letters data-cursor="Appeler">06 68 93 24 19</a>
  <p class="phone-band__sub" data-reveal>Mar – Ven 9 h – 12 h 30 &amp; 15 h – 18 h 30 · Sam 9 h – 13 h 30 · Dim 9 h – 12 h 30</p>
</section>
</main>''' + FOOTER + tail())

# ═══════════════════════════ MARIAGES ═══════════════════════════
def mariages():
    cards = [('img/scard-1.webp', 'Gâteau personnalisé « Lya, 1 an »', 'Commande sur mesure · tortue en pâte à sucre · premier anniversaire'),
             ('img/scard-2.webp', 'Le Merveilleux', 'Pâtisserie d’antan · meringue, chantilly, copeaux de chocolat noir'),
             ('img/scard-3.webp', 'Wedding cake « Laëtitia & Julien »', 'Trois étages · roses en sucre · plaque dédicacée au cornet'),
             ('img/scard-4.webp', 'Pièce montée nougatine & amande', 'Choux vanille, praliné, chocolat · montage carré, décor nougatine')]
    stack = ''.join(f'''
    <article class="scard" style="--i:{i}">
      <img src="{img}" alt="" loading="lazy">
      <div class="scard__body"><span class="scard__n">0{i+1}</span><h3>{t}</h3><p>{d}</p></div>
    </article>''' for i, (img, t, d) in enumerate(cards))
    return (head('Mariages, anniversaires & pièces montées — La Pâtisserie Des Douceurs', 'Pièces montées de mariage, gâteaux d’anniversaire et desserts d’événement sur commande à Aubière. Simulateur de devis en ligne.', 'p-mariages')
        + nav('mariages.html')
        + f'''<main id="top">
<section class="mhero">
  <div class="mhero__pin">
    <video class="mhero__video" autoplay muted loop playsinline poster="img/mariages-hero.webp" data-hero-img data-src-hd="video/mariages-hero.mp4" data-src-sd="video/mariages-hero-720.mp4"></video>
    <div class="mhero__veil"></div>
    <div class="mhero__slide" data-mslide>
      <p class="eyebrow" data-letters>Sur commande</p>
      <h1 class="mhero__h"><span data-letters>Le gâteau</span><span data-letters>du jour J</span></h1>
      <p class="mhero__p">Pièces montées pour mariages et célébrations, gâteaux d'anniversaire, desserts d'événement — conçus avec vous, livrés sur place.</p>
      <div class="mhero__cta"><a class="btn btn--light" href="#simulateur" data-magnet data-cursor="Estimer">Estimer ma commande</a></div>
    </div>
    <div class="mhero__slide" data-mslide><span class="mhero__num" aria-hidden="true">01</span><h2 class="mhero__h"><span data-letters>On en</span><span data-letters>parle</span></h2><p class="mhero__p">Nombre de parts, date, lieu, envies. Par téléphone, par e-mail, ou avec le simulateur juste en dessous.</p></div>
    <div class="mhero__slide" data-mslide><span class="mhero__num" aria-hidden="true">02</span><h2 class="mhero__h"><span data-letters>Yohann</span><span data-letters>conçoit</span></h2><p class="mhero__p">Parfums, étages, décor. Un devis précis sous 48 h, une dégustation possible pour les mariages.</p></div>
    <div class="mhero__slide" data-mslide><span class="mhero__num" aria-hidden="true">03</span><h2 class="mhero__h"><span data-letters>Livré</span><span data-letters>le jour J</span></h2><p class="mhero__p">Montage et livraison sur place à Aubière, Clermont-Ferrand et alentours. Vous n'avez rien à porter.</p></div>
    <div class="mhero__bar"><i id="mBar"></i></div>
  </div>
</section>

<section class="stackcards">
  <header class="stackcards__head"><p class="eyebrow" data-reveal>Réalisations</p><h2 class="h2" data-letters>Elles sont passées par l’atelier</h2></header>
  <div class="stackcards__list">{stack}</div>
</section>

<section class="simu" id="simulateur">
  <div class="simu__intro">
    <p class="eyebrow" data-reveal>Simulateur</p>
    <h2 class="h2" data-letters>Estimez votre commande</h2>
    <p class="simu__lead" data-reveal>Une fourchette indicative en 30 secondes. Le devis définitif est établi par Yohann après échange — il ne remplace pas la conversation, il la prépare.</p>
  </div>
  <form class="simu__form" id="simu" data-reveal>
    <fieldset>
      <legend>Type de pièce</legend>
      <div class="simu__choices">
        <label><input type="radio" name="type" value="choux" checked><span><b>Pièce montée en choux</b><small>Croquembouche, nougatine, caramel</small></span></label>
        <label><input type="radio" name="type" value="wedding"><span><b>Wedding cake</b><small>Entremets à étages, décor sur mesure</small></span></label>
        <label><input type="radio" name="type" value="anniv"><span><b>Gâteau d’anniversaire</b><small>Entremets personnalisé, sous 24 h possible</small></span></label>
        <label><input type="radio" name="type" value="buffet"><span><b>Buffet de desserts</b><small>Assortiment de pièces individuelles</small></span></label>
      </div>
    </fieldset>
    <fieldset>
      <legend>Nombre de parts <output id="partsOut">60</output></legend>
      <input type="range" name="parts" id="parts" min="6" max="250" step="2" value="60">
      <div class="simu__scale"><span>6</span><span>60</span><span>120</span><span>250</span></div>
    </fieldset>
    <fieldset>
      <legend>Parfums <small>(deux au maximum)</small></legend>
      <div class="simu__tags" id="parfums">
        <label><input type="checkbox" value="Vanille"><span>Vanille</span></label>
        <label><input type="checkbox" value="Chocolat"><span>Chocolat</span></label>
        <label><input type="checkbox" value="Framboise"><span>Framboise</span></label>
        <label><input type="checkbox" value="Praliné"><span>Praliné</span></label>
        <label><input type="checkbox" value="Citron"><span>Citron</span></label>
        <label><input type="checkbox" value="Caramel"><span>Caramel</span></label>
        <label><input type="checkbox" value="Pistache"><span>Pistache</span></label>
        <label><input type="checkbox" value="Fruits de saison"><span>Fruits de saison</span></label>
      </div>
    </fieldset>
    <fieldset>
      <legend>Options</legend>
      <div class="simu__tags">
        <label><input type="checkbox" name="opt" value="Décor floral" data-price="60"><span>Décor floral</span></label>
        <label><input type="checkbox" name="opt" value="Nougatine sculptée" data-price="40"><span>Nougatine sculptée</span></label>
        <label><input type="checkbox" name="opt" value="Personnalisation (prénoms, texte)" data-price="20"><span>Personnalisation</span></label>
        <label><input type="checkbox" name="opt" value="Présentoir prêté" data-price="0"><span>Présentoir prêté</span></label>
        <label><input type="checkbox" name="opt" value="Livraison et montage sur place" data-price="35"><span>Livraison &amp; montage</span></label>
      </div>
    </fieldset>
    <fieldset class="simu__when">
      <legend>Quand et où</legend>
      <input type="date" name="date" id="simuDate" aria-label="Date de l’événement" required>
      <input type="text" name="lieu" placeholder="Lieu (ville ou salle)">
    </fieldset>
    <aside class="simu__result" data-3d>
      <p class="eyebrow">Estimation indicative</p>
      <p class="simu__price"><span id="priceLow">—</span> <i>à</i> <span id="priceHigh">—</span></p>
      <p class="simu__detail" id="priceDetail"></p>
      <p class="simu__note">Fourchette calculée à partir de tarifs indicatifs, hors dégustation. Le devis définitif dépend du décor et de la date.</p>
      <div class="simu__send">
        <input type="text" name="nom" placeholder="Votre nom" required>
        <input type="tel" name="tel" placeholder="Votre téléphone" required>
        <button class="btn btn--light" type="submit" data-cursor="Envoyer" data-magnet>Envoyer la demande de devis</button>
      </div>
      <p class="boutique__ok">Votre demande s’ouvre dans votre messagerie — il ne reste qu’à l’envoyer.</p>
    </aside>
  </form>
</section>

<section class="faq">
  <p class="eyebrow" data-reveal>Questions fréquentes</p>
  <h2 class="h2" data-letters>Avant de commander</h2>
  <div class="faq__list">
    <details data-reveal><summary>Combien de temps à l’avance ?</summary><p>Un gâteau d’anniversaire peut se faire sous 24 h selon le planning. Pour une pièce montée de mariage, comptez 3 à 4 semaines, davantage en juin et septembre.</p></details>
    <details data-reveal><summary>Peut-on goûter avant ?</summary><p>Oui, pour les mariages : une dégustation des parfums est proposée lors du rendez-vous de commande.</p></details>
    <details data-reveal><summary>Livrez-vous ?</summary><p>Oui, à Aubière, Clermont-Ferrand et alentours. Le montage est fait sur place pour les pièces montées. Livraison le jour même possible.</p></details>
    <details data-reveal><summary>Comment régler ?</summary><p>Un acompte à la commande, le solde à la livraison ou au retrait. Carte bancaire, sans contact et espèces acceptés en boutique.</p></details>
    <details data-reveal><summary>Allergies, sans gluten ?</summary><p>Parlez-en à la commande : certaines recettes peuvent être adaptées. L’atelier travaille fruits à coque, gluten, lait et œufs.</p></details>
  </div>
</section>
</main>''' + FOOTER + tail('<script src="simulateur.js"></script>'))

# ═══════════════════════════ SAISONS ═══════════════════════════
SEASONS = [
  ('noel', 'Noël', 'Décembre', '#120A0D', '#F6EBE6', 'img/cake-3.webp', 'Bûches maison, chocolats de fêtes, coffrets à offrir. Les bûches se commandent à partir de fin novembre.', ['Bûches pâtissières et glacées', 'Coffrets de chocolats', 'Sablés et confiseries de Noël']),
  ('galette', 'Galette', 'Janvier', '#3A1A22', '#F6EBE6', 'img/croissant.webp', 'Galette individuelle au feuilletage croustillant, crème d’amande équilibrée. Frangipane et versions du moment.', ['Galette frangipane, 4 à 8 parts', 'Galette individuelle', 'Brioche des rois']),
  ('paques', 'Pâques', 'Mars – Avril', '#EFC9CF', '#120A0D', 'img/macaron.webp', 'Moulages, œufs garnis, sujets en chocolat — tout est coulé à l’atelier.', ['Œufs et moulages', 'Fritures et petits sujets', 'Entremets de Pâques']),
  ('ete', 'Été', 'Juin – Septembre', '#F6EBE6', '#120A0D', 'img/berries.webp', 'Glaces et sorbets aux fruits frais, tartes de saison, pièces montées de mariage.', ['Sorbets et crèmes glacées', 'Tartes aux fruits', 'Saison des mariages']),
]

def saisons():
    words = ''.join(f'<a href="#{k}" class="type-hero__word" style="--c:{bg if i in (2, 3) else "#E48C9D"}" data-letters>{n}</a>' for i, (k, n, when, bg, *_) in enumerate(SEASONS))
    panels = ''
    for i, (k, n, when, bg, fg, img, lead, items) in enumerate(SEASONS):
        lis = ''.join(f'<li>{x}</li>' for x in items)
        panels += f'''
<section class="panel" id="{k}" style="--bg:{bg};--fg:{fg}" data-panel>
  <div class="panel__inner">
    <span class="panel__ghost" aria-hidden="true">{n}</span>
    <figure class="panel__fig"><img src="{img}" alt="" loading="lazy" data-panel-img></figure>
    <div class="panel__text">
      <p class="eyebrow">{when}</p>
      <h2 class="panel__title" data-letters>{n}</h2>
      <p class="panel__lead">{lead}</p>
      <ul class="panel__list">{lis}</ul>
      <a class="link" href="tel:+33668932419">Commander <i>→</i></a>
    </div>
    <span class="panel__count">0{i+1} / 0{len(SEASONS)}</span>
  </div>
</section>'''
    ig = ''.join(f'<img src="{i}" alt="" loading="lazy">' for i in ['img/cake-3.webp', 'img/croissant.webp', 'img/macaron.webp', 'img/berries.webp', 'img/cake-2.webp', 'img/tart.webp', 'img/pastry.webp', 'img/cake-5.webp'])
    return (head('Saisons — Noël, galette, Pâques, été — La Pâtisserie Des Douceurs', 'Bûches de Noël, galettes des rois, chocolats de Pâques, glaces d’été : les rendez-vous de l’année à La Pâtisserie Des Douceurs, Aubière.', 'p-saisons')
        + nav('saisons.html')
        + f'''<main id="top">
<section class="type-hero">
  <p class="eyebrow" data-reveal>Les rendez-vous de l’année</p>
  <div class="type-hero__words">{words}</div>
  <p class="type-hero__lead" data-reveal>Quatre moments où la vitrine change de visage. Tout se commande à l’avance — et part vite. Cliquez une saison.</p>
</section>
<div class="stack">{panels}</div>
<section class="ig-band">
  <p class="eyebrow" data-reveal>La vitrine, chaque semaine</p>
  <a class="ig-band__handle" href="{IG}" target="_blank" rel="noopener" data-cursor="Ouvrir"><svg class="ig-ico ig-ico--big" viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="2.5" y="2.5" width="19" height="19" rx="5.5" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4.2" stroke="currentColor" stroke-width="1.8"/><circle cx="17.4" cy="6.6" r="1.4" fill="currentColor"/></svg>@lapatisseriedesdouceurs</a>
  <div class="marquee ig-band__row" aria-hidden="true"><div class="marquee__row" data-marquee><span class="ig-band__set">{ig}</span><span class="ig-band__set">{ig}</span></div></div>
</section>
</main>''' + FOOTER + tail())

# ═══════════════════════════ À PROPOS ═══════════════════════════
def apropos():
    moments = [('4 h 30', 'Le four', 'Les baguettes de tradition et les pains au levain partent en premier. La pièce est encore fraîche.'),
               ('6 h', 'Les entremets', 'Montage à la poche, repos au froid, glaçage velours. Ce qui a été fait la veille sort de cellule.'),
               ('9 h', 'La boutique ouvre', 'Vitrine dressée. Les premières commandes du jour se retirent — parfois passées la veille.'),
               ('12 h 30', 'Pause', 'Fermeture jusqu’à 15 h. Le temps de couler le chocolat, de turbiner les glaces en été.'),
               ('15 h', 'Réouverture', 'Jusqu’à 18 h 30. On prend les commandes de la semaine, on parle pièces montées.')]
    mm = ''.join(f'<div class="day__moment" data-moment="{i}"><b>{t}</b><h3>{h}</h3><p>{p}</p></div>' for i, (t, h, p) in enumerate(moments))
    reviews = [('Les desserts sont parfaitement équilibrés, ni écœurants ni trop sucrés — on en reprendrait. Le pâtissier est très accueillant et gentil.', 'Avis Google'),
               ('Gâteau d’anniversaire commandé à peine 24 h avant, et qui était excellent et magnifique !', 'Charlotte C.'),
               ('Un superbe chocolatier. L’un des meilleurs pâtissiers de la région, sans discussion.', 'Avis Google'),
               ('Superbe tarte aux myrtilles !', 'Benoît T.'),
               ('Très bon accueil avec une excellente pâtisserie.', 'Pascal L.'),
               ('L’un des meilleurs gâteaux que j’aie achetés.', 'Avis Google')]
    cols = [[], [], []]
    for i, r in enumerate(reviews): cols[i % 3].append(r)
    wall = ''.join(f'<div class="wall__col" data-speed="{s}">' + ''.join(f'<blockquote data-reveal><p>« {q} »</p><cite>{a} · 5/5</cite></blockquote>' for q, a in c) + '</div>' for c, s in zip(cols, ['-0.3', '0.2', '-0.15']))
    return (head('La maison — Yohann Girard, pâtissier chocolatier à Aubière', 'Yohann Girard a ouvert La Pâtisserie Des Douceurs à Aubière en 2017 : pâtisserie générale, chocolats fins, glaces artisanales, pain au levain — tout est fait à l’atelier.', 'p-maison')
        + nav('a-propos.html')
        + f'''<main id="top">
<section class="portrait-hero">
  <div class="portrait-hero__text">
    <p class="eyebrow" data-reveal>La maison</p>
    <h1 class="portrait-hero__title" data-letters>Un artisan, un atelier</h1>
    <p class="portrait-hero__lead" data-reveal>Yohann Girard — pâtissier, chocolatier, glacier et boulanger. Installé au 7 rue des Ramacles depuis novembre 2017.</p>
    <div class="facts" data-reveal>
      <div class="fact"><b><span data-count="2017">0</span></b><span class="fact__label">Novembre 2017 · ouverture rue des Ramacles</span></div>
      <div class="fact"><b><span class="fact__note">4,9</span><i>/5</i></b><span class="fact__stars" aria-label="4,9 sur 5">★★★★★</span><span class="fact__label">Une cinquantaine d’avis Google</span></div>
      <div class="fact"><b><span data-count="4">0</span></b><span class="fact__tags"><i>Pâtissier</i><i>Chocolatier</i><i>Glacier</i><i>Boulanger</i></span></div>
    </div>
  </div>
  <figure class="portrait-hero__fig tilt" data-tilt data-reveal-clip>
    <div class="tilt__inner"><img src="img/maison-hero.webp" alt="La vitrine de la boutique, rue des Ramacles" data-parallax-img></div>
    <span class="portrait-hero__stamp" data-speed="-0.4">Fait<br>maison</span>
  </figure>
</section>

<section class="quote">
  <p class="quote__mark" aria-hidden="true">«</p>
  <p class="quote__text" data-scrub-words>Une pâtisserie générale au sens plein : entremets, tartes, gâteaux d’anniversaire et pièces montées sur commande, chocolats fins, glaces artisanales, confiseries — et le pain, au levain et en tradition, avec des farines soigneusement sélectionnées. Pas de sous-traitance : ce qui est en vitrine a été fait ici, par lui.</p>
</section>

<section class="day" id="journee">
  <div class="day__pin">
    <div class="day__clock" aria-hidden="true">
      <span class="day__halo"></span>
      <span class="day__glow" id="clockGlow"></span>
      <span class="day__disc">
        <span class="day__ticks" id="clockTicks"></span>
        <i class="day__hand" id="clockHand"><b></b></i>
        <span class="day__time" id="clockTime">4 h 30</span>
      </span>
    </div>
    <div class="day__text">
      <p class="eyebrow">Une journée à l’atelier</p>
      <div class="day__moments">{mm}</div>
      <div class="day__dots" aria-hidden="true">{''.join('<i></i>' for _ in moments)}</div>
    </div>
  </div>
</section>

<section class="trev">
  <p class="trev__eyebrow" data-reveal>Témoignages</p>
  <h2 class="trev__title" data-reveal>Des clients <span>conquis</span></h2>
  <div class="trev__grid">
    <article class="trev__card" data-reveal>
      <header><svg class="trev__g" viewBox="0 0 24 24" width="20" height="20" aria-label="Google"><path fill="#4285F4" d="M23.5 12.3c0-.9-.1-1.5-.3-2.2H12v4.1h6.5c-.1 1.1-.8 2.7-2.4 3.8l3.7 2.9c2.2-2.1 3.7-5.1 3.7-8.6z"/><path fill="#34A853" d="M12 24c3.2 0 6-1.1 7.9-2.9l-3.7-2.9c-1 .7-2.4 1.2-4.2 1.2-3.2 0-6-2.2-6.9-5.2L1.3 17.1C3.3 21.2 7.3 24 12 24z"/><path fill="#FBBC05" d="M5.1 14.2c-.3-.7-.4-1.4-.4-2.2s.1-1.5.4-2.2L1.3 6.9C.5 8.5 0 10.2 0 12s.5 3.5 1.3 5.1l3.8-2.9z"/><path fill="#EA4335" d="M12 4.6c2.3 0 3.8 1 4.7 1.8l3.3-3.2C18 1.2 15.2 0 12 0 7.3 0 3.3 2.8 1.3 6.9l3.8 2.9c.9-3 3.7-5.2 6.9-5.2z"/></svg><span class="trev__score">5,0 <i>★</i></span></header>
      <p class="trev__quote">« Vraiment superbe pâtisserie. Tout est bon : le chocolat maison, la guimauve… et les gâteaux. Hmmm, le tiramisu ! Très bien servi par le chef. »</p>
      <footer><b>A</b><div><strong>Aminou</strong><span>Tiramisu, chocolat maison · il y a 8 mois</span></div></footer>
    </article>
    <article class="trev__card" data-reveal>
      <header><svg class="trev__g" viewBox="0 0 24 24" width="20" height="20" aria-label="Google"><path fill="#4285F4" d="M23.5 12.3c0-.9-.1-1.5-.3-2.2H12v4.1h6.5c-.1 1.1-.8 2.7-2.4 3.8l3.7 2.9c2.2-2.1 3.7-5.1 3.7-8.6z"/><path fill="#34A853" d="M12 24c3.2 0 6-1.1 7.9-2.9l-3.7-2.9c-1 .7-2.4 1.2-4.2 1.2-3.2 0-6-2.2-6.9-5.2L1.3 17.1C3.3 21.2 7.3 24 12 24z"/><path fill="#FBBC05" d="M5.1 14.2c-.3-.7-.4-1.4-.4-2.2s.1-1.5.4-2.2L1.3 6.9C.5 8.5 0 10.2 0 12s.5 3.5 1.3 5.1l3.8-2.9z"/><path fill="#EA4335" d="M12 4.6c2.3 0 3.8 1 4.7 1.8l3.3-3.2C18 1.2 15.2 0 12 0 7.3 0 3.3 2.8 1.3 6.9l3.8 2.9c.9-3 3.7-5.2 6.9-5.2z"/></svg><span class="trev__score">5,0 <i>★</i></span></header>
      <p class="trev__quote">« Gâteau d'anniversaire commandé à peine 24 h avant, et qui était excellent et magnifique ! Je recommande fortement. »</p>
      <footer><b>CC</b><div><strong>Charlotte C.</strong><span>Commande en 24 h · il y a 2 ans</span></div></footer>
    </article>
    <article class="trev__card" data-reveal>
      <header><svg class="trev__g" viewBox="0 0 24 24" width="20" height="20" aria-label="Google"><path fill="#4285F4" d="M23.5 12.3c0-.9-.1-1.5-.3-2.2H12v4.1h6.5c-.1 1.1-.8 2.7-2.4 3.8l3.7 2.9c2.2-2.1 3.7-5.1 3.7-8.6z"/><path fill="#34A853" d="M12 24c3.2 0 6-1.1 7.9-2.9l-3.7-2.9c-1 .7-2.4 1.2-4.2 1.2-3.2 0-6-2.2-6.9-5.2L1.3 17.1C3.3 21.2 7.3 24 12 24z"/><path fill="#FBBC05" d="M5.1 14.2c-.3-.7-.4-1.4-.4-2.2s.1-1.5.4-2.2L1.3 6.9C.5 8.5 0 10.2 0 12s.5 3.5 1.3 5.1l3.8-2.9z"/><path fill="#EA4335" d="M12 4.6c2.3 0 3.8 1 4.7 1.8l3.3-3.2C18 1.2 15.2 0 12 0 7.3 0 3.3 2.8 1.3 6.9l3.8 2.9c.9-3 3.7-5.2 6.9-5.2z"/></svg><span class="trev__score">5,0 <i>★</i></span></header>
      <p class="trev__quote">« Les réalisations de ce pâtissier sont les meilleures que j'ai mangées. Desserts parfaitement équilibrés, jamais écœurants. Un sans-faute. »</p>
      <footer><b>SB</b><div><strong>Sanaa Brm</strong><span>Desserts équilibrés · il y a 1 an</span></div></footer>
    </article>
    <article class="trev__card" data-reveal>
      <header><svg class="trev__g" viewBox="0 0 24 24" width="20" height="20" aria-label="Google"><path fill="#4285F4" d="M23.5 12.3c0-.9-.1-1.5-.3-2.2H12v4.1h6.5c-.1 1.1-.8 2.7-2.4 3.8l3.7 2.9c2.2-2.1 3.7-5.1 3.7-8.6z"/><path fill="#34A853" d="M12 24c3.2 0 6-1.1 7.9-2.9l-3.7-2.9c-1 .7-2.4 1.2-4.2 1.2-3.2 0-6-2.2-6.9-5.2L1.3 17.1C3.3 21.2 7.3 24 12 24z"/><path fill="#FBBC05" d="M5.1 14.2c-.3-.7-.4-1.4-.4-2.2s.1-1.5.4-2.2L1.3 6.9C.5 8.5 0 10.2 0 12s.5 3.5 1.3 5.1l3.8-2.9z"/><path fill="#EA4335" d="M12 4.6c2.3 0 3.8 1 4.7 1.8l3.3-3.2C18 1.2 15.2 0 12 0 7.3 0 3.3 2.8 1.3 6.9l3.8 2.9c.9-3 3.7-5.2 6.9-5.2z"/></svg><span class="trev__score">5,0 <i>★</i></span></header>
      <p class="trev__quote">« Superbe prestation pour un mariage de 120 convives. Mignardises excellentes, support créé sur mesure. Rapport qualité-prix excellent. »</p>
      <footer><b>GD</b><div><strong>Guillaume Desgache</strong><span>Mariage, 120 convives · il y a 1 an</span></div></footer>
    </article>
    <article class="trev__card" data-reveal>
      <header><svg class="trev__g" viewBox="0 0 24 24" width="20" height="20" aria-label="Google"><path fill="#4285F4" d="M23.5 12.3c0-.9-.1-1.5-.3-2.2H12v4.1h6.5c-.1 1.1-.8 2.7-2.4 3.8l3.7 2.9c2.2-2.1 3.7-5.1 3.7-8.6z"/><path fill="#34A853" d="M12 24c3.2 0 6-1.1 7.9-2.9l-3.7-2.9c-1 .7-2.4 1.2-4.2 1.2-3.2 0-6-2.2-6.9-5.2L1.3 17.1C3.3 21.2 7.3 24 12 24z"/><path fill="#FBBC05" d="M5.1 14.2c-.3-.7-.4-1.4-.4-2.2s.1-1.5.4-2.2L1.3 6.9C.5 8.5 0 10.2 0 12s.5 3.5 1.3 5.1l3.8-2.9z"/><path fill="#EA4335" d="M12 4.6c2.3 0 3.8 1 4.7 1.8l3.3-3.2C18 1.2 15.2 0 12 0 7.3 0 3.3 2.8 1.3 6.9l3.8 2.9c.9-3 3.7-5.2 6.9-5.2z"/></svg><span class="trev__score">5,0 <i>★</i></span></header>
      <p class="trev__quote">« 👑 La meilleure galette des rois d'Auvergne. Découverte au marché d'Aubière — la boutique est à quelques pas. »</p>
      <footer><b>CK</b><div><strong>Clémentine Kaul</strong><span>Galette des rois · il y a 5 ans</span></div></footer>
    </article>
    <article class="trev__card" data-reveal>
      <header><svg class="trev__g" viewBox="0 0 24 24" width="20" height="20" aria-label="Google"><path fill="#4285F4" d="M23.5 12.3c0-.9-.1-1.5-.3-2.2H12v4.1h6.5c-.1 1.1-.8 2.7-2.4 3.8l3.7 2.9c2.2-2.1 3.7-5.1 3.7-8.6z"/><path fill="#34A853" d="M12 24c3.2 0 6-1.1 7.9-2.9l-3.7-2.9c-1 .7-2.4 1.2-4.2 1.2-3.2 0-6-2.2-6.9-5.2L1.3 17.1C3.3 21.2 7.3 24 12 24z"/><path fill="#FBBC05" d="M5.1 14.2c-.3-.7-.4-1.4-.4-2.2s.1-1.5.4-2.2L1.3 6.9C.5 8.5 0 10.2 0 12s.5 3.5 1.3 5.1l3.8-2.9z"/><path fill="#EA4335" d="M12 4.6c2.3 0 3.8 1 4.7 1.8l3.3-3.2C18 1.2 15.2 0 12 0 7.3 0 3.3 2.8 1.3 6.9l3.8 2.9c.9-3 3.7-5.2 6.9-5.2z"/></svg><span class="trev__score">5,0 <i>★</i></span></header>
      <p class="trev__quote">« Tarte aux myrtilles délicieuse, brioche feuilletée aussi. Une tarte préparée à la dernière minute pour un anniversaire : tout le monde s'est régalé ! »</p>
      <footer><b>SR</b><div><strong>Steve Rogers</strong><span>Dernière minute, réussie · il y a 4 ans</span></div></footer>
    </article>
    <article class="trev__card" data-reveal>
      <header><svg class="trev__g" viewBox="0 0 24 24" width="20" height="20" aria-label="Google"><path fill="#4285F4" d="M23.5 12.3c0-.9-.1-1.5-.3-2.2H12v4.1h6.5c-.1 1.1-.8 2.7-2.4 3.8l3.7 2.9c2.2-2.1 3.7-5.1 3.7-8.6z"/><path fill="#34A853" d="M12 24c3.2 0 6-1.1 7.9-2.9l-3.7-2.9c-1 .7-2.4 1.2-4.2 1.2-3.2 0-6-2.2-6.9-5.2L1.3 17.1C3.3 21.2 7.3 24 12 24z"/><path fill="#FBBC05" d="M5.1 14.2c-.3-.7-.4-1.4-.4-2.2s.1-1.5.4-2.2L1.3 6.9C.5 8.5 0 10.2 0 12s.5 3.5 1.3 5.1l3.8-2.9z"/><path fill="#EA4335" d="M12 4.6c2.3 0 3.8 1 4.7 1.8l3.3-3.2C18 1.2 15.2 0 12 0 7.3 0 3.3 2.8 1.3 6.9l3.8 2.9c.9-3 3.7-5.2 6.9-5.2z"/></svg><span class="trev__score">5,0 <i>★</i></span></header>
      <p class="trev__quote">« Excellente tarte aux fruits rouges, myrtilles fraîches et framboises. Demandes spéciales réalisées sans souci. Très bons chocolats. »</p>
      <footer><b>AL</b><div><strong>Alice</strong><span>Demandes spéciales · il y a 3 ans</span></div></footer>
    </article>
    <article class="trev__card" data-reveal>
      <header><svg class="trev__g" viewBox="0 0 24 24" width="20" height="20" aria-label="Google"><path fill="#4285F4" d="M23.5 12.3c0-.9-.1-1.5-.3-2.2H12v4.1h6.5c-.1 1.1-.8 2.7-2.4 3.8l3.7 2.9c2.2-2.1 3.7-5.1 3.7-8.6z"/><path fill="#34A853" d="M12 24c3.2 0 6-1.1 7.9-2.9l-3.7-2.9c-1 .7-2.4 1.2-4.2 1.2-3.2 0-6-2.2-6.9-5.2L1.3 17.1C3.3 21.2 7.3 24 12 24z"/><path fill="#FBBC05" d="M5.1 14.2c-.3-.7-.4-1.4-.4-2.2s.1-1.5.4-2.2L1.3 6.9C.5 8.5 0 10.2 0 12s.5 3.5 1.3 5.1l3.8-2.9z"/><path fill="#EA4335" d="M12 4.6c2.3 0 3.8 1 4.7 1.8l3.3-3.2C18 1.2 15.2 0 12 0 7.3 0 3.3 2.8 1.3 6.9l3.8 2.9c.9-3 3.7-5.2 6.9-5.2z"/></svg><span class="trev__score">5,0 <i>★</i></span></header>
      <p class="trev__quote">« Gâteau d'anniversaire au chocolat commandé la veille pour le lendemain : excellent, nous nous sommes tous régalés ! »</p>
      <footer><b>EF</b><div><strong>Estelle Freulon</strong><span>Commandé la veille · il y a 2 ans</span></div></footer>
    </article>
    <article class="trev__card" data-reveal>
      <header><svg class="trev__g" viewBox="0 0 24 24" width="20" height="20" aria-label="Google"><path fill="#4285F4" d="M23.5 12.3c0-.9-.1-1.5-.3-2.2H12v4.1h6.5c-.1 1.1-.8 2.7-2.4 3.8l3.7 2.9c2.2-2.1 3.7-5.1 3.7-8.6z"/><path fill="#34A853" d="M12 24c3.2 0 6-1.1 7.9-2.9l-3.7-2.9c-1 .7-2.4 1.2-4.2 1.2-3.2 0-6-2.2-6.9-5.2L1.3 17.1C3.3 21.2 7.3 24 12 24z"/><path fill="#FBBC05" d="M5.1 14.2c-.3-.7-.4-1.4-.4-2.2s.1-1.5.4-2.2L1.3 6.9C.5 8.5 0 10.2 0 12s.5 3.5 1.3 5.1l3.8-2.9z"/><path fill="#EA4335" d="M12 4.6c2.3 0 3.8 1 4.7 1.8l3.3-3.2C18 1.2 15.2 0 12 0 7.3 0 3.3 2.8 1.3 6.9l3.8 2.9c.9-3 3.7-5.2 6.9-5.2z"/></svg><span class="trev__score">5,0 <i>★</i></span></header>
      <p class="trev__quote">« Un accueil des plus chaleureux par le pâtissier, qui a réalisé un gâteau magnifique et succulent malgré un thème très précis. »</p>
      <footer><b>WM</b><div><strong>William Mouret</strong><span>Thème sur mesure · il y a 1 an</span></div></footer>
    </article>
  </div>
  <div class="trev__more" data-reveal><a class="btn btn--light" href="https://share.google/u4BPhog5sqUFzvgVQ" target="_blank" rel="noopener" data-cursor="Ouvrir" data-magnet>★ Voir plus d'avis Google</a></div>
</section>

<section class="addr-band">
  <p class="eyebrow" data-reveal>Venez la goûter</p>
  <a class="addr-band__line" href="{MAPS}" target="_blank" rel="noopener" data-letters data-cursor="Itinéraire">7 rue des Ramacles</a>
  <a class="addr-band__line addr-band__line--small" href="{MAPS}" target="_blank" rel="noopener" data-letters>63170 Aubière</a>
  <div class="cta-band__actions" data-reveal><a class="btn btn--light" href="contact.html" data-magnet>Horaires &amp; accès</a><a class="btn btn--ghost" href="{TEL}" data-magnet>06 68 93 24 19</a></div>
</section>
</main>''' + FOOTER + tail())

# ═══════════════════════════ CONTACT ═══════════════════════════
def contact():
    return (head('Contact & horaires — La Pâtisserie Des Douceurs, 7 rue des Ramacles, Aubière', 'Horaires, adresse, téléphone et accès de La Pâtisserie Des Douceurs à Aubière (63170). Commandes au 06 68 93 24 19.', 'p-contact')
        + nav('contact.html')
        + f'''<main id="top">
<section class="tel-hero">
  <p class="eyebrow" data-reveal>Commandes &amp; questions</p>
  <a class="tel-hero__num" href="{TEL}" data-letters data-cursor="Appeler">06 68 93 24 19</a>
  <p class="tel-hero__now" id="openNow" data-reveal></p>
  <div class="tel-hero__alt" data-reveal><a href="mailto:{MAIL}">{MAIL}</a> · <a href="{IG}" target="_blank" rel="noopener"><svg class="ig-ico" viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="2.5" y="2.5" width="19" height="19" rx="5.5" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4.2" stroke="currentColor" stroke-width="1.8"/><circle cx="17.4" cy="6.6" r="1.4" fill="currentColor"/></svg>Instagram</a> · <a href="{FB}" target="_blank" rel="noopener">Facebook</a></div>
</section>

<section class="hours">
  <div class="hours__grid">
    <div class="hours__day" data-3d><b>Lun</b><span class="hours__closed">Fermé</span></div>
    <div class="hours__day" data-3d><b>Mar</b><span>9 h – 12 h 30</span><span>15 h – 18 h 30</span></div>
    <div class="hours__day" data-3d><b>Mer</b><span>9 h – 12 h 30</span><span>15 h – 18 h 30</span></div>
    <div class="hours__day" data-3d><b>Jeu</b><span>9 h – 12 h 30</span><span>15 h – 18 h 30</span></div>
    <div class="hours__day" data-3d><b>Ven</b><span>9 h – 12 h 30</span><span>15 h – 18 h 30</span></div>
    <div class="hours__day" data-3d><b>Sam</b><span>9 h – 13 h 30</span></div>
    <div class="hours__day" data-3d><b>Dim</b><span>9 h – 12 h 30</span></div>
  </div>
</section>

<section class="contact">
  <div class="contact__grid">
    <div class="contact__info">
      <dl class="boutique__info">
        <div data-reveal><dt>Adresse</dt><dd><a href="{MAPS}" target="_blank" rel="noopener" data-cursor="Itinéraire">7 rue des Ramacles<br>63170 Aubière</a><br><small>Bus P40 · E1 · E6 à 20 m · Tram A à 1 km · Parking à proximité</small></dd></div>
        <div data-reveal><dt>Accès</dt><dd><small>Entrée de plain-pied · parking et toilettes adaptés · CB, sans contact et espèces · livraison le jour même possible</small></dd></div>
      </dl>
      <form class="boutique__form" data-reveal id="orderForm">
        <input type="text" name="nom" placeholder="Votre nom" required>
        <input type="tel" name="tel" placeholder="Votre téléphone" required>
        <input type="date" name="date" aria-label="Date souhaitée">
        <textarea name="msg" rows="3" placeholder="Votre message ou votre commande" required></textarea>
        <button class="btn btn--light" type="submit" data-cursor="Envoyer" data-magnet>Envoyer</button>
        <p class="boutique__ok">Votre message s’ouvre dans votre messagerie — il ne reste qu’à l’envoyer.</p>
      </form>
    </div>
    <div class="contact__map" data-reveal-clip>
      <iframe title="Plan — La Pâtisserie Des Douceurs" src="https://www.google.com/maps?q=La+P%C3%A2tisserie+Des+Douceurs,+7+Rue+des+Ramacles,+63170+Aubi%C3%A8re&output=embed&z=16" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      <a class="btn btn--light contact__go" href="{MAPS}" target="_blank" rel="noopener" data-magnet>Itinéraire</a>
    </div>
  </div>
</section>
</main>''' + FOOTER + tail())

# ═══════════════════════════ MENTIONS ═══════════════════════════
def mentions():
    return (head('Mentions légales, CGV & confidentialité — La Pâtisserie Des Douceurs', 'Informations légales, conditions générales de vente pour les commandes et politique de confidentialité de La Pâtisserie Des Douceurs, Aubière.', 'p-legal')
        + nav('')
        + f'''<main id="top">
<section class="legal-hero">
  <p class="eyebrow" data-reveal>Informations légales</p>
  <h1 data-letters>Mentions légales</h1>
</section>
<section class="legal">
  <nav class="legal__nav" data-reveal><a href="#editeur">Éditeur</a><a href="#cgv">CGV commandes</a><a href="#confidentialite">Confidentialité</a><a href="#credits">Crédits</a></nav>
  <article class="legal__body">
    <h2 id="editeur" data-letters>Éditeur du site</h2>
    <p data-reveal>La Pâtisserie Des Douceurs — Yohann Girard, entrepreneur individuel.<br>7 rue des Ramacles, 63170 Aubière, France.<br>SIREN 833 167 109 · SIRET 833 167 109 00010 · TVA intracommunautaire FR04833167109 · Code NAF 1071D (pâtisserie).<br>Téléphone : 06 68 93 24 19 · E-mail : {MAIL}.<br>Directeur de la publication : Yohann Girard.</p>
    <p data-reveal>Hébergement : <em>à compléter (prestataire, adresse, téléphone)</em>.</p>

    <h2 id="cgv" data-letters>Conditions générales de vente — commandes</h2>
    <p data-reveal><strong>Commande.</strong> Les commandes (gâteaux d’anniversaire, entremets, pièces montées, buffets) se passent en boutique, par téléphone ou par e-mail. Une commande est confirmée à réception de l’acompte indiqué sur le devis. Les estimations du simulateur en ligne sont indicatives et ne constituent pas une offre.</p>
    <p data-reveal><strong>Délais.</strong> Les délais sont indiqués à la commande selon le planning de l’atelier. Les pièces montées de mariage se commandent au moins trois semaines à l’avance.</p>
    <p data-reveal><strong>Prix et paiement.</strong> Prix TTC. Acompte à la commande, solde au retrait ou à la livraison. Carte bancaire, sans contact et espèces acceptés.</p>
    <p data-reveal><strong>Annulation.</strong> Toute annulation doit être signalée au plus tôt. Au-delà du délai indiqué sur le devis, l’acompte reste acquis pour couvrir les matières engagées.</p>
    <p data-reveal><strong>Livraison.</strong> Livraison et montage sur place possibles à Aubière, Clermont-Ferrand et alentours, selon devis. Le client s’assure d’un lieu de dépose adapté (température, stabilité).</p>
    <p data-reveal><strong>Allergènes.</strong> L’atelier utilise notamment gluten, lait, œufs, fruits à coque, soja. Signalez toute allergie à la commande.</p>
    <p data-reveal><strong>Conservation.</strong> Les produits frais se conservent au réfrigérateur et se consomment dans les 24 à 48 h selon indication.</p>
    <p data-reveal><strong>Litiges.</strong> En cas de difficulté, contactez d’abord la boutique. Médiation de la consommation : <em>médiateur à désigner</em>. À défaut, les tribunaux compétents sont ceux du ressort de Clermont-Ferrand.</p>

    <h2 id="confidentialite" data-letters>Données personnelles</h2>
    <p data-reveal>Les formulaires de ce site ouvrent votre messagerie : les informations saisies (nom, téléphone, date, message) sont envoyées par vous-même à l’adresse {MAIL} et servent uniquement à traiter votre demande. Elles ne sont ni stockées sur le site ni transmises à des tiers. Vous pouvez demander leur suppression à la même adresse.</p>
    <p data-reveal>Ce site n’utilise pas de cookies de suivi. La carte interactive de la page Contact est fournie par Google Maps, qui peut déposer ses propres cookies lors de son chargement.</p>

    <h2 id="credits" data-letters>Crédits</h2>
    <p data-reveal>Conception et réalisation : <em>à compléter</em>. Photographies : <em>à remplacer par les photographies de la boutique</em> (visuels provisoires Unsplash). Polices : Cormorant Garamond, Inter (licences SIL OFL).</p>
  </article>
</section>
</main>''' + FOOTER + tail())

PAGES = {'carte.html': carte, 'mariages.html': mariages, 'saisons.html': saisons, 'a-propos.html': apropos, 'contact.html': contact, 'mentions-legales.html': mentions}
for f, fn in PAGES.items():
    open(f, 'w', encoding='utf-8').write(fn())
    print('ecrit', f)

# ── index.html : nav vers les pages + liens du pied de page ──
p = 'index.html'; s = open(p, encoding='utf-8').read()
links = ''.join(f'<a href="{h}">{l}</a>' for h, l in NAV_LINKS)
s = re.sub(r'<nav class="nav__links">.*?</nav>', f'<nav class="nav__links">{links}</nav>', s, flags=re.S)
s = re.sub(r'<div class="menu" id="menu">.*?</div>', f'<div class="menu" id="menu">\n  <a href="#produits">Vitrine</a>{links}\n</div>', s, flags=re.S)
s = s.replace('<a class="btn btn--ghost" href="tel:+33668932419" data-magnet>Commander</a>', '<a class="btn btn--ghost" href="mariages.html" data-magnet>Commander un gâteau</a>')
open(p, 'w', encoding='utf-8').write(s)
print('index.html mis a jour')
