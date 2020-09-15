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
print("l'erreur est ici? \n")
matches = re.findall(r"<input type=\"hidden\" name=\"csrf_token\" value=\"*(.*)\"",reponse)
print("\n")
print(matches)
print("le token vaut :  {}.".format(matches[0]))
csrf=matches[0]
print(csrf)

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


