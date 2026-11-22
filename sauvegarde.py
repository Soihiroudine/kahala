import json
import os


class Sauver:
    """Lecture et écriture d'une sauvegarde JSON."""

    def __init__(self, base=None, fichier="kahala.json"):
        self.donne = self.baseDonne() if base is None else dict(base)
        self.fichier = fichier

    def chargerFichier(self, fichier=None):
        chemin = fichier or self.fichier
        if not os.path.exists(chemin):
            return False
        try:
            with open(chemin, "r", encoding="utf-8") as flux:
                donnees = json.load(flux)
        except (OSError, json.JSONDecodeError):
            return False
        if not isinstance(donnees, dict):
            return False
        self.donne = donnees
        self.fichier = chemin
        return True

    def creationFichier(self, fichier=None):
        chemin = fichier or self.fichier
        dossier = os.path.dirname(os.path.abspath(chemin))
        os.makedirs(dossier, exist_ok=True)
        with open(chemin, "w", encoding="utf-8") as flux:
            json.dump(self.donne, flux, ensure_ascii=False, indent=2)
        self.fichier = chemin

    def sauvegardeDonne(self, fichier=None):
        self.creationFichier(fichier)

    def acceeDonne(self, cle, defaut=None):
        return self.donne.get(cle, defaut)

    def existanceCle(self, cle):
        return cle in self.donne

    def modifierDonne(self, cle, valeur):
        self.donne[cle] = valeur

    def supprimerCle(self, cle):
        return self.donne.pop(cle, None)

    def supprimerFichier(self, fichier=None):
        chemin = fichier or self.fichier
        if os.path.exists(chemin):
            os.remove(chemin)
            return True
        return False

    def baseDonne(self):
        return {
            "nomJoueur1": "",
            "nomJoueur2": "",
            "partieJouer": 0,
            "gainJoueur1": [],
            "gainJoueur2": [],
            "plateau": [[], []],
            "sauvegardeAuto": True,
        }
    