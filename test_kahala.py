import os
import tempfile
import unittest

from Joueur import Joueur
from plateau_de_jeu import Kahala
from sauvegarde import Sauver


class JoueurTests(unittest.TestCase):
    def test_plus_et_moins(self):
        joueur = Joueur("Ada", 5, True)
        joueur.plus(2)
        self.assertEqual(joueur.getPoint(), 7)
        joueur.moins(3)
        self.assertEqual(joueur.getPoint(), 4)

    def test_reset(self):
        joueur = Joueur("Ada", 5)
        joueur.reset_points()
        self.assertEqual(joueur.getPoint(), 0)


class KahalaTests(unittest.TestCase):
    def make_board(self):
        return Kahala(Joueur("A"), Joueur("B"), 0)

    def total_graines(self, board):
        return (
            sum(map(sum, board.cases))
            + board.joueur[0].getPoint()
            + board.joueur[1].getPoint()
        )

    def test_plateau_initial(self):
        board = self.make_board()
        self.assertEqual(board.cases, [[4] * 6, [4] * 6])
        self.assertEqual(self.total_graines(board), 48)

    def test_distribution_conserve_le_nombre(self):
        board = self.make_board()
        board.cases = [[12, 0, 0, 0, 0, 0], [6, 6, 6, 6, 6, 6]]
        board.modificationPlateau(1)
        self.assertEqual(self.total_graines(board), 48)

    def test_derniere_graine_dans_grenier_redonne_un_tour(self):
        board = self.make_board()
        board.cases = [[0, 0, 0, 0, 0, 1], [4, 4, 4, 4, 4, 4]]
        rejoue = board.modificationPlateau(6)
        self.assertTrue(rejoue)
        self.assertEqual(board.joueur[0].getPoint(), 1)

    def test_capture_seulement_si_case_adverse_pleine(self):
        board = self.make_board()
        board.cases = [[0, 1, 0, 0, 0, 0], [0, 0, 4, 0, 0, 0]]
        board.modificationPlateau(2)
        self.assertGreaterEqual(board.joueur[0].getPoint(), 0)

    def test_capture_tous_met_48_graines_dans_le_score(self):
        board = self.make_board()
        board.cases = [[4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4]]
        board.captureTous()
        self.assertEqual(sum(j.getPoint() for j in board.joueur), 48)
        self.assertTrue(board.joueurCasesTousVide())

    def test_initialisation_remet_scores_et_cases(self):
        board = self.make_board()
        board.joueur[0].plus(10)
        board.joueur[1].plus(12)
        board.initialisationCases()
        self.assertEqual(board.cases, [[4] * 6, [4] * 6])
        self.assertEqual([j.getPoint() for j in board.joueur], [0, 0])


class SauverTests(unittest.TestCase):
    def test_creation_chargement_suppression(self):
        with tempfile.TemporaryDirectory() as dossier:
            fichier = os.path.join(dossier, "save.json")
            sauvegarde = Sauver(fichier=fichier)
            sauvegarde.modifierDonne("nomJoueur1", "Ada")
            sauvegarde.sauvegardeDonne()
            self.assertTrue(os.path.exists(fichier))

            chargee = Sauver(fichier=fichier)
            self.assertTrue(chargee.chargerFichier())
            self.assertEqual(chargee.acceeDonne("nomJoueur1"), "Ada")
            self.assertTrue(chargee.existanceCle("nomJoueur1"))

            self.assertTrue(chargee.supprimerFichier())
            self.assertFalse(os.path.exists(fichier))


if __name__ == "__main__":
    unittest.main()
