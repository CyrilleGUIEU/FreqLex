from tkinter import Text,Tk,END,font
from math import sqrt

COULEUR_ABSENT="blue"
COULEUR_FREQUENT=(0,255,0)
COULEUR_RARE=(255,0,0)

def convertit_indice_couleur(enonce,mot):
    couleur=[]
    m=mot.valeur_moyenne
    sigma=sqrt(m)
    if m>1+3*sigma:
        indf=1
    elif m<1-3*sigma:
        indf=0
    else:
        indf=(m+3*sigma-1)/(6*sigma)
    for j in range(3):
        couleur.append(indf*COULEUR_FREQUENT[j]+(1-indf)*COULEUR_RARE[j])
    c="#"
    for x in couleur:
        s=str(hex(int(x)))[2:]
        if len(s)==1:
            s="0"+s
        c=c+s
    return c

def colore_mots(zone_texte,enonce,base_lexique,liste_poids,lecteur):
    #Coloration des mots
    for m in enonce.mots_absents:
        position=m.position
        position_suivante=zone_texte.index(position+"+"+str(m.longueur)+" chars")
        zone_texte.tag_add(m.original,position,position_suivante)
        zone_texte.tag_config(m.original, foreground=COULEUR_ABSENT)
    for m in enonce.liste_lexique:
        couleur=convertit_indice_couleur(enonce,m)
        zone_texte.tag_config(m.original, foreground=couleur)
        position=m.position
        position_suivante=zone_texte.index(position+"+"+str(m.longueur)+" chars")
        zone_texte.tag_add(m.original,position,position_suivante)

if __name__=="__main__":
    from time import time
    import pickle

    from gestion_texte import ensemble_mots
    from base_lexique import NCP,FICHIER_SAUVEGARDE,rang_mot
    #Récupération des données
    with open ("../"+FICHIER_SAUVEGARDE, 'rb') as fp:
        #La variable "lexique" est la liste des graphème ordonnée par fréquence décroissante
        lexiquep = pickle.load(fp)

    blabla="""Longtemps ignorées, confinées dans un anonymat, au mieux poli mais le plus souvent méprisant, les Bleues s’apprêtent à disputer leur première vraie compétition sous la lumière des projecteurs. ­Demi-finaliste surprise en 2011 et quart de finaliste méritante en 2015, l’équipe de France féminine n’a depuis cessé de croître jusqu’à rattraper son retard sur les nations historiques, en particulier les multiples championnes du monde américaines (1991, 1999 et 2015) et allemandes (2003 et 2007).

Si vite et si fort que les joueuses de la sélectionneuse Corinne Diacre doivent désormais assumer, vendredi 7 juin, le jour du match d’ouverture de la Coupe du monde féminine au Parc des Princes, un statut inédit de favorites, renforcé par le fait d’évoluer à domicile.

Depuis deux ans, les footballeuses françaises, au quatrième rang du classement FIFA, ont en effet battu au moins une fois toutes les meilleures équipes : des Etats-Unis à l’Allemagne, en passant par le Japon, le Canada ou encore l’Angleterre… Elles viennent même d’enchaîner treize victoires lors de leurs quatorze dernières rencontres.
Lire aussi Coupe du monde féminine 2019 : les Bleues concluent leur préparation par un succès

La désillusion d’un Euro 2017 décevant, achevé une nouvelle fois en quarts de finale pour la quatrième fois consécutive lors d’un grand tournoi, paraît loin. Nommée un mois après l’élimination sans gloire des Françaises face aux Anglaises, Corinne Diacre s’est montrée patiente, menant d’abord une large revue d’effectif avant de fixer son groupe, parfois au prix de choix forts, comme la non-sélection de la meilleure buteuse de Division 1, la jeune Parisienne Marie-Antoinette Katoto. """
    fenetre=Tk()
    t=Text(fenetre)
    t.pack()
    t.insert(END,blabla)
    
    ens_mot=ensemble_mots(lexiquep)
    print(str(time()))
    ens_mot.ajoute_mots_fenetre(t)
    print(str(time()))
    #ens_mot.creer_dict_longueurs()
    #ens_mot.affiche_dict_longueurs()
##    ens_mot.creer_liste_absents(0)
##    print(ens_mot.absents)
##    ens_mot.creer_liste_lexique(0)
##    l=ens_mot.liste_lexique
##    for x in l:
##        print(x.original)
    #ens_mot.affiche()
    ens_mot.creer_liste_absents(0)
    ens_mot.creer_liste_lexique(0)
    colore_mots(t,0,ens_mot)
    for m in ens_mot.liste_lexique:
        print(m.original,m.position)


