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

## Utilisation
Compilation :
```bash
make
./regexp < test.1
python3 main.py
