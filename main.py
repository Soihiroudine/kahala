import gestion_du_jeu
from datetime import datetime

def start():
    maintenant = datetime.now()

    if maintenant.hour >= 5 and maintenant.hour <= 18:
        jeu = gestion_du_jeu.Jeu()
        jeu.start()
    else:
        print("Il n'est pas le temps de jouer !!! :( ")
        _ = input("sortie (clicker sur un button)")

if __name__ == "__main__":
    start()
