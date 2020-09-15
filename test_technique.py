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


