# Comparaison d’expressions régulières via automates

## Objectif
Comparer deux expressions régulières (potentiellement différentes) et décider si elles reconnaissent le **même langage**.

Idée : on transforme chaque expression régulière en automate, puis on applique :
- suppression des ε-transitions (si nécessaire)
- déterminisation
- complétion
- minimisation  
Puis on compare les automates minimaux (unicité à isomorphisme près).

---

## Fonctionnement (pipeline)
1. **Flex** : transforme les caractères de l’expression régulière en **tokens**
2. **Bison/Yacc** : vérifie la grammaire + exécute les **actions sémantiques**
3. Génère un fichier `main.py` qui construit les automates et lance `egal(A1, A2)`
4. Les fonctions automates sont dans `automate.py`

---

1. Contenu du projet
-------------------
- regexp.l      : analyse lexicale (Flex)
- regexp.y      : analyse syntaxique (Bison)
- automate.py   : implémentation des automates et opérations
- Makefile      : compilation automatique
- test.1        : premier test
- test.2        : second test
- test.3        : troisième test
- pdf/          : automates dessinés en PDF
- README        : instructions d’utilisation

2. Compilation
--------------
Pour compiler le projet, exécuter : make

3. Génération d’un test
-----------------------
Pour générer le fichier main.py à partir d’un test :
./regexp < test.1 (pour le test 1)

4. Exécution
------------
Pour lancer la comparaison des expressions :
python3 main.py

5. Nettoyage
------------
Pour supprimer les fichiers générés :
make clean

6. Tests Unitaires
------------
Pour voir les tests unitaires des fonctions faites dans automate.py :
make test
