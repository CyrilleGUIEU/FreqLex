"""Interface graphique pour une étude d'énoncé à l'aide d'un lexique fréquentiel
"""


# On importe Tkinter pour construire l'interface graphique
from tkinter import Label,Scale,DISABLED,font,Tk,END,LabelFrame,Button,GROOVE,VERTICAL,WORD,S,N,Frame,Scrollbar,Text,Listbox
#Le module pickle sert à importer les données
import pickle

#Ces modules sont des modules du projet freqlex
from gui_freqlex import liste_mots,fenetre_freqlex,LARGEUR_CADRE_ENONCE,LARGEUR_LISTE_MOTS,cadre_cp
from licence_freqlex import Licence,cree_cadre_credits,FICHIER_LICENCE
from gestion_texte import ensemble_mots
from gestion_couleurs import colore_mots,convertit_indice_couleur,COULEUR_ABSENT
from classes_lecteur import donnees_lecteur


class GUI():
    def __init__(self):
        print("Démarrage de l'interface graphique...")
        #Récupération des données
        fichier=open("Data/base_lexicale.pickle","rb")
        self.base_lexicale=pickle.load(fichier)
        fenetre=fenetre_freqlex()
        #Cet objet contient l'énoncé enrichi par l'analyse lexicale
        self.enonce=ensemble_mots(self.base_lexicale)

        self.lecteur=donnees_lecteur()
        #On crée les  polices
        police_mots=font.Font(fenetre, size=16, family='Courier')
        police_enonce=font.Font(fenetre, size=12, family='Courier')  
        #Definition de l'interface graphique
        #Ce cadre contient le texte à analyser
        cadre_enonce = LabelFrame(fenetre, borderwidth=2,
                                relief=GROOVE,text="Enoncé")
        asc_enonce=Scrollbar(cadre_enonce,orient=VERTICAL)
        #L'attribut texte_enonce est utilisé par la méthode recupere_texte
        self.texte_enonce = Text(cadre_enonce, wrap=WORD,font=police_enonce,width=LARGEUR_CADRE_ENONCE)
        self.texte_enonce.bind("<Key>", self.ecoute_clavier)
        self.texte_enonce.insert(END,"Dans ce cadre, collez n'importe quel texte pour en obtenir une analyse lexicale.")
        
        ## association du déplacement de la glissière des scrollbar avec la position visible dans  
        ## le widget Text et inversement.  
        asc_enonce.config(command = self.texte_enonce.yview) 
        self.texte_enonce.config(yscrollcommand = asc_enonce.set)
        ## Placement du widget Text et des Scrollbar associés 
        self.texte_enonce.grid(column=0, row=0) 
        asc_enonce.grid(column=1, row=0, sticky=S+N)
        
        #Ce cadre contient le choix du profil de lecteur
        cadre_lecteur = LabelFrame(fenetre,text="Profil de lecteur",height=1, borderwidth=2,
                                relief=GROOVE)
        bouton_profil_precedent = Button(cadre_lecteur,text="<",command=self.profil_precedent)
        bouton_profil_precedent.grid(column=0,row=0)
        self.affichage_profil_actuel = Text(cadre_lecteur,height=1,width=LARGEUR_LISTE_MOTS)
        self.affichage_profil_actuel.insert(END,self.lecteur.profil_actuel)
        self.affichage_profil_actuel.grid(column=1,row=0)
        bouton_profil_suivant = Button(cadre_lecteur,text=">",command=self.profil_suivant)
        bouton_profil_suivant.grid(column=2,row=0)
        

        #Le cadre de comparaison des deux mots
        self.cadre_compare=LabelFrame(fenetre, borderwidth=2,
                                relief=GROOVE,text="Comparaison de deux mots")
        self.cadre_compare.parent=self
        self.compare=cadre_cp(self.cadre_compare,self.base_lexicale,self.lecteur)

        #Ce cadre contient les mots du lexique classés
        self.zone_mots_lexique=liste_mots(fenetre,"Classement par difficulté lexicale:",self.compare)
        self.zone_mots_lexique.parent=self
        #Ce cadre contient les mots absents des lexiques
        self.zone_mots_absents = liste_mots(fenetre,"Mots absents des bases",self.compare)
        self.zone_mots_absents.mots.configure(height=3)
        #Ce cadre contiendra des explications sur les objets de la fenêtre
        largeur_infos=LARGEUR_CADRE_ENONCE+LARGEUR_LISTE_MOTS
        cadre_infos = LabelFrame(fenetre,text="Infos",height=2, borderwidth=2,
                                relief=GROOVE)
        self.infos = Text(cadre_infos,bg="grey",height=3,width=largeur_infos)
        self.infos.insert(END,"Survolez les noms des bases de données pour obtenir des explications, clqiuez sur les mots de la liste pour obtenir des détails.")
        self.infos.grid(column=0,row=0)
        #Ce cadre contient le texte des crédits
        cadre_credits = cree_cadre_credits(fenetre)

        #On place les cadres de premier niveau
        cadre_lecteur.grid(column=1,row=0)
        self.zone_mots_lexique.cadre.grid(column=1,row=1)
        self.cadre_compare.grid(column=1,row=2)
        self.zone_mots_absents.cadre.grid(column=1,row=3)
        cadre_enonce.grid(column=0,row=0,rowspan=3)
        cadre_credits.grid(column=0,row=3)
        cadre_infos.grid(column=0,row=4,columnspan=2)

        
        self.fenetre=fenetre
        self.analyse()
        # On démarre la boucle Tkinter qui s'interrompt quand on ferme la fenêtre
        fenetre.mainloop()
        
    def actualise_profil(self,p):
        self.lecteur.actualise_profil(p)
        self.affichage_profil_actuel.delete("0.0",END)
        self.affichage_profil_actuel.insert(END,self.lecteur.profil_actuel)
        self.analyse()
    def profil_precedent(self):
        i=self.lecteur.profils.index(self.lecteur.profil_actuel)
        i=(i-1)%self.lecteur.nb_profils
        self.actualise_profil(self.lecteur.profils[i])
    def profil_suivant(self):
        i=self.lecteur.profils.index(self.lecteur.profil_actuel)
        i=(i+1)%self.lecteur.nb_profils
        self.actualise_profil(self.lecteur.profils[i])
    #Fonction qui gère le traitement de l'énoncé
    def affiche_mots_absents(self):
        #On efface l'affichage des mots absents
        self.zone_mots_absents.mots.delete(0,END)
        #On génère la liste des mots absents du lexique
        mots_absents=[]
        for k in self.enonce.mfl:
            if k.freq==[0 for k in self.base_lexicale.bddl_brute]:
                mots_absents.append(k)
        self.mots_absents=mots_absents
        self.enonce.mots_absents=mots_absents
        #On insère les mots absents dans la zone des mots absents
        mots_affiches=[] #Ce tableau évite d'afficher les doublons
        for mot in self.mots_absents:
            if mot.minuscule not in mots_affiches:
                self.zone_mots_absents.ajoute_mot_couleur(mot.original,COULEUR_ABSENT)
                mots_affiches.append(mot.minuscule)
    def affiche_mots_lexique(self):
        #On efface l'affichage des mots du lexique
        self.zone_mots_lexique.mots.delete(0,END)
        #On génère la liste des mots du lexique
        self.enonce.creer_liste_lexique(self.compare.donne_liste_poids(),self.lecteur)
        #On insère les mots du lexique dans la zone des mots du lexique
        mots_affiches=[] #Ce tableau évite d'afficher les doublons
        self.dict_moyennes={}
        for mot in self.enonce.liste_lexique:
            if mot.minuscule not in mots_affiches:
                valeur=self.enonce.dict_moyennes[mot]
                chaine=mot.original+"->"+str(valeur)
                couleur=convertit_indice_couleur(self.enonce,mot)
                self.zone_mots_lexique.ajoute_mot_couleur(chaine,couleur)
                mots_affiches.append(mot.minuscule)
                self.dict_moyennes[mot.minuscule]=valeur
        self.zone_mots_lexique.liste_mots=mots_affiches
                
    
    
        
    def ecoute_clavier(self,event):
        touche = event.keysym
        if touche=="Return":
            self.analyse()
            
        
    def analyse(self):
        texte_initial=self.infos.get("1.0",END)
        self.infos.delete("0.0",END)
        self.infos.insert(END,"Calcul en cours, merci de patienter....")
        self.fenetre.update()
        #On efface les éventuelles données
        self.enonce.efface_liste_mots()
        #Extraction du texte à partir du cadre
        self.enonce.ajoute_mots_fenetre(self.texte_enonce,self.base_lexicale)
        #Actualisation de l'affcihage des mots absents
        self.affiche_mots_absents()
        self.affiche_mots_lexique()
        #Coloration des mots de la zone d'énoncé
        colore_mots(self.texte_enonce,self.enonce,self.base_lexicale,self.compare.donne_liste_poids(),self.lecteur)
        self.infos.delete("0.0",END)
        self.infos.insert(END,texte_initial)
                
             
            

if __name__=="__main__":
    GUI()
else:
    fichier_ouvert=False
    try:
        open(FICHIER_LICENCE,"r")
        #Lancement de l'application
        fichier_ouvert=True
        GUI()
    except FileNotFoundError:
        #Fenêtre d'acceptation de la licence
        if fichier_ouvert==False:
            Licence(GUI)

