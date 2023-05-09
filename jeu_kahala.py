import random as r

class Kahala:
    def __init__(self, joueur1, joueur2):
        self.graineMaxi = 48
        self.cases = [[4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4]]
        self.joueur = [joueur1, joueur2]
        self.tour = r.choice([0,1]) # choisi aléatoirement le premier joueur qui va jouer
        self.capturer = False
    
    def initialisationCases(self):
        # Mise a jour du jeu
        # initialisation de la case
        self.cases = [[4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4]]
        for jn in range(len(self.joueur)):
            self.joueur[jn].moins()

    def moitierDesGraine(self):
        # On va voir si un des joueurs possède plus de la moitier des graines dans son grenier
        for joueur in self.joueur:
            if joueur.getPoint() > self.graineMaxi//2:
                return True
        return False

    def tourChangeJoueur(self):
        # Permet de passer au tour du joueur suivant
        if self.tour == 0:
            self.tour = 1
        elif self.tour == 1:
            self.tour = 0

    def tourJoueur(self):
        # Retourn un chiffre : 0 ou 1 representant le rang du le joueur qui joue actuellement
        return self.tour

    def rangJoueurAdverse(self):
        # permet de connaitre le rang du joueur advairse
        if self.tourJoueur() == 0:
            return 1
        else:
            return 0
    
    def joueurCasesTousVide(self):
        # 0 Si tous les cases du joueur actuelle ou advairse sont vide 
        # n sinon
        vide1 = 0
        vide2 = 0
        for j in range(len(self.joueur)):
            for nb in self.cases[j]:
                if j == 0 and nb > 0:
                    vide1 += 1
                elif j == 1 and nb > 0:
                    vide2 += 1
        return vide1 == 0 or vide2 == 0
    
    # methode pour permettre de tout capturer
    def captureTous(self):
        self.capturer = True
        for j in range(len(self.joueur)):
            for rang in range(len(self.cases[j])):
                self.joueur[j].plus(self.cases[j][rang])
                self.cases[j][rang] = 0

    # Methode pour acceder à la case de l'adversaire
    def positionAdvairse(self, nb):
        if nb == 0:
            return 5
        elif nb == 1:
            return 4
        elif nb == 2:
            return 3
        elif nb == 3:
            return 2
        elif nb == 4:
            return  1
        elif nb == 5:
            return 0
        else:
            return -1

    # Methode pour l'affichage du plateau de jeu
    def plateau(self):
        print("")
        print()
        print(" "*20 + self.joueur[0].getName())
        print(" "*5+"    6  " +"    5   "+ "   4   "+ "   3   "+ "   2   "+ "   1   ")
        print("-------------------------------------------------------")
        print("|" + " GA " + " | " + f" {self.cases[0][5]:<2d} " + " | " + f" {self.cases[0][4]:<2d} " + " | " + f" {self.cases[0][3]:<2d} " + " | " + f" {self.cases[0][2]:<2d} " + " | " + f" {self.cases[0][1]:<2d} " + " | " + f" {self.cases[0][0]:<2d} " + " | " +  "    " + "| ")
        print("|" + f" {self.joueur[0].getPoint():<2d} " + " |-----------------------------------------|" + f" {self.joueur[1].getPoint():<2d}" + "  | ")
        print("|" + "    " + " | " + f" {self.cases[1][0]:<2d} " + " | " + f" {self.cases[1][1]:<2d} " + " | " + f" {self.cases[1][2]:<2d} " + " | " + f" {self.cases[1][3]:<2d} " + " | " + f" {self.cases[1][4]:<2d} " + " | " + f" {self.cases[1][5]:<2d} " + " | " +  "GB  " + "| ")
        print("-------------------------------------------------------")
        print(" "*5+"    1  " +"    2   "+ "   3   "+ "   4   "+ "   5   "+ "   6   ")
        print(" "*20 + self.joueur[1].getName())

    # Modification du plateau
    def modificationPlateau(self, indice):
        nombre = self.cases[self.tour][indice-1] # recupere les graines de la case selectionner
        indiceAdverse = 0 # Il va etre utiliser quand l'on voudra acceder au cases de l'adversaire (indice en fonction du develloppeur)
        position = indice # position suivante (indice en fonction du develloppeur)

        while nombre != 0:
            if position <= 5:
                # capture les graines advairse si la cases de destination est egale a zero, 0
                if (nombre == 1) and (self.cases[self.tour][position] == 0):
                    self.joueur[self.tour].plus(self.cases[self.rangJoueurAdverse()][self.positionAdvairse(position)])
                    self.joueur[self.tour].plus()

                    self.cases[self.rangJoueurAdverse()][self.positionAdvairse(position)] = 0
                    self.cases[self.tour][indice-1] -= 1

                    print(f"Le joueur {self.joueur[self.tourJoueur()].getName()} a capturer les graines de la case {self.positionAdvairse(position)+1}")
                    nombre -= 1
                    position += 1
                # navigation dans les cases du joueur
                else:
                    self.cases[self.tour][position] += 1 
                    self.cases[self.tour][indice-1] -= 1
                    nombre -= 1
                    position += 1
            # ajout de +1 graine dans le grenier, quand on encore n graine non distribuer et que nous somme à la fin de sa table 
            elif position == 6:
                self.joueur[self.tour].plus()
                self.cases[self.tour][indice-1] -= 1
                nombre -= 1
                position += 1
            else:
                # l'accès au case de l'adversaire
                self.cases[self.rangJoueurAdverse()][indiceAdverse] += 1
                self.cases[self.tour][indice-1] -= 1
                # position += 1
                indiceAdverse += 1 
                nombre -= 1
                if indiceAdverse == 6:
                    position = 0
                    indiceAdverse = 0