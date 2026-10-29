# Happy Place V2 : prototype des 6 premiers écrans

Projet de fin de formation Product Builder (Maestro). Jury le 2026-11-06. Happy Place est le tableau de bord interne du cabinet de recrutement fictif Bigger Boat (220 salariés). Ce dépôt est un PROTOTYPE séparé de l'appli existante (`KARIMALAMJEB/happy-place-karima`). Ce qu'on valide ici sera ensuite copié dans l'appli.

## Règles de travail (priorité : économiser les tokens)
- Réponds en français, court. Pas de tiret cadratin. Vouvoiement ou "nous" dans les documents destinés au jury, tutoiement avec Karima.
- Ne relis pas les captures d'écran sauf demande. Contrôle les écrans avec `audit_stitch.py` (code seulement) et les captures Playwright minimales.
- Travaille par groupe d'écrans, une étape à la fois, et montre ce qui change avant de pousser.
- Aucune donnée inventée en dehors de celles de ce fichier : pas de SLA, de référence de demande, de niveau de gravité, de titre de poste, de "version". Personas fictifs uniquement.
- Desktop uniquement. Pas de mobile.
- Hors périmètre : Supabase, authentification, chatbot, suivi de réalisation des demandes validées. Données factices dans un seul fichier `src/data/demo.ts`.

## Stack
Même base que l'appli existante : Vite, React 19, TanStack Start/Router, Tailwind 4, shadcn/ui (Radix), TypeScript. Lis le `package.json` de `happy-place-karima` pour aligner les versions. Polices : Bodoni Moda, Inter Tight, Space Grotesk (Google Fonts, auto-hébergées si possible). Tailwind compilé en local, pas de CDN.

## Sources
- Export Stitch : `stitch_happy_place_v2_dashboard_2.zip` (20 `code.html`, dont les 3 tableaux de bord et les 2 détails). Les dossiers `tableau_de_bord_*` et `d_tail_de_la_demande_*` / `manager_d_tail_*` sont la base visuelle.
- L'écran Indicateurs (vue admin) n'est pas dans le zip : le reconstruire d'après la capture fournie et la section dédiée ci-dessous.
- Le code Stitch ne fait pas foi pour les couleurs et les boutons : ce fichier fait foi.

## Charte "Corporate"
- Fond écru `#F5F4F1`, cartes blanches, bordure `#CDCDD1` 1 px, texte `#232428`, texte secondaire `#68686D`, anthracite `#28282D` (texte dessus `#F9F8F5`), surfaces neutres `#EEEDEA` et `#E6E4E1`.
- Rose poudré `#C99695` (décoratif, jamais en texte), rose clair `#F5D5D4`, rose très clair `#F8DDDC` (survol, actif). Pêche `#F0D0BC` (texte `#482A1D`). Rouge `#C2272D` (fond `#FED2CD`, texte `#72020E`). Vert `#298646` (fond `#DCEFE1`, texte `#14522A`). Bordure de champ `#55555A`. Focus orange `#D9822B`, 3 px, décalage 2 px.
- Titres Bodoni Moda 700. Texte Inter Tight 14/20 (12 px minimum partout). Libellés, boutons, onglets, badges : Space Grotesk 700 majuscules 12 à 13 px, interlettrage 1,1 px.
- Angles droits, aucune ombre, aucun dégradé, aucun emoji. Boutons et champs 44 px minimum. Contraste 4,5:1. Aucune information portée par la couleur seule : un libellé ET une vraie icône (jamais "[✓]" en texte). Carrousel avec pause. Photo absente : bloc `#EEEDEA` avec icône, jamais de texte alternatif visible.

## Boutons par rôle (44 px, icône 16 px à gauche)
- Valide : fond `#298646`, texte blanc, icône coche. Refuse : fond blanc, bordure 1,5 px et texte `#C2272D`, icône croix.
- Modifie, enregistre, change un état : fond `#F8DDDC`, bordure 1,5 px `#C99695`, texte anthracite. Relance : fond `#F0D0BC`, texte `#482A1D`, icône cloche. Publie : fond `#C99695`, texte anthracite (jamais blanc).
- Consulte, ouvre, revient : fond blanc, bordure 1,5 px anthracite. Principal : fond `#28282D`, un seul par page ("DÉPOSER UNE DEMANDE").
- Aucun autre élément à fond noir (ni menu, ni onglet, ni filtre, ni segment, ni étape de frise). Actif (menu, onglet, filtre, segment) : fond `#F8DDDC` + trait de 3 px `#C99695` (barre à gauche pour le menu). Pastilles du menu : carré `#C2272D`, chiffre blanc. Désactivé : fond `#EEEDEA`, bordure `#CDCDD1`, texte `#68686D`, avec explication visible.

## Vocabulaire (trois niveaux distincts)
- Décision : EN ATTENTE (pêche, sablier), VALIDÉE (vert, coche), REFUSÉE (rouge clair, croix). Côté manager : À VALIDER. Côté auteur : EN ATTENTE DE RÉPONSE. EN RETARD = relance possible.
- Nature : BLOQUANTE (rouge, triangle d'alerte) ou NON BLOQUANTE. Jamais "point bloquant".
- Suivi du blocage (seulement pour une bloquante) : OUVERT, EN COURS, RÉSOLU. Franchi : fond `#EEEDEA` + coche anthracite. Actuel : fond `#F8DDDC` + trait 3 px `#C99695`. À venir : blanc, texte `#68686D`, sans cadenas. Pas de passage direct d'OUVERT à RÉSOLU. Responsable et date cible visibles. Seuls le Responsable, le manager ou l'admin changent le suivi.
- Visibilité : ÉQUIPE, ENTREPRISE, CONFIDENTIEL (cadenas), étiquette à la même place sur chaque ligne.
- Relance : possible après 5 jours sans réponse ; avant, bouton désactivé avec "Relance possible après 5 jours".

## Structure commune
- Menu latéral : Tableau de bord, Actualités, Demandes, Indicateurs, Boîte à outils, Annuaire. Marque "BIGGER BOAT / HAPPY PLACE" sans étiquette V2. En-tête "HAPPY PLACE V2", recherche, avatar (initiales, nom, équipe), bouton "SE DÉCONNECTER" (style consulte). Pastilles : Actualités 3 ; Demandes 2 (collab), 3 (manager), 2 (admin). Jamais "Cockpit", "Intranet", "Points bloquants".
- Date de référence : mardi 27 octobre 2026.
- Ligne 1 : Actualités (2/3) + Indicateurs clés (1/3). Ensuite blocs en pleine largeur.
- Actualités : onglets ENTREPRISE (actif par défaut) et MON ÉQUIPE · [équipe], 3 diapositives chacun, défilement 6 s, barre basse : "METTRE EN PAUSE (6S) / REPRENDRE", légende "Communication interne Bigger Boat", repères, flèches. Image, une catégorie, titre, un bouton de lecture. Pas de paragraphe.
- Indicateurs clés (3 tuiles cliquables vers Indicateurs, sous-titre "Performance de l'entreprise") : EFFECTIF 220 salariés, MANDATS ACTIFS 24, OBJECTIF ANNUEL ATTEINT 82 % (une seule ligne chacun).
- Boîte à outils : 4 tuiles cliquables, icône + titre : PROCESS, OUTILS, INFOS RH, ASSISTANCE ET SUPPORT.
- Lignes de demandes : ligne compacte de 64 px, entièrement cliquable, chevron. Contenu : titre, étiquette BLOQUANTE si besoin, étiquette de décision, date courte. Barre gauche rouge 4 px seulement si bloquante. Aucun bouton, frise, responsable ou valideur dans la ligne. Au-dessus : onglets, filtre TOUTES / BLOQUANTES / NON BLOQUANTES, filtre "Équipe" (liste déroulante, défaut "Toutes les équipes") seulement sur l'onglet ENTREPRISE. Les bloquantes en premier, pas d'en-têtes de groupe.

## Données factices (une seule source)
- Équipes : Direction Conseil, Direction Commerciale, People, Direction Générale, [à compléter avec la liste réelle].
- Personas : Gontran Lefèvre (collaborateur, Direction Conseil, manager Julien Roche), Kesha Diallo (manager, Direction Commerciale), Olivia Brun (admin, People), Samir Haddad (responsable), Lina Moreau, Yanis Okafor, Maëlle Fontaine.
- Collaborateur Gontran, 4 demandes : (1) Accès outil de sourcing : BLOQUANTE, EN ATTENTE, suivi EN COURS, responsable Samir Haddad, date cible mercredi 29 octobre 2026, déposée le 21 oct. 2026, valideur Julien Roche, CONFIDENTIEL. (2) Clavier ergonomique séparé : NON BLOQUANTE, EN ATTENTE, 26 oct. 2026, ÉQUIPE, "Relance possible dans 4 jours". (3) Abonnement outil de rédaction de CV : REFUSÉE par Olivia Brun le 25 oct. 2026, motif "Solution interne existante". (4) Écran 27 pouces 4K : VALIDÉE par Julien Roche le 24 oct. 2026, étiquette "TERMINÉE" non cliquable. Phrase d'accueil : "2 réponses reçues, 1 relance possible et 1 demande bloquante en cours."
- Blocs du bas du collaborateur (gardés, allégés, pleine largeur, côte à côte, même hauteur) : "RÉPONSES REÇUES (2 NOUVELLES)" (cartes compactes : titre, décision, bouton "CONSULTER LE MOTIF" pour la refusée) et "RELANCES POSSIBLES (1 ÉLIGIBLE)" (Accès outil de sourcing, EN RETARD, "Aucune réponse depuis 6 jours · relance possible après 5 jours", bouton RELANCER LE VALIDEUR). Cartes blanches, barre gauche 4 px (verte validée, rouge refusée, pêche relance), seulement dans ces deux blocs.
- Manager Kesha : phrase "3 demandes à valider, dont 1 bloquante, et 2 brouillons à publier." Boutons : RÉDIGER UNE ACTUALITÉ (consulte), DÉPOSER UNE DEMANDE (principal). Bandeau : "Votre droit de publication : vous publiez directement pour la Direction Commerciale, sans validation. Pour toute l'entreprise, la publication passe par People." 3 demandes à valider : Accès outil de suivi commercial (BLOQUANTE, auteur Consultant, 26 oct. 2026, ÉQUIPE, suivi EN COURS, responsable Samir Haddad, cible vendredi 30 octobre 2026), Extension d'accès à un outil d'équipe (26 oct. 2026, ÉQUIPE), Équipement ergonomique bureau (25 oct. 2026, CONFIDENTIEL). Une seule pastille "3 EN ATTENTE DE VOTRE DÉCISION". Pas de boutons Valider ou Refuser dans les lignes. Brouillons : Bilan mi-trimestre grands comptes, Process d'intégration commerciale, étiquette BROUILLON (pêche), bouton "PUBLIER À L'ÉQUIPE".
- Admin Olivia : phrase "2 demandes à valider, dont 1 bloquante, et 2 brouillons à publier." Boutons : PUBLIER UNE ANNONCE ENTREPRISE (publie), DÉPOSER UNE DEMANDE (principal). Onglets À VALIDER et SUPERVISION GLOBALE. À valider : Machine à café du 2ᵉ étage (BLOQUANTE, auteur Lina Moreau, ENTREPRISE, suivi OUVERT, responsable Yanis Okafor, cible vendredi 30 octobre 2026), Menu de la cantine (auteur Maëlle Fontaine, ENTREPRISE, 26 oct.). Supervision : tableau 4 colonnes (Demande, Auteur, Visibilité, Décision), 4 lignes : Équipement ergonomique (Lina Moreau, ÉQUIPE, EN ATTENTE), Télétravail exceptionnel (Gontran Lefèvre, ÉQUIPE, VALIDÉE), Abonnement outil de rédaction de CV (Gontran Lefèvre, CONFIDENTIEL, REFUSÉE), Accès outil de sourcing (Gontran Lefèvre, CONFIDENTIEL, EN ATTENTE, BLOQUANTE). Deux brouillons d'annonces entreprise (titres de Stitch, à valider par Karima) avec "PUBLIER À L'ENTREPRISE". Pas de bloc "Administration", pas de LDAP, SLA ou KPI de délai.
- Actualités : ENTREPRISE, "Séminaire annuel : rendez-vous le 14 décembre" (Direction Générale, 27 octobre 2026, catégorie ÉVÉNEMENT CABINET) ; MON ÉQUIPE · DIRECTION COMMERCIALE, "Séminaire opérationnel et synergies Q4" (par Kesha Diallo, 26 octobre 2026). Les 2 autres diapositives de chaque onglet : contenu fictif sobre, à faire valider par Karima.

## Détail de la demande
- Retour (consulte) + fil d'Ariane (manager : "Demandes de mon équipe / titre" ; collaborateur : "Mes demandes / titre"). Titre, étiquettes (nature, décision, visibilité), 3 informations (auteur, date de dépôt, valideur), motif (citation), choix de nature BLOQUANTE / NON BLOQUANTE avec bouton ENREGISTRER (grisé tant que rien n'a changé), SUIVI DU BLOCAGE si bloquante (frise + responsable + date cible), pied d'actions. Pas de textes d'aide, pas de "Réf.", pas de "Mode lecture seule".
- Vue manager (Accès outil de suivi commercial, auteur Consultant, déposée lundi 26 octobre 2026, valideur Kesha Diallo) : bouton CHANGER LE STATUT (modifie) seulement dans le suivi ; pied : REFUSER AVEC MOTIF (refuse) et VALIDER LA DEMANDE (valide). Décision : À VALIDER.
- Vue collaborateur (Accès outil de sourcing, auteur Gontran Lefèvre, déposée mercredi 21 octobre 2026, valideur Julien Roche) : frise en lecture seule, pas de bouton de statut ; pied : RELANCER LE VALIDEUR (relance), actif après 5 jours (ici 6 jours sans réponse, dernier contact 21 oct.). Décision : EN ATTENTE DE RÉPONSE.

## Écran Indicateurs (vue admin)
Titre "Indicateurs de performance de l'entreprise", aide "Ces indicateurs sont saisis à la main par People. Ils s'affichent sur le tableau de bord de tous les collaborateurs." Formulaire "Saisie des indicateurs" : une ligne par indicateur (libellé, valeur, unité, période) : Effectif 220 salariés ; Mandats actifs 24 ; Objectif annuel atteint 82 %. AJOUTER UN INDICATEUR (modifie), suppression par icône. "Dernière mise à jour : lundi 26 octobre 2026 par Olivia Brun". ANNULER (consulte), ENREGISTRER ET PUBLIER (modifie). Bloc "Aperçu côté collaborateur" avec les 3 tuiles en lecture seule. Pas de mentions "Config admin", "Rendu exact", "Système à jour". Message "MISE À JOUR À FAIRE" (pêche) seulement si la dernière mise à jour dépasse 30 jours.

## Interactions à construire
Sélecteur de profil (Gontran / Kesha / Olivia), carrousel (6 s, pause, flèches, onglets), onglets Mon suivi / Entreprise (ou Mon équipe / Entreprise), filtres, ligne cliquable vers le détail du bon profil, changement de nature (état local), relance désactivée avant 5 jours, tuile d'indicateurs vers l'écran Indicateurs, saisie d'indicateurs avec aperçu mis à jour. Focus clavier visible partout.

## Ordre de travail
1. Socle : variables de charte, polices, composants boutons / étiquettes / menu / en-tête.
2. Les 3 tableaux de bord + `demo.ts`.
3. Interactions de l'accueil.
4. Les 2 détails et l'écran Indicateurs.
5. Test des 30 secondes par Karima (3 ou 4 tâches chronométrées), puis corrections.
6. Ensuite seulement : fonctionnalités, puis Supabase.
