from tkinter import font,LabelFrame,Scrollbar,Listbox,Tk,GROOVE,VERTICAL,S,N 

#Paramètres de l'interface graphique
LARGEUR_CADRE_ENONCE=50
LARGEUR_LISTE_MOTS=25

class liste_mots:
    """Définit un cadre contenant une liste de mot avec un ascenseur"""
    def __init__(self,parent,titre):
        police_mots=font.Font(parent, size=12, family='Courier')
        self.cadre = LabelFrame(parent, borderwidth=2,
                                relief=GROOVE,text=titre)
        self.ascenseur=Scrollbar(self.cadre,orient=VERTICAL)
        self.mots=Listbox(self.cadre, font=police_mots, width=LARGEUR_LISTE_MOTS,yscrollcommand = self.ascenseur.set )
        self.mots.grid(column=0,row=0)
        self.ascenseur.grid(column=1,row=0,sticky=S+N)
        self.ascenseur.config( command = self.mots.yview )
    def ajoute_mot_couleur(self,mot,couleur):
        fin=self.mots.size()
        self.mots.insert(fin,mot)
        self.mots.itemconfig(fin,fg=couleur)

def fenetre_freqlex(test=False):
    fenetre=Tk()
    fenetre.title('FreqLex')
    if test:
        fenetre.wm_iconbitmap('../DATA/icon.ico')
    else:
        fenetre.wm_iconbitmap('DATA/icon.ico')
    return(fenetre)

if __name__=="__main__":
    f=fenetre_freqlex(test=True)
    l=liste_mots(f,"Test")
    l.mots.insert(0,"test1")
    l.mots.insert(1,"test2")
    l.cadre.pack()
    l.ajoute_mot_couleur("t4","red")
    l.ajoute_mot_couleur("t5","blue")
    l.mots.select_set(0,0)
    
