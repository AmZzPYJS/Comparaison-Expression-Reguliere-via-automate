import copy as cp


class automate:
    """
    classe de manipulation des automates
    l'alphabet est l'ensemble des caractères alphabétiques minuscules et "E" pour epsilon, 
    et "O" pour l'automate vide
    """
    
    def __init__(self, expr="O"):
        """
        construit un automate élémentaire pour une expression régulière expr 
            réduite à un caractère de l'alphabet, ou automate vide si "O"
        identifiant des états = entier de 0 à n-1 pour automate à n états
        état initial = état 0
        """
        
        # alphabet
        self.alphabet = list("abc")
        # l'expression doit contenir un et un seul caractère de l'alphabet
        if expr not in (self.alphabet + ["O", "E"]):
            raise ValueError("l'expression doit contenir un et un seul\
                           caractère de l'alphabet " + str(self.alphabet))
        # nombre d'états
        if expr == "O":
            # langage vide
            self.n = 1
        elif expr == "E":
            self.n = 1
        else:
            self.n = 2
        # états finals: liste d'états (entiers de 0 à n-1)
        if expr == "O":
            self.final = []
        elif expr == "E":
            self.final = [0]
        else:
            self.final = [1]
        # transitions: dico indicé par (état, caractère) qui donne la liste des états d'arrivée
        self.transition =  {} if (expr in ["O", "E"]) else {(0,expr): [1]}
        # nom de l'automate: obtenu par application des règles de construction
        self.name = "" if expr == "O" else "(" + expr + ")" 
        
    def __str__(self):
        """affichage de l'automate par fonction print"""
        res = "Automate " + self.name + "\n"
        res += "Nombre d'états " + str(self.n) + "\n"
        res += "Etats finals " + str(self.final) + "\n"
        res += "Transitions:\n"
        for k,v in self.transition.items():    
            res += str(k) + ": " + str(v) + "\n"
        res += "*********************************"
        return res
    
    def ajoute_transition(self, q0, a, qlist):
        """ ajoute la liste de transitions (q0, a, q1) pour tout q1 
            dans qlist à l'automate
            qlist est une liste d'états
        """
        if not isinstance(qlist, list):
            raise TypeError("Erreur de type: ajoute_transition requiert une liste à ajouter")
        if (q0, a) in self.transition:
            self.transition[(q0, a)] = self.transition[(q0, a)] + qlist
        else:
            self.transition.update({(q0, a): qlist})


def decaler_automate(a, decalage):
    """Copie de a avec tous les états +decalage."""
    b = cp.deepcopy(a)
    b.final = [q + decalage for q in b.final]
    b.transition = {
        (q + decalage, symb): [d + decalage for d in dests]
        for (q, symb), dests in b.transition.items()
    }
    return b


def concatenation(a1, a2):
    a1b = cp.deepcopy(a1)
    a2b = decaler_automate(a2, a1.n)

    a = automate("O")
    a.alphabet = a1.alphabet
    a.n = a1.n + a2.n

    a.transition = {}
    a.transition.update(a1b.transition)
    a.transition.update(a2b.transition)

    init_a2 = a1.n
    for f in a1b.final:
        a.ajoute_transition(f, "E", [init_a2])

    a.final = a2b.final
    a.name = f"({a1.name}.{a2.name})"
    return a


def union(a1, a2):
    a1b = decaler_automate(a1, 1)
    a2b = decaler_automate(a2, 1 + a1.n)

    a = automate("O")
    a.alphabet = a1.alphabet
    a.n = 1 + a1.n + a2.n

    a.transition = {}
    a.transition.update(a1b.transition)
    a.transition.update(a2b.transition)

    a.ajoute_transition(0, "E", [1, 1 + a1.n])
    a.final = a1b.final + a2b.final
    a.name = f"({a1.name}+{a2.name})"
    return a


def etoile(a1):
    a1b = decaler_automate(a1, 1)

    a = automate("O")
    a.alphabet = a1.alphabet
    a.n = a1.n + 1

    a.transition = {}
    a.transition.update(a1b.transition)

    a.final = [0] + a1b.final

    a.ajoute_transition(0, "E", [1])
    for f in a1b.final:
        a.ajoute_transition(f, "E", [1, 0])

    a.name = f"({a1.name})*"
    return a


def acces_epsilon(a):
    """ retourne la liste pour chaque état des états accessibles par epsilon
        transitions pour l'automate a
        res[i] est la liste des états accessible pour l'état i
    """
    # on initialise la liste résultat qui contient au moins l'état i pour chaque état i
    res = [[i] for i in range(a.n)]
    for i in range(a.n):
        candidats = list(range(i)) + list(range(i+1, a.n))
        new = [i]
        while True:
            # liste des epsilon voisins des états ajoutés en dernier:
            voisins_epsilon = []
            for e in new:
                if (e, "E") in a.transition.keys():
                    voisins_epsilon += [j for j in a.transition[(e, "E")]]
            # on calcule la liste des nouveaux états:
            new = list(set(voisins_epsilon) & set(candidats))
            # si la nouvelle liste est vide on arrête:
            if new == []:
                break
            # sinon on retire les nouveaux états ajoutés aux états candidats
            candidats = list(set(candidats) - set(new))
            res[i] += new 
    return res


def supression_epsilon_transitions(a):
	a = cp.deepcopy(a)
	res = automate("O")
	res.name = a.name
	res.n = a.n
	res.alphabet = a.alphabet

	acces = acces_epsilon(a)

	res.final = []
	finals = set(a.final)
	for i in range(a.n):
		if set(acces[i]) & finals:
			res.final.append(i)

	res.transition = {}
	for i in range(a.n):
		for x in a.alphabet:
			dest = set()
			for p in acces[i]:
				if (p, x) in a.transition:
					for q in a.transition[(p, x)]:
						dest.update(acces[q])  
			if dest:
				res.transition[(i, x)] = sorted(dest)

	return res


def determinisation(a):
    a_entree = cp.deepcopy(a)

    dfa = automate("O")
    dfa.alphabet = a_entree.alphabet
    dfa.transition = {}
    dfa.name = a_entree.name

    ensembles = [frozenset([0])]
    a_traiter = [frozenset([0])]

    while a_traiter:
        S = a_traiter.pop(0)
        id_S = ensembles.index(S)

        for c in a_entree.alphabet:
            arrivee = set()
            for q in S:
                if (q, c) in a_entree.transition:
                    arrivee.update(a_entree.transition[(q, c)])

            if not arrivee:
                continue

            T = frozenset(arrivee)
            if T not in ensembles:
                ensembles.append(T)
                a_traiter.append(T)

            id_T = ensembles.index(T)
            dfa.transition[(id_S, c)] = [id_T]

    dfa.n = len(ensembles)

    dfa.final = []
    finals_nfa = set(a_entree.final)
    for i, S in enumerate(ensembles):
        if set(S) & finals_nfa:
            dfa.final.append(i)

    return dfa


def completion(a):
    a = cp.deepcopy(a)
    etat_poubelle = None

    for q in range(a.n):
        for c in a.alphabet:
            if (q, c) not in a.transition:
                if etat_poubelle is None:
                    etat_poubelle = a.n
                    a.n += 1
                a.transition[(q, c)] = [etat_poubelle]

    if etat_poubelle is not None:
        for c in a.alphabet:
            a.transition[(etat_poubelle, c)] = [etat_poubelle]

    return a


def minimisation(a):
    """ retourne l'automate minimum
        a doit être déterministe complet
        algo par raffinement de partition (algo de Moore)
    """
    # on copie pour éviter les effets de bord     
    a = cp.deepcopy(a)
    res = automate()
    res.name = a.name
    
    # Étape 1 : partition initiale = finaux / non finaux
    part = [set(a.final), set(range(a.n)) - set(a.final)]
    # on retire les ensembles vides
    part = [e for e in part if e != set()]  
    
    # Étape 2 : raffinement jusqu’à stabilité
    modif = True
    while modif:
        modif = False
        new_part = []
        for e in part:
            # sous-ensembles à essayer de séparer
            classes = {}
            for q in e:
                # signature = tuple des indices des blocs atteints pour chaque lettre
                signature = []
                for c in a.alphabet:
                    for i, e2 in enumerate(part):
                        if a.transition[(q, c)][0] in e2:
                            signature.append(i)
                # on ajoute l'état q à la clef signature calculée
                classes.setdefault(tuple(signature), set()).add(q)
            if len(classes) > 1:
                # s'il y a >2 signatures différentes on a séparé des états dans e
                modif = True
                new_part.extend(classes.values())
            else:
                new_part.append(e)
        part = new_part    
     
    # Étape 3 : on construit le nouvel automate minimal
    mapping = {}
    # on associe à chaque état q le nouvel état i
    # obtenu comme étant l'indice du sous-ensemble de part
    for i, e in enumerate(part):
        for q in e:
            mapping[q] = i

    res.n = len(part)
    res.final = list({mapping[q] for q in a.final if q in mapping})
    for i, e in enumerate(part):
        # on récupère un élément de e:
        representant = next(iter(e))
        for c in a.alphabet:
            q = a.transition[(representant, c)][0]
            res.transition[(i, c)] = [mapping[q]]
    return res


def tout_faire(a):
    a1 = supression_epsilon_transitions(a)
    a2 = determinisation(a1)
    a3 = completion(a2)
    a4 = minimisation(a3)
    return a4


def egal(a1, a2):
    a1 = tout_faire(a1)
    a2 = tout_faire(a2)

    if a1.alphabet != a2.alphabet or a1.n != a2.n:
        return False

    m = {0: 0}
    file = [0]

    while file:
        q1 = file.pop(0)
        q2 = m[q1]

        if (q1 in a1.final) != (q2 in a2.final):
            return False

        for c in a1.alphabet:
            r1 = a1.transition[(q1, c)][0]
            r2 = a2.transition[(q2, c)][0]

            if r1 in m:
                if m[r1] != r2:
                    return False
            else:
                m[r1] = r2
                file.append(r1)

    return len(set(m.values())) == len(m.values()) and len(m) == a1.n

    

# TESTS

if __name__ == "__main__":
    print("TEST : decaler_automate")
    a = automate("a")
    b = decaler_automate(a, 3)
    print("Automate original a:\n", a)
    print("Automate décalé b:\n", b)

    assert a.n == 2
    assert a.final == [1]
    assert a.transition == {(0, "a"): [1]}
    assert b.n == a.n, "decaler_automate ne doit pas changer n"
    assert b.final == [4]
    assert b.transition == {(3, "a"): [4]}
    print("decaler_automate : OK")


    print("TEST: union")
    A = automate("a")
    B = automate("b")
    U = union(A, B)
    print(U)

    assert U.n == 1 + A.n + B.n
    assert (0, "E") in U.transition
    assert set(U.transition[(0, "E")]) == {1, 1 + A.n}
    assert len(U.final) == 2
    print("union : OK")


    print("TEST : concatenation")
    A = automate("a")
    B = automate("b")
    C = concatenation(A, B)
    print(C)

    # états = n1+n2
    assert C.n == A.n + B.n
    # epsilon depuis final de A vers init de B décalé
    init_B = A.n
    for f in A.final:
        assert (f, "E") in C.transition, "Il manque l'epsilon de concaténation"
        assert init_B in C.transition[(f, "E")]
    print("concatenation : OK")


    print("TEST : etoile")
    A = automate("a")
    S = etoile(A)
    print(S)

    assert S.n == A.n + 1
    assert 0 in S.final, "etoile doit accepter epsilon => état 0 final"
    assert (0, "E") in S.transition
    assert 1 in S.transition[(0, "E")], "0 doit aller vers l'état initial de A décalé"
    print("etoile : OK")


    print("TEST : determinisation")
    # AFN simple : 0 --a--> 1 et 2 (non déterministe)
    nfa = automate("O")
    nfa.alphabet = list("abc")
    nfa.n = 3
    nfa.final = [2]
    nfa.transition = {}
    nfa.ajoute_transition(0, "a", [1, 2])
    nfa.ajoute_transition(1, "b", [2])

    print("NFA:\n", nfa)
    dfa = determinisation(nfa)
    print("DFA:\n", dfa)

    # propriété simple : en DFA, toutes les transitions ont 0 ou 1 destination (ici 1)
    for (q, c), dests in dfa.transition.items():
        assert c != "E"
        assert len(dests) == 1
    print("determinisation : OK")


    print("TEST : completion")
    d = automate("O")
    d.alphabet = list("abc")
    d.n = 2
    d.final = [1]
    d.transition = {(0, "a"): [1]}  # transitions manquantes

    print("Avant complétion:\n", d)
    dc = completion(d)
    print("Après complétion:\n", dc)

    # automate complet : pour tout état et toute lettre il y a une transition
    for q in range(dc.n):
        for c in dc.alphabet:
            assert (q, c) in dc.transition
            assert len(dc.transition[(q, c)]) == 1
    print("completion : OK")


    print("TEST : minimisation")
    # On minimise un automate déjà complet
    dm = minimisation(dc)
    print("Minimisé:\n", dm)

    # doit rester complet
    for q in range(dm.n):
        for c in dm.alphabet:
            assert (q, c) in dm.transition
            assert len(dm.transition[(q, c)]) == 1
    print("minimisation : OK")

    print("TEST : egal (FAUX)")
    # faux : (a+b).c != a.c + b
    left = concatenation(union(automate("a"), automate("b")), automate("c"))
    right = union(concatenation(automate("a"), automate("c")), automate("b"))

    print("left:", left.name)
    print("right:", right.name)
    assert egal(left, right) is False
    print("egal (FAUX) : OK")





    
