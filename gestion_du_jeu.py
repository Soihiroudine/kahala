import random

from Joueur import Joueur
from plateau_de_jeu import Kahala


class Jeu:
    """Gère la configuration, la saisie et la boucle de partie."""

    def __init__(self):
        self.j1 = Joueur("Joueur_A")
        self.j2 = Joueur("Joueur_B")
        self.game = Kahala(self.j1, self.j2, random.choice([0, 1]))
        self.indice = 0
        self.inteligenceOrdi = 1

    def continuerOuQuitter(self):
        reponse = input("Continuer (o/n): ").strip().lower()
        return reponse in {"n", "non", "quit", "quitter"}

    def gagnant(self):
        score1 = self.j1.getPoint()
        score2 = self.j2.getPoint()
        if score1 > score2:
            print(f"Le joueur {self.j1.getName()} a gagné avec {score1} graines.")
            return "j1"
        if score2 > score1:
            print(f"Le joueur {self.j2.getName()} a gagné avec {score2} graines.")
            return "j2"
        print(f"Égalité : les deux joueurs ont {score1} graines.")
        return "egalite"

    def verificationDeLaSaisie(self):
        return not 1 <= self.indice <= 6

    def uneBonneSaisie(self, humain):
        if humain:
            while True:
                try:
                    nom = self.game.joueur[self.game.tourJoueur()].getName()
                    saisie = input(f"--- {nom} choisit entre 1 à 6 : ").strip()
                    if saisie.lower() in {"quit", "quitter", "exit"}:
                        print("\nFin de programme.")
                        return None
                    self.indice = int(saisie)
                except ValueError:
                    print("\nErreur : veuillez saisir un nombre entier.")
                    continue
                except KeyboardInterrupt:
                    print("\nFin de programme.")
                    return None

                if self.verificationDeLaSaisie():
                    print("\nErreur : mettre un nombre entre 1 et 6.")
                elif self.game.cases[self.game.tourJoueur()][self.indice - 1] <= 0:
                    print(f"\nErreur : la case {self.indice} est vide.")
                else:
                    return self.indice
        else:
            nom = self.game.joueur[self.game.tourJoueur()].getName()
            print(f"L'ordinateur {nom} fait son choix...")
            choix = [1, 2, 3, 4, 5, 6]
            if self.inteligenceOrdi == 1:
                self.ordiNonInteligent(choix)
            else:
                self.ordiRandom(choix)
            return self.indice

    def choixIntelligence(self):
        while True:
            try:
                print("\nNiveau de l'ordinateur :")
                print("  1 - facile")
                print("  2 - aléatoire (moyen)")
                choix = int(input("Votre choix : ").strip())
            except (ValueError, KeyboardInterrupt):
                print("\nErreur : mettre un nombre entre 1 et 2.")
                continue
            if 1 <= choix <= 2:
                self.inteligenceOrdi = choix
                return
            print("\nErreur : mettre un nombre entre 1 et 2.")

    def casesDisponibles(self):
        rang = self.game.tourJoueur()
        return [
            indice
            for indice in range(1, 7)
            if self.game.cases[rang][indice - 1] > 0
        ]

    def ordiRandom(self, nb):
        disponibles = self.casesDisponibles()
        if disponibles:
            self.indice = random.choice(disponibles)
        else:
            self.indice = 0
        return self.indice

    def ordiNonInteligent(self, nb):
        for indice in nb:
            if self.game.cases[self.game.tourJoueur()][indice - 1] > 0:
                self.indice = indice
                return indice
        self.indice = 0
        return 0

    def miseAjourJoueur(self, joueur, humain, numero):
        nom = input(f"Nom du joueur {numero} : ").strip()
        if nom:
            joueur.setName(nom)
        joueur.setHumain(humain)

    def modeJeu(self, mode):
        if mode == 1:
            reponse = input("Voulez-vous mettre vos noms (o/n): ").strip().lower()
            if reponse in {"o", "oui"}:
                self.miseAjourJoueur(self.j1, True, 1)
                self.miseAjourJoueur(self.j2, True, 2)
            else:
                self.j1.setHumain(True)
                self.j2.setHumain(True)
        elif mode == 2:
            reponse = input("Voulez-vous mettre votre nom (o/n): ").strip().lower()
            if reponse in {"o", "oui"}:
                self.miseAjourJoueur(self.j1, True, 1)
            else:
                self.j1.setHumain(True)
            self.j2.setName("Renard")
            self.j2.setHumain(False)
            self.choixIntelligence()
        elif mode == 3:
            self.choixIntelligence()
            self.j1.setName("Renard")
            self.j2.setName("Lapin")
            self.j1.setHumain(False)
            self.j2.setHumain(False)

    def choisirMode(self):
        while True:
            print("\nChoisir le mode de jeu :")
            print("  1 - Humain vs Humain")
            print("  2 - Humain vs Ordinateur")
            print("  3 - Ordinateur vs Ordinateur")
            try:
                mode = int(input("Le mode : ").strip())
            except (ValueError, KeyboardInterrupt):
                print("\nErreur : mettre un nombre entre 1 et 3.")
                continue
            if 1 <= mode <= 3:
                return mode
            print("\nErreur : mettre un nombre entre 1 et 3.")

    def start(self):
        print("\nBonjour à vous, bienvenue dans le jeu du Kahala")
        print("----------------------------------------------")
        self.modeJeu(self.choisirMode())

        while True:
            self.game.plateau()
            print()

            if self.game.joueurCasesTousVide():
                self.game.captureTous()
                self.gagnant()
                self.game.plateau()

                if self.continuerOuQuitter():
                    print("Vous avez quitté le jeu.")
                    break
                self.game.initialisationCases()
                self.game.tour = random.choice([0, 1])
                continue

            joueur = self.game.joueur[self.game.tourJoueur()]
            choix = self.uneBonneSaisie(joueur.getHumain())
            if choix is None:
                break

            print(f"{joueur.getName()} a choisi : {choix}")
            rejoue = self.game.modificationPlateau(choix)
            if not rejoue:
                self.game.tourChangeJoueur()
