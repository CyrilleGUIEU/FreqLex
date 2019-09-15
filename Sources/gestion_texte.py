from tkinter import Text,Tk,END,font
import pickle

from classes_lecteur import donnees_lecteur

 
class mot_fl():
    def __init__(self,mot_original,position):
        self.original=mot_original
        self.position=position
        self.minuscule=self.original.lower()
        self.longueur=len(self.original)

    def affiche(self):
        liste_affichage=[["Mot original:",self.original],["Position:",self.position],
                         ["Minuscule:",self.minuscule],["Longueur:",self.longueur],
                         ["Rangs:",self.rangs]]
        for c in liste_affichage:
            print(c[0],str(c[1]))

class ensemble_mots():
    def __init__(self,base_lexicale,dl=donnees_lecteur()):
        self.mfl=[]
        self.bl=base_lexicale
        fichier=open("Data/dict_archive.pickle","rb")
        self.dict_archive=pickle.load(fichier)
        fichier.close()
        self.dl=dl
            
    def efface_liste_mots(self):        
        #On efface la liste
        self.mfl=[]
    def taille_lexique(self,r):
        return len(self.lexiquep[r])
    def affiche_mfl(self):
        for x in self.mfl:
            x.affiche()
    
    def creer_liste_absents(self,r):
        """Etablit la liste des mots absents du lexique n° 'r'"""
        self.liste_absents=[]
        for x in self.mfl:
            if x.rangs[r]==None:
                self.liste_absents.append(x)

    def creer_liste_lexique(self,liste_poids,lecteur):
        """Renvoie la liste des mot par ordre décroissant de leur moyenne d'apparition"""
               
        liste_moyennes=[]
        dict_moyennes={}
        dict_lexique={}

        for x in self.mfl:
            x.n=lecteur.n
            freq=x.freq
            freq_ponderee=0
            k=0
            for f in freq:
                freq_ponderee=freq_ponderee+f*liste_poids[k]
                k=k+1
            if freq_ponderee!=0:
                valeur_moyenne=freq_ponderee*lecteur.n/10**6
                x.valeur_moyenne=valeur_moyenne
                if  valeur_moyenne in liste_moyennes:
                    dict_lexique[valeur_moyenne].append(x)
                else:
                    liste_moyennes.append(valeur_moyenne)
                    dict_lexique[valeur_moyenne]=[x]
                    dict_moyennes[x]=valeur_moyenne
        liste_moyennes.sort()
        self.liste_lexique=[]
        for k in liste_moyennes:
            for x in dict_lexique[k]:
                self.liste_lexique.append(x)
        self.dict_moyennes=dict_moyennes
            
    
    def ajoute(self,mot):
        if mot.minuscule in self.dict_archive.keys():
            mot.freq=self.dict_archive[mot.minuscule]
        else:
            mot.freq=self.bl.liste_freq2forme(mot.minuscule)
            self.dict_archive[mot.minuscule]=mot.freq
        self.mfl.append(mot)
    def ajoute_mots_fenetre(self,zone_texte,liste_lexique):
        """Ajoute les mots du texte de la zone de texte 'zone_texte' à l'ensemble"""
        position="0.0"
        position_suivante="1.0"
        position_debut_mot="1.0"
        mot_actuel=""
        mot_precedent=""
        mot_liaison=""
        #Ces caractères sont des caractères de liaison possibles
        exceptions=["'","-","’"]
        #Table de conversion pour les symboles ayants plusieurs formes
        conversion={"’":"'"}
        
        t=zone_texte
        #Cette boucle scanne le texte lettre par lettre
        while position_suivante!=position:
            position=position_suivante
            position_suivante=t.index(position+"+1 chars")
            lettre=t.get(position)
            if lettre in conversion:
                lettre=conversion[lettre]
            if lettre.isalpha():
                mot_actuel=mot_actuel+lettre
            else:
                if lettre in exceptions:
                    if mot_actuel!="" and mot_actuel[0].isalpha():
                        #self.ajoute(mot_fl(mot_actuel,position_debut_mot))
                        mot_precedent=mot_actuel
                        position_debut_mot_precedent=position_debut_mot
                        mot_liaison=lettre
                else:
                    if mot_actuel!="" and mot_actuel[0].isalpha():
                        if mot_liaison=="":
                            self.ajoute(mot_fl(mot_actuel,position_debut_mot))
                        else:
                            mot_compose=mot_precedent+mot_liaison+mot_actuel
                            if liste_lexique.liste_freq2forme(mot_compose)!=[0 for k in self.bl.bddl_brute]:
                                self.ajoute(mot_fl(mot_compose,position_debut_mot_precedent))
                            else:
                                self.ajoute(mot_fl(mot_precedent,position_debut_mot_precedent))
                                self.ajoute(mot_fl(mot_actuel,position_debut_mot))
                            mot_liaison=""                            
                mot_precedent=mot_actuel
                position_debut_mot_precedent=position_debut_mot
                mot_actuel=""
            if mot_actuel=="":
                position_debut_mot=position_suivante
            

        
        
        
if __name__=="__main__":
    from time import time
    import pickle
    from base_lexique import NCP,FICHIER_SAUVEGARDE,rang_mot
    #Récupération des données
    with open ("../"+FICHIER_SAUVEGARDE, 'rb') as fp:
        #La variable "lexique" est la liste des graphème ordonnée par fréquence décroissante
        lexiquep = pickle.load(fp)

    blabla="""Longtemps ignorées, confinées dans un anonymat, au mieux poli mais le plus souvent méprisant, les Bleues s’apprêtent à disputer leur première vraie compétition sous la lumière des projecteurs. ­Demi-finaliste surprise en 2011 et quart de finaliste méritante en 2015, l’équipe de France féminine n’a depuis cessé de croître jusqu’à rattraper son retard sur les nations historiques, en particulier les multiples championnes du monde américaines (1991, 1999 et 2015) et allemandes (2003 et 2007).

Si vite et si fort que les joueuses de la sélectionneuse Corinne Diacre doivent désormais assumer, vendredi 7 juin, le jour du match d’ouverture de la Coupe du monde féminine au Parc des Princes, un statut inédit de favorites, renforcé par le fait d’évoluer à domicile.

Depuis deux ans, les footballeuses françaises, au quatrième rang du classement FIFA, ont en effet battu au moins une fois toutes les meilleures équipes : des Etats-Unis à l’Allemagne, en passant par le Japon, le Canada ou encore l’Angleterre… Elles viennent même d’enchaîner treize victoires lors de leurs quatorze dernières rencontres.
Lire aussi Coupe du monde féminine 2019 : les Bleues concluent leur préparation par un succès

La désillusion d’un Euro 2017 décevant, achevé une nouvelle fois en quarts de finale pour la quatrième fois consécutive lors d’un grand tournoi, paraît loin. Nommée un mois après l’élimination sans gloire des Françaises face aux Anglaises, Corinne Diacre s’est montrée patiente, menant d’abord une large revue d’effectif avant de fixer son groupe, parfois au prix de choix forts, comme la non-sélection de la meilleure buteuse de Division 1, la jeune Parisienne Marie-Antoinette Katoto."""
    fenetre=Tk()
    t=Text(fenetre)
    t.pack()
    t.insert(END,blabla)
    #colore_mot(t,"consécutive","#649a00")
    m=mot_fl("test","1.1")
    ens_mots=ensemble_mots(lexiquep)
    print(str(time()))
    ens_mots.ajoute_mots_fenetre(t,lexiquep[0])
    print(str(time()))
    ens_mots.efface_liste_mots()
    print(str(time()))
    ens_mots.ajoute_mots_fenetre(t,lexiquep[0])
    print(str(time()))
    #ens_mot.creer_dict_longueurs()
    #ens_mot.affiche_dict_longueurs()
    ens_mots.creer_liste_absents(0)
    print(ens_mots.liste_absents)
    ens_mot.creer_liste_lexique(0)
    l=ens_mots.liste_lexique
    for x in l:
        print(x.original)
    #ens_mot.affiche()
