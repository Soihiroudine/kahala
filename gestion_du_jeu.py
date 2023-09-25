import random
import time
from Joueur import Joueur
from plateau_de_jeu import Kahala


"""
La classe Jeu va être celui qui va gerer le Jeu
"""

class Jeu:
    def __init__(self):
        # Valeur par default des noms de joueur
        self.j1 = Joueur("Joueur_A")
        self.j2 = Joueur("Joueur_B")
        self.game = Kahala(self.j1, self.j2, random.choice([0, 1]))
        self.indice = 0
        self.inteligenceOrdi = 1
        
    def continuerOuQuitter(self):
        OuiNon = input("Continuer (o/n): ")
        return OuiNon == "n" or OuiNon == "quit"
        
    def gagnant(self): 
        if self.j1.getPoint() > self.j2.getPoint():
            self.j1.information()
            print(f"Le joueur {self.j1.getName()} a gagner !\n")
        elif self.j1.getPoint() == self.j2.getPoint():
            print(f"Les deux Joueurs sont la même valeur : {self.j1.getPoint()}\n")
        else:
            self.j2.information()
            print(f"Le joueur {self.j2.getName()} a gagner !\n")

    def verificationDeLaSaisie(self):  # Verification de l'indice si c'est entre 1 et 6
        return (self.indice < 1) or (self.indice > 6)
    
    def uneBonneSaisie(self, humain):  # verification de la saisie d'une case dans le plateau
        if humain:
            while True:
                try:
                    print(f"--- {self.game.joueur[self.game.tourJoueur()].getName()} ", end=" ")
                    self.indice = input("choisi entre 1 à 6 : ")
                    self.indice = int(self.indice)
                except ValueError:
                    # 1 - choisir un nombre entier
                    print("\n Erreur : veiller saisir un nombre !")
                    time.sleep(1)
                    self.game.plateau()
                except KeyboardInterrupt:
                    print("\n\tFin de programme par une touche !\n")
                    break
                else:
                    # 2 - Que le nombre est entre 1 et 6 (6 compris)
                    if self.verificationDeLaSaisie(): 
                        print("\n Erreur : Mettre un nombre entre 1 et 6")
                        time.sleep(1)
                        self.game.plateau()
                    # - 3. Que la case selectionner a au minimum 1 graine
                    elif self.game.cases[self.game.tourJoueur()][self.indice-1] <= 0:
                        print(f"\n Erreur : La case {self.indice} est vide")
                        time.sleep(1)
                        self.game.plateau()
                    else:
                        return self.indice  
        else:
            print(f"l'ordinateur {self.game.joueur[self.game.tourJoueur()].getName()} fait son choix....")
            time.sleep(1)
            choix = [1, 2, 3, 4, 5, 6]  # nombre de cases, nombre de choix

            if self.inteligenceOrdi == 1:
                self.ordiNonInteligent(choix)
            elif self.inteligenceOrdi == 2:
                self.ordiRandom(choix)
            # elif self.inteligenceOrdi == 3:
            #     print("Pas encore mis d'intelliegence !")
            #     return 0
            return self.indice 
    
    def choixIntelligence(self):
        while True:
            try:
                print("\n Niveau de l'ordinateur :")
                print("  1 - facile")
                print("  2 - Ordinateur qui choisit à l'instint (moyen)")
                # print("  3 - ordinateur intelligent (fort)")
                self.inteligenceOrdi = input("Votre choix : ")
                self.inteligenceOrdi = int(self.inteligenceOrdi)
            except ValueError:
                # 1 - choisir un nombre entier
                print("\n Erreur : veiller saisir un nombre !")
            except KeyboardInterrupt:
                print("\n\tFin de programme par une touche !\n")
            else:
                if self.inteligenceOrdi < 0 and self.inteligenceOrdi > 3:
                    print("\n Erreur : Mettre un nombre entre 1 ou 2")
                # elif self.inteligenceOrdi == 3:
                #     print("\n Pas de cerveau existant")
                else:
                    break

    # l'ordinateur va choisi de façon aleatoire
    def ordiRandom(self, nb):
        self.indice = random.choice(nb)
        while self.verificationDeLaSaisie() or self.game.cases[self.game.tourJoueur()][self.indice-1] <= 0:
            self.indice = random.choice(nb) 

    # l'ordinateur va choisir la premiere valeur 
    # La seul condition est que la case doit être supérieur à 0
    # Est que l'indice prit soit entre 1 et 6
    def ordiNonInteligent(self, nb):
        for elt in nb:
            self.indice = elt
            if not(self.verificationDeLaSaisie()) and not(self.game.cases[self.game.tourJoueur()][self.indice-1] <= 0):
                return self.indice
       
    def miseAjourJoueur(self, joueur, humain, numero):
        nom = input(f"Nom du joueur {numero} :")
        joueur.setName(nom)
        joueur.setHumain(humain)

    # Il va permettre d'avoir le mode de jeu que l'on veut
    def modeJeu(self, mode):
        if mode == 1: # humain contre humain
            # Saisie d'information des joueur
            sePresenter = input("Voulez-vous mettre vos noms (o/n): ")
            if sePresenter == "o":
                self.miseAjourJoueur(self.j1, True, 1)
                self.miseAjourJoueur(self.j2, True, 2)
                print()
            else:
                print("Je vous attribue des noms par default")
                self.j1.setHumain(True)
                self.j2.setHumain(True)
            print(f"C'est a vous de jouer {self.j1.getName()} et {self.j2.getName()}")

        elif mode == 2: # humain contre machine
            print("Vous avez choisit humain vs ordinateur")
            sePresenter = input("Voulez-vous mettre votre nom (o/n): ")
            if sePresenter == "o":
                self.miseAjourJoueur(self.j1, True, 1)
            else:
                print("Je vous attribue des noms par default")
                self.j1.setHumain(True)
            self.choixIntelligence()
            self.j2.setName("Renard")
            print(f"C'est a vous de jouer {self.j1.getName()} et {self.j2.getName()}")

        elif mode == 3:  # Machine contre machine
            print("Vous avez choisit ordinateur vs ordinateur")
            self.choixIntelligence()
            self.j1.setName("Renard")
            self.j2.setName("Lapin")

    # Ceci est la fonction de mise en marche du jeu
    def start(self):
        print("\nBonjour a vous bienvenu dans le jeu du kahala")
        print("----------------------------------------------")
    
        # chosir avec qui jouer
        # - Humain vs Humain
        # - Humain vs Ordinateur
        # - Ordinateur vs Ordinateur
        while True:
            try:
                print()
                print("Chosit le mode de jeu : ")
                print("  1 - Humain vs Humain")
                print("  2 - Humain vs Ordinateur")
                print("  3 - Ordinateur vs Ordinateur")

                quiJoue = input("le mode : ")
                quiJoue = int(quiJoue)
            except ValueError:
                # 1 - choisir un nombre entier
                print("\n Erreur : veiller saisir un nombre !")
            else:
                if quiJoue < 0 and quiJoue > 4:
                    print("\n Erreur : Mettre un nombre entre 1 et 3")
                else:
                    break

        # Application du mode choist
        self.modeJeu(quiJoue)

        # Boucle principale du jeu 
        while True:
            print("")
            self.game.plateau()
            print("")
               
            # on va verifier que les cases du joueur actuelle qui a jouer est vide 
            # Ou si un des joueur possede la moitier des graines dans son grenier
            if self.game.joueurCasesTousVide() or self.game.moitierDesGraine():
                # Capture tous les dernier element de l'advairse dans son grenier
                self.game.captureTous()
                
                # Affiche qui a gagner (son nombre de graine aussi)
                self.gagnant()
                time.sleep(1)

                # Affichage du tableau finale
                self.game.plateau()

                # Arrete le programme si c'est le joueur dit n'importe quelle element qui n'est pas [oui, o]
                if self.continuerOuQuitter():
                    
                    self.game.plateau()
                    print("Vous avez quitter le jeu !")
                    print("Au-revoir !!!!\n")
                    break 
                elif self.game.capturer:
                    self.game.initialisationCases()
            else:
                # Methode pour la Saisie de l'indice
                # Si la saisie n'est pas bonne elle lui redemande de le faire
                # Si ce n'est pas un nombre entier : il lui redemande 
                # Si le chiffre n'est pas compris entre 1 et 6 : il lui redemande

                # si une touche spéciale est activer le programme s'arrète
                if type(self.uneBonneSaisie(self.game.joueur[self.game.tourJoueur()].getHumain())) != type(1):
                    break
                
                # Affichage de la case que le joueur a choisi
                print(f"{self.game.joueur[self.game.tourJoueur()].getName()} a choisi : {self.indice}")
                if not(self.game.joueur[self.game.tourJoueur()].getHumain()):
                    time.sleep(1)
             
                # Application de la modification du plateau en fonction de la case choisi
                self.game.modificationPlateau(self.indice)
                self.game.tourChangeJoueur()