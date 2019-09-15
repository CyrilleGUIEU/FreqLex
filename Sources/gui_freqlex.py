from tkinter import font,LabelFrame,Scrollbar,Listbox,Tk,GROOVE,VERTICAL,S,N,Label,Scale,Entry,END
#from prepaBases.bdd_freqlex import base_freqlex
#from prepaBases.classes_bddl import bddl
from classes_bdfl import base_freqlex
from classes_lecteur import donnees_lecteur

#Paramètres de l'interface graphique
LARGEUR_CADRE_ENONCE=50
LARGEUR_LISTE_MOTS=50
NB_DECIMALES=2

class liste_mots:
    """Définit un cadre contenant une liste de mot avec un ascenseur"""
    def __init__(self,parent,titre,compare):
        police_mots=font.Font(parent, size=12, family='Courier')
        self.cadre = LabelFrame(parent, borderwidth=2,
                                relief=GROOVE,text=titre)
        self.ascenseur=Scrollbar(self.cadre,orient=VERTICAL)
        self.mots=Listbox(self.cadre, font=police_mots, width=LARGEUR_LISTE_MOTS,yscrollcommand = self.ascenseur.set )
        self.mots.bind('<<ListboxSelect>>', self.selection)
        self.mots.grid(column=0,row=0)
        self.ascenseur.grid(column=1,row=0,sticky=S+N)
        self.ascenseur.config( command = self.mots.yview )
        self.liste_mots=[]
        self.compare=compare
    def ajoute_mot_couleur(self,mot,couleur):
        fin=self.mots.size()
        self.mots.insert(fin,mot)
        self.mots.itemconfig(fin,fg=couleur)
        self.liste_mots.append(mot)
    def selection(self,e):
        mot=self.liste_mots[self.mots.curselection()[0]]
        self.compare.modifie_mot1(mot)
        self.parent.infos.delete("0.0",END)
        valeur=self.parent.dict_moyennes[mot]
        texte="Selon ce modèle, le mot '"+mot+"' a été lu en moyenne "+str(round(valeur,NB_DECIMALES))+ "fois par un élève de ce profil au cours de l'année écoulée."
        self.parent.infos.insert(END,texte)
        
        
    



class cadre_cp:
    """Définit une zone de comparaison des fréquences
et de contrôle des poids"""

    def __init__(self,parent,base_fl,lecteur):
        self.police_titre=('Times', -20, 'bold')
        self.police_nombre=('Arial', -20, 'bold')
        self.parent=parent
        self.bfl=base_fl
        self.lecteur=lecteur
        self.mot1=""
        self.mot2=""
        self.titre_colonne1=Label(parent,text="Base de données",font=self.police_titre)
        self.titre_colonne1.grid(column=0,row=0)
        self.titre_colonne2=Entry(parent,width=15,font=self.police_titre)
        self.titre_colonne2.grid(column=1,row=0)
        self.titre_colonne2.insert(END,self.mot1)
        self.titre_colonne3=Entry(parent,width=15,font=self.police_titre)
        self.titre_colonne3.grid(column=2,row=0)
        self.titre_colonne3.insert(END,self.mot2)
        self.titre_colonne3.bind("<Return>",self.actualise_mot2)
        self.titre_colonne4=Label(parent,text="Poids de chaque base",font=self.police_titre)
        self.titre_colonne4.grid(column=3,row=0)
        self.titre_ligne=[]
        for k in range(self.bfl.n_base):
            tl=Label(parent,font=self.police_titre,text=self.bfl.bddl_brute[k].nom)
            tl.grid(column=0,row=k+1)
            tl.bind("<Enter>", lambda event, obj=self.bfl.bddl_brute[k]: self.actualise_info(event, obj))
            self.titre_ligne.append(tl)
        self.titre_derniere_ligne=Label(parent,font=self.police_titre,text="Cumul:")
        self.titre_derniere_ligne.grid(column=0,row=k+2)
        self.curseur=[]
        def enter(event,c):
            c.active=True
        def leave(event,c):
            c.active=False
        for k in range(self.bfl.n_base):
            c=Scale(parent, orient='horizontal', resolution=1/10**NB_DECIMALES,from_=0, to=1,
                    command=self.actualise_cumul)
            c.grid(column=3,row=k+1)
            #Remettre cette ligne pour une répartition équitable des lectures
            #c.set(1.0/self.bfl.n_base)
            #A CHANGER: valeurs initales des poids de chaque base
            dict_params={"Blog":0.21,"Twitter":0.21,"Journaux":0.04,"Livres":0.12,"Films":0.42}
            c.set(dict_params[self.bfl.bddl_brute[k].nom])
            c.val_mem=c.get()
            c.active=False
            c.bind("<Enter>", lambda event, obj=c: enter(event, obj))
            c.bind("<Leave>", lambda event, obj=c: leave(event, obj))
            self.curseur.append(c)
        self.cumul=Label(parent,font=self.police_nombre)
        self.cumul.grid(column=3,row=k+2)

        self.freqp1=Label(parent,font=self.police_nombre)
        self.freqp1.grid(column=1,row=k+2)

        self.freqp2=Label(parent,font=self.police_nombre)
        self.freqp2.grid(column=2,row=k+2)

        
        self.freq1=[]
        for k in range(self.bfl.n_base):
            f=Label(parent,font=self.police_nombre,text="#")
            f.grid(column=1,row=k+1)
            self.freq1.append(f)
            
        self.freq2=[]
        for k in range(self.bfl.n_base):
            f=Label(parent,font=self.police_nombre,text="#")
            f.grid(column=2,row=k+1)
            self.freq2.append(f)
        self.modifie_mot1("")
        self.modifie_mot2("")
    def actualise_info(self,event,objet):
        #self.parent.parent.infos.configure(text=objet.description)
        self.parent.parent.infos.delete("0.0",END)
        self.parent.parent.infos.insert(END,objet.description)
            
        #self.actualise_cumul("")
    def modifie_mot1(self,valeur):
        self.mot1=valeur
        self.titre_colonne2.configure(state="normal")
        self.titre_colonne2.delete(0,END)
        self.titre_colonne2.insert(END,self.mot1)
        self.titre_colonne2.configure(state="disabled")

        self.liste_freq1=self.bfl.liste_freq2forme(valeur)
        
        k=0
        for f in self.freq1:
            #print(liste_freq[k])
            f.configure(text=str(round(self.liste_freq1[k],NB_DECIMALES)))
            k=k+1
        self.actualise_cumul(None)
    def modifie_mot2(self,valeur):
        self.mot2=valeur
        self.titre_colonne3.delete(0,END)
        self.titre_colonne3.insert(END,self.mot2)
        
        self.liste_freq2=self.bfl.liste_freq2forme(valeur)
        
        k=0
        for f in self.freq2:
            m=self.calcule_moyenne(self.liste_freq2[k])
            f.configure(text=self.chaine2nombre(m))
            f.configure(text=str(round(self.liste_freq2[k],NB_DECIMALES)))
            k=k+1
        self.actualise_cumul(None)
    def actualise_mot2(self,event):
        self.mot2=self.titre_colonne3.get()
        self.liste_freq2=self.bfl.liste_freq2forme(self.mot2)
        k=0
        for f in self.freq2:
            #print(liste_freq[k])
            m=self.calcule_moyenne(self.liste_freq2[k])
            f.configure(text=self.chaine2nombre(m))
            k=k+1
        self.actualise_cumul(event)
        
    def donne_liste_poids(self):
        rep=[]
        for c in self.curseur:
            rep.append(c.get())
        return rep
    def calcule_moyenne(self,frequence):
        return frequence*self.lecteur.n/10**6
    def chaine2nombre(self,nombre):
        if nombre==0:
            return "0"
        elif nombre<10**(-NB_DECIMALES+1):
            return "<10^{}".format(-NB_DECIMALES+1)
        else:
            return str(round(nombre,NB_DECIMALES-1))
    def actualise_cumul(self,valeur):
        if self.bfl.n_base>=2:
            for c in self.curseur:
                if c.active:
                    cur_modif=c
                    v0=cur_modif.val_mem
                    delta=c.get()-v0
                    if delta!=0:
                        if v0!=1:
                            cumul=0
                            for c1 in self.curseur:
                                if c1.active==False:
                                    v=c1.get()
                                    nouvelle_valeur=v*(1-delta/(1-v0))
                                    c1.set(nouvelle_valeur)
                                    cumul=cumul+nouvelle_valeur
                            c.set(1-cumul)
                        else:
                            cumul=0
                            nouvelle_valeur=-delta/(self.bfl.n_base-1)
                            for c1 in self.curseur:
                                if c1.active==False:
                                    c1.set(nouvelle_valeur)
                                    cumul=cumul+nouvelle_valeur
                            c.set(1-cumul)
                        
                            
        s=0
        for c in self.curseur:
            s=s+c.get()
            c.val_mem=c.get()
        #m=self.calcule_moyenne(s)
        
        self.cumul.configure(text=self.chaine2nombre(s))
        fp1=0
        fp2=0
        k=0
        self.liste_freq1=self.bfl.liste_freq2forme(self.mot1)
        self.liste_freq2=self.bfl.liste_freq2forme(self.mot2)
        for c in self.curseur:
            fp1=fp1+c.get()*self.liste_freq1[k]
            fp2=fp2+c.get()*self.liste_freq2[k]
            k=k+1
        m1,m2=self.calcule_moyenne(fp1),self.calcule_moyenne(fp2)
        self.freqp1.configure(text=self.chaine2nombre(m1))
        self.freqp2.configure(text=self.chaine2nombre(m2))
            
        
        

        
def fenetre_freqlex(test=False):
    fenetre=Tk()
    fenetre.title('FreqLex')
    fenetre.wm_iconbitmap('Data/icon.ico')
    #&fenetre.geometry("800x600")
    return(fenetre)

if __name__=="__main__":
    f=fenetre_freqlex(test=True)
##    l=liste_mots(f,"Test")
##    l.mots.insert(0,"test1")
##    l.mots.insert(1,"test2")
##    l.cadre.pack()
##    l.ajoute_mot_couleur("t4","red")
##    l.ajoute_mot_couleur("t5","blue")
##    l.mots.select_set(0,0)
    import pickle
    #from bdd_freqlex import base_freqlex
    fichier=open("Data/base_lexicale.pickle","rb")
    bl=pickle.load(fichier)                                    
    c=cadre_cp(f,bl,donnees_lecteur())
    c.modifie_mot1("agonisants")
    c.modifie_mot2("blessants")
    
