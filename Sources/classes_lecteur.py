
class donnees_lecteur:
    def __init__(self,age=11):
        self.nbre_mots_inf=59000
        self.nbre_mots_median=883000
        self.nbre_mots_sup=4200000
        self.dict_profils={"10% des enfants de 11 ans qui lisent le moins":self.nbre_mots_inf,
                     "Lecteur médian âgé de 11 ans":self.nbre_mots_median,
                     "10% des enfants de 11 ans qui lisent le plus":self.nbre_mots_sup}
        self.profils=list(self.dict_profils.keys())
        self.actualise_profil(self.profils[-1]) #choix par défaut
        self.nb_profils=len(self.profils)
        
    def actualise_profil(self,p):
        self.profil_actuel=p
        self.n=self.dict_profils[p]

    def interprete_couleur_rare(self):
        return """Pour le profil d'élève '{}', il y a une probabilité supérieure à 99% que l'élève n'ai pas rencontré un mot de cette couleur au cours de l'année écoulée.""".format(self.profil_actuel)
    def interprete_couleur_fréquente(self):
        return """Pour le profil d'élève '{}', il y a une probabilité supérieure à 99% que l'élève ai rencontré ce mot au cours de l'année écoulée.""".format(self.profil_actuel)
    
    def interprete_moyenne(self,mot,moyenne):
        return """Un élève du profil '{}' a rencontré ce mot en moyenne {} fois au cours de l'année écoulée.""".format(self.profil_actuel,mot,moyenne)


if __name__=="___main___":
    pass
