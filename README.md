# Le jeu du Kahala

## Outils

- Python 3 pour la version console
- Un navigateur web récent pour la version web

## Jouer au jeu

## Version web

Ouvrez `index.html` dans un navigateur. Choisissez un mode et les noms, puis démarrez une partie.
La version web fonctionne sans serveur et sans dépendance externe.

- Deux joueurs sur le même appareil
- Joueur contre ordinateur (choix facile ou aléatoire)
- Ordinateur contre ordinateur, coup par coup

## Version console

Pour jouer au Kahala dans le terminal, exécutez `main.py`.

Vous pouvez ouvrir un terminal et executer le fichier.
Bien sur il faut que python soit installer dans votre machine.

### Affichage du jeu en console

```text

                        Joueur A
             6      5      4      3      2      1
    -------------------------------------------------------
    | GA  |  5   |  5   |  5   |  6   |  4   |  4   |     |
    | 0   |-----------------------------------------| 1   |
    |     |  4   |  4   |  4   |  4   |  4   |  0   |  GB |
    -------------------------------------------------------
             1      2      3      4      5      6
                        Joueur B

    --- Joueur B  choisi entre 1 à 6 :
```

### Remarque
Le jeu du kahala ne possède pas tous les règles du jeu d'origine, je l'ai fait plutôt simple.

