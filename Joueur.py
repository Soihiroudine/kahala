
class Joueur:
    '''
    Creation de classe joueur qui contient :
    le nom du joueur bien sure demander
    et les point qu'il possède (dans notre jeu l'attribue point est le grenier')
    '''
    
    def __init__(self, name=""):
        self.nom = name
        self.point = 0 # le grenier du joueur
        self.humain = False # definit c'est un ordinateur : False ou un humain : True

    def getName(self):
        return self.nom
    
    def getPoint(self):
        return self.point
    
    def getHumain(self):
        return self.humain
    
    def setHumain(self, a):
        self.humain = a

    def setName(self, nom):
        self.nom = nom
        
    def plus(self, graine = 1):
        self.point += graine

    def moins(self, graine = 0):
        self.point = graine

    def information(self):
        print(f"Le joueur {self.nom} a {self.point} graines.")