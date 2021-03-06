
from request import Request, Log
import re
import urllib
import urllib.parse


#Requête pour creer un compte (méthode Post) :

req = Request(ssl=True, host='www.snipes.fr', debug=True)

reponse = req.request('/registration',
    headers= {
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
    }
)


#Recupération du Token
if reponse is None:
    print("ERROR")
    exit()
matches = re.findall(r"<input type=\"hidden\" name=\"csrf_token\" value=\"*(.*)\"",reponse)
print("le token vaut :  {}.".format(matches[0]))
csrf=matches[0]

# Demande des parametres de creation du compte :

prenom = input("\n saisissez un prenom: ")
prenom="dwfrm_profile_register_firstName=" + prenom
nom = input("\n saisissez un nom: ")
nom="dwfrm_profile_register_lastName=" + nom
mail = input("\n saisissez un mail: ")
mail_confirm="dwfrm_profile_register_emailConfirm" + mail
mail="dwfrm_profile_register_email=" + mail
mdp = input("\n saisissez un mdp (au moins : 1 majuscule , 1 chiffre , 1 carectere spec) :")
mdp_confirm = "dwfrm_profile_register_passwordConfirm=" + mdp
mdp="dwfrm_profile_register_password=" + mdp
phone="dwfrm_profile_register_phone=&"
birthday="dwfrm_profile_register_birthday=&"
policy="dwfrm_profile_register_acceptPolicy=true"
csrf_token=csrf
param="dwfrm_profile_register_title=Herr&"+prenom+"&"+nom+"&"+mail+"&"+mail_confirm+"&"+mdp+"&"+mdp_confirm+"&"+phone+birthday+policy+"&csrf_token="+csrf

#Creation du compte
reponse = req.request('/on/demandware.store/Sites-snse-FR-Site/fr_FR/Account-SubmitRegistration',method="post",body=param,
    headers= {
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'content-type':'application/x-www-form-urlencoded;charset=UTF-8',
                
    }
)
print(reponse)

# Saisie de l'url par l'utilisateur :
url_product=input("\n veuillez renseigner l'url de la chaussure souhaitée : ")
print(url_product)
url_p = re.findall(r"\/p\/.+\.html",url_product)
print("l'url est' :  {}.".format(url_p[0]))

#Extraction des différentes tailles dans le code html :

reponse = req.request(url=url_p[0],
    headers= {
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
    }
)

if reponse is None:
    print("ERROR")
    exit()

tailles = re.findall(r"data-attr-id=\"size\" data-value=\"\d*\s?\d?\/?\d\"",reponse)
taille_str= ', '.join(tailles)
final_size = re.findall(r"data-value=\"\d*\s?\d?\/?\d\"",taille_str)

# saisie de la taille souhaitée :

size = ', '.join(final_size)
size_string = size.replace('data-value=', 'size = ').replace(',', ' or ')
choix=input("choisissez une taille parmis : " + size_string)
print('\n')
f={'chosen=size&dwvar_00013801853801_212':choix}
choix_t = urllib.parse.urlencode(f)

# Creation de l'url pour avoir la bonne taille :
size_url = url_p[0] + "?" + choix_t

prix = re.findall(r"\"price\":\d+\D?\d*,\"",reponse)
prix_f=', '.join(prix)
prix_f = re.findall(r"\d+.?\d+",prix_f)
prix_item = prix_f[0]

#Recuperation qté max :
qte=0
nb = float(prix_f[0])
while (nb*qte <= 500):
    qte+=1

# Recupération des données utiles pour l'ajout au panier :
reponse = req.request(url=size_url,
    headers= {
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
    }
)

id_items = re.findall(r"data-pid=\"\d+\"",reponse)
pid = re.findall(r"\d+",id_items[0])
pid = ', '.join(pid)
optionId = re.findall(r"dwvar_\d+_\d+&",reponse)
option=re.findall(r"(\d+&)",optionId[0])
option=', '.join(option)
option=option[:len(option)-1]

#Ajout des paramètres du POST

var='[{"optionId"'
var2=':"{}"'.format(option)
var3=',"selectedValueId":"{}"'.format(choix)
var4='}]'
vartot=var+var2+var3+var4
f={'pid':pid,'options':vartot,'quantity':'1'}
param = urllib.parse.urlencode(f)

# Finalisation de l'ajout au panier

print('\n')

reponse = req.request('/on/demandware.store/Sites-snse-FR-Site/fr_FR/Cart-AddProduct',method="post",body=param,
    headers= {
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'content-type':'application/x-www-form-urlencoded;charset=UTF-8',
                
    }
)
print(reponse)

# Demande de la quantité souhaité

# nb_item=input(" indiquer la quantité souhaite (max = {} )".format(qte))
# uuid = re.findall(r"data-uuid=\"\d+.*\d+\"",reponse)
# item_uuid = re.findall(r"\d+.*\d+",uuid[0])
# uuid_f = ', '.join(item_uuid)

# #Ajout de la quantité indiqué :

# f={'pid':pid,'quantity':nb_item,'uuid':uuid_f}
# encoded = urllib.parse.urlencode(f)
# url_qte = '/on/demandware.store/Sites-snse-FR-Site/fr_FR/Cart-UpdateQuantity?' + encoded
# reponse = req.request(url_qte,
#     headers= {
#         'Cache-Control': 'no-cache',
#         'Connection': 'keep-alive',
#         'DNT': '1',
#         'Pragma': 'no-cache',
#         'Upgrade-Insecure-Requests': '1',
#     }
# )

# print(reponse)