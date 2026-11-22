
class Kahala:
    """Plateau de jeu à deux rangées de six cases."""

    def __init__(self, joueur1, joueur2, tour: int) -> None:
        self.graineMaxi = 48
        self.cases = [[4] * 6, [4] * 6]
        self.joueur = [joueur1, joueur2]
        self.tour = tour
        self.capturer = False

    def initialisationCases(self) -> None:
        self.cases = [[4] * 6, [4] * 6]
        for joueur in self.joueur:
            joueur.reset_points()
        self.capturer = False

    def moitierDesGraine(self) -> bool:
        return any(joueur.getPoint() > self.graineMaxi // 2 for joueur in self.joueur)

    def tourChangeJoueur(self) -> None:
        self.tour = 1 - self.tour

    def tourJoueur(self) -> int:
        return self.tour

    def rangJoueurAdverse(self) -> int:
        return 1 - self.tour

    def joueurCasesTousVide(self) -> bool:
        return any(all(case == 0 for case in ligne) for ligne in self.cases)

    def captureTous(self) -> None:
        self.capturer = True
        for rang, ligne in enumerate(self.cases):
            reste = sum(ligne)
            self.joueur[rang].plus(reste)
            self.cases[rang] = [0] * 6

    def positionAdvairse(self, nb: int, m: int = 5) -> int:
        if not 0 <= nb <= 5:
            raise IndexError("La position doit être comprise entre 0 et 5.")
        return 5 - nb

    def plateau(self) -> None:
        print("")
        print()
        print(" " * 20 + self.joueur[0].getName())
        print(" " * 5 + "    6  " + "    5   " + "   4   " + "   3   " + "   2   " + "   1   ")
        print("-------------------------------------------------------")
        print("|" + " GA " + " | " + f" {self.cases[0][5]:<2d} " + " | " + f" {self.cases[0][4]:<2d} " + " | " + f" {self.cases[0][3]:<2d} " + " | " + f" {self.cases[0][2]:<2d} " + " | " + f" {self.cases[0][1]:<2d} " + " | " + f" {self.cases[0][0]:<2d} " + " | " + "    " + "| ")
        print("|" + f" {self.joueur[0].getPoint():<2d} " + " |-----------------------------------------|" + f" {self.joueur[1].getPoint():<2d}" + "  | ")
        print("|" + "    " + " | " + f" {self.cases[1][0]:<2d} " + " | " + f" {self.cases[1][1]:<2d} " + " | " + f" {self.cases[1][2]:<2d} " + " | " + f" {self.cases[1][3]:<2d} " + " | " + f" {self.cases[1][4]:<2d} " + " | " + f" {self.cases[1][5]:<2d} " + " | " + "GB  " + "| ")
        print("-------------------------------------------------------")
        print(" " * 5 + "    1  " + "    2   " + "   3   " + "   4   " + "   5   " + "   6   ")
        print(" " * 20 + self.joueur[1].getName())

    def modificationPlateau(self, indice: int) -> bool:
        """Distribue les graines et retourne True si le joueur rejoue."""
        if not 1 <= indice <= 6:
            raise ValueError("L'indice doit être compris entre 1 et 6.")

        row = self.tour
        pit = indice - 1
        nombre = self.cases[row][pit]
        if nombre <= 0:
            raise ValueError("La case choisie est vide.")

        self.cases[row][pit] = 0
        last_store = False
        last_row = row
        last_pit = pit

        while nombre > 0:
            if row == 0:
                if pit < 5:
                    pit += 1
                else:
                    self.joueur[0].plus()
                    last_row = 0
                    last_pit = -1
                    last_store = True
                    row = 1
                    pit = 0
                    nombre -= 1
                    if nombre == 0:
                        break
                    continue
            else:
                if pit < 5:
                    pit += 1
                else:
                    self.joueur[1].plus()
                    last_row = 1
                    last_pit = -1
                    last_store = True
                    row = 0
                    pit = 5
                    nombre -= 1
                    if nombre == 0:
                        break
                    continue

            self.cases[row][pit] += 1
            last_row = row
            last_pit = pit
            last_store = False
            nombre -= 1

        # Si la graine se termine dans un grenier, le joueur rejoue.
        rejoue = last_store

        # Une capture exige une case propre à soi, contenant 1 graine,
        # et une case adverse contenant au moins une graine.
        if not rejoue and last_row == self.tour and 0 <= last_pit <= 5:
            if self.cases[last_row][last_pit] == 1:
                opposite = self.cases[1 - last_row][5 - last_pit]
                if opposite > 0:
                    gain = opposite + 1
                    self.cases[last_row][last_pit] = 0
                    self.cases[1 - last_row][5 - last_pit] = 0
                    self.joueur[last_row].plus(gain)
                    print(
                        f"Le joueur {self.joueur[last_row].getName()} "
                        f"a capturé {gain} graines."
                    )

        return rejoue