class Joueur:
    """Représente un joueur et son grenier."""

    def __init__(self, name: str = "", point: int = 0, humain: bool = False) -> None:
        self.nom = name
        self.point = max(0, point)
        self.humain = humain

    @property
    def name(self) -> str:
        return self.nom

    @property
    def score(self) -> int:
        return self.point

    @property
    def is_human(self) -> bool:
        return self.humain

    def getName(self) -> str:
        return self.name

    def getPoint(self) -> int:
        return self.score

    def getHumain(self) -> bool:
        return self.is_human

    def setHumain(self, humain: bool) -> None:
        self.humain = bool(humain)

    def setName(self, nom: str) -> None:
        if not isinstance(nom, str):
            raise TypeError("Le nom doit être une chaîne de caractères.")
        self.nom = nom.strip()

    def plus(self, graine: int = 1) -> None:
        if graine < 0:
            raise ValueError("La quantité doit être positive.")
        self.point += graine

    def moins(self, graine: int = 0) -> None:
        """Compatibilité avec l'ancienne API. Un argument positif soustrait."""
        if graine > self.point:
            graine = self.point
        self.point -= graine

    def reset_points(self) -> None:
        self.point = 0

    def information(self) -> None:
        print(f"Le joueur {self.nom} a {self.point} graines.")