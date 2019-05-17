texte="""Les inégalités territoriales dans l’Union européenne
Malgré sa prospérité d’ensemble, l’Union européenne est traversée par des inégalités territoriales.
-L’Union  européenne est  marquée  par  une  opposition  forte  et  ancienne  entre  le  centre  et  la 
périphérie.
Le centre se caractérise par de fortes densités d’hommes et d’activités, une grande 
prospérité, la concentration des activités de commandement et la maîtrise technologique. 
Dans cet espace, les villes grandes, moyennes et petites sont nombreuses;
la finance et les sièges sociaux  des  grandes  multinationales  sont  concentrés  dans  quelques  métropoles  
(Francfort,  Paris, Londres,  Amsterdam...)
À l’inverse, les périphéries européennes (Irlande, péninsule ibérique, 
sud de l’Italie, Balkans) se caractérisent par des densités de population
et d’activités plus basses.
-Mais l’opposition Est/Ouest est de loin la plus profonde et la plus ancienne de l’espace européen.
Malgré les réformes mises en place après la chute du communisme, on retrouve en 2008 des écarts de niveaux de PIB par habitant importants.
Les pays de l’Europe orientale gardent des faiblesses importantes: leur croissance s’appuie uniquement sur le développement de secteurs 
à  faibles  ou  moyennes  technologies. 
De  plus,  beaucoup  de  ces  pays  ont  été  très  touchés  par  la crise  de  2008-2010,  les  ramenant  plusieurs  années  en  arrière  en  ce  qui  concerne  leur  niveau  de 
PIB par habitant. 

PIB par habitant: le Produit Intérieur Brut par habitant est un indicateur de richesse
Les pays de l’Europe orientale : les pays de l’Europe de l’Est"""


ligne="a priori	apRijoRi	a priori	NOM	m		0.41	0.47	0.41	0.47		2	3	1	8	8	V CCVVCV	VCCVYVCV	1	0	4	5	a-pRi-jo-Ri	4	V-CCV-YV-CV	iroirp a	iRojiRpa	a prio-ri	ADV,NOM	93	16	3.8	3.25	a-priori	2"

def texte_liste(t1):
    liste_mots=[]
    i=0
    mot=""
    t=t1+"."
    while t!="":
        #test
        #print(t[0:i+1])
        
        if t[0:i+1].isalpha():
            mot=t[0:i+1]
            i=i+1
        else:
            t=t[i+1:]
            if mot!="":
                liste_mots.append(mot)
            #test
            #print(liste_mots)
            mot=""
            i=0
    return liste_mots
if __name__=="__main__":
    print(ligne.split('\t'))
    print(texte_liste(texte))
        
        
