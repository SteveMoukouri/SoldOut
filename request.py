import socket
import ssl
import re
import zlib
import base64
from time import time

USERAGENT="Mozilla/5.0 (X11; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0"

class Log:
    """
    Cette classe est utilisée pour écrire dans la console.
    """
    def __init__(self):
        pass

    def Info(self, msg, end='\n'):
        color, init = "\33[1;36m", "[*] "
        self.print(color, init, msg, end)

    def Warning(self, msg, end='\n'):
        color, init = "\033[1;31m", "[!] "
        self.print(color, init, msg, end)

    def Error(self, msg, end='\n'):
        color, init = "\033[1;31m", "[!] "
        self.print(color, init, msg, end)

    def White(self, msg, end='\n'):
        color, init = "\33[1;1m", ''
        self.print(color, init, msg, end)

    def Send(self, msg, end='\n'):
        color, init = "\033[32m", "[>] "
        msg = msg.replace('\n', '\n[>] ')
        self.print(color, init, msg, end)

    def Recv(self, msg, end='\n'):
        color, init = "\033[1;30m", "[<] "
        msg = msg.replace('\n', '\n[<] ')
        self.print(color, init, msg, end)

    def Comment(self, msg, end='\n'):
        color, init = "\33[1;1m", '[#] '
        self.print(color, init, msg, end)

    def print(self, color, init, msg, end):
        print(color + init + str(msg) + "\033[00m", end=end)

class Request(Log):
    """
    Cette classe est utilisée pour envoyer des requêtes HTTP. Nous avons choisi d'écrire notre propre classe plutôt
    que d'utiliser les bibliothèques Python déjà disponibles pour avoir plus de contrôle sur le contenu des requêtes.
    La seule fonction à savoir maîtriser est request(), les autres fonctions lui sont auxiliaires.
    """
    def __init__(self, ssl, host, debug=False, interval=3, timeout=3, lang='en', useragent=USERAGENT, vhttp="1.1"):
        self.ssl        = ssl
        self.host       = host
        self.debug      = debug
        self.cookies    = {}
        self.interval   = interval
        self.timeout    = timeout
        self.lang       = lang
        self.response   = ""
        self.useragent  = USERAGENT
        self.headers    = ""
        self.vhttp      = vhttp
        self.status     = ""

    def create_req(self, url, method, cookies, body, headers):
        """
        Crée et encode la requête HTTP à envoyer
        """
        req_cookies = ""
        i = False
        for name in cookies:
            if i:
                req_cookies += "; "
            req_cookies += "{}={}".format(name, cookies[name])
            i = True
        req = "{} {} HTTP/{}\n".format(method.upper(), url, self.vhttp)
        req += "Host: {}\n".format(self.host)
        headers['User-Agent'] = self.useragent
        if not 'Accept' in headers:
            headers['Accept'] = '*/*'
        if not 'Accept-Encoding' in headers:
            headers['Accept-Encoding'] = 'raw'
        if not 'Accept-Language' in headers:
            headers['Accept-Language'] = self.lang
        if body != "":
            headers["Content-Length"] = str(len(body))
        if cookies != {}:
            headers["Cookie"] = req_cookies
        for name in headers:
            req += '{}: {}\n'.format(name, headers[name])
        req += "\n"
        req = req.replace("\n", "\r\n")
        req += body
        if self.debug:
            self.Send(req)
        return req.encode()

    def GetCookies(self, headers):
        '''
        Ajoute les nouveaux cookies
        '''
        for find in [r'Set-Cookie: (.+?)=(.+?);', r'set-cookie: (.+?)=(.+?);']:
            cookies = re.findall(find, headers)
            for cook in cookies:
                self.cookies[cook[0]] = cook[1]

    def recv(self, sock, url):
        '''
        Recoit la réponse HTTP
        '''
        data = b""
        trun = time()
        while True:
            raw_data = b''
            try:
                raw_data = sock.recv(100000)
            except socket.timeout:
                break
            except Exception as e:
                self.Error('Error Recv: {}'.format(e))
                break
            data += raw_data
            if time() - trun > self.timeout:
                self.Warning('Timeout: Recv takes too much time ({})'.format(time() - trun))
                break
        try:
            data = data.decode('utf8')
            return data
        except:
            self.Warning('Can\'t decode data recv')
        ldata = data.split(b'\r\n\r\n')
        header = ldata[0].decode('utf8')
        body = ldata[1]
        if 'gzip' in header:
            body = zlib.decompress(body, 16+zlib.MAX_WBITS)
            return header + '\r\n\r\n' + body.decode()
        return header

    # ==================================================================== #
    # Connection                                                           #
    # ==================================================================== #
    def http(self, url, headers):
        '''
        Se connecte au port 80 (http)
        '''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, 80))
        sock.settimeout(self.interval)
        # Envoie la requête
        sock.send(headers)
        # Recoie la requête
        return self.recv(sock, url)

    def https(self, url, headers):
        '''
        Se connecte au port 443 (https)
        '''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context = ssl._create_default_https_context()
        context.check_hostname = self.host
        sock = context.wrap_socket(sock, server_hostname=self.host)
        try:
            sock.connect((self.host, 443))
           
        except Exception as e:
            
            self.Error(str(e))
            return None
        sock.settimeout(self.interval)
        # Envoie la requête
        
        sock.write(headers)
        # Recoie la requête
        
        return self.recv(sock, url)

    # ==================================================================== #
    # Main Function                                                        #
    # ==================================================================== #
    def request(self, url, method="get", headers={}, cookies=None, body=""):
        '''
        Fonction principale
        '''
        self.status = ""
        self.response = ""
        self.headers = ""
        if cookies == None:
            cookies = self.cookies

        # En-tête
        protocol = 'http'
        if self.ssl:
            protocol = 'https'
        if self.debug:
            self.White("#============================================================#")
            self.White("# {} {}://{}{} #".format(method.upper(), protocol, self.host, url))
            self.White("#============================================================#")
        else:
            self.White("[@] {} {}://{}{}".format(method.upper(), protocol, self.host, url))

        # Envoie et Recoie
        print("J'ai fini l'entête")
        data = self.create_req(url, method, cookies, body, headers)
        if self.ssl:
            
            self.response = self.https(url, data)
        else:
            self.response = self.http(url, data)

        # Traite la reponse
        
        if not self.response in ["", None]:
            self.headers = self.response.split('\r\n\r\n')[0]
            if self.debug:
                self.Recv(self.headers)
            self.status  = re.findall(r'HTTP/1\.1 ([0-9]*)', self.headers)[0]
            self.Info("Status: " + self.status)
            if re.match(r'.*[Ss]et-[Cc]ookie:.*', self.headers, re.DOTALL):
                self.GetCookies(self.headers)
        if self.debug:
            self.Info("Cookies: " + str(list(self.cookies)))
        return self.response