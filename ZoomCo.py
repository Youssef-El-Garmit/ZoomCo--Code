from tkinter import *
import tkinter as tk
import subprocess
import os
import re
import datetime
from tkinter import ttk
import copy
import importlib.util
import psutil
import sys
import AutomateZoomCo
import ListProg

'''
def openAutomateAtStart():
    if sys.platform == "darwin":
        os.system("osascript -e 'tell application \"System Events\" to make login item at end with properties {path:\""+os.path.dirname(os.path.abspath(sys.argv[0]))+"/AutomateZoomCo\", hidden:false}'")
    #if sys.platform == "win32":
        #os.system("schtasks /create /tn \"AutomateZoomCo\" /sc onlogon /tr \""+os.path.dirname(os.path.abspath(sys.argv[0]))+"/AutomateZoomCo\"")
'''

def CheckProgrammeRunning():
    for proc in psutil.process_iter():
        try:
            if proc.name()=="AutomateZoomCo" or proc.name()=="AutomateZoomCo.exe":
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False



class App(tk.Frame):
    def __init__(self, parent, h=datetime.datetime.now().time().hour,m=datetime.datetime.now().time().minute, state="normal"):
        super().__init__(parent)
        self.h=h
        self.m=m
        self.state=state
        self.hourstr=tk.StringVar(self,self.h)
        self.hour = tk.Spinbox(self,from_=0,to=23,wrap=True,textvariable=self.hourstr,width=3, state=self.state)
        self.minstr=tk.StringVar(self,m)
        self.minstr.trace("w",self.trace_var)
        self.last_value = ""
        self.min = tk.Spinbox(self,from_=0,to=59,wrap=True,textvariable=self.minstr,width=3, state=self.state)
        self.hour.grid()
        self.min.grid(row=0,column=1)

    def trace_var(self,*args):
        if self.last_value == "59" and self.minstr.get() == "0":
            self.hourstr.set(int(self.hourstr.get())+1 if self.hourstr.get() !="23" else 0)
        self.last_value = self.minstr.get()

def activerDuree():
    if CheckDuree.get() == 1:
        DureeSpinBox.min.configure(state="normal")
        DureeSpinBox.hour.configure(state="normal")
        #EteindreOrdi.pack(expand=True, fill=X, side=TOP)

    elif CheckDuree.get() == 0:
        DureeSpinBox.min.configure(state="disabled")
        DureeSpinBox.hour.configure(state="disabled")
        #EteindreOrdi.pack_forget()

def activerActivation():
    if CheckActivation.get() == 1:
        Perso2.configure(bg="green")
        Perso2.configure(bg="green")
        if not(CheckProgrammeRunning()):
            subprocess.Popen(os.path.dirname(os.path.abspath(__file__))+"/AutomateZoomCo",shell=True) #ici
    elif CheckActivation.get() == 0:
        Perso2.configure(bg="red")
        Perso2.configure(bg="red")
        if CheckProgrammeRunning():
            if sys.platform == "darwin":
                os.system("pkill AutomateZoomCo")
            if sys.platform == "win32":
                os.system("taskkill /f /im AutomateZoomCo.exe")

def TrietArrangelist():
    spec = importlib.util.spec_from_file_location("ListProg",
                                                  os.path.dirname(os.path.abspath(__file__)) + '/ListProg.py')
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    ListNonTrier = foo.ListeProg
    List = {}
    for key in sorted(ListNonTrier):
        if key[0] < datetime.datetime.now()-datetime.timedelta(minutes=2) and key[1] < datetime.datetime.now()-datetime.timedelta(minutes=2):
            continue
        List[key] = ListNonTrier.get(key)
    with open(os.path.dirname(os.path.abspath(__file__)) + '/ListProg.py', 'w') as f:
        print("import datetime\nListeProg=" + str(List), file=f)

def AfficherCalendrier():
    TrietArrangelist()
    spec = importlib.util.spec_from_file_location("ListProg",
                                                  os.path.dirname(os.path.abspath(__file__)) + '/ListProg.py')
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    List=foo.ListeProg
    count=0
    st1 =ttk.Style()
    st1.configure('Red.TCheckbutton', foreground='#154e72')
    st2 =ttk.Style()
    st2.configure('Blue.TCheckbutton', foreground='black')
    ListeProg = BodyCa.winfo_children()
    for i in ListeProg:
        i.destroy()
    for i in List:
        if i[0].time()==i[1].time():
            res = "Le " + str(i[0].date().strftime('%d-%m-%Y')) + " à " + str(i[0].time().strftime('%H:%M')) + " : " + str(EntréeTitre.get()) + "\n"
        if i[0].time()!=i[1].time():
            res = "Le " + str(i[0].date().strftime('%d-%m-%Y')) + " à " + str(i[0].time().strftime('%H:%M')) + " : " + str(
                EntréeTitre.get()) + "\nJusqu'au " + str(i[1].date().strftime('%d-%m-%Y')) + " à " + str(i[1].time().strftime('%H:%M')) + "\n"

        if isinstance(List.get(i)[0],list):
            res+="Id Reunion: " + str(List.get(i)[0][0]) + " | Mdp: " + \
               str(List.get(i)[0][1])
        if not(isinstance(List.get(i)[0], list)):
            res+="Lien Zoom: " + str(List.get(i)[0])
        if count%2==0:
            ttk.Checkbutton(BodyCa, text=res, variable=i,
                        onvalue=1, offvalue=0,style='Red.TCheckbutton').pack(fill=BOTH,expand=True)
        else:
            ttk.Checkbutton(BodyCa, text=res, variable=i,
                        onvalue=1, offvalue=0, style='Blue.TCheckbutton').pack(fill=BOTH, expand=True)
        count+=1

'''
def SudoShell(action,Date,Date2="",Action2=""):
    if Date2=="":
        return os.system("""osascript -e 'do shell script "pmset schedule """+ action +""" \\\"""" + str(Date.strftime('%d/%m/%Y %H:%M:%S')) + """\\\"\" with prompt "ZoomCo" with administrator privileges'""")
    else:
        return os.system("""osascript -e 'do shell script "pmset schedule """+ action +""" \\\"""" +
                         str(Date.strftime('%d/%m/%Y %H:%M:%S')) + """\\\" | pmset schedule """+ Action2 +""" \\\"""" +
                         str(Date2.strftime('%d/%m/%Y %H:%M:%S')) + """\\\"\" with prompt "ZoomCo" with administrator privileges'""")
'''

def OpTime(DateHeureDebut,H=0,M=0,S=0,Op="+"):
    if Op=="+":
        DateHeureFinale = DateHeureDebut + datetime.timedelta(hours=H, minutes=M, seconds=S)
        return DateHeureFinale
    if Op=="-":
        DateHeureFinale=DateHeureDebut - datetime.timedelta(hours=H,minutes=M,seconds=S)
        return DateHeureFinale

def SupprProg():
    ListeProg= BodyCa.winfo_children()
    spec = importlib.util.spec_from_file_location("ListProg",
                                                  os.path.dirname(os.path.abspath(__file__)) + '/ListProg.py')
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    NvListe= foo.ListeProg
    AncienneList = copy.copy(NvListe)
    count=0
    res=""
    for i in ListeProg:
        if "selected" in i.state():
            '''
            if sys.platform == "darwin":
                if len(list(NvListe)[count]) == 2:
                    res += " pmset schedule cancel wakeorpoweron \\\"" + str(OpTime(list(NvListe)[count][0],M=10,Op="-").strftime('%d/%m/%Y %H:%M:%S')) + "\\\" |"
                if len(list(NvListe)[count]) == 3:
                    res += " pmset schedule cancel wakeorpoweron \\\"" + str(OpTime(list(NvListe)[count][0],M=10,Op="-").strftime('%d/%m/%Y %H:%M:%S')) + \
                           "\\\" | pmset schedule cancel shutdown \\\"" + str(OpTime(list(NvListe)[count][1],M=10,Op="+").strftime('%d/%m/%Y %H:%M:%S')) + "\\\" |"
            '''
            del AncienneList[list(NvListe)[count]]
        count+=1
    '''
    if res=="":
        return
    
    if sys.platform == "darwin":
        if os.system("""osascript -e 'do shell script \""""+ res[:-1] + """\" with prompt "ZoomCo" with administrator privileges'""") != 0:
            return
    '''
    with open(os.path.dirname(os.path.abspath(__file__))+'/ListProg.py', 'w') as f:
        print("import datetime\nListeProg="+str(AncienneList), file=f)
    Perso1.invoke()

'''
def TurnOff():
    if EteindreOrd.get()==1:
        EteindreOrdi.config(fg="green")
    if EteindreOrd.get()!=1:
        EteindreOrdi.config(fg="red")
'''

def CheckActivations():
    if CheckProgrammeRunning():
        CheckActivation.set(1)
        activerActivation()
    else:
        CheckActivation.set(0)
        activerActivation()

def CheckLienOrIdMdp():
    if CheckLien.get() == 1:
        EntréeLienZoom.pack_forget()
        EntreIdZoom.pack(side=LEFT,expand=True)
        EntreMdpZoom.pack(side=RIGHT,expand=True)
        return True
    else:
        EntreIdZoom.pack_forget()
        EntreMdpZoom.pack_forget()
        EntréeLienZoom.pack(fill=X, expand=True)
        return False

def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

def CheckEntrer():
    try:
        datetime.datetime.strptime(DateChoisi.get(), '%d/%m/%Y')
    except ValueError:
        return Message.config(text="Date non valide ou non-conforme !")
    if CheckDuree.get() == 1:
        HeureDebut= datetime.time(int(HeureSpinBox.hour.get()),int(HeureSpinBox.min.get()))
        DateHeureDebut=(datetime.datetime.combine(datetime.datetime.strptime(DateChoisi.get(), '%d/%m/%Y'),HeureDebut))
        DateHeureFin= DateHeureDebut+datetime.timedelta(hours=int(DureeSpinBox.hour.get()),minutes=int(DureeSpinBox.min.get()))
        '''
        if EteindreOrd.get()==1:
            Choix=DateHeureDebut,DateHeureFin,True
        else:
            Choix = DateHeureDebut, DateHeureFin
        '''
        Choix = DateHeureDebut, DateHeureFin #ca ou le commentaire
    if CheckDuree.get() == 0:
        HeureDebut= datetime.time(int(HeureSpinBox.hour.get()),int(HeureSpinBox.min.get()))
        DateHeureDebut=(datetime.datetime.combine(datetime.datetime.strptime(DateChoisi.get(), '%d/%m/%Y'),HeureDebut))
        DateHeureFin=DateHeureDebut
        Choix = DateHeureDebut,DateHeureFin
    spec = importlib.util.spec_from_file_location("ListProg",
                                                  os.path.dirname(os.path.abspath(__file__)) + '/ListProg.py')
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    dictionary=foo.ListeProg
    if DateHeureDebut < datetime.datetime.now() and DateHeureFin < datetime.datetime.now():
        return Message.config(text="Date et/ou heure non valide !")
    for i in dictionary:
        if time_in_range(i[0],i[1],DateHeureDebut) or time_in_range(i[0],i[1],DateHeureFin) or time_in_range(DateHeureDebut,DateHeureFin,i[0]) or time_in_range(DateHeureDebut,DateHeureFin,i[1]):
            return Message.config(text="Une réunion est déjà programmé à cette heure !")
    if CheckLienOrIdMdp():
        IdChoisi = EntreIdZoom.get()
        MdpChoisi = EntreMdpZoom.get()
        if (len(IdChoisi)!=10 and len(IdChoisi)!=11) or IdChoisi=="Id Reunion" or ("\\" in MdpChoisi) or (" " in MdpChoisi) or len(MdpChoisi)==0 or not(str(IdChoisi).isnumeric()):
            Message.config(text="Id ou Mdp non valide!")
            EntreIdZoom.config(text="Id Reunion")
            return EntreMdpZoom.config(text="Mdp Reunion")
        dictionary[Choix]=[EntreIdZoom.get(),EntreMdpZoom.get()],EntréeTitre.get()

    if not(CheckLienOrIdMdp()):
        LienChoisi = EntréeLienZoom.get()
        NumConf = re.search('/j/(.*)pwd', LienChoisi).group(1)[:-1]
        if "zoom.us/j/" not in LienChoisi or "?pwd=" not in LienChoisi or not(str(NumConf).isnumeric()) or (len(NumConf)!=10 and len(NumConf)!=11):
            Message.config(text="Lien non valide ou non-conforme !")
            return EntréeLienZoom.config(text="https://zoom.us/j/xxxxxx?pwd=xxxxxx")
        dictionary[Choix]= EntréeLienZoom.get(),EntréeTitre.get()
    '''
    if sys.platform == "darwin":
        DateEtHeureAllumage= OpTime(DateHeureDebut,M=10,Op="-")
        if CheckDuree.get()==1 and EteindreOrd.get()==1:
            DateEtHeureEteignage = OpTime(DateHeureFin, M=10, Op="+")
            if SudoShell("wakeorpoweron",DateEtHeureAllumage,DateEtHeureEteignage,"shutdown") !=0:
                return
        elif SudoShell("wakeorpoweron",DateEtHeureAllumage) !=0:
            return
    '''
    with open(os.path.dirname(os.path.abspath(__file__))+'/ListProg.py', 'w') as f:
        print("import datetime\nListeProg="+str(dictionary), file=f)
    EntreIdZoom.delete(0,END)
    EntreIdZoom.insert(0,"Id Reunion")
    EntréeLienZoom.delete(0,END)
    EntréeLienZoom.insert(0,"https://zoom.us/j/xxxxxx?pwd=xxxxxx")
    EntréeTitre.delete(0,END)
    EntréeTitre.insert(0,"Cour de Maths")
    EntreMdpZoom.delete(0,END)
    EntreMdpZoom.insert(0,"Mdp Reunion")
    if CheckDuree.get()==1:
        Durée.invoke()
    TrietArrangelist()
    if CalendrierProg.winfo_ismapped()==1:
        Perso1.invoke()
    Message.config(text="Votre réunion à été programmé avec succés")

'''
openAutomateAtStart()
'''

fenetrePrincipale = Tk()
fenetrePrincipale.resizable(False, False)
#Icon = PhotoImage(file = "icon.png")
#fenetrePrincipale.iconphoto(False, Icon)
fenetrePrincipale.title("ZoomCo")
PropHero = Frame(fenetrePrincipale)
PropHero.pack(expand=0, fill=X, side=TOP)
CheckActivation=IntVar()
CalendrierProg=Toplevel(fenetrePrincipale)
CalendrierProg.bind("",CalendrierProg.update())
#CalendrierProg.iconphoto(False, Icon)
CalendrierProg.resizable(False, False)
TitreSuppr=Label(CalendrierProg,text="Selectionner les programmations à supprimer",bg="black",fg='white')
TitreSuppr.pack(fill=X, side=TOP)
BodyCa=Frame(CalendrierProg)
BodyCa.pack(fill=BOTH,expand=True)
ButtonSuppr= Button(CalendrierProg,text="Supprimer",bg="white",fg='red',command=SupprProg)
ButtonSuppr.pack(fill=X, side=BOTTOM)
CalendrierProg.title("Calendrier des Programmations")
Perso1 = Button(PropHero, text='Calendrier\ndes Programmation', width=5,command=lambda:[CalendrierProg.deiconify(),AfficherCalendrier()])
Perso2 = Checkbutton(PropHero, text="Activer\n  l'Automatisation  ", variable=CheckActivation,
                     onvalue=1, offvalue=0,bg='red', fg='white',width=5, command=activerActivation)
CalendrierProg.withdraw()
CalendrierProg.protocol("WM_DELETE_WINDOW", CalendrierProg.withdraw)
Perso2.pack(side="left", fill=BOTH, expand=True)
Perso1.pack(side="right", fill=BOTH, expand=True)
Body = Frame(fenetrePrincipale)
Body.pack(expand=True, fill=BOTH)
MessageFrame= Frame(Body)
MessageFrame.pack(fill=X)
Message = Label(MessageFrame, text="Bienvenue dans le programmeur ZoomCo", bg='black', fg='white')
Message.pack(fill=X, expand=0)
LienZoom= Frame(Body)
LienZoom.pack(fill=X, expand=True)
CheckLien=IntVar()
LienZoomTitre = Checkbutton(LienZoom, text='Lien Zoom', variable=CheckLien, onvalue=0, offvalue=1,
                    bg='#154e72', fg='white', width=10, command=CheckLienOrIdMdp)
IdMdpTitre = Checkbutton(LienZoom, text='Id et Mdp', variable=CheckLien, onvalue=1, offvalue=0,
                    bg='#154e72', fg='white', width=10, command=CheckLienOrIdMdp)
LienZoomTitre.pack(fill=BOTH,side=LEFT, expand=True)
IdMdpTitre.pack(fill=BOTH,side=RIGHT, expand=True)
ZoomCoEntre= Frame(Body)
EntréeLienZoom = Entry(ZoomCoEntre)
EntreIdZoom= Entry(ZoomCoEntre)
EntreMdpZoom= Entry(ZoomCoEntre)
EntreIdZoom.insert(0,"Id Reunion")
EntreMdpZoom.insert(0,"Mdp Reunion")
EntréeLienZoom.insert(0, 'https://zoom.us/j/xxxxxx?pwd=xxxxxx')
ZoomCoEntre.pack(fill=X)
EntréeLienZoom.pack(fill=X, expand=True)
ParamConnexion = Frame(Body)
ParamConnexionTitre = Frame(ParamConnexion)
ParamConnexionEntrée = Frame(ParamConnexion)
ParamConnexion.pack(expand=True, fill=X)
ParamConnexionTitre.pack(expand=0, fill=X)
ParamConnexionEntrée.pack(expand=0, fill=X)
HeureEntre = Frame(ParamConnexionEntrée)
DuréeEntre = Frame(ParamConnexionEntrée)
DateEntrer = Frame(ParamConnexionEntrée)
DateChoisi = Entry(DateEntrer, width=10)
DateChoisi.insert(0,datetime.datetime.now().strftime('%d/%m/%Y'))
DateChoisi.pack(expand=True)
HeureSpinBox = App(HeureEntre)
HeureSpinBox.pack(expand=True)
DureeSpinBox = App(DuréeEntre,h="1",m="30", state="disabled")
DureeSpinBox.pack(expand=True)
CheckActivations()
DateEntrer.pack(side="left", fill="both", expand=True)
HeureEntre.pack(side="left", fill="both", expand=True)
DuréeEntre.pack(side="left", fill="both", expand=True)
CheckDuree= IntVar()
Date = Label(ParamConnexionTitre, text="Date", bg='#154e72', fg='white', width=10)
Heure = Label(ParamConnexionTitre, text="Heure", bg='#154e72', fg='white', width=10)
Durée = Checkbutton(ParamConnexionTitre, text='Durée', variable=CheckDuree, onvalue=1, offvalue=0,
                    bg='#154e72', fg='white', width=10, command=activerDuree)
Date.pack(side="left", fill="both", expand=True)
Heure.pack(side="left", fill="both", expand=True)
Durée.pack(side="left", fill="both", expand=True)
Titre = Frame(Body).pack(expand=True, fill=X)
TitreTitre= Label(Titre, text="Titre de la réunion", bg='#154e72', fg='white')
'''
EteindreOrd=IntVar()
EteindreOrdi= Checkbutton(Titre, text="Éteindre l'ordinateur à la fin de la durée", bg='white', fg='red', variable=EteindreOrd , command=TurnOff)
EteindreOrdi.invoke()
'''
EntréeTitre = Entry(Titre)
EntréeTitre.insert(0, 'Cour de Maths')
ProgrammerBut = Button(fenetrePrincipale, text='Programmer', fg="#154e72",command=CheckEntrer)
ProgrammerBut.pack(expand=0, fill=X, side=BOTTOM)
EntréeTitre.pack(fill=X, expand=0, side=BOTTOM)
TitreTitre.pack(fill=X, expand=0, side=BOTTOM)


fenetrePrincipale.mainloop()