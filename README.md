# Le jeu du Kahala

## Outils

- Python 3 pour la version console
- Un navigateur web récent pour la version web

## Jouer au jeu

## Règles du Kahala

Cette version se joue à deux, sur un plateau de deux rangées de six cases. Au début, chaque case contient quatre graines. Le but est de récolter plus de graines que l'adversaire.

À son tour, un joueur choisit une case non vide de sa rangée et en prend toutes les graines. Il les distribue une par une dans les cases suivantes, dans le sens du parcours autour du plateau, puis dans son propre grenier. Il continue dans la rangée adverse si nécessaire, en sautant le grenier adverse.

- Si la dernière graine tombe dans son propre grenier, le joueur rejoue.
- Si la dernière graine tombe dans une case vide de sa propre rangée, il capture cette graine et celles de la case opposée, à condition que cette dernière contienne des graines.
- La partie se termine dès qu'une rangée est vide. Les graines restantes dans l'autre rangée sont ajoutées au grenier de son propriétaire.
- Le joueur qui a le plus de graines dans son grenier gagne. En cas d'égalité, la partie est nulle.

## Version web

Ouvrez `index.html` dans un navigateur. Choisissez un mode et les noms, puis démarrez une partie.
La version web fonctionne sans serveur et sans dépendance externe.
Le bouton « Aide » affiche les règles pendant la partie.

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

Le Kahala présenté ici ne reprend pas toutes les règles du jeu d'origine ; cette version est volontairement simplifiée.
