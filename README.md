# Le jeu du Kahala en mode console

## Outils

- Python 3

## Jouer au jeu

Pour jouer au jeu du kahala, il faut executer le ficher `main.py`.

Vous pouvez ouvrir un terminal et executer le fichier.
Bien sur il faut que python soit installer dans votre machine.

### Affichage du jeu

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

## <span style="color:#af0654; font-weight:bold;">Probleme</span>

Le jeu n'est pas totalement fini. Il menque l'implementation de l'algorithme minMax. Le niveau trois de l'inteligence de l'ordinateur.

Dans tous les cas si est selectionner quand c'est au tour de l'ordinateur, le programme s'arrète.
