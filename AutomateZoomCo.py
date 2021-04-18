import os
import re
import sys
from _datetime import datetime
import time
import importlib.util


def ConvertZoomLink(link):
    if isinstance(link,list):
        linkApp="zoommtg://zoom.us/join?confno="+str(link[0])+"&pwd="+str(link[1])
        return linkApp
    else:
        NumConfAndPass = re.search('/j/(.*)', link).group(1)
        NumConfAndPass = NumConfAndPass.replace('?','&')
        linkApp = "zoommtg://zoom.us/join?confno="+NumConfAndPass
        return linkApp


while True:
    spec = importlib.util.spec_from_file_location("ListProg",
                                                  os.path.dirname(os.path.abspath(sys.argv[0])) + '/ListProg.py')
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    now = datetime.now().strftime('%d-%m-%Y %H:%M')
    for i in foo.ListeProg:
        if now == i[0].strftime('%d-%m-%Y %H:%M'):
            os.system("pkill zoom.us")
            if sys.platform == "darwin":
                os.system("open '" + ConvertZoomLink(foo.ListeProg.get(i)[0]) + "'")
            if sys.platform == "win32":
                os.system("start '" + ConvertZoomLink(foo.ListeProg.get(i)[0]) + "'")
            if i[1].strftime('%d-%m-%Y %H:%M') == i[0].strftime('%d-%m-%Y %H:%M'):
                NvListe = foo.ListeProg
                del NvListe[i]
                with open(os.path.dirname(os.path.abspath(__file__))+'/ListProg.py', 'w') as f:
                    print("import datetime\nListeProg=" + str(NvListe), file=f)
            break
        if now == i[1].strftime('%d-%m-%Y %H:%M') and i[1].strftime('%d-%m-%Y %H:%M')!=i[0].strftime('%d-%m-%Y %H:%M') :
            if sys.platform == "darwin":
                os.system("pkill zoom.us")
            if sys.platform == "win32":
                os.system("taskkill /f /im Zoom.exe")
            NvListe = foo.ListeProg
            del NvListe[i]
            with open(os.path.dirname(os.path.abspath(__file__))+'/ListProg.py', 'w') as f:
                print("import datetime\nListeProg=" + str(NvListe), file=f)
            break
    time.sleep(60)
