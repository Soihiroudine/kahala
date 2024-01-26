import json, os

class Sauver:
    """
    Classe qui va permettre de manipuler un fichier json
    - Creation de fichier json
    - Charger les donner du fichier json
    - Accès aux donner du fichier à partir de la cle
    - Verifier l'existance d'une cle
    - Supression du fichier
    - suppression de donner
    - modifier une donner  
    """
    def __init__(self, base = {}):
        self.donne = base

    def chargerFichier(self, fichier):
        """
        Chargement des données d'un fichier json
        """
        pass

    def creationFichier(self):
        """
        Permet la creation d'un fichier json
        """
        pass

    def sauvegardeDonne(self):
        """
        Sauvegarder les données dans un fichier json
        """
        pass

    def acceeDonne(self, cle):
        """
        Permet d'acceder à une donnée grâce à sa clé
        """
        pass

    def existanceCle(self, cle):
        """
        Vérifie qu'une cle existe
        """
        pass

    def baseDonne(self):
        """
        Donne le squellete de base des données
        """
        element = {
            "nomJoueur1": "",
            "nomJoueur2": "",
            "partieJouer": 0,
            "gainJoueur1": [],
            "gainJoueur2": []
        }
        return element



    