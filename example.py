from request import Request, Log

req = Request(ssl=True, host='www.google.com', debug=True)

reponse = req.request('/',
    headers= {
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        
    }
)

print(reponse)