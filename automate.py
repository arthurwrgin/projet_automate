# ------------------------------------------------------------------ #
#  STRUCTURE DE DONNÉES
#  On représente un automate comme un DICTIONNAIRE avec 5 clés :
#
#  automate = {
#    "nb_symboles" : int         ex: 2
#    "nb_etats"    : int         ex: 5
#    "initiaux"    : [int]       ex: [0]
#    "terminaux"   : [int]       ex: [4]
#    "transitions" : dict        ex: {"0a": [1,2], "1b": [3]}
#  }
#
#  Pour les transitions, la CLÉ est une chaîne "état+symbole"
#  ex: "0a" = depuis l'état 0 avec le symbole 'a'
#  La VALEUR est une liste d'états d'arrivée (liste car NFA possible)
# ------------------------------------------------------------------ #
# 1-point sur les dictionnaires
## Une liste : on accède par INDEX (0, 1, 2...)
#fruits = ["pomme", "banane", "cerise"]
#print(fruits[0])  # "pomme"

# Un dictionnaire : on accède par CLÉ (un nom)
#personne = {"nom": "Alice", "age": 20}
#print(personne["nom"])   # "Alice"
#print(personne["age"])   # 20

#format des automates en .txt
'''
2        ← nombre de symboles dans l'alphabet
5        ← nombre d'états
1 0      ← nb d'états initiaux, puis leurs numéros
1 4      ← nb d'états terminaux, puis leurs numéros
6        ← nombre de transitions
0 a 0    ← transition : état_départ symbole état_arrivée
0 b 0
0 a 1
1 b 2
2 a 3
3 a 4
'''
# ============================================================
#  ÉTAPE 1 : Lecture et affichage
# ============================================================

def lire_automate(nom_fichier):
    try:
        with open(nom_fichier, "r") as f:
            lignes = [ligne.strip() for ligne in f.readlines()]
            lignes = [l for l in lignes if l != ""]

        nb_symboles = int(lignes[0])
        nb_etats    = int(lignes[1])

        parties  = lignes[2].split()
        nb_init  = int(parties[0])
        initiaux = [int(parties[i]) for i in range(1, nb_init + 1)]

        parties   = lignes[3].split()
        nb_term   = int(parties[0])
        terminaux = [int(parties[i]) for i in range(1, nb_term + 1)]

        nb_transitions = int(lignes[4])

        transitions  = {}
        a_poubelle   = False

        for i in range(nb_transitions):
            p   = lignes[5 + i].split()
            sym = p[1]

            # L'état départ peut être 'P' ou un entier
            dep = p[0] if p[0] == "P" else int(p[0])
            # L'état arrivée peut être 'P' ou un entier
            arr = p[2] if p[2] == "P" else int(p[2])

            if dep == "P" or arr == "P":
                a_poubelle = True

            cle = str(dep) + sym
            if cle in transitions:
                transitions[cle].append(arr)
            else:
                transitions[cle] = [arr]

        return {
            "nb_symboles" : nb_symboles,
            "nb_etats"    : nb_etats,
            "initiaux"    : initiaux,
            "terminaux"   : terminaux,
            "transitions" : transitions,
            "a_poubelle"  : a_poubelle
        }

    except FileNotFoundError:
        print(f"ERREUR : Le fichier '{nom_fichier}' est introuvable.")
        return None
    except Exception as e:
        print(f"ERREUR lors de la lecture : {e}")
        return None
# ------------------------------------------------------------
# lire_automate(nom_fichier)
# ------------------------------------------------------------
# PARAMÈTRE  : nom_fichier (str) → chemin vers le fichier .txt
#              ex: "automate_07.txt"
#
# RENVOIE    : un dictionnaire automate (structure décrite ci-dessus)
#              ou None si le fichier est introuvable ou mal formaté
#
# COMMENT    : Lit le fichier ligne par ligne et construit le dictionnaire.
#              Ligne 1 → nb_symboles, Ligne 2 → nb_etats,
#              Ligne 3 → initiaux, Ligne 4 → terminaux,
#              Ligne 5 → nb_transitions, Lignes suivantes → transitions.
#              Gère les états "P" (poubelle) dans les fichiers qui en ont déjà un
#              (ex: automate_41.txt), en les gardant comme chaîne "P"
#              au lieu de les convertir en entier.
#              Les ε-transitions sont notées '*' dans les fichiers.



def get_alphabet(automate):
    """Retourne la liste des symboles. Ex: nb_symboles=4 → ['a','b','c','d']"""
    return [chr(ord('a') + i) for i in range(automate["nb_symboles"])]

# ------------------------------------------------------------
# get_alphabet(automate)
# ------------------------------------------------------------
# PARAMÈTRE  : automate (dict) → un automate quelconque
#
# RENVOIE    : liste de caractères ['a', 'b', ...] de longueur nb_symboles
#              ex: nb_symboles=3 → ['a', 'b', 'c']
#
# COMMENT    : Utilise le code ASCII : ord('a')=97, donc chr(97+i) donne
#              'a', 'b', 'c'... selon le rang i.
#              Ne dépend que de "nb_symboles" dans le dictionnaire.




def afficher_automate(automate):
    """
    Affiche la table de transitions.
    États entiers + état poubelle 'P' si présent.
    """
    if automate is None:
        print("Aucun automate à afficher.")
        return

    alphabet    = get_alphabet(automate)
    initiaux    = automate["initiaux"]
    terminaux   = automate["terminaux"]
    transitions = automate["transitions"]
    a_poubelle  = automate.get("a_poubelle", False)

    etats = list(range(automate["nb_etats"]))
    if a_poubelle:
        etats.append("P")

    print("\n" + "=" * 55)
    print("  TABLE DE TRANSITIONS")
    print("=" * 55)

    largeur_col = 8
    for etat in etats:
        for sym in alphabet:
            cle = str(etat) + sym
            if cle in transitions:
                contenu = ",".join(str(e) for e in transitions[cle])
                largeur_col = max(largeur_col, len(contenu) + 2)

    entete = "        " + " | "
    for sym in alphabet:
        entete += sym.center(largeur_col) + " | "
    print(entete)
    print("-" * len(entete))

    for etat in etats:
        est_initial  = (etat in initiaux)
        est_terminal = (etat in terminaux)

        if est_initial and est_terminal:
            prefixe = "-> * "
        elif est_initial:
            prefixe = "->   "
        elif est_terminal:
            prefixe = "  *  "
        else:
            prefixe = "     "

        nom_etat = str(etat).rjust(2)
        ligne    = prefixe + nom_etat + " | "

        for sym in alphabet:
            cle = str(etat) + sym
            if cle in transitions:
                contenu = ",".join(str(e) for e in transitions[cle])
            else:
                contenu = "--"
            ligne += contenu.center(largeur_col) + " | "

        print(ligne)

    print("=" * 55)
    print(f"  Alphabet  : {{{', '.join(alphabet)}}}")
    print(f"  États     : {list(range(automate['nb_etats']))}" + (" + P (poubelle)" if a_poubelle else ""))
    print(f"  Initiaux  : {initiaux}")
    print(f"  Terminaux : {terminaux}")
    print("=" * 55 + "\n")
# ------------------------------------------------------------
# afficher_automate(automate)
# ------------------------------------------------------------
# PARAMÈTRE  : automate (dict) → un automate avec états entiers
#              (automate lu depuis fichier, standardisé, ou complété)
#
# RENVOIE    : rien (affichage console uniquement)
#
# COMMENT    : Affiche une table de transitions alignée avec :
#              "->" devant l'état initial, "*" devant les états terminaux.
#              Affiche "--" quand il n'y a pas de transition pour un couple
#              (état, symbole). Si "a_poubelle" est True, ajoute l'état 'P'
#              en dernière ligne. Calcule automatiquement la largeur des
#              colonnes pour que tout soit bien aligné.


def afficher_afdc(afdc):
    """
    Affiche la table d'un AFDC avec états nommés
    (concaténation : "01", "013", "P", etc.)
    """
    if afdc is None:
        print("Aucun automate à afficher.")
        return

    alphabet    = get_alphabet(afdc)
    initiaux    = afdc["initiaux"]
    terminaux   = afdc["terminaux"]
    transitions = afdc["transitions"]
    a_poubelle  = afdc.get("a_poubelle", False)
    noms_etats  = afdc.get("noms_etats", [str(i) for i in range(afdc["nb_etats"])])

    etats = list(noms_etats)
    if a_poubelle:
        etats.append("P")

    print("\n" + "=" * 60)
    print("  TABLE DE TRANSITIONS (AFDC)")
    print("=" * 60)

    largeur_col  = max(8, max(len(n) for n in etats) + 2)
    largeur_etat = max(6, max(len(n) for n in etats) + 2)

    for etat in etats:
        for sym in alphabet:
            cle = str(etat) + sym
            if cle in transitions:
                contenu = ",".join(str(e) for e in transitions[cle])
                largeur_col = max(largeur_col, len(contenu) + 2)

    entete = " " * (largeur_etat + 7) + " | "
    for sym in alphabet:
        entete += sym.center(largeur_col) + " | "
    print(entete)
    print("-" * len(entete))

    for etat in etats:
        est_initial  = (etat in initiaux)
        est_terminal = (etat in terminaux)

        if est_initial and est_terminal:
            prefixe = "-> * "
        elif est_initial:
            prefixe = "->   "
        elif est_terminal:
            prefixe = "  *  "
        else:
            prefixe = "     "

        nom_etat = str(etat).rjust(largeur_etat)
        ligne    = prefixe + nom_etat + " | "

        for sym in alphabet:
            cle = str(etat) + sym
            if cle in transitions:
                contenu = ",".join(str(e) for e in transitions[cle])
            else:
                contenu = "--"
            ligne += contenu.center(largeur_col) + " | "

        print(ligne)

    print("=" * 60)
    print(f"  Alphabet  : {{{', '.join(alphabet)}}}")
    print(f"  États     : {noms_etats}" + (" + P (poubelle)" if a_poubelle else ""))
    print(f"  Initiaux  : {initiaux}")
    print(f"  Terminaux : {terminaux}")
    print("=" * 60 + "\n")

# ------------------------------------------------------------
# afficher_afdc(afdc)
# ------------------------------------------------------------
# PARAMÈTRE  : afdc (dict) → un automate issu de déterminisation,
#              dont les états ont des NOMS (chaînes) comme "01", "013", "P"
#              et non pas des entiers. Doit avoir la clé "noms_etats".
#
# RENVOIE    : rien (affichage console uniquement)
#
# COMMENT    : Même logique qu'afficher_automate mais adapté aux états
#              nommés par concaténation. Calcule la largeur des colonnes
#              en fonction du nom le plus long pour garder un affichage aligné.
#              Utilisée après déterminisation et après minimisation.



# ============================================================
#  ÉTAPE 2 : Vérifications
# ============================================================

def est_deterministe(automate):
    raisons = []
    if len(automate["initiaux"]) > 1:
        raisons.append(f"  - Plusieurs états initiaux : {automate['initiaux']}")
    for cle, etats_arr in automate["transitions"].items():
        if cle.endswith("*"):
            continue  # on ignore les ε-transitions pour ce test
        if len(etats_arr) > 1:
            etat = cle[:-1]
            sym  = cle[-1]
            raisons.append(f"  - Depuis état {etat} avec '{sym}' : {etats_arr}")
    return (len(raisons) == 0), raisons

# ------------------------------------------------------------
# est_deterministe(automate)
# ------------------------------------------------------------
# PARAMÈTRE  : automate (dict)
#
# RENVOIE    : tuple (bool, [str])
#              → (True, [])  si l'automate est déterministe
#              → (False, ["raison1", "raison2"...]) sinon
#
# COMMENT    : Vérifie deux conditions :
#              1. Un seul état initial (len(initiaux) <= 1)
#              2. Pour chaque clé du dictionnaire transitions,
#                 la liste d'arrivée contient au plus 1 état.
#              Ignore les ε-transitions (clés finissant par '*').
#              Retourne toutes les violations trouvées pour les afficher.


def est_standard(automate):
    raisons = []
    if len(automate["initiaux"]) != 1:
        raisons.append(f"  - Doit avoir exactement 1 état initial (a {len(automate['initiaux'])})")
        return False, raisons
    etat_initial = automate["initiaux"][0]
    for cle, etats_arr in automate["transitions"].items():
        if cle.endswith("*"):
            continue
        if etat_initial in etats_arr:
            etat_dep = cle[:-1]
            sym      = cle[-1]
            raisons.append(f"  - L'état initial {etat_initial} est atteint depuis {etat_dep} avec '{sym}'")
    return (len(raisons) == 0), raisons
# ------------------------------------------------------------
# est_standard(automate)
# ------------------------------------------------------------
# PARAMÈTRE  : automate (dict)
#
# RENVOIE    : tuple (bool, [str])
#              → (True, [])  si l'automate est standard
#              → (False, ["raison1"...]) sinon
#
# COMMENT    : Vérifie deux conditions :
#              1. Exactement un état initial
#              2. Cet état initial n'apparaît jamais comme état d'ARRIVÉE
#                 dans aucune transition.
#              Ignore les ε-transitions.
#              S'arrête dès la condition 1 non vérifiée (inutile de continuer).



def est_complet(automate):
    raisons  = []
    alphabet = get_alphabet(automate)
    for etat in range(automate["nb_etats"]):
        for sym in alphabet:
            cle = str(etat) + sym
            if cle not in automate["transitions"]:
                raisons.append(f"  - Pas de transition depuis état {etat} avec '{sym}'")
    return (len(raisons) == 0), raisons
# ------------------------------------------------------------
# est_complet(automate)
# ------------------------------------------------------------
# PARAMÈTRE  : automate (dict) → doit être déterministe
#
# RENVOIE    : tuple (bool, [str])
#              → (True, [])  si l'automate est complet
#              → (False, ["raison1"...]) sinon
#
# COMMENT    : Pour chaque état (0 à nb_etats-1) et chaque symbole
#              de l'alphabet, vérifie qu'une transition existe dans
#              le dictionnaire transitions. Si une clé manque → incomplet.
#              Liste toutes les transitions manquantes.


def afficher_proprietes(automate):
    print("\n" + "=" * 55)
    print("  PROPRIÉTÉS DE L'AUTOMATE")
    print("=" * 55)

    det, raisons_det = est_deterministe(automate)
    print("  Déterministe : " + ("OUI" if det else "NON"))
    for r in raisons_det:
        print(r)

    std, raisons_std = est_standard(automate)
    print("  Standard     : " + ("OUI" if std else "NON"))
    for r in raisons_std:
        print(r)

    if det:
        comp, raisons_comp = est_complet(automate)
        print("  Complet      : " + ("OUI" if comp else "NON"))
        for r in raisons_comp:
            print(r)
    else:
        print("  Complet      : (non vérifié car non déterministe)")

    print("=" * 55 + "\n")
# ------------------------------------------------------------
# afficher_proprietes(automate)
# ------------------------------------------------------------
# PARAMÈTRE  : automate (dict)
#
# RENVOIE    : rien (affichage console)
#
# COMMENT    : Appelle est_deterministe, est_standard, est_complet
#              et affiche OUI/NON + les raisons si NON.
#              N'appelle est_complet que si l'automate est déterministe
#              (car "complet" n'a de sens que pour un automate déterministe).



# ============================================================
#  ÉTAPE 3 : Standardisation
# ============================================================

def standardisation(automate):
    nouvel_initial = automate["nb_etats"]
    alphabet       = get_alphabet(automate)

    nouvelles_transitions = {}
    for cle, etats in automate["transitions"].items():
        nouvelles_transitions[cle] = list(etats)

    for ancien in automate["initiaux"]:
        for sym in alphabet:
            cle_ancien = str(ancien) + sym
            cle_nouvel = str(nouvel_initial) + sym
            if cle_ancien in automate["transitions"]:
                dests = automate["transitions"][cle_ancien]
                if cle_nouvel in nouvelles_transitions:
                    for e in dests:
                        if e not in nouvelles_transitions[cle_nouvel]:
                            nouvelles_transitions[cle_nouvel].append(e)
                else:
                    nouvelles_transitions[cle_nouvel] = list(dests)

    nouveaux_terminaux = list(automate["terminaux"])
    for ancien in automate["initiaux"]:
        if ancien in automate["terminaux"]:
            nouveaux_terminaux.append(nouvel_initial)
            break

    return {
        "nb_symboles" : automate["nb_symboles"],
        "nb_etats"    : automate["nb_etats"] + 1,
        "initiaux"    : [nouvel_initial],
        "terminaux"   : nouveaux_terminaux,
        "transitions" : nouvelles_transitions,
        "a_poubelle"  : False
    }
# ------------------------------------------------------------
# standardisation(automate)
# ------------------------------------------------------------
# PARAMÈTRE  : automate (dict) → automate non standard
#
# RENVOIE    : un nouveau dictionnaire automate (le standardisé)
#              L'automate d'origine n'est PAS modifié.
#
# COMMENT    : Crée un nouvel état initial i0 = nb_etats
#              (ce numéro est forcément libre car les états vont de 0 à nb_etats-1).
#              Copie dans i0 toutes les transitions qui partaient des anciens
#              états initiaux (union des transitions si plusieurs initiaux).
#              Si un ancien état initial était terminal, i0 est aussi terminal.
#              Retourne un nouveau dictionnaire avec nb_etats+1 états.
#              Travaille sur des COPIES des listes/dicts pour ne pas
#              modifier l'automate original.




# ============================================================
#  GESTION DES ε-TRANSITIONS (notées '*' dans les fichiers)
# ============================================================

def a_epsilon(automate):
    """Vérifie si l'automate contient des ε-transitions (notées '*')."""
    for cle in automate["transitions"]:
        if cle.endswith("*"):
            return True
    return False
# a_epsilon(automate)
# ------------------------------------------------------------
# PARAMÈTRE  : automate (dict)
#
# RENVOIE    : bool → True si au moins une clé du dictionnaire
#              transitions se termine par '*', False sinon
#
# COMMENT    : Simple parcours des clés du dictionnaire transitions.
#              Utilisée dans le main() pour décider si on doit
#              appliquer le traitement spécial ε-clôtures.



def epsilon_cloture_etat(etat, transitions):
    """
    Calcule la ε-clôture d'un seul état :
    = l'état lui-même + tous les états atteignables par '*'-transitions.
    """
    cloture   = [etat]
    a_traiter = [etat]
    while len(a_traiter) > 0:
        courant = a_traiter.pop(0)
        cle_eps = str(courant) + "*"
        if cle_eps in transitions:
            for dest in transitions[cle_eps]:
                if dest not in cloture:
                    cloture.append(dest)
                    a_traiter.append(dest)
    return sorted(cloture)
# ------------------------------------------------------------
# epsilon_cloture_etat(etat, transitions)
# ------------------------------------------------------------
# PARAMÈTRES : etat (int) → un état de l'automate
#              transitions (dict) → le dictionnaire des transitions
#
# RENVOIE    : liste triée d'entiers → tous les états atteignables
#              depuis "etat" par une suite (éventuellement vide)
#              de ε-transitions ('*'). L'état lui-même est toujours inclus.
#
# COMMENT    : BFS (parcours en largeur) : on part de l'état,
#              on suit tous les '*', puis les '*' des états atteints, etc.
#              jusqu'à ce qu'il n'y ait plus de nouveaux états à explorer.
#              ex: ε-clôture(0) avec 0→*→1, 1→*→3 donne [0, 1, 3]



def epsilon_cloture_ensemble(ensemble, transitions):
    """
    Calcule la ε-clôture d'un ensemble d'états =
    union des ε-clôtures de chaque état de l'ensemble.
    """
    result = []
    for e in ensemble:
        for x in epsilon_cloture_etat(e, transitions):
            if x not in result:
                result.append(x)
    return sorted(result)
# ------------------------------------------------------------
# epsilon_cloture_ensemble(ensemble, transitions)
# ------------------------------------------------------------
# PARAMÈTRES : ensemble (liste d'entiers) → un ensemble d'états
#              transitions (dict)
#
# RENVOIE    : liste triée d'entiers → union des ε-clôtures
#              de chaque état de l'ensemble
#
# COMMENT    : Appelle epsilon_cloture_etat pour chaque état
#              de l'ensemble et fusionne les résultats sans doublons.
#              Utilisée pour calculer l'état initial du DFA lors
#              de la déterminisation d'un automate asynchrone.



# ============================================================
#  ÉTAPE 4 : Déterminisation et complétion
#  (gère aussi les automates asynchrones avec ε-transitions)
# ============================================================

def completion_seulement(automate):
    """
    Complète un automate déterministe non complet.
    Transitions manquantes → 'P'.
    """
    alphabet        = get_alphabet(automate)
    besoin_poubelle = False

    nouvelles_transitions = {}
    for cle, etats in automate["transitions"].items():
        nouvelles_transitions[cle] = list(etats)

    for etat in range(automate["nb_etats"]):
        for sym in alphabet:
            cle = str(etat) + sym
            if cle not in nouvelles_transitions:
                nouvelles_transitions[cle] = ["P"]
                besoin_poubelle = True

    if besoin_poubelle:
        for sym in alphabet:
            nouvelles_transitions["P" + sym] = ["P"]

    correspondance = {e: str(e) for e in range(automate["nb_etats"])}
    if besoin_poubelle:
        correspondance["P"] = "P (poubelle)"

    return {
        "nb_symboles"    : automate["nb_symboles"],
        "nb_etats"       : automate["nb_etats"],
        "initiaux"       : list(automate["initiaux"]),
        "terminaux"      : list(automate["terminaux"]),
        "transitions"    : nouvelles_transitions,
        "a_poubelle"     : besoin_poubelle,
        "correspondance" : correspondance
    }
# ------------------------------------------------------------
# completion_seulement(automate)
# ------------------------------------------------------------
# PARAMÈTRE  : automate (dict) → déterministe mais incomplet
#
# RENVOIE    : un nouveau dictionnaire automate complété,
#              avec "a_poubelle": True et une clé "correspondance"
#              (chaque état correspond à lui-même).
#
# COMMENT    : Pour chaque état et chaque symbole, si la transition
#              manque dans le dictionnaire, on l'ajoute en pointant
#              vers l'état poubelle 'P' (chaîne, pas un entier).
#              Ajoute ensuite les transitions Pa→P, Pb→P... pour que
#              'P' boucle sur lui-même. 'P' n'est jamais terminal.
#              Les états et initiaux/terminaux restent inchangés.


def determinisation_et_completion(automate):
    """
    Construit l'AFDC à partir d'un automate non déterministe.
    Gère aussi les automates asynchrones (ε-transitions notées '*') :
    dans ce cas, l'état initial = ε-clôture de l'état initial,
    et chaque transition suit le symbole PUIS calcule la ε-clôture.
    """
    alphabet        = get_alphabet(automate)
    terminaux_nfa   = automate["terminaux"]
    transitions_nfa = automate["transitions"]
    est_async       = a_epsilon(automate)

    # --- Affichage des ε-clôtures si automate asynchrone ---
    if est_async:
        print("\n  ε-clôtures :")
        for etat in range(automate["nb_etats"]):
            cloture = epsilon_cloture_etat(etat, transitions_nfa)
            print(f"    ε-clôture({etat}) = {cloture}")

    def liste_vers_nom(liste_etats):
        """[0,1,3] → '013',  [10,2] → '10.2',  [] → 'P'"""
        if len(liste_etats) == 0:
            return "P"
        tri = sorted(liste_etats)
        if all(e < 10 for e in tri):
            return "".join(str(e) for e in tri)
        else:
            return ".".join(str(e) for e in tri)

    def calculer_destinations(ensemble, sym):
        """
        Calcule les états atteignables depuis un ensemble avec un symbole.
        Si async : on suit sym PUIS on calcule la ε-clôture des états atteints.
        Si sync  : on suit sym directement.
        """
        apres_sym = []
        for etat in ensemble:
            cle = str(etat) + sym
            if cle in transitions_nfa:
                for d in transitions_nfa[cle]:
                    if d not in apres_sym:
                        apres_sym.append(d)

        if est_async:
            # On calcule la ε-clôture des états atteints
            return epsilon_cloture_ensemble(apres_sym, transitions_nfa)
        else:
            return sorted(apres_sym)

    # --- État initial ---
    # Si async : ε-clôture de l'état initial
    # Si sync  : l'état initial tel quel
    if est_async:
        ensemble_initial = epsilon_cloture_ensemble(
            sorted(automate["initiaux"]), transitions_nfa
        )
    else:
        ensemble_initial = sorted(automate["initiaux"])

    nom_initial = liste_vers_nom(ensemble_initial)

    # --- BFS sur les ensembles d'états ---
    a_traiter       = [ensemble_initial]
    deja_vus        = {nom_initial: ensemble_initial}
    trans_ensembles = {}

    while len(a_traiter) > 0:
        ens_courant = a_traiter.pop(0)
        nom_courant = liste_vers_nom(ens_courant)
        for sym in alphabet:
            dests    = calculer_destinations(ens_courant, sym)
            nom_dest = liste_vers_nom(dests)
            trans_ensembles[nom_courant + sym] = nom_dest
            if nom_dest not in deja_vus:
                deja_vus[nom_dest] = dests
                a_traiter.append(dests)

    a_poubelle = "P" in deja_vus

    # --- Transitions DFA ---
    nouvelles_transitions = {}
    for nom_etat in deja_vus:
        for sym in alphabet:
            cle_trans = nom_etat + sym
            if cle_trans in trans_ensembles:
                nouvelles_transitions[nom_etat + sym] = [trans_ensembles[cle_trans]]
            elif nom_etat == "P":
                nouvelles_transitions["P" + sym] = ["P"]

    # --- États terminaux du DFA ---
    terminaux_dfa = []
    for nom in deja_vus:
        if nom == "P":
            continue
        for e in deja_vus[nom]:
            if e in terminaux_nfa:
                terminaux_dfa.append(nom)
                break

    # --- Correspondance ---
    correspondance = {}
    for nom in deja_vus:
        if nom == "P":
            correspondance["P"] = "P (poubelle)"
        else:
            correspondance[nom] = "{" + ",".join(str(e) for e in deja_vus[nom]) + "}"

    noms_vrais = [n for n in deja_vus if n != "P"]

    return {
        "nb_symboles"    : automate["nb_symboles"],
        "nb_etats"       : len(noms_vrais),
        "noms_etats"     : noms_vrais,
        "initiaux"       : [nom_initial],
        "terminaux"      : terminaux_dfa,
        "transitions"    : nouvelles_transitions,
        "a_poubelle"     : a_poubelle,
        "correspondance" : correspondance
    }
# ------------------------------------------------------------
# determinisation_et_completion(automate)
# ------------------------------------------------------------
# PARAMÈTRE  : automate (dict) → NFA (non déterministe)
#              ou automate asynchrone (avec ε-transitions)
#
# RENVOIE    : un dictionnaire AFDC avec les clés supplémentaires :
#              "noms_etats"    → liste des noms d'états DFA (ex: ["0","01","013"])
#              "correspondance"→ dict nom → ensemble NFA d'origine
#              Les états sont nommés par CONCATÉNATION des états NFA
#              qui les composent : {0,1} → "01", {0,1,3} → "013"
#              Si états >= 10 : {10,2} → "10.2" (séparateur '.')
#              L'état poubelle s'appelle toujours 'P'.
#
# COMMENT    : Algorithme BFS sur les ensembles d'états (subset construction).
#              Pour les automates SYNCHRONES (sans ε) :
#                - État initial = {état_initial_NFA}
#                - Depuis un ensemble E avec symbole a : union des états
#                  atteignables depuis chaque état de E avec a
#              Pour les automates ASYNCHRONES (avec '*') :
#                - État initial = ε-clôture de {état_initial_NFA}
#                - Depuis un ensemble E avec symbole a : on suit a
#                  PUIS on calcule la ε-clôture des états atteints
#              Un état DFA est terminal s'il contient au moins un
#              état terminal du NFA d'origine.
#              Affiche les ε-clôtures si automate asynchrone.



def afficher_correspondance(afdc):
    print("\n  Correspondance états AFDC → états NFA d'origine :")
    print("  " + "-" * 40)
    cles = sorted([k for k in afdc["correspondance"] if k != "P"])
    if "P" in afdc["correspondance"]:
        cles.append("P")
    for nom in cles:
        print(f"    État {nom}  ←  {afdc['correspondance'][nom]}")
    print("  " + "-" * 40)
# ------------------------------------------------------------
# afficher_correspondance(afdc)
# ------------------------------------------------------------
# PARAMÈTRE  : afdc (dict) → automate avec clé "correspondance"
#              (produit par completion_seulement ou determinisation_et_completion)
#
# RENVOIE    : rien (affichage console)
#
# COMMENT    : Affiche la table "État X ← {états NFA d'origine}".
#              Trie les états normaux d'abord, puis 'P' en dernier.
#              Exigée par le sujet pour montrer la composition de chaque
#              état DFA en termes d'états du NFA d'origine.


# ============================================================
#  ÉTAPE 5 : Minimisation (algorithme de Moore)
# ============================================================

def minimisation(afdc):
    """
    Minimise un AFDC (algorithme de Moore).
    Partition 0 : {terminaux} | {non-terminaux}
    On raffine jusqu'à stabilité.
    """
    # Normalisation : tous les états deviennent des entiers
    if "noms_etats" in afdc:
        noms         = afdc["noms_etats"] + (["P"] if afdc.get("a_poubelle") else [])
        nom_vers_int = {nom: i for i, nom in enumerate(noms)}
        int_vers_nom = {i: nom for i, nom in enumerate(noms)}
        nb_etats     = len(noms)
        initiaux     = [nom_vers_int[n] for n in afdc["initiaux"]]
        terminaux    = [nom_vers_int[n] for n in afdc["terminaux"]]
        alphabet     = get_alphabet(afdc)
        transitions  = {}
        for nom_dep in noms:
            for sym in alphabet:
                cle = str(nom_dep) + sym
                if cle in afdc["transitions"]:
                    nom_arr = afdc["transitions"][cle][0]
                    transitions[str(nom_vers_int[nom_dep]) + sym] = nom_vers_int[nom_arr]
    else:
        alphabet     = get_alphabet(afdc)
        int_vers_nom = None

        # On garde les états comme strings pour pouvoir distinguer "P"
        etats_list = [str(e) for e in range(afdc["nb_etats"])]
        if afdc.get("a_poubelle"):
            etats_list.append("P")

        nb_etats  = len(etats_list)
        nom_vers_idx = {n: i for i, n in enumerate(etats_list)}

        initiaux  = [nom_vers_idx[str(i)] for i in afdc["initiaux"]]
        terminaux = [nom_vers_idx[str(t)] for t in afdc["terminaux"]]

        # int_vers_nom : index → nom affiché (entier ou "P")
        int_vers_nom = {i: n for i, n in enumerate(etats_list)}

        transitions = {}
        for etat in etats_list:
            for sym in alphabet:
                cle = str(etat) + sym
                if cle in afdc["transitions"]:
                    arr = str(afdc["transitions"][cle][0])
                    transitions[str(nom_vers_idx[etat]) + sym] = nom_vers_idx[arr]

    etats = list(range(nb_etats))

    # Cas spéciaux
    if len(terminaux) == 0:
        print("  → Aucun état terminal : automate minimal = 1 état non terminal.")
        return None, True
    if len(terminaux) == nb_etats:
        print("  → Tous les états terminaux : automate minimal = 1 état terminal.")
        return None, True

    # Partition initiale
    groupe_T  = sorted([e for e in etats if e in terminaux])
    groupe_NT = sorted([e for e in etats if e not in terminaux])
    partition = [g for g in [groupe_T, groupe_NT] if len(g) > 0]

    print("\n" + "=" * 55)
    print("  MINIMISATION (algorithme de Moore)")
    print("=" * 55)

    def afficher_partition(partition, int_vers_nom):
        if int_vers_nom:
            return [[int_vers_nom[e] for e in g] for g in partition]
        return partition

    print(f"\n  Partition 0 : {afficher_partition(partition, int_vers_nom)}")

    def trouver_groupe(etat, partition):
        for i, groupe in enumerate(partition):
            if etat in groupe:
                return i
        return -1

    def afficher_partition(partition, int_vers_nom):
        if int_vers_nom:
            return [[int_vers_nom[e] for e in g] for g in partition]
        return partition

    num_iter = 1
    while True:
        nouvelle_partition = []
        for groupe in partition:
            if len(groupe) == 1:
                nouvelle_partition.append(groupe)
                continue
            motifs = {}
            for etat in groupe:
                motif = tuple(
                    trouver_groupe(transitions[str(etat) + sym], partition)
                    if str(etat) + sym in transitions else -1
                    for sym in alphabet
                )
                if motif not in motifs:
                    motifs[motif] = []
                motifs[motif].append(etat)
            for sous_groupe in motifs.values():
                nouvelle_partition.append(sorted(sous_groupe))

        print(f"  Partition {num_iter} : {afficher_partition(nouvelle_partition, int_vers_nom)}")

        if nouvelle_partition == partition:
            print(f"\n  → Partition {num_iter} = Partition {num_iter-1} : ARRÊT")
            partition_finale = nouvelle_partition
            break

        partition = nouvelle_partition
        num_iter += 1

    # Automate déjà minimal ?
    if len(partition_finale) == nb_etats:
        print("  → L'automate est déjà minimal !")
        print("=" * 55 + "\n")
        return afdc, True

    # Construction de l'automate minimal
    print("\n  Construction de l'automate minimal...")

    def groupe_vers_nom(groupe):
        if int_vers_nom:
            vrais_noms = [int_vers_nom[e] for e in sorted(groupe)]
            if vrais_noms == ["P"]:
                return "P"
            # Si un seul élément, on garde son nom tel quel
            if len(vrais_noms) == 1:
                return vrais_noms[0]
            # Si les noms sont déjà des noms composés (contiennent "."),
            # on crée un nom court avec les indices de groupe
            if any("." in n for n in vrais_noms):
                return f"G{sorted(groupe)[0]}"
            # Sinon concaténation simple des entiers < 10, séparateur sinon
            if all(n != "P" and n.isdigit() and int(n) < 10 for n in vrais_noms):
                return "".join(vrais_noms)
            return ".".join(vrais_noms)
        if all(e < 10 for e in groupe):
            return "".join(str(e) for e in sorted(groupe))
        return ".".join(str(e) for e in sorted(groupe))

    noms_groupes     = [groupe_vers_nom(g) for g in partition_finale]
    etat_vers_groupe = {}
    for i, groupe in enumerate(partition_finale):
        for etat in groupe:
            etat_vers_groupe[etat] = noms_groupes[i]

    initial_min   = etat_vers_groupe[initiaux[0]]
    terminaux_min = []
    for i, groupe in enumerate(partition_finale):
        for e in groupe:
            if e in terminaux:
                terminaux_min.append(noms_groupes[i])
                break

    transitions_min = {}
    for i, groupe in enumerate(partition_finale):
        representant = groupe[0]
        nom_groupe   = noms_groupes[i]
        for sym in alphabet:
            cle = str(representant) + sym
            if cle in transitions:
                transitions_min[nom_groupe + sym] = [etat_vers_groupe[transitions[cle]]]

    correspondance_min = {}
    for i, groupe in enumerate(partition_finale):
        nom = noms_groupes[i]
        if int_vers_nom:
            noms_orig = [int_vers_nom[e] for e in groupe]
            correspondance_min[nom] = "{" + ",".join(noms_orig) + "}"
        else:
            correspondance_min[nom] = "{" + ",".join(str(e) for e in groupe) + "}"

    afdcm = {
        "nb_symboles"    : afdc["nb_symboles"],
        "nb_etats"       : len(partition_finale),
        "noms_etats"     : noms_groupes,
        "initiaux"       : [initial_min],
        "terminaux"      : terminaux_min,
        "transitions"    : transitions_min,
        "a_poubelle"     : False,
        "correspondance" : correspondance_min
    }

    print("=" * 55 + "\n")
    return afdcm, False
# ------------------------------------------------------------
# minimisation(afdc)
# ------------------------------------------------------------
# PARAMÈTRE  : afdc (dict) → automate déterministe et complet
#              (peut avoir des états entiers ou des noms comme "01")
#
# RENVOIE    : tuple (afdcm, deja_minimal)
#              → (afdcm, False)  : afdcm est le nouvel automate minimal construit
#              → (afdc,  True)   : l'automate était déjà minimal (pas de construction)
#              → (None,  True)   : cas dégénéré (0 terminaux ou tous terminaux)
#
# COMMENT    : Algorithme de Moore (partitions itératives).
#              NORMALISATION : convertit d'abord tous les états en entiers
#              (indice dans une liste) pour simplifier les calculs,
#              qu'ils soient entiers ou noms comme "01", "013".
#              Garde int_vers_nom pour reconvertir à l'affichage.
#
#              PARTITION 0 : [groupe_terminaux, groupe_non_terminaux]
#              ITÉRATIONS : pour chaque groupe, calcule le "motif" de chaque état
#              (tuple des numéros de groupes destination pour chaque symbole).
#              Deux états avec le même motif restent ensemble,
#              deux états avec des motifs différents se séparent.
#              ARRÊT : quand partition N = partition N-1.
#
#              CONSTRUCTION : si moins de groupes que d'états,
#              on construit l'automate minimal. Chaque groupe devient un état,
#              nommé par concaténation de ses états (ex: groupe [1,2] → "12").
#              On prend un représentant par groupe pour construire les transitions.
#
#              Affiche chaque partition numérotée (exigé par le sujet).



def afficher_automate_minimal(afdcm):
    print("\n--- Automate minimal (AFDCM) ---")
    afficher_afdc(afdcm)
    print("\n  Correspondance états AFDCM → états AFDC d'origine :")
    print("  " + "-" * 40)
    for nom, contenu in afdcm["correspondance"].items():
        print(f"    État {nom}  ←  {contenu}")
    print("  " + "-" * 40 + "\n")
# ------------------------------------------------------------
# afficher_automate_minimal(afdcm)
# ------------------------------------------------------------
# PARAMÈTRE  : afdcm (dict) → automate minimal (a toujours "noms_etats")
#
# RENVOIE    : rien (affichage console)
#
# COMMENT    : Appelle afficher_afdc pour la table de transitions,
#              puis affiche la table de correspondance
#              "état minimal ← {états AFDC qu'il regroupe}".
#              Exigée par le sujet.



# ============================================================
#  ÉTAPE 6 : Reconnaissance de mots
# ============================================================

def reconnaitre_mot(mot, afdc):
    """
    Vérifie si un mot est reconnu par l'AFDC.
    On suit les transitions lettre par lettre depuis l'état initial.
    """
    alphabet = get_alphabet(afdc)
    etat     = afdc["initiaux"][0]

    for lettre in mot:
        if lettre not in alphabet:
            print(f"  ⚠ La lettre '{lettre}' n'est pas dans l'alphabet {alphabet}")
            return False
        cle = str(etat) + lettre
        if cle in afdc["transitions"]:
            etat = afdc["transitions"][cle][0]
        else:
            return False

    return etat in afdc["terminaux"]
# reconnaitre_mot(mot, afdc)
# ------------------------------------------------------------
# PARAMÈTRES : mot (str) → le mot à tester ex: "aab"
#              afdc (dict) → l'automate sur lequel tester
#              (utilise de préférence l'AFDCM si disponible)
#
# RENVOIE    : bool → True si le mot est reconnu, False sinon
#
# COMMENT    : Simule l'exécution de l'automate lettre par lettre.
#              Part de l'état initial, suit les transitions dans
#              le dictionnaire. Si une lettre n'est pas dans l'alphabet
#              ou si une transition manque → rejette le mot.
#              À la fin du mot : vérifie si l'état courant est terminal.
#              Le mot vide est géré dans le main() directement
#              (vérifie si l'état initial est terminal).



# ============================================================
#  ÉTAPE 7 : Langage complémentaire
# ============================================================

def automate_complementaire(afdc):
    """
    Construit l'automate du langage complémentaire.
    On inverse les états terminaux et non-terminaux.
    """
    if "noms_etats" in afdc:
        tous_les_etats = list(afdc["noms_etats"])
    else:
        tous_les_etats = [str(e) for e in range(afdc["nb_etats"])]

    if afdc.get("a_poubelle"):
        tous_les_etats.append("P")

    terminaux_actuels  = afdc["terminaux"]
    nouveaux_terminaux = [e for e in tous_les_etats if e not in terminaux_actuels]

    complement             = dict(afdc)
    complement["terminaux"] = nouveaux_terminaux
    return complement
# ------------------------------------------------------------
# automate_complementaire(afdc)
# ------------------------------------------------------------
# PARAMÈTRE  : afdc (dict) → l'AFDC ou l'AFDCM
#              (le programme indique lequel il utilise)
#
# RENVOIE    : un nouveau dictionnaire automate représentant
#              le complémentaire. Seule la clé "terminaux" change :
#              les anciens terminaux deviennent non-terminaux et
#              vice-versa. Toutes les transitions restent identiques.
#
# COMMENT    : Construit la liste de TOUS les états (vrais états + 'P'),
#              puis les nouveaux terminaux = tous les états qui N'ÉTAIENT PAS
#              dans l'ancienne liste terminaux.
#              Utilise dict(afdc) pour faire une copie superficielle
#              du dictionnaire avant de modifier uniquement "terminaux".
#              L'état poubelle 'P', qui était non-terminal, devient
#              terminal dans le complémentaire.


# ============================================================
#  PROGRAMME PRINCIPAL
# ============================================================

def main():
    print("=" * 55)
    print("  TRAITEMENT D'AUTOMATES FINIS")
    print("=" * 55)

    continuer = True
    while continuer:
        print("\nQuel automate voulez-vous charger ?")
        print("(numéro ex: 21 pour automate_21.txt)")
        print("(0 pour quitter)")

        choix = input("Votre choix : ").strip()

        if choix == "0":
            print("Au revoir !")
            continuer = False
        else:
            num         = choix.zfill(2)
            nom_fichier = f"automate_{num}.txt"

            print(f"\nChargement de '{nom_fichier}'...")
            automate = lire_automate(nom_fichier)

            if automate is not None:
                print(f"Automate #{num} chargé avec succès !")

                # --- Étape 1 : affichage ---
                afficher_automate(automate)

                # --- Étape 2 : propriétés ---
                afficher_proprietes(automate)

                # --- Étape 3 : standardisation ---
                est_std, _ = est_standard(automate)
                if not est_std:
                    rep = input("Voulez-vous standardiser ? (o/n) : ").strip().lower()
                    if rep == "o":
                        automate = standardisation(automate)
                        print("\n--- Automate standardisé ---")
                        afficher_automate(automate)
                    else:
                        print("  → Standardisation ignorée.")
                else:
                    print("  → L'automate est déjà standard.")

                # --- Étape 4 : déterminisation et/ou complétion ---
                # Pour les automates asynchrones, on passe directement
                # dans determinisation_et_completion qui gère les ε
                if a_epsilon(automate):
                    print("  → Automate asynchrone (ε-transitions) détecté.")
                    print("  → Déterminisation avec ε-clôtures + complétion...")
                    afdc = determinisation_et_completion(automate)
                    print("\n--- Automate déterministe et complet (AFDC) ---")
                    afficher_afdc(afdc)
                    afficher_correspondance(afdc)
                else:
                    est_det, _ = est_deterministe(automate)
                    est_comp, _ = est_complet(automate) if est_det else (False, [])

                    if est_det and est_comp:
                        print("  → L'automate est déjà déterministe et complet.")
                        afdc = automate

                    elif est_det and not est_comp:
                        print("  → Déterministe mais incomplet → complétion...")
                        afdc = completion_seulement(automate)
                        print("\n--- Automate déterministe et complet (AFDC) ---")
                        afficher_automate(afdc)
                        afficher_correspondance(afdc)

                    else:
                        print("  → Non déterministe → déterminisation + complétion...")
                        afdc = determinisation_et_completion(automate)
                        print("\n--- Automate déterministe et complet (AFDC) ---")
                        afficher_afdc(afdc)
                        afficher_correspondance(afdc)

                # --- Étape 5 : minimisation ---
                print("\n  → Minimisation en cours...")
                afdcm, deja_minimal = minimisation(afdc)

                if afdcm is None:
                    print("  → Cas dégénéré (0 terminaux ou tous terminaux).")
                elif deja_minimal:
                    print("  → L'automate est déjà minimal.")
                    afficher_automate_minimal(afdc) if "noms_etats" not in afdc else afficher_automate_minimal(afdc)
                else:
                    afficher_automate_minimal(afdcm)

                # --- Étape 6 : reconnaissance de mots ---
                print("\n" + "=" * 55)
                print("  RECONNAISSANCE DE MOTS")
                print("  (tapez 'fin' pour arrêter)")
                print("=" * 55)

                automate_reconnaissance = afdcm if (afdcm is not None and not deja_minimal) else afdc

                mot = input("\n  Entrez un mot : ").strip()
                while mot != "fin":
                    if mot == "":
                        resultat = afdc["initiaux"][0] in afdc["terminaux"]
                    else:
                        resultat = reconnaitre_mot(mot, automate_reconnaissance)
                    if resultat:
                        print(f"  '{mot}' → OUI ✓")
                    else:
                        print(f"  '{mot}' → NON ✗")
                    mot = input("\n  Entrez un mot : ").strip()

                # --- Étape 7 : langage complémentaire ---
                print("\n" + "=" * 55)
                print("  LANGAGE COMPLÉMENTAIRE")
                print("=" * 55)

                if afdcm is not None and not deja_minimal:
                    base = afdcm
                    print("  → Complémentaire calculé à partir de l'AFDCM")
                else:
                    base = afdc
                    print("  → Complémentaire calculé à partir de l'AFDC")

                acomp = automate_complementaire(base)
                print("\n--- Automate complémentaire ---")
                if "noms_etats" in acomp:
                    afficher_afdc(acomp)
                else:
                    afficher_automate(acomp)


if __name__ == "__main__":
    main()