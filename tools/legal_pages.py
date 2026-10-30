# Génère les pages légales de la vitrine Sillage (FR + EN).
# Usage : python3 legal_pages.py <racine du dépôt sillage-site>
import os, sys, json

ROOT = sys.argv[1]
DATE_FR = "29 octobre 2026"
DATE_EN = "29 October 2026"

LOGO = """<svg width="40" height="37" viewBox="0 0 64 60" aria-hidden="true">
<circle cx="17" cy="31" r="10" fill="#14201B"></circle>
<rect x="5" y="30" width="50" height="13" rx="6.5" fill="#14201B"></rect>
<circle cx="38" cy="24" r="15" fill="#FFFFFF" stroke="#14201B" stroke-width="5"></circle>
<g stroke="#E0A21B" stroke-width="2" stroke-linecap="round"><path d="M38 15.5v2.5M38 30v2.5M29.5 24h2.5M44 24h2.5M32 18l1.8 1.8M42.2 28.2L44 30M32 30l1.8-1.8M42.2 19.8L44 18"></path></g>
<circle cx="38" cy="24" r="4" fill="#E0A21B"></circle>
<g fill="#3E86C0"><rect x="16" y="47" width="4" height="9" rx="2" transform="rotate(18 18 51)"></rect><rect x="28" y="47" width="4" height="9" rx="2" transform="rotate(18 30 51)"></rect><rect x="40" y="47" width="4" height="9" rx="2" transform="rotate(18 42 51)"></rect></g>
</svg>"""

CSS = """
*{box-sizing:border-box}
body{margin:0;background:#FFFFFF;color:#14201B;font-family:Archivo,system-ui,-apple-system,"Segoe UI",sans-serif;font-size:17px;line-height:1.6;-webkit-text-size-adjust:100%}
a{color:#23629A}a:hover{color:#14201B}
header{position:sticky;top:0;z-index:5;background:rgba(255,255,255,.92);backdrop-filter:blur(10px);border-bottom:1px solid #CDD4CE}
.bar{max-width:1200px;margin:0 auto;padding:12px 24px;display:flex;align-items:center;justify-content:space-between;gap:16px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:#14201B;font-weight:800;font-size:24px;letter-spacing:-.03em}
.lang{font-size:14px;font-weight:600;text-decoration:none;color:#14201B;border:1px solid #CDD4CE;border-radius:999px;padding:8px 14px;min-height:40px;display:inline-flex;align-items:center}
main{max-width:760px;margin:0 auto;padding:48px 24px 72px}
.kicker{font-family:"IBM Plex Mono",ui-monospace,monospace;font-weight:500;font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:#8A5A00;margin:0 0 10px}
h1{font-weight:800;font-size:clamp(34px,6vw,52px);line-height:1.05;letter-spacing:-.03em;margin:0 0 16px}
.lead{font-size:19px;color:#4C5852;margin:0 0 8px}
.date{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:13px;color:#4C5852;margin:0 0 36px}
h2{font-weight:700;font-size:23px;line-height:1.25;letter-spacing:-.01em;margin:40px 0 12px;padding-top:20px;border-top:1px solid #E3E8E4}
h3{font-weight:700;font-size:18px;margin:22px 0 6px}
p{margin:0 0 14px}
ul,ol{margin:0 0 14px;padding-left:22px}
li{margin:0 0 8px}
.card{background:#F1F3F0;border-radius:16px;padding:18px 20px;margin:0 0 16px}
.card p:last-child{margin:0}
.mono{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:15px}
.promise{background:#FBF1DA;border-left:4px solid #E0A21B;border-radius:14px;padding:16px 18px;margin:0 0 24px}
table{width:100%;border-collapse:collapse;margin:0 0 16px;font-size:15px}
th,td{text-align:left;vertical-align:top;padding:10px 8px;border-bottom:1px solid #E3E8E4}
th{font-weight:700;font-size:14px;color:#4C5852}
footer{background:#121B17;color:#A3AEA8}
.foot{max-width:1200px;margin:0 auto;padding:32px 24px 48px;display:flex;flex-wrap:wrap;justify-content:space-between;gap:20px;font-size:14px}
.foot a{color:#A3AEA8}
.foot nav{display:flex;flex-wrap:wrap;gap:24px}
.foot a[aria-current]{color:#EEF1EC;font-weight:600}
@media (max-width:560px){main{padding:32px 16px 56px}.bar{padding:10px 16px}.foot{padding:28px 16px 40px}table{font-size:14px}th,td{padding:8px 4px}}
"""

def page(lang, title, desc, kicker, h1, lead, date_label, body, other_href, other_label, home, foot_links, current):
    cur = ' aria-current="page"'
    foot = "".join(
        '<a href="%s"%s>%s</a>' % (h, cur if k == current else "", t) for k, h, t in foot_links)
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex">
<link rel="icon" type="image/svg+xml" href="/img/favicon.svg">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700;800&amp;family=IBM+Plex+Mono:wght@500&amp;display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<header><div class="bar">
<a class="brand" href="{home}">{LOGO}<span>Sillage</span></a>
<a class="lang" href="{other_href}" hreflang="{'en' if lang == 'fr' else 'fr'}">{other_label}</a>
</div></header>
<main>
<p class="kicker">{kicker}</p>
<h1>{h1}</h1>
<p class="lead">{lead}</p>
<p class="date">{date_label}</p>
{body}
</main>
<footer><div class="foot">
<span>© 2026 Sillage · {'La météo sur ta trace.' if lang == 'fr' else 'Weather along your route.'}</span>
<nav aria-label="{'Liens légaux' if lang == 'fr' else 'Legal links'}">{foot}</nav>
</div></footer>
</body>
</html>
"""

FOOT_FR = [("ml", "/mentions-legales/", "Mentions légales"), ("conf", "/confidentialite/", "Confidentialité"),
           ("del", "/supprimer-mon-compte/", "Supprimer mon compte"), ("c", "mailto:hello@sillage-ride.eu", "Contact")]
FOOT_EN = [("ml", "/en/legal-notice/", "Legal notice"), ("conf", "/en/privacy/", "Privacy"),
           ("del", "/en/delete-account/", "Delete my account"), ("c", "mailto:hello@sillage-ride.eu", "Contact")]

# ---------------------------------------------------------------- Mentions légales
ML_FR = """
<h2>Éditeur</h2>
<div class="card">
<p>Le site sillage-ride.eu et l'application Sillage sont édités par l'association <strong>Beyond the Track</strong>, association régie par la loi du 1<sup>er</sup> juillet 1901, déclarée à la préfecture de Meurthe-et-Moselle le 17 juin 2025.</p>
<p>Siège : 8 rue Charles Péguy, 54140 Jarville-la-Malgrange, France<br>
<span class="mono">RNA W543017048 · SIREN 988 271 904</span><br>
Contact : <a href="mailto:hello@sillage-ride.eu">hello@sillage-ride.eu</a></p>
</div>

<h2>Directeur de la publication</h2>
<p>Antoine Chareyre, président de l'association.</p>

<h2>Hébergement</h2>
<ul>
<li><strong>Site sillage-ride.eu</strong> : GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis (GitHub Pages).</li>
<li><strong>Données de l'application</strong> (comptes, parcours, alertes) : Supabase, serveurs situés à Francfort, Allemagne.</li>
<li><strong>Nom de domaine et boîte e-mail</strong> : OVH SAS, 2 rue Kellermann, 59100 Roubaix, France.</li>
</ul>

<h2>Propriété intellectuelle</h2>
<p>Le nom Sillage, son logo, les textes, les visuels et le code de l'application appartiennent à l'association Beyond the Track. Toute reproduction sans accord écrit est interdite.</p>

<h2>Crédits</h2>
<ul>
<li>Fonds de carte © contributeurs <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>, CyclOSM, IGN (Géoplateforme).</li>
<li>Données météo : <a href="https://open-meteo.com">Open-Meteo</a> (licence CC BY 4.0), MET Norway, Météo-France et les autres services météorologiques nationaux cités dans l'application.</li>
<li>Polices : Archivo, IBM Plex Mono, Atkinson Hyperlegible (licence SIL Open Font).</li>
</ul>

<h2>Données personnelles</h2>
<p>Ce que Sillage garde, pourquoi et combien de temps : voir la page <a href="/confidentialite/">Confidentialité</a>.</p>
"""

ML_EN = """
<h2>Publisher</h2>
<div class="card">
<p>The sillage-ride.eu website and the Sillage app are published by <strong>Beyond the Track</strong>, a non-profit association under the French law of 1 July 1901, registered with the Meurthe-et-Moselle prefecture on 17 June 2025.</p>
<p>Registered office: 8 rue Charles Péguy, 54140 Jarville-la-Malgrange, France<br>
<span class="mono">RNA W543017048 · SIREN 988 271 904</span><br>
Contact: <a href="mailto:hello@sillage-ride.eu">hello@sillage-ride.eu</a></p>
</div>

<h2>Publication director</h2>
<p>Antoine Chareyre, president of the association.</p>

<h2>Hosting</h2>
<ul>
<li><strong>sillage-ride.eu website</strong>: GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA (GitHub Pages).</li>
<li><strong>App data</strong> (accounts, routes, alerts): Supabase, servers in Frankfurt, Germany.</li>
<li><strong>Domain name and mailbox</strong>: OVH SAS, 2 rue Kellermann, 59100 Roubaix, France.</li>
</ul>

<h2>Intellectual property</h2>
<p>The Sillage name, logo, texts, visuals and app code belong to the Beyond the Track association. Reproduction without written permission is prohibited.</p>

<h2>Credits</h2>
<ul>
<li>Map tiles © <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, CyclOSM, IGN (Géoplateforme).</li>
<li>Weather data: <a href="https://open-meteo.com">Open-Meteo</a> (CC BY 4.0 licence), MET Norway, Météo-France and the other national weather services named in the app.</li>
<li>Fonts: Archivo, IBM Plex Mono, Atkinson Hyperlegible (SIL Open Font Licence).</li>
</ul>

<h2>Personal data</h2>
<p>What Sillage keeps, why and for how long: see the <a href="/en/privacy/">Privacy</a> page.</p>
"""

# ---------------------------------------------------------------- Confidentialité
CONF_FR = """
<div class="promise"><p style="margin:0"><strong>En bref :</strong> on ne garde que ce qu'il faut pour te donner la météo sur ta trace. Pas de publicité, pas de revente, pas de pistage.</p></div>

<h2>Qui est responsable ?</h2>
<p>L'association <strong>Beyond the Track</strong>, éditrice de Sillage (coordonnées dans les <a href="/mentions-legales/">mentions légales</a>). Pour toute question sur tes données : <a href="mailto:hello@sillage-ride.eu">hello@sillage-ride.eu</a>.</p>

<h2>Ce qu'on garde, et pourquoi</h2>
<h3>Ton compte</h3>
<p>Ton e-mail et ton mot de passe (chiffré : personne ne peut le lire, pas même nous), ton prénom si tu le donnes, pour te connecter et te reconnaître sur tous tes appareils.</p>
<h3>Le mode démo (sans compte)</h3>
<p>Si tu essaies Sillage sans compte, sur nos traces d'exemple, on crée un compte technique anonyme (sans e-mail ni nom) pour ouvrir la démo. Rien de ce que tu fais n'est enregistré. Pour éviter les abus, on compte les visites sans compte par adresse IP : l'adresse est transformée en une empreinte illisible qui change chaque jour, et effacée au bout de 2 jours.</p>
<h3>Tes parcours</h3>
<p>Les traces GPX que tu importes (points, distance, dénivelé, nom) et la date de leur dernière utilisation, pour les retrouver partout. Tes parcours ne sont visibles que par toi.</p>
<h3>Tes alertes météo</h3>
<p>Le parcours, l'heure de départ, les jours, ta langue, tes unités et ton fuseau horaire, plus l'identifiant technique de ton appareil, pour t'envoyer la notification au bon moment.</p>
<h3>Le journal d'utilisation</h3>
<p>Ouvertures de l'app, imports de GPX et calculs météo, pour la sécurité du service et pour améliorer l'app. Avec le compte gratuit, on note aussi quelles traces tu as chargées dans le mois (l'identifiant du parcours, sans la trace), pour compter tes nouvelles traces.</p>
<h3>La lettre d'info (si tu t'y inscris)</h3>
<p>Ton e-mail, ton prénom, ton profil (cycliste ou organisateur·rice) et, pour les organisateurs, le nom et le type de ton événement.</p>
<h3>Les statistiques de visite</h3>
<p>Un identifiant aléatoire (sans cookie), la page vue, le type d'appareil. <strong>Sur le site web uniquement</strong>, on ajoute la ville approximative déduite de ton adresse IP ; l'adresse IP elle-même n'est jamais conservée. <strong>Dans l'app iPhone et Android, aucune localisation n'est relevée.</strong></p>

<h2>Combien de temps</h2>
<table>
<thead><tr><th>Donnée</th><th>Durée</th></tr></thead>
<tbody>
<tr><td>Compte, parcours, alertes</td><td>Jusqu'à la suppression de ton compte. Un compte sans aucune connexion pendant <strong>3 ans</strong> est supprimé, après un e-mail d'avertissement un mois avant.</td></tr>
<tr><td>Mode démo</td><td>Compte technique effacé après <strong>30 jours</strong> sans visite ; empreinte de l'adresse IP effacée après 2 jours</td></tr>
<tr><td>Journal d'utilisation</td><td>12 mois</td></tr>
<tr><td>Décompte des traces du compte gratuit</td><td>13 mois</td></tr>
<tr><td>Statistiques de visite</td><td>25 mois</td></tr>
<tr><td>Lettre d'info</td><td>Jusqu'à ta désinscription</td></tr>
</tbody>
</table>

<h2>Sur quelle base</h2>
<ul>
<li><strong>Le service que tu utilises</strong> : compte, parcours, alertes, journal d'utilisation.</li>
<li><strong>Ton accord</strong> : lettre d'info et notifications. Tu peux le retirer à tout moment.</li>
<li><strong>Notre intérêt légitime</strong> : sécurité et statistiques de visite anonymes. Tu peux t'y opposer en nous écrivant.</li>
</ul>

<h2>Qui d'autre voit tes données</h2>
<p>Seulement les services techniques qui font tourner Sillage, chacun pour sa tâche :</p>
<ul>
<li><strong>Supabase</strong> (serveurs à Francfort, Allemagne) : stockage du compte, des parcours et des alertes.</li>
<li><strong>Brevo</strong> (France) : envoi des e-mails (compte, lettre d'info).</li>
<li><strong>Google Firebase</strong> : envoi des notifications sur iPhone et Android.</li>
<li><strong>OVH</strong> (France) : nom de domaine et boîte e-mail.</li>
<li><strong>GitHub</strong> : hébergement du site.</li>
<li><strong>ipapi.co / ipwho.is</strong> : ville approximative des visites du site web.</li>
<li><strong>Services météo et cartes</strong> (Open-Meteo, MET Norway, OpenStreetMap, IGN…) : ils reçoivent des points de coordonnées le long de ta trace pour calculer la météo ou afficher la carte. Jamais ton nom ni ton e-mail.</li>
</ul>
<p>Certains de ces services sont situés aux États-Unis. Ces transferts sont encadrés par les garanties prévues par le RGPD (décision d'adéquation EU-US Data Privacy Framework ou clauses contractuelles types).</p>

<h2>Tes droits</h2>
<p><strong>Supprimer ton compte</strong> se fait directement dans Sillage : page Moi → « Supprimer mon compte ». Tout est effacé immédiatement. <a href="/supprimer-mon-compte/">Comment faire</a>.</p>
<p>Tu peux aussi consulter, corriger ou exporter tes données, et t'opposer à certains traitements. Pour cela, écris à <a href="mailto:hello@sillage-ride.eu">hello@sillage-ride.eu</a> : on te répond sous un mois.</p>
<p>Si tu estimes que tes droits ne sont pas respectés, tu peux saisir la <a href="https://www.cnil.fr/fr/plaintes">CNIL</a>.</p>

<h2>Sur ton appareil</h2>
<p>Sillage garde tes réglages (thème, unités, langue, dernier parcours ouvert…) et un cache des prévisions dans la mémoire de ton navigateur ou de ton téléphone. Ils servent seulement au fonctionnement de l'app. Il n'y a ni cookie publicitaire ni outil de pistage.</p>

<h2>Changements</h2>
<p>Si cette page change de façon importante, on te prévient dans l'app ou par e-mail. La date de la dernière version est indiquée en haut.</p>
"""

CONF_EN = """
<div class="promise"><p style="margin:0"><strong>In short:</strong> we only keep what we need to give you the weather along your route. No ads, no data selling, no tracking.</p></div>

<h2>Who is responsible?</h2>
<p>The <strong>Beyond the Track</strong> association, publisher of Sillage (details in the <a href="/en/legal-notice/">legal notice</a>). For any question about your data: <a href="mailto:hello@sillage-ride.eu">hello@sillage-ride.eu</a>.</p>

<h2>What we keep, and why</h2>
<h3>Your account</h3>
<p>Your e-mail and password (encrypted: nobody can read it, not even us), and your first name if you give it, to sign you in and recognise you on all your devices.</p>
<h3>Demo mode (without an account)</h3>
<p>If you try Sillage without an account, on our sample routes, we create an anonymous technical account (no e-mail, no name) to open the demo. Nothing you do is saved. To prevent abuse, we count visits without an account per IP address: the address is turned into an unreadable fingerprint that changes every day, and erased after 2 days.</p>
<h3>Your routes</h3>
<p>The GPX tracks you import (points, distance, elevation, name) and when you last used them, so you find them everywhere. Your routes are visible only to you.</p>
<h3>Your weather alerts</h3>
<p>The route, start time, days, language, units and time zone, plus the technical identifier of your device, to send you the notification at the right time.</p>
<h3>Usage log</h3>
<p>App launches, GPX imports and weather calculations, to keep the service secure and improve the app. With the free account, we also note which routes you loaded during the month (the route's identifier, not the route itself), to count your new routes.</p>
<h3>Newsletter (if you sign up)</h3>
<p>Your e-mail, first name, profile (rider or organiser) and, for organisers, the name and type of your event.</p>
<h3>Visit statistics</h3>
<p>A random identifier (no cookie), the page viewed and the device type. <strong>On the website only</strong>, we add the approximate city derived from your IP address; the IP address itself is never stored. <strong>The iPhone and Android app collects no location at all.</strong></p>

<h2>How long</h2>
<table>
<thead><tr><th>Data</th><th>Retention</th></tr></thead>
<tbody>
<tr><td>Account, routes, alerts</td><td>Until you delete your account. An account with no sign-in for <strong>3 years</strong> is deleted, after a warning e-mail one month before.</td></tr>
<tr><td>Demo mode</td><td>Technical account erased after <strong>30 days</strong> without a visit; IP fingerprint erased after 2 days</td></tr>
<tr><td>Usage log</td><td>12 months</td></tr>
<tr><td>Free account route count</td><td>13 months</td></tr>
<tr><td>Visit statistics</td><td>25 months</td></tr>
<tr><td>Newsletter</td><td>Until you unsubscribe</td></tr>
</tbody>
</table>

<h2>Legal basis</h2>
<ul>
<li><strong>The service you use</strong>: account, routes, alerts, usage log.</li>
<li><strong>Your consent</strong>: newsletter and notifications. You can withdraw it at any time.</li>
<li><strong>Our legitimate interest</strong>: security and anonymous visit statistics. You can object by writing to us.</li>
</ul>

<h2>Who else sees your data</h2>
<p>Only the technical services that run Sillage, each for its own task:</p>
<ul>
<li><strong>Supabase</strong> (servers in Frankfurt, Germany): storage of accounts, routes and alerts.</li>
<li><strong>Brevo</strong> (France): sending e-mails (account, newsletter).</li>
<li><strong>Google Firebase</strong>: sending notifications on iPhone and Android.</li>
<li><strong>OVH</strong> (France): domain name and mailbox.</li>
<li><strong>GitHub</strong>: website hosting.</li>
<li><strong>ipapi.co / ipwho.is</strong>: approximate city of website visits.</li>
<li><strong>Weather and map services</strong> (Open-Meteo, MET Norway, OpenStreetMap, IGN…): they receive coordinates along your route to compute the weather or display the map. Never your name or e-mail.</li>
</ul>
<p>Some of these services are based in the United States. These transfers are covered by the safeguards of the GDPR (EU-US Data Privacy Framework adequacy decision or standard contractual clauses).</p>

<h2>Your rights</h2>
<p><strong>Deleting your account</strong> is done right in Sillage: Me page → “Delete my account”. Everything is erased immediately. <a href="/en/delete-account/">How to do it</a>.</p>
<p>You can also access, correct or export your data, and object to some processing. Just write to <a href="mailto:hello@sillage-ride.eu">hello@sillage-ride.eu</a>: we reply within one month.</p>
<p>If you believe your rights are not respected, you can lodge a complaint with the <a href="https://www.cnil.fr/en/complaints">CNIL</a> (French data protection authority).</p>

<h2>On your device</h2>
<p>Sillage keeps your settings (theme, units, language, last opened route…) and a forecast cache in your browser or phone storage. They are only used to run the app. There are no advertising cookies and no tracking tools.</p>

<h2>Changes</h2>
<p>If this page changes significantly, we will let you know in the app or by e-mail. The date of the latest version is shown at the top.</p>
"""

DEL_FR = """
<h2>Depuis l'app ou le site</h2>
<ol>
<li>Ouvre Sillage : l'app sur ton téléphone, ou la <a href="https://antoinechry.github.io/plan-my-ride/">version web</a>. Connecte-toi.</li>
<li>Va dans <strong>Moi</strong> (onglet en bas sur téléphone, à gauche sur ordinateur).</li>
<li>Dans « Mon compte », touche <strong>Supprimer mon compte</strong>.</li>
<li>Saisis ton mot de passe et confirme avec <strong>Supprimer définitivement</strong>.</li>
</ol>

<h2>Ce qui est effacé</h2>
<div class="card">
<p>Immédiatement et définitivement : ton compte (e-mail, mot de passe, prénom), tes parcours, tes alertes météo, ton journal d'utilisation et ton inscription à la lettre d'info.</p>
</div>
<p>Seules restent les statistiques de visite anonymes (identifiant aléatoire, sans lien avec ton compte), effacées au bout de 25 mois.</p>

<h2>Tu n'as plus accès à ton compte ?</h2>
<ul>
<li><strong>Mot de passe oublié</strong> : sur l'écran de connexion, touche « Mot de passe oublié ? » pour en choisir un nouveau, puis suis les étapes ci-dessus.</li>
<li><strong>Plus d'accès du tout</strong> : écris à <a href="mailto:hello@sillage-ride.eu?subject=Supprimer%20mon%20compte">hello@sillage-ride.eu</a> depuis l'adresse de ton compte, avec l'objet « Supprimer mon compte ». On le supprime et on te le confirme par e-mail, dans un délai d'un mois au plus.</li>
</ul>

<p>Plus de détails sur tes données : page <a href="/confidentialite/">Confidentialité</a>.</p>
"""

DEL_EN = """
<h2>From the app or the website</h2>
<ol>
<li>Open Sillage: the app on your phone, or the <a href="https://antoinechry.github.io/plan-my-ride/">web version</a>. Sign in.</li>
<li>Go to <strong>Me</strong> (bottom tab on a phone, left side on a computer).</li>
<li>Under “My account”, tap <strong>Delete my account</strong>.</li>
<li>Enter your password and confirm with <strong>Delete permanently</strong>.</li>
</ol>

<h2>What gets erased</h2>
<div class="card">
<p>Immediately and for good: your account (e-mail, password, first name), your routes, your weather alerts, your usage log and your newsletter subscription.</p>
</div>
<p>Only anonymous visit statistics remain (a random identifier with no link to your account), erased after 25 months.</p>

<h2>Can't access your account?</h2>
<ul>
<li><strong>Forgot your password</strong>: on the sign-in screen, tap “Forgot your password?” to choose a new one, then follow the steps above.</li>
<li><strong>No access at all</strong>: write to <a href="mailto:hello@sillage-ride.eu?subject=Delete%20my%20account">hello@sillage-ride.eu</a> from your account's address, with the subject “Delete my account”. We delete it and confirm by e-mail within one month at most.</li>
</ul>

<p>More about your data: <a href="/en/privacy/">Privacy</a> page.</p>
"""

PAGES = [
    ("mentions-legales/index.html", page("fr", "Mentions légales · Sillage", "Éditeur, hébergement et crédits de Sillage.",
        "Sillage", "Mentions légales", "Qui édite Sillage, qui l'héberge, et à qui on doit les cartes et la météo.",
        f"Version du {DATE_FR}", ML_FR, "/en/legal-notice/", "English", "/", FOOT_FR, "ml")),
    ("confidentialite/index.html", page("fr", "Confidentialité · Sillage", "Ce que Sillage garde de tes données, pourquoi et combien de temps.",
        "Sillage", "Confidentialité", "Ce que Sillage garde de tes données, pourquoi, combien de temps, et comment tout effacer.",
        f"Version du {DATE_FR}", CONF_FR, "/en/privacy/", "English", "/", FOOT_FR, "conf")),
    ("en/legal-notice/index.html", page("en", "Legal notice · Sillage", "Publisher, hosting and credits of Sillage.",
        "Sillage", "Legal notice", "Who publishes Sillage, who hosts it, and who we owe the maps and weather to.",
        f"Version of {DATE_EN}", ML_EN, "/mentions-legales/", "Français", "/", FOOT_EN, "ml")),
    ("en/privacy/index.html", page("en", "Privacy · Sillage", "What Sillage keeps of your data, why and for how long.",
        "Sillage", "Privacy", "What Sillage keeps of your data, why, for how long, and how to erase it all.",
        f"Version of {DATE_EN}", CONF_EN, "/confidentialite/", "Français", "/", FOOT_EN, "conf")),
    ("supprimer-mon-compte/index.html", page("fr", "Supprimer mon compte · Sillage", "Comment supprimer ton compte Sillage et toutes tes données.",
        "Sillage", "Supprimer mon compte", "Tu peux effacer ton compte et toutes tes données à tout moment, sans rien demander à personne.",
        f"Version du {DATE_FR}", DEL_FR, "/en/delete-account/", "English", "/", FOOT_FR, "del")),
    ("en/delete-account/index.html", page("en", "Delete my account · Sillage", "How to delete your Sillage account and all your data.",
        "Sillage", "Delete my account", "You can erase your account and all your data at any time, without asking anyone.",
        f"Version of {DATE_EN}", DEL_EN, "/supprimer-mon-compte/", "Français", "/", FOOT_EN, "del")),
]

# ---------------------------------------------------------------- Confirmation de l'adresse (lien de l'e-mail d'inscription)
CONFIRM_CSS = """<style>
.st{display:none}.st.on{display:block}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:52px;padding:0 26px;border-radius:999px;background:#E0A21B;color:#14201B;font-weight:700;font-size:17px;text-decoration:none;margin:6px 0 18px}
.btn:hover{background:#c98f12;color:#14201B}
.soon{display:flex;gap:10px;flex-wrap:wrap;margin:0 0 18px}
.soon span{font-size:14px;font-weight:600;border:1px solid #CDD4CE;border-radius:999px;padding:8px 14px;color:#4C5852}
.spin{width:28px;height:28px;border:3px solid #E3E8E4;border-top-color:#E0A21B;border-radius:50%;animation:sp 1s linear infinite;margin:8px 0 18px}
@keyframes sp{to{transform:rotate(360deg)}}
@media (prefers-reduced-motion:reduce){.spin{animation:none}}
</style>"""

def confirm_body(lang):
    fr = lang == 'fr'
    app = "https://antoinechry.github.io/plan-my-ride/"
    if fr:
        T = dict(wait="On vérifie ton lien…", okh="Merci{p} !", okl="Ton adresse est confirmée et ton compte Sillage est prêt.",
            okt="Il ne te reste plus qu'à te connecter avec ton e-mail et ton mot de passe, puis à importer ta première trace GPX.",
            btn="Rejoindre Sillage", soon="Bientôt sur", already="Ton adresse était déjà confirmée : tu peux te connecter.",
            errh="Ce lien ne marche plus", invalid="Il a peut-être déjà servi, ou il est incomplet. Essaie simplement de te connecter : si ton adresse est confirmée, tout est prêt.",
            expired="Il était valable 48 heures. Connecte-toi à Sillage : tu pourras te faire renvoyer un nouveau lien.",
            neterr="Impossible de joindre Sillage pour l'instant. Réessaie dans un moment.", btn2="Aller sur Sillage",
            help='Un souci ? Écris-nous à <a href="mailto:hello@sillage-ride.eu">hello@sillage-ride.eu</a>.')
    else:
        T = dict(wait="Checking your link…", okh="Thank you{p}!", okl="Your address is confirmed and your Sillage account is ready.",
            okt="All that's left is to sign in with your e-mail and password, then import your first GPX route.",
            btn="Join Sillage", soon="Coming soon to", already="Your address was already confirmed: you can sign in.",
            errh="This link no longer works", invalid="It may have been used already, or it is incomplete. Just try signing in: if your address is confirmed, you're all set.",
            expired="It was valid for 48 hours. Sign in to Sillage: you'll be able to get a new link.",
            neterr="Sillage can't be reached right now. Please try again in a moment.", btn2="Go to Sillage",
            help='Any trouble? Write to <a href="mailto:hello@sillage-ride.eu">hello@sillage-ride.eu</a>.')
    appl = app
    return CONFIRM_CSS + f"""
<div id="sWait" class="st on"><div class="spin" aria-hidden="true"></div><p>{T['wait']}</p></div>
<div id="sOk" class="st">
<p id="okAlready" class="promise" hidden>{T['already']}</p>
<p>{T['okt']}</p>
<a class="btn" href="{appl}">{T['btn']}</a>
<p class="kicker">{T['soon']}</p>
<div class="soon"><span>App Store</span><span>Google Play</span></div>
</div>
<div id="sErr" class="st">
<p id="errTxt"></p>
<a class="btn" href="{appl}">{T['btn2']}</a>
</div>
<p style="margin-top:28px;font-size:15px;color:#4C5852">{T['help']}</p>
<script>
(function(){{
  var T={json.dumps(T, ensure_ascii=False)};
  var h1=document.querySelector('h1'), lead=document.querySelector('.lead');
  function show(id){{['sWait','sOk','sErr'].forEach(function(k){{document.getElementById(k).classList.toggle('on',k===id);}});}}
  function err(kind){{h1.textContent=T.errh;lead.textContent='';document.getElementById('errTxt').textContent=T[kind]||T.invalid;show('sErr');}}
  var t=new URLSearchParams(location.search).get('t');
  if(t) history.replaceState(null,'',location.pathname);
  if(!t) return err('invalid');
  fetch('https://bsypkdsnhiepvcnhmfsm.supabase.co/functions/v1/confirm-email',{{method:'POST',headers:{{'content-type':'application/json'}},body:JSON.stringify({{t:t}})}})
  .then(function(r){{return r.json();}})
  .then(function(d){{
    if(!d||!d.ok) return err(d&&d.error==='expired'?'expired':'invalid');
    var p=(d.prenom||'').trim();
    h1.textContent=T.okh.replace('{{p}}',p?{'" "' if fr else '" "'}+p:'');
    lead.textContent=T.okl;
    if(d.already) document.getElementById('okAlready').hidden=false;
    show('sOk');
  }})
  .catch(function(){{err('neterr');}});
}})();
</script>
"""

def confirm_page(lang):
    fr = lang == 'fr'
    html = page(lang, "Compte confirmé · Sillage" if fr else "Account confirmed · Sillage",
        "Confirmation de ton adresse e-mail Sillage." if fr else "Confirmation of your Sillage e-mail address.",
        "Sillage", "Confirmation" , "", "", confirm_body(lang),
        "/en/account-confirmed/" if fr else "/compte-confirme/", "English" if fr else "Français", "/",
        FOOT_FR if fr else FOOT_EN, "")
    return html.replace('<p class="date"></p>\n', '')

PAGES += [("compte-confirme/index.html", confirm_page("fr")), ("en/account-confirmed/index.html", confirm_page("en"))]

import re, json
def nbsp_fr(html):
    # espaces insécables avant ? : ! ; » et après « dans le contenu des pages françaises
    a, b = html.index("<main>"), html.index("</main>")
    m = re.sub(r" ([?:!;»])", " \\1", html[a:b]).replace("« ", "« ")
    m = m.replace("https :", "https:").replace("mailto :", "mailto:")
    return html[:a] + m + html[b:]

for rel, html in PAGES:
    if 'lang="fr"' in html[:60]:
        html = nbsp_fr(html)
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("écrit", rel, len(html))
