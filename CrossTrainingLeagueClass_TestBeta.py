# -*- coding: utf-8 -*-

'''
Autor: Asier Juan  Fecha: 01/07/2022
Version 1.1 
Description: Script to create the data base with user profiles and corresponding graphs of performance on different Crossfit areas.
'''
from IPython.display import display
from ipywidgets import HBox, VBox, Layout, GridspecLayout, GridBox, AppLayout
from ipywidgets import interact, interactive, fixed, interact_manual, FloatSlider, Dropdown, Checkbox
from ipywidgets import ToggleButton, SelectionSlider, FloatText, jslink, Select, HTML, Image, Button, Tab
import numpy as np
# Import libraries
import string
import configparser
import bcrypt
import time
import datetime
import ipydatetime
import calendar
import os
import pandas as pd
import matplotlib.pyplot as plt
import pickle
from ipywidgets import widgets
from IPython.display import YouTubeVideo   
from operator import itemgetter                                                      
class CrossTrainingLeague_ZGZ(object):
    
    def __init__(self):
        BoxList=['Eolo','Cierzo','Wonkru','Hiberus','Box&Fitness','Utgard','Devil','Tutanza','OneLeague']
        BoxList.sort()
        
        self.BoxListHost=['Eolo','Cierzo','Wonkru','Hiberus','Box&Fitness','Utgard','Devil','Tutanza','OneLeague']
        self.BoxListHost.sort()
        #self.BoxListHostCompetitionHours=
        self.CategoryList=['Escalado','Pro','Rx']
        self.savedeleteControl=False
        self.pos_textoaviso=0

        
        #self.stafigure=[None,None] # Este es el original para plotear RawData y ScaledData
        self.stafigure=[None]
        style = {'description_width': '110px'}
        # Widgets for the Log In Window
        self.UserName=widgets.Text(
        value='',
        placeholder='',
        description='Nombre usuario',
        disabled=False,
        layout=Layout(width='auto', grid_area='UserName'),
        style=style
        )
        self.PassWord=widgets.Password(
        value='********',
        description='Contraseña',
        disabled=False,
        layout=Layout(width='auto', grid_area='PassWord'),
        style=style
        )
        self.LogIn=widgets.Button(
                    value=False,
                    description='Acceder',
                    disabled=False,
                    indent=False,
                    layout=Layout(width='auto', grid_area='LogIn'),
                    
        )
        
        # Widgets to create a new user
        self.NewUserName=widgets.Text(
        value='',
        placeholder='',
        description='Nombre usuario',
        disabled=False,
        layout=Layout(width='auto', grid_area='NewUserName'),
        style=style
        )
        
        
        self.NewOjo=widgets.Password(
        value='********',
        description='Contraseña',
        disabled=False,
        layout=Layout(width='auto', grid_area='NewOjo'),
        style=style
        
        )

        self.ConfirmOjo=widgets.Password(
        value='********',
        description='Repetir contraseña',
        disabled=False,
        layout=Layout(width='auto', grid_area='ConfirmOjo'),
        style=style
        )
        self.Box=widgets.Dropdown(
        options=BoxList,
        value=BoxList[0],
        description='Box',
        layout=Layout(width='auto', grid_area='Box'),
        style=style
        #layout=Layout(width='max-content', grid_area='Box'),
        )
        
        self.AccessCode=widgets.Text(
        value='',
        placeholder='',
        description='Código',
        disabled=False,
        layout=Layout(width='auto', grid_area='AccessCode'),
        style=style
        )
        
        
        self.DateOfBirth=widgets.DatePicker(
        description='Fecha de nacimiento',
        disabled=False,
        layout=Layout(width='auto', grid_area='DateOfBirth'),
        style=style
        )
        self.Gender=widgets.Dropdown(
        options=[('Femenina', 'M'),('Masculina', 'H')],
        value='M',
        description='División',
        #layout=Layout(width= 'max-content', grid_area='Gender'),
        layout=Layout(width='auto', grid_area='Gender'),
        style=style
        #layout=Layout({'width': 'max-content'}, grid_area='Gender'),
        )
        
        self.heigth=widgets.IntText(
        value=0,
        description='Altura[cm]',
        disabled=False,
        layout=Layout(width='auto', grid_area='heigth'),
        )   
        self.weight=widgets.IntText(
        value=0,
        description='Peso[Kg]',
        disabled=False,
        layout=Layout(width='auto', grid_area='weight'),
        )   
        #style = {'description_width': '100px'}
        self.Category=widgets.Dropdown(
        options=self.CategoryList,
        value=self.CategoryList[0],
        description='Categoría',
        #indent=False,
        #layout=Layout(width='auto', grid_area='Category'),
        layout=Layout(width='max-content', grid_area='Category'),
        style=style
        )
        
        self.CreateNewUserButton=widgets.Button(
                    value=False,
                    description='Crear Atleta',
                    disabled=False,
                    #indent=False,
                    layout=Layout(width='auto', grid_area='CreateNewUser'),
                    
        )
        self.CreateNewOwnerButton=widgets.Button(
                    value=False,
                    description='Crear Box',
                    disabled=False,
                    #indent=False,
                    layout=Layout(width='auto', grid_area='CreateNewOwner'),
                    
        )
        
        self.CreateNewUserButton.on_click(self.CreateNewUser)
        self.CreateNewOwnerButton.on_click(self.CreateNewUser)
        
        self.WindowToPlot=widgets.Dropdown(
        options=['None','Perfil Usuario', 'Clasificación', 'Calendario'],
        value='None',
        description='Tab:',
        disabled=False,
        )  
        
        self.AvisoUserCreated=widgets.HTML(
                    value="<b></b>",
                    placeholder='',
                    description='',
                    indent=False,
                    layout=Layout(width='auto', grid_area='AvisoUserCreated'),
                    )
                        
        self.AvisoLogin=widgets.HTML(
                    value="<b></b>",
                    placeholder='',
                    description='',
                    indent=False,
                    layout=Layout(width='auto', grid_area='AvisoLogin'),
                    )
        self.AvisoInvitationCreated=widgets.HTML(
                    value="<b></b>",
                    placeholder='',
                    description='',
                    indent=False,
                    layout=Layout(width='auto', grid_area='AvisoInvitationCreated'),
                    )

        self.NombreMes=widgets.HTML(
                    value="<b>ENERO</b>",
                    placeholder='',
                    description='',
                    indent=False,
                    layout=Layout(width='auto', grid_area='AvisoInvitationCreated'),
                    )
                        
        self.HeaderHost=widgets.HTML(
                    value="<b>Anfitriones</b>",
                    placeholder='',
                    description='',
                    indent=False,
                    layout=Layout(width='auto', grid_area='Anfitriones',border='solid'),
                    )
        self.HeaderGuest=widgets.HTML(
                    value="<b>Visitantes</b>",
                    placeholder='',
                    description='',
                    indent=False,
                    layout=Layout(width='auto', grid_area='Visitantes',border='solid'),
                    )
        
        
        
        self.check=widgets.Checkbox(
                    value=False,
                    description='Dibujar estadísticas',
                    disabled=True,
                    indent=False
                    
        )
        


        # Widgets for WODs & Callenges # Avocado --> Aqúi se crean los wods, fechas etc..
        # TODA ESTA PARTE TIENE QUE QUEDAR COMPLETAMENTE DEFINIDA ANES DEL INICIO DE LA COMPETICIÓN (LOS VIDEO E IMÁGENES ASOCIADAS A LOS WOD CUANDO LLEGUE LA FECHA DEL MES)
        self.CalendarMonths=['Enero'] # avocado -Hay que editar el self.Monthsgrid en consecuencia
        self.currentDate=datetime.date.today()
        self.currentMonth=datetime.date.today().month
        self.StartDate=datetime.date(2022,11,30)
        self.CalendarEndDates=[datetime.date(2022,12,30)]
        self.WodNames=[ ['Wod1-A','Wod1-B','Wod2-A','Wod2-B','Wod3']] # Cada lista representa un mes, si hay mas meses se añade otra lista dentro (Weven Wod 1 A&B are performed together, here they are typed as individuals since each part is independent for the leaderboard)
        self.UniqueWodNames=[ ['Wod1','Wod2','Wod3']] # Unique wod names, these will be the options available for the owners to generate invitations (Same strcuture as self.WodNames)
        self.SharedWod=[ [None,None,[1,2]]] # For each unique WodName here is defined wich of them is common for two or more categories. If [], the wod is unique for each one, of [0,1], the wod will be the same for category 0 and 1 as defined in categories list
                        
        
        # Youtube ID video associated to each wod
        self.YoutubeIDs=[ ["d_78hCLPITs","d_78hCLPITs","d_78hCLPITs","d_78hCLPITs","d_78hCLPITs"]
                         ]
        
        # Type of mark of every Wod
        self.markType=[ ["Kgs","Time","Reps","Time","Reps"]
                       ]
        
        # Active months para ir activando los meses con sus wods etc.. cuando llegue la fecha
        #self.ActiveMonths=['Semana1','Semana2']
        m=0
        
        # Comento esta parte de momento para que no falle al terminar el mes
        '''
        for i in range(len(self.CalendarEndDates)):
            if(self.CalendarEndDates[i]<self.currentDate):
                m+=1
        '''
        self.ActiveMonths=self.CalendarMonths[0:m+1]

        # Hacer plana la lista de WodNames para crear las entradas en la base de datos
        self.WodNamesFlat=[]
        for fila in range(len(self.WodNames)):
            for columna in range(len(self.WodNames[fila])):
                self.WodNamesFlat.append(self.WodNames[fila][columna])
        self.ActiveWodNamesFlat=[]
        for fila in range(len(self.ActiveMonths)):
                for columna in range(len(self.WodNames[fila])):
                    self.ActiveWodNamesFlat.append(self.WodNames[fila][columna])
        #self.WODcaledarOptions=self.WodNames[m]

        self.WODcaledarOptions=self.UniqueWodNames[m]
        self.sharedWodcaledarOptions=self.SharedWod[m]
               

        #print('Initialization')
        #%% CREACION PERFILES DE USUARIO (STATIC)
        
        # On this part, any new user is included, or any new entry on the profile of an already defined user in updated.
        
        # Static Example with 6 users: Hombre1 Mujer1
        # Fixed code used to generate an empty profile for a new user
        

        
        self.UserDefinition_List=['Age','Gender','Heigth','Weight','HomeBox','Category']
        #self.UserBenchMarksDict=['Strength','Haltero','Gymnastics','HeroWODs','Other']
        #self.UserBenchMarksDict=['Strength','Haltero']
        self.Strength_BenchM=['BackSquat','DeadLift','BenchPress','OH squat','StrictPress']
        Haltero_BenchM=['SquatSnatch','SquatClean','PowerSnatch','PowerClean','C&J']
        
        Gymnastics_BenchM=['MaxUPullUps','MaxUC2B','MaxUMuscleUp','MaxStrictHSPU']
        HeroWODs_BenchM=['Fran','FriendlyFran','Murph','Cindy']
        Other_BenchM=['5kmrun','100mswim']
        # Aquí genero 
        self.UserBenchMarksDict={"Fuerza":dict.fromkeys(self.Strength_BenchM),"Halterofilia":dict.fromkeys(Haltero_BenchM)}
    
        # This static list will be genraed as new users create an account in the platform
        self.UserNamesList=[]
        UserWodEntries=[[2200,10000/550,10000/1005,10000/630,63,10000/990],[2200,10000/550,10000/1005,10000/630,63,10000/990],[1800,10000/480,10000/1105,10000/690,68,10000/1100,75],[1800,10000/480,10000/1105,10000/690,68,10000/1100],[1600,10000/485,10000/1105,10000/690,60,10000/1100],
                        [2400,10000/460,10000/1005,10000/690,72,10000/1000],[1600,10000/455,10000/1100,10000/735,75,10000/1250],[2000,10000/530,10000/1005,10000/630,60,10000/990],[2000,10000/530,10000/1005,10000/630,60,10000/990],[2000,10000/530,10000/1005,10000/630,60,10000/990],[2000,10000/530,10000/1005,10000/630,60,10000/990],[2000,10000/530,10000/1005,10000/630,60,10000/990]]
        UserWodPoints=[[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
        
        # Example of entries for user definition(These values will come from the data entered by the user in the app)
        # Thisis now used to create a dummy case
        # INPUTS: 
        UserDefinitionEntries=[[32,'H',175,71,'WhiteGym','NotScaled-Base'],[29,'M',165,55,'Crossfit Eolo','NotScaled-Base'],[29,'H',173,75,'WhiteGym','NotScaled-Base'],[25,'H',178,84,'WhiteGym','NotScaled-Advance'],[29,'H',175,73,'WhiteGym','NotScaled-Base'],[28,'H',186,83,'WhiteGym','NotScaled-Advance'],[34,'H',175,73,'WhiteGym','NotScaled-Advance'],[23,'M',165,55,'WhiteGym','NotScaled-Base'],[27,'M',151,61,'AgroBox','NotScaled-Base'],[27,'M',151,61,'AgroBox','NotScaled-Advance'],[27,'M',151,61,'AgroBox','NotScaled-Advance'],[27,'M',151,61,'AgroBox','NotScaled-Advance']]
        #Strength_BenchM_Inputs=[[130,170,105,85],[90,90,60,55]]
        #Haltero_BenchM_Inputs=[[71,100,95],[42,55,48]]
        # De momento lo meto así para generar Dummy automatico, el orden es por usuarioy dentro sel orden que aparece en self.UserBenchMarksDict
        Inputs_Benchmarks=[ [[130,170,105,85,65],[71,100,77,95,95]],  [[90,90,60,55,38],[42,55,38,52,51]],[[120,190,95,95,58],[80,100,80,95,95]] ,[[165,220,110,95,75],[88,110,85,105,98]] ,[[125,170,90,80,60],[70,95,65,95,95]] , [[140,200,105,105,65],[93,105,87,115,115]], [[130,200,105,100,75],[88,110,85,100,105]] ,[[80,80,62,50,51],[38,61,42,52,47]],[[64. , 64. , 49.6, 40. , 40.8],
               [30.4, 48.8, 33.6, 41.6, 37.6]],[[64. , 64. , 49.6, 40. , 40.8],[30.4, 48.8, 33.6, 41.6, 37.6]],[[64. , 64. , 49.6, 40. , 40.8],[30.4, 48.8, 33.6, 41.6, 37.6]],[[64. , 64. , 49.6, 40. , 40.8],[30.4, 48.8, 33.6, 41.6, 37.6]]]  
        
        self.Inputs_BenchmarksInit=[[[1,1,1,1,1],[1,1,1,1,1]]]
        self.DataBase={}
        self.DataBaseOwners={}
        '''
        # Loop to create the data base.
        self.DataBase={}
        
        
        for w1,userName in enumerate(self.UserNamesList):
            self.DataBase[userName]={}  
            self.DataBase[userName]['Definition']=dict.fromkeys(self.UserDefinition_List)
            self.DataBase[userName]['BenchMarks']={"Strength":dict.fromkeys(self.Strength_BenchM),"Haltero":dict.fromkeys(Haltero_BenchM)}# Esto daba error de enlazamiento de datos self.UserBenchMarksDict.copy()
            self.DataBase[userName]['WODmarks']=dict.fromkeys(self.WodNamesFlat)
            self.DataBase[userName]['RawWODmarks']=dict.fromkeys(self.WodNamesFlat)
            self.DataBase[userName]['WODpoints']=dict.fromkeys(self.WodNamesFlat)
            self.DataBase[userName]['WODpositions']=dict.fromkeys(self.WodNamesFlat)
            self.DataBase[userName]['WodResultsYoutube']=dict.fromkeys(self.WodNamesFlat)
            self.DataBase[userName]['Host']={}
            self.DataBase[userName]['Guest']={}
            for w2,userEntry in enumerate(zip(self.UserDefinition_List.copy(),UserDefinitionEntries.copy()[w1])):
                self.DataBase[userName]['Definition'][userEntry[0]]= userEntry[1]
                
            for w3,result in enumerate(zip(self.WodNamesFlat.copy(),UserWodEntries.copy()[w1])):
                self.DataBase[userName]['WODmarks'][result[0]]= result[1]
                self.DataBase[userName]['RawWODmarks'][result[0]]= str(result[1])
            for w4,points in enumerate(zip(self.WodNamesFlat.copy(),UserWodPoints.copy()[w1]))
                self.DataBase[userName]['WODpoints'][points[0]]= points[1] 
                self.DataBase[userName]['WODpositions'][points[0]]= '---'  
                self.DataBase[userName]['WodResultsYoutube'][points[0]] = '---'                
            # User becnhMarks                   
            # User becnhMarks
            for key in enumerate(self.UserBenchMarksDict.copy().keys()):

                for w3,activity_value in enumerate(zip(self.DataBase[userName]['BenchMarks'][key[1]],Inputs_Benchmarks.copy()[w1][key[0]])):

                    self.DataBase[userName]['BenchMarks'][key[1]][activity_value[0]]=activity_value[1]
        '''   
        if os.path.exists(os.path.join(os.getcwd(),'DataBase.users')):
            with open(os.path.join(os.getcwd(),'DataBase.users'), 'rb') as fin:
                self.DataBase=pickle.load(fin)
        if os.path.exists(os.path.join(os.getcwd(),'DataBaseOwners.users')):
            with open(os.path.join(os.getcwd(),'DataBaseOwners.users'), 'rb') as fin:
                self.DataBaseOwners=pickle.load(fin)    
 
        self.DummyWidget=widgets.Output()
        with self.DummyWidget:
            display()
     
        self.widgets_dict={"UserName":self.UserName,"PassWrod":self.PassWord,"WindowToPlot":self.WindowToPlot,"check":self.check}
        self.StatsCategory=widgets.RadioButtons(
        options=list(self.UserBenchMarksDict.keys()),
    #    value='pineapple', # Defaults to 'pineapple'
    #    layout={'width': 'max-content'}, # If the items' names are long
        description='',
        disabled=False,
        layout=Layout(width='auto'),
        )
        self.EnterNewPR=widgets.Button(
        value=False,
        description='Guardar',
        disabled=False,
        button_style='', # 'success', 'info', 'warning', 'danger' or ''
        #tooltip='Description',
        layout=Layout(width='auto'),
        icon='' # (FontAwesome names without the `fa-` prefix)
        )
        #print('Ha entrado al widgets_functon')
        self.NewPR=widgets.FloatText(
        value=0.0,
        description='PR:',
        disabled=False,
        #layout={'width': 'max-content'}
        layout=Layout(width='auto'),
        style={'description_width': '50px'}

        
        )

        self.widgets_dict["NewPR"]=self.NewPR
        self.widgets_dict["StatsCategory"]=self.StatsCategory
        self.widgets_dict["EnterNewPR"]=self.EnterNewPR
        # entries=self.Strength_BenchM se usa cuando no tenga el database inicial que uso para crear la aplicación
        #entries=list(self.DataBase[self.UserNamesList[0]]['BenchMarks'][self.widgets_dict["StatsCategory"].value].keys())
        entries=self.Strength_BenchM
        
        self.CategoryEtries=widgets.Dropdown(
        options=entries,
        value=entries[0],
        description='',
        layout={'width': 'max-content'},

        #layout=Layout(width='auto'),
        )
        

        self.widgets_dict["CategoryEtries"]=self.CategoryEtries

    
    def widgets_function(self):


        print('')
            
    def header_widget(self):
       #title=HTML(value=r'<p style="font-size:20px"><b>PRUEBAS</b>')#, layout=Layout(height='40px', width=width_col))#, border='2px solid gray'))

       file_image = open('LogoDummy.png', 'rb')
       image = file_image.read()

       header_image=Image(
         value=image,
         format='png', 
         width='400px'
       )
       grid=GridBox(children=[header_image],
         layout=Layout(
             width='90%',
             grid_template_rows='auto auto',
             grid_template_columns='auto',
        ))

       return grid
       
        
        
    def main(self):

        


        # Define tab structure
        self.grid = widgets.Tab() #layout=Layout(height="1500px"))
            
        self.grid.titles=['Acceso','Crear Atleta','Crear Box']

        LogIngrid=GridBox(children=[self.UserName,self.PassWord,self.LogIn,self.AvisoLogin],
                      layout=Layout(
                          width='auto',
                          grid_template_columns='auto',
                          grid_template_rows='auto auto auto auto',
                          grid_template_areas='''
                            "UserName"
                            "PassWord"
                            "LogIn"
                            "AvisoLogin"
                            '''
                          )
                     ) 


        NewUsergrid=widgets.GridBox(children=[self.NewUserName,self.NewOjo,self.ConfirmOjo,self.DateOfBirth,self.Gender,self.Box,self.AccessCode,self.Category,self.CreateNewUserButton,self.AvisoUserCreated],
                      layout=widgets.Layout(
                          width='auto',
                          grid_template_rows='auto auto auto auto auto auto auto auto auto auto',
                          grid_template_columns='auto',
                          grid_template_areas='''
                            "NewUserName"
                            "NewOjo"
                            "ConfirmOjo"
                            "DateOfBirth"
                            "Gender"
                            "Box"
                            "AccessCode"
                            "Category"
                            "CreateNewUser"
                            "AvisoUserCreated"
                            ''')
                                )
        NewBoxOwnergrid=widgets.GridBox(children=[self.NewUserName,self.NewOjo,self.ConfirmOjo,self.Box,self.AccessCode,self.CreateNewOwnerButton,self.AvisoUserCreated],
                      layout=widgets.Layout(
                          width='auto',
                          grid_template_rows='auto auto auto auto auto auto auto',
                          grid_template_columns='auto',
                          grid_template_areas='''
                            "NewUserName"
                            "NewOjo"
                            "ConfirmOjo"
                            "Box"
                            "AccessCode"
                            "CreateNewOwner"
                            "AvisoUserCreated"
                            ''')
                                )                        
        for i, title in enumerate(self.grid.titles):
            self.grid.set_title(i, title)
        self.grid.children=[LogIngrid,NewUsergrid,NewBoxOwnergrid]
        
        
        #Check if the username is in the DataBase and confirm the password to show the user interface
        def checkAccess(b):
            if((self.UserName.value in self.DataBase.keys() and bcrypt.checkpw(bytes(self.PassWord.value,'utf-8'), self.DataBase[self.UserName.value]['ojos'])) or (self.UserName.value in self.DataBaseOwners.keys() and bcrypt.checkpw(bytes(self.PassWord.value,'utf-8'), self.DataBaseOwners[self.UserName.value]['ojos'])) ): #Curro
                
            
                if(self.UserName.value in self.DataBase.keys() and bcrypt.checkpw(bytes(self.PassWord.value,'utf-8'), self.DataBase[self.UserName.value]['ojos'])):
                    self.typeUser='Atleta'

                    #print(self.typeUser,self.DataBase[self.UserName.value]['Definition']['HomeBox'])
                else:
                    self.typeUser='Owner'

                def rankmin(x):
                    u, inv, counts = np.unique(x, return_inverse=True, return_counts=True)
                    csum = np.zeros_like(counts)
                    csum[1:] = counts[:-1].cumsum()
                    return csum[inv]
                    #print(self.typeUser,self.DataBaseOwners[self.UserName.value]['HomeBox'])
                    
                
                titles=[]
                children=[]
                # This if select wether or not to generate the user profile (if Athlete yes, if Owner not)
                if(self.typeUser=='Atleta'):
                    # Defino un gridspeclayout para ahí definir el GridBox, con GridBox sólo no se actualiza
                    self.UserProfile_grid = GridspecLayout(2, 8)
                    titles.append('Perfil')
                    children.append(self.UserProfile_grid)
                    
                    self.plotUserProfile(name=self.widgets_dict['UserName'].value,benchmarkType=self.widgets_dict["StatsCategory"].value)
                    #TAB para el perfil de usuario
                    def actualizar(valor):
                        #print('ha entrado a actualizar widget')
                        entries=list(self.DataBase[self.widgets_dict["UserName"].value]['BenchMarks'][self.widgets_dict["StatsCategory"].value].keys())
                        #print(entries)
                        # self.CategoryEtries=widgets.Dropdown(
                        # options=entries,
                        # value=entries[0],
                        # description='PR selection:',
                        # )
    
                        # self.widgets_dict["CategoryEtries"]=self.CategoryEtries
                        self.widgets_dict["CategoryEtries"].options=entries 
                        self.widgets_dict["CategoryEtries"].index=1
                        self.plotUserProfile(name=self.widgets_dict['UserName'].value,benchmarkType=self.widgets_dict["StatsCategory"].value)
                        for i in range(len(self.stafigure)):
                            self.wid_plot[i].clear_output()
                            with self.wid_plot[i]:
                                display(self.stafigure[i]) 
                    self.StatsCategory.observe(actualizar,'value')
                    
                    
                    
                    
                    def EnterNewPR(b):
                        #inicio=time.time()
                        if os.path.exists(os.path.join(os.getcwd(),'DataBase.users')):
                            with open(os.path.join(os.getcwd(),'DataBase.users'), 'rb') as fin:
                                self.DataBase=pickle.load(fin)
                        if(self.widgets_dict["NewPR"].value>0):
                            self.DataBase[self.widgets_dict["UserName"].value]['BenchMarks'][self.widgets_dict["StatsCategory"].value][self.widgets_dict["CategoryEtries"].value]=self.widgets_dict["NewPR"].value
                        fin=time.time()
                        #print(fin-inicio)
                            
                        self.plotUserProfile(name=self.widgets_dict['UserName'].value,benchmarkType=self.widgets_dict["StatsCategory"].value)
                        for i in range(len(self.stafigure)):
                            self.wid_plot[i].clear_output()
                            with self.wid_plot[i]:
                                display(self.stafigure[i]) 
                                
                                
                                
                                
                        if os.path.exists(os.path.join(os.getcwd(),'DataBase.users')):
                            with open(os.path.join(os.getcwd(),'DataBase.users'), 'wb') as fout:
                                        pickle.dump(self.DataBase, fout)
                    self.EnterNewPR.on_click(EnterNewPR)
                    
                    
                    
                    
                    griduserPLot=GridspecLayout(3, 1)
                    self.wid_plot=[]
                    for i in range(len(self.stafigure)):
                        self.wid_plot.append(widgets.Output(layout={'border': '1px none black'}))
                        with self.wid_plot[i]:
                            display(self.stafigure[i])   
                        griduserPLot[i,0]=self.wid_plot[i]
                        
                    griduser=GridBox(children=[self.StatsCategory,self.widgets_dict['CategoryEtries'],self.NewPR,self.EnterNewPR],
                    layout=Layout(
                    width='auto',
                    grid_template_rows='auto auto auto auto',
                    grid_template_columns='100%',
                    )
                    )
                    
                    
                    self.UserProfile_grid[0,0:3]=griduser
                    self.UserProfile_grid[0:2,3:8]=griduserPLot
                
                
                #***********************************************************************
                
                
                
                
                
                #**********************************************************************************************************************************
                #**********************************************************************************************************************************
                #**********************************************************************************************************************************
                #**********************************************************************************************************************************
                # WODs & Callenges
                self.Wods_grid = GridspecLayout(39,10,width='auto',height='auto')  
                if(self.typeUser=='Atleta'):    
                    self.Category.value=self.DataBase[self.UserName.value]['Definition']['Category']

                elif(self.typeUser=='Owner'):
                    self.Category.value=self.CategoryList[0]
                    
                    
                titles.append('Wods')
                children.append(self.Wods_grid)
                
                
                def MonthSelected(month):
                    self.indiceMonth=self.CalendarMonths.index(month.description)

                    self.WodorChaSelection.options=self.WodNames[self.indiceMonth]
                    self.WodorChaSelection.value=self.WodNames[self.indiceMonth][0]
                    changeWODorChallenge('valor')
                    
                    
                    
                    
                    
                    
                self.Months_widgets=[]
                self.children_months=[]
                for i,month in enumerate(self.CalendarMonths):
                    if(month in self.ActiveMonths):
                        disabledValue=False
                    else:
                        disabledValue=True
                    
                    self.Months_widgets.append(widgets.Button(
                                value=False,
                                description=month,
                                disabled=disabledValue,
                                indent=False,
                                layout=Layout(width='auto', grid_area=month),
                                
                    ))
                    self.children_months.append(self.Months_widgets[i])
                    self.Months_widgets[i].on_click(MonthSelected)

                self.Monthsgrid=widgets.GridBox(children=self.children_months,
                              layout=widgets.Layout(
                                  width='100%',
                                  height='auto',
                                  grid_template_rows='auto',
                                  grid_template_columns='auto',
                                  grid_template_areas='''
                                    "Enero"
                                
                                    ''')) 
                                         
                self.WodorChallenge=widgets.RadioButtons(
                #options=['Wods', 'Challenges'],
                options=['Wods'],
                description='',
                orientation='horizontal',
                disabled=False,
                indent=False,
                layout=Layout(height='auto',width='auto', align = 'left'),
                )
                style = {'description_width': '35px'}
                self.WodorChaSelection=widgets.Dropdown(
                options=self.WodNames[0],
                value=self.WodNames[0][0],
                indent=False,
                description='Wod',
                layout=Layout(height='auto',width='max-content'),
                style=style
                )
                
                file= open(os.path.join(os.getcwd(),self.WodorChaSelection.value+'_'+self.Category.value+'.png'), "rb")
                image = file.read()
                self.WOD_image =widgets.Image(
                    value=image,
                    format='png',
                    width='auto',
                    height='453px',
                    
                )
                
                
                #self.gridSLMarks= GridspecLayout(3, 3,layout=Layout(width='auto'))
                
                def changeWODorChallenge(valor):
                    style = {'description_width': '35px'}
                    self.AvisoFormato.value="<b></b>"

                    file= open(os.path.join(os.getcwd(),self.WodorChaSelection.value+'_'+self.Category.value+'.png'), "rb")
                    if(self.typeUser=='Owner'):
                        Disabled=True
                        
                    elif((self.Category.value==self.DataBase[self.UserName.value]['Definition']['Category']) and ((self.CalendarEndDates[self.indiceMonth]-datetime.date.today()).days>=0) and (datetime.date.today()>=self.StartDate) ):

                        Disabled=False
                    else:
                        Disabled=True

                    self.youIDwidget.disabled=Disabled
                    '''
                    self.youIDwidget=widgets.Text(
                            value='',
                            description='Youtube',
                            disabled=Disabled,
                            layout=widgets.Layout(
                                width='50px')
                            )
                    '''       
                    #self.gridSLMarks[3,0]=self.youIDwidget
                    image = file.read()
                    self.WOD_image.value=image
                    
                    indice=self.WodNames[self.indiceMonth].index(self.WodorChaSelection.value)
                    video=self.YoutubeIDs[self.indiceMonth][indice]
                    vid=YouTubeVideo(video,width=320)
                    tipoWod=self.markType[self.indiceMonth][indice]
                    if(tipoWod=='Reps' or tipoWod=='Kgs'): 

                        self.Wods_grid[3,0:4]=widgets.IntText(
                                value=0,
                                description=tipoWod,
                                disabled=Disabled,
                                layout=widgets.Layout(
                                    width='auto'),
                                style =style
                                )
                        self.Wods_grid[3,4:7]=self.DummyWidget
                    elif(tipoWod=='Time'):
                        self.Wods_grid[3,0:4]=widgets.IntText(
                                value=0,
                                indent=False,
                                description='min:',
                                disabled=Disabled,
                                layout=widgets.Layout(
                                    width='auto'),
                                style = style
                                )
                        self.Wods_grid[3,4:7]=widgets.IntText(
                                value=0,
                                description='sec:',
                                disabled=Disabled,
                                layout=widgets.Layout(
                                    width='auto'),
                                style = style
                                )
                        '''
                        gridTime=GridBox(children=[minutes,sec],
                          layout=Layout(
                              border='solid',
                              width='45%',
                              grid_template_rows='auto auto',
                              grid_template_columns='auto',
                         ))
                        '''
                        #self.gridSLMarks[0:1,0]=gridTime
                        
                    
                    self.wid_Youtube.clear_output()
                    with self.wid_Youtube:
                        display(vid)

                    

                   # Hasta aqui ahora trbajando 
                    
                    
                self.WodorChaSelection.observe(changeWODorChallenge,'value')

                self.Category.observe(changeWODorChallenge,'value')
                self.indiceMonth=0
                indice=self.WodNames[self.indiceMonth].index(self.WodorChaSelection.value)
                video=self.YoutubeIDs[self.indiceMonth][indice]
                vid=YouTubeVideo(video,width=320)
                #vid=YouTubeVideo("z1f-RKOHT4g")
                self.wid_Youtube=widgets.Output(layout=Layout(width='auto',height='auto'))
                with self.wid_Youtube:
                    display(vid)  
                if(self.typeUser=='Atleta'):    
                
                    if(self.Category.value==self.DataBase[self.UserName.value]['Definition']['Category']  and ((self.CalendarEndDates[self.indiceMonth]-datetime.date.today()).days>=0) and (datetime.date.today()>=self.StartDate)):
                        Disabled=False
                    else:
                        Disabled=True
                elif(self.typeUser=='Owner'):
                        Disabled=True
                        

                style = {'description_width': '35px'}
                

                self.youIDwidget=widgets.Text(
                        value='',
                        description='URL',
                        disabled=Disabled,
                        indent=False,
                        layout=widgets.Layout(
                        width='auto'),
                        style=style
                        )
                        
                self.Wods_grid[4,0:7]=self.youIDwidget
                if(self.markType[0][0]=='Reps' or self.markType[0][0]=='Kgs'): 

                    self.Wods_grid[3,0:4]=widgets.IntText(
                            value=0,
                            description=self.markType[0][0],
                            disabled=Disabled,
                            indent=False,
                            layout=widgets.Layout(
                                width='auto'),
                            style=style
                            )
                    self.Wods_grid[3,4:7]=self.DummyWidget
                elif(self.markType[0][0]=='Time'):
                    self.Wods_grid[3,0:4]=widgets.IntText(
                            value=0,
                            description='min:',
                            disabled=Disabled,
                            layout=widgets.Layout(
                                width='auto'),
                            style=style
                            )
                    self.Wods_grid[3,4:7]=widgets.IntText(
                            value=0,
                            description='sec:',
                            disabled=Disabled,
                            layout=widgets.Layout(
                                width='auto'),
                            style=style
                            )
                    '''
                    gridTime=GridBox(children=[minutes,sec],
                      layout=Layout(
                          border='solid',
                          width='45%',
                          grid_template_rows='auto auto',
                          grid_template_columns='auto',
                     ))
                    
                    self.gridSLMarks[0:1,0]=gridTime
                    '''
                #self.gridSLMarks[0,0]=


                self.Wods_grid[5,0:7]=widgets.Button(
                                    value=False,
                                    description='Guardar resultado',
                                    disabled=False,
                                    indent=False,
                                    layout=Layout(width='auto', grid_area='LogIn'),
                                    style=style
                                        
                            )
                
                

                self.AvisoFormato=widgets.HTML(
                            value="<b></b>",
                            placeholder='',
                            description='',
                            indent=False,
                            layout=Layout(width='auto'),
                            style=style
                        )

                self.Wods_grid[3,7:]=self.AvisoFormato

                
                def EnterResult(valor):
                    
                    if os.path.exists(os.path.join(os.getcwd(),'DataBase.users')):
                        with open(os.path.join(os.getcwd(),'DataBase.users'), 'rb') as fin:
                            self.DataBase=pickle.load(fin)
                            
                    #time.sleep(15)
                    if((self.CalendarEndDates[self.indiceMonth]-datetime.date.today()).days>=0):
                    #if(self.DataBase[self.widgets_dict['UserName'].value]['WODmarks'][self.WodorChaSelection.value]==None):
                        indice=self.WodNames[self.indiceMonth].index(self.WodorChaSelection.value)
                        
                        if(self.markType[self.indiceMonth][indice]=='Reps'):  
                            if(self.Wods_grid[3,0:4].value>10000):
                                self.AvisoFormato.value="<b>Not valid data</b>"
                            else:
                                self.DataBase[self.widgets_dict['UserName'].value]['WODmarks'][self.WodorChaSelection.value]=self.Wods_grid[3,0:4].value
                                self.DataBase[self.widgets_dict['UserName'].value]['RawWODmarks'][self.WodorChaSelection.value]=str(self.Wods_grid[3,0:4].value)
                                self.AvisoFormato.value="<b>Data saved</b>"
                        if(self.markType[self.indiceMonth][indice]=='Kgs'):  
                            if(self.Wods_grid[3,0:4].value>10000):
                                self.AvisoFormato.value="<b>Not valid data</b>"
                            else:
                                self.DataBase[self.widgets_dict['UserName'].value]['WODmarks'][self.WodorChaSelection.value]=self.Wods_grid[3,0:4].value
                                self.DataBase[self.widgets_dict['UserName'].value]['RawWODmarks'][self.WodorChaSelection.value]=str(self.Wods_grid[3,0:4].value)
                                self.AvisoFormato.value="<b>Data saved</b>"
                        if(self.markType[self.indiceMonth][indice]=='Time'):   
                            # Arreglar en caso de que metan mas de dos cifras
                            minutos=self.Wods_grid[3,0:4].value
                            segundos=self.Wods_grid[3,4:7].value
                            
                            if((minutos>59 or segundos>59) or (minutos==0 and segundos==0)):
                                self.AvisoFormato.value="<b>Not valid data</b>"
                            else: 
                                self.DataBase[self.widgets_dict['UserName'].value]['RawWODmarks'][self.WodorChaSelection.value]=str(minutos)+":"+str(segundos)
                                self.DataBase[self.widgets_dict['UserName'].value]['WODmarks'][self.WodorChaSelection.value]=10000/(60*minutos+segundos)
                                self.AvisoFormato.value="<b>Data saved</b>"
                        self.DataBase[self.widgets_dict['UserName'].value]['WodResultsYoutube'][self.WodorChaSelection.value]=self.youIDwidget.value
                        self.LeaderBoard=LeaderBoardGeneration()
                        self.wid_LeaderBoard.clear_output()
                        with self.wid_LeaderBoard:
                            display(self.LeaderBoard) 
                        
                        with open(os.path.join(os.getcwd(),'DataBase.users'), 'wb') as fout:
                                    pickle.dump(self.DataBase, fout)
                    #else:
                        #self.AvisoFormato.value="<b>Data already exists</b>"
                
                self.Wods_grid[5,0:7].on_click(EnterResult) 
                #self.gridSLMarks[2,0:1].on_click(EnterResult)
                    
                
                self.Wods_grid[0,0:]=self.Monthsgrid
                self.Wods_grid[1:3,0:4]=self.WodorChallenge
                self.Wods_grid[2,5:]=self.WodorChaSelection
                self.Wods_grid[1,5:]=self.Category
                #self.Wods_grid[3:6,0:9]=self.gridSLMarks
                self.Wods_grid[6:20,:]=self.WOD_image
                self.Wods_grid[20:31,:]=self.wid_Youtube             
                    
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                '''
                self.LeaderBoard=LeaderBoardGeneration()
                self.wid_LeaderBoard=widgets.Output(layout=Layout(width='auto', grid_area='LeaderBoard'))
                with self.wid_LeaderBoard:
                    display(self.LeaderBoard)  
                '''   
                # Widgets for leaderboard sorting
                
                
                self.Video_LeaderBoard=widgets.Checkbox(
                            value=False,
                            description='Videos',
                            disabled=False,
                            indent=False,
                            layout=Layout(width='auto', grid_area='Video_LeaderBoard'),
                            
                )
                
                if(self.typeUser=='Atleta'):    
                    valuecat=self.DataBase[self.UserName.value]['Definition']['Category']
                    valuegen=self.DataBase[self.UserName.value]['Definition']['Gender']

                elif(self.typeUser=='Owner'):
                    valuecat='Pro'
                    valuegen='Mix'
                        
                self.Category_LeaderBoard=widgets.Dropdown(
                options=self.CategoryList,
                value=valuecat,
                description='Categoría',
                layout=Layout(width='auto', grid_area='Category_LeaderBoard'),
                )
                
                stylegenlead = {'description_width': '48px'}
                self.Gender_LeaderBoard=widgets.Dropdown(
                options=[('Mixta','Mix'),('Femenina', 'M'),('Masculina', 'H')],
                value=valuegen,
                description='División',
                layout=Layout(width='auto', grid_area='Gender_LeaderBoard'),
                style=stylegenlead
                )
                
                
                self.colNames=(self.ActiveWodNamesFlat.copy())
                self.colNames.insert(0,'Total')
                
                self.WOD_LeaderBoard=widgets.Dropdown(
                    options=self.colNames,
                    value=self.colNames[0],
                    description='Wod',
                    layout=Layout(width='auto', grid_area='WOD_LeaderBoard'),
                    )   
                      
                # LeaderBoard
                def LeaderBoardGeneration():
                    Category=self.Category_LeaderBoard.value
                    Gender=self.Gender_LeaderBoard.value
                    video=self.Video_LeaderBoard.value
                    #ResultadosNotScaledBaseMen=[]
                    KeysNotScaledBaseMen=[]
                    Resultados=[]
                    Color=[]
                    #self.rawMarks=[]
                    Names=[]
                    #ResultadosNotScaledBaseWomen=[]
                    #ResultadosNotScaledAdvanceMen=[]
                    #ResultadosNotScaledAdvanceWomen=[]
                    # Esta parte se llama cuando ploteas leaderboard: Primero se lee el DataBase por is alguien ha metido datos nuevos y se sacan los
                    # resultados por wod y los nombres según categoria y sexo seleccionados
                    keys=self.DataBase.keys()
                    for i in range(len(keys)):
                        temp=[]
                        color_temp=[]
                        #temp2=[]
                        
                        if(self.DataBase[list(keys)[i]]['Definition']['Category']==Category):
                    
                            if(self.DataBase[list(keys)[i]]['Definition']['Gender']==Gender or Gender=='Mix'):
                                
                                self.DondeVideo=np.asarray([('outube' in str(self.DataBase[list(keys)[i]]['WodResultsYoutube'][wod])) for wod in self.ActiveWodNamesFlat])==True
                                self.DondeResult=np.asarray([((self.DataBase[list(keys)[i]]['WODmarks'][wod]))!=None for wod in self.ActiveWodNamesFlat])==True
                                AnyVideo=np.all(self.DondeVideo==self.DondeResult)
                                if(video==False or video==AnyVideo):
                                    for key in(self.DataBase[list(keys)[i]]['WODmarks']):
                                        if(key in self.ActiveWodNamesFlat):
                                            if(self.DataBase[list(keys)[i]]['WODmarksCorrected'][key]!=None):
                                                #print('Ha pillado que hay corrected')
                                                temp.append(self.DataBase[list(keys)[i]]['WODmarksCorrected'][key])
                                            else:
                                                temp.append(self.DataBase[list(keys)[i]]['WODmarks'][key])
                                                
                                            # Obtener colores del LeaderBoard    
                                            if(self.DataBase[list(keys)[i]]['WODmarksCorrected'][key]!=None):
                                                color_temp.append('color:lightgreen')
                                            
                                            elif('youtube' in str(self.DataBase[list(keys)[i]]['WodResultsYoutube'][key])): # Crear un buen condicional, aunque debería de valer
                                                color_temp.append('color:lightblue')
                                            else:
                                                color_temp.append('color:black')
                                            


                                    Resultados.append(temp)
                                    Color.append(color_temp)
                                    Names.append(list(keys)[i])

                    self.OriginalColor=pd.DataFrame(Color)
                    self.Color=pd.DataFrame(Color)
                    self.Color.insert(0, 'Puntos', len(self.Color)*['color:black'])
                    self.Names=Names
                    self.Resultados=Resultados

                    if(np.shape((np.asarray(Resultados)))[0]>0):   

                        # Una vez sacados estos datos, se realiza la puntuación y ordenación
                        for i in range(np.shape((np.asarray(Resultados)))[1]):
                            wodName=self.WodNamesFlat.copy()[i]
                            datos=np.asarray(Resultados)[:,i]
                            notnone=np.where(datos!=None)[0].tolist()
                            NombresConResultados=np.asarray(Names)[notnone]
                            positions=rankmin(-datos[notnone])
                            orden=np.linspace(0,len(notnone)-1,len(notnone)).astype(int)

                            if(len(notnone)==1):
                                Puntos=[100]
                            else:

                                #Puntos=(np.round((100-(orden*(99/(len(orden)-1)))))).astype(int)
                                Puntos=(100-(orden*(99/(len(orden)-1))))
                                #Puntos=np.round((100-(orden*(99/(len(orden)-1)))),1)
                            for j,Nombre in enumerate(NombresConResultados):

                                self.DataBase[Nombre]['WODpoints'][wodName]=Puntos[positions[j]]   
                                self.DataBase[Nombre]['WODpositions'][wodName]=positions[j]+1

        
                        Points=[]
                        Positions=[]
                        self.rawMarks=[]
                        WodResultsYoutube=[]
                        for i in range(len(keys)):
                            temp=[]
                            temp2=[]
                            temp3=[]
                            temp4=[]
                            if(self.DataBase[list(keys)[i]]['Definition']['Category']==Category):
                        
                                if(self.DataBase[list(keys)[i]]['Definition']['Gender']==Gender or Gender=='Mix'):
                                    self.DondeVideo=np.asarray([('youtube' in str(self.DataBase[list(keys)[i]]['WodResultsYoutube'][wod])) for wod in self.ActiveWodNamesFlat])==True
                                    self.DondeResult=np.asarray([((self.DataBase[list(keys)[i]]['WODmarks'][wod]))!=None for wod in self.ActiveWodNamesFlat])==True
                                    AnyVideo=np.all(self.DondeVideo==self.DondeResult)
                                    
                                    if(video==False or video==AnyVideo):
                                        for key in (self.DataBase[list(keys)[i]]['WODpoints']):
                                            if(key in self.ActiveWodNamesFlat):
                                                temp.append(self.DataBase[list(keys)[i]]['WODpoints'][key])
                                                
                                                if(self.DataBase[list(keys)[i]]['WODmarksCorrected'][key]!=None):
                                                    temp2.append(self.DataBase[list(keys)[i]]['RawWODmarksCorrected'][key])
                                                else:
                                                    temp2.append(self.DataBase[list(keys)[i]]['RawWODmarks'][key])
                                                temp3.append(self.DataBase[list(keys)[i]]['WODpositions'][key])
                                                temp4.append(self.DataBase[list(keys)[i]]['WodResultsYoutube'][key])

                                        
                                        Points.append(temp)
                                        self.rawMarks.append(temp2)
                                        Positions.append(temp3)
                                        WodResultsYoutube.append(temp4)
                                        

                                        Points[-1].insert(0,np.sum(np.asarray(Points[-1])))
                                        self.rawMarks[-1].insert(0,np.sum(np.asarray(Points[-1])))
                                        Positions[-1].insert(0,np.sum(np.asarray(Points[-1])))
                                        WodResultsYoutube[-1].insert(0,np.sum(np.asarray(Points[-1])))

                                        KeysNotScaledBaseMen.append(list(keys)[i])
                                        #Points[i].insert(0,np.sum(np.asarray(temp)))
                        #print(Points)
                        self.tempdataframe=Points.copy()
                        '''
    
                        '''
                        
                        
                        
                        self.Points=Points
                        self.Positions=Positions
                        colNames_rawData=[s+'_rawData'for s in self.colNames]
                        colNames_positions=[s+'_positions'for s in self.colNames]
                        colNames_WodResultsYoutube=[s+'_youtube'for s in self.colNames]
                        self.PointsDataFrame=(pd.DataFrame(self.Points,columns=self.colNames,index=self.Names)).round(1)
                        self.Color.columns=self.colNames
                        self.Color.index=self.Names
                        self.IndiceDataFrame=self.PointsDataFrame.sort_values(by='Total', ascending=False)
                        self.Color=self.Color.reindex(self.IndiceDataFrame.index)
                        posprueba=[]
                        for i in range(len(self.IndiceDataFrame['Total'].values)):
                            
                            if ((self.IndiceDataFrame['Total'].values[i]!=self.IndiceDataFrame['Total'].values[i-1]) or i==0):
                                posprueba.append(i+1)
                                
                            else:
                                posprueba.append(posprueba[i-1])
                        self.posprueba=posprueba
                                
                        Indice=pd.Index([j+' ('+str(posprueba[i])+')' for i,j in enumerate(self.IndiceDataFrame.index)])
                        self.indice=Indice

                        
                        
                        rawMarksDataFrame=pd.DataFrame(self.rawMarks,columns=colNames_rawData,index=self.Names)
                        PositionsDataFrame=pd.DataFrame(self.Positions,columns=colNames_positions,index=self.Names)
                        self.colNames_WodResultsYoutubeDataFrame=pd.DataFrame(WodResultsYoutube,columns=colNames_WodResultsYoutube,index=self.Names)
                        

                        self.prueba3=pd.concat([self.PointsDataFrame,PositionsDataFrame,rawMarksDataFrame,self.colNames_WodResultsYoutubeDataFrame], axis=1)
                        self.prueba3=self.prueba3.sort_values(by='Total', ascending=False)
                        self.prueba3=self.prueba3.set_index(Indice)
                        
                        
                        self.Color.index=self.prueba3.index.copy()
                        self.Color.index=self.prueba3.index.copy()
                        # Aquí se ordenan los dos dataframe por puntos totales o por mwod antes de unirlos
                        self.prueba3=self.prueba3.sort_values(by=self.WOD_LeaderBoard.value, ascending=False)
                        
                        
                        
                        
                        self.final=pd.DataFrame(columns=self.colNames,index=self.prueba3.index)
                        self.final2=pd.DataFrame(columns=self.colNames,index=self.prueba3.index)
                        for i in range(len(self.colNames)):
                            if(self.colNames[i]=='Total'):
                                self.final[self.colNames[i]] = self.prueba3[self.colNames[i]].map(str)
                                self.final2[self.colNames[i]] = self.prueba3[self.colNames[i]].map(str)
                            else:
                                
                                #self.final[self.colNames[i]] = self.PointsDataFrame[self.colNames[i]].map(str) + ' (' + self.prueba[colNames_rawData[i]].map(str)+ ')'
                                self.final[self.colNames[i]] = self.prueba3[colNames_positions[i]].map(str) + ' (' + self.prueba3[colNames_rawData[i]].map(str)+ ')'
                                self.final2[self.colNames[i]] = self.prueba3[colNames_positions[i]].map(str) + ' (' + self.prueba3[colNames_WodResultsYoutube[i]].map(str)+ ')'
                    
                    else:
                        self.final=pd.DataFrame(columns=self.colNames)
                        self.final2=pd.DataFrame(columns=self.colNames)

                    if(video):
                        #export=self.final2
                        export=self.final
                    else:
                        export=self.final
                    

                    self.Color=self.Color.reindex(export.index)
                    self.Color.index=export.index.copy()
                    if(len(self.Color)>0):
                        export=export.style.apply(lambda _: self.Color, axis=None)
                    
                    
                    
                    
                    return  export
                
                self.LeaderBoard=LeaderBoardGeneration()
                self.wid_LeaderBoard=widgets.Output(layout=Layout(width='auto', grid_area='LeaderBoard'))
                with self.wid_LeaderBoard:
                    display(self.LeaderBoard) 
                
                
                
                def SortLeaderBoard(valor):
                    self.LeaderBoard=LeaderBoardGeneration()
                    self.wid_LeaderBoard.clear_output()
                    with self.wid_LeaderBoard:
                        display(self.LeaderBoard) 
                
                self.Category_LeaderBoard.observe(SortLeaderBoard,'value')
                self.Gender_LeaderBoard.observe(SortLeaderBoard,'value')
                self.WOD_LeaderBoard.observe(SortLeaderBoard,'value')
                self.Video_LeaderBoard.observe(SortLeaderBoard,'value')
                self.DummyWidget2=widgets.HTML(
                disabled=True,
                value="<b></b>",
                    placeholder='',
                description='',
                layout=Layout(width='170px', grid_area='Dummy',border='None')
                )

               # "Video_LeaderBoard Category_LeaderBoard Gender_LeaderBoard WOD_LeaderBoard"
               #,self.Gender_LeaderBoard,self.WOD_LeaderBoard
                LeaderBoardgrid=widgets.GridBox(children=[self.Video_LeaderBoard,self.Category_LeaderBoard,self.wid_LeaderBoard,self.DummyWidget2,self.Gender_LeaderBoard,self.WOD_LeaderBoard],
                              layout=widgets.Layout(
                                  width='auto',
                                  grid_template_rows='auto auto auto auto',
                                  grid_template_columns='auto auto auto auto',
                                  grid_template_areas='''
                                    "Video_LeaderBoard Category_LeaderBoard Dummy Dummy"
                                    "Gender_LeaderBoard WOD_LeaderBoard Dummy Dummy"
                                    "LeaderBoard LeaderBoard LeaderBoard LeaderBoard"
                                    "LeaderBoard LeaderBoard LeaderBoard LeaderBoard"
                                    ''')
                                        ) 
                
                
                #self.LeaderBoard_grid = GridspecLayout(2, 3,width='auto',height='700px')
                #self.LeaderBoard_grid = GridspecLayout(2, 3,width='auto',height='auto')
                #self.LeaderBoard_grid[1,0:2]=self.wid_LeaderBoard
                titles.append('Clasificación')
                #children.append(self.LeaderBoard_grid)
                children.append(LeaderBoardgrid)
                

#***************************************************************************************************************
#***************************************************************************************************************
#***************************************************************************************************************
#***************************************************************************************************************







                # TODO ESTO QUEDA PENDIENTE, QUIERO HACER UN CALENDARIO DE BOTONES PARA QUE DESPLIEGUEN LAS INVITACIONES CREADAS
                Optionswod=self.WODcaledarOptions.copy() # Curro
                Optionswod.insert(0,'Cualquiera')
                Optionsbox=self.BoxListHost.copy()
                Optionsbox.insert(0,'Cualquiera')
                Optionscat=self.CategoryList.copy()
                Optionscat.insert(0,'Cualquiera')
                self.PreviousDaySelected=None
                self.LeagueCalendarGrid= GridspecLayout(15,7,width='320px',height='auto')  
                '''
                self.DummyWidget=widgets.Output()
                with self.DummyWidget:
                    display()
                '''
                '''        
                widgets.Text(
                        value='',
                        description='',
                        disabled=True,
                        layout=widgets.Layout(
                            width='auto',border=None)
                        )
                '''  

                self.OpenSpots_widget_Locals=widgets.IntText(
                    value=0,
                    description='Locales',
                    style={'description_width': '50px'},
                    disabled=False,
                    layout=Layout(width='auto')
                )
                self.OpenSpots_widget_Visitors=widgets.IntText(
                    value=0,
                    description='Visitantes',
                    style={'description_width': '75px'},
                    disabled=False,
                    layout=Layout(width='auto')
                )
                self.AvailableInvitations=widgets.Output(layout={'border': '1px none black'})


                Time_picker = ipydatetime.TimePicker(
                    description='Hora',
                    
                    
                    
                    
                    )
                def ColorActiveFilteredDays(b):
                    
                    
                    if os.path.exists(os.path.join(os.getcwd(),'DataBaseOwners.users')):
                        with open(os.path.join(os.getcwd(),'DataBaseOwners.users'), 'rb') as fin:
                            self.DataBaseOwners=pickle.load(fin)
                    '''
                    for limpiar in (self.Days_Calendar_widget):
                        limpiar.style.button_color=None
                        limpiar.layout.border=None
                        Days_Calendar_np=np.asarray(self.Days_Calendar)
                        #active_days
                    '''    
                    if(self.HostorGuest.value=='Ver HEATS'):
                        for limpiar in (self.Days_Calendar_widget):
                            limpiar.style.button_color=None
                            limpiar.layout.border=None
                            Days_Calendar_np=np.asarray(self.Days_Calendar)
                            #active_days
                        
                        # Give blue color to any dat in the calendar qit any invitation open
                        '''
                        for key in (self.DataBaseOwners.keys()):

                            for dia in(self.DataBaseOwners[key]['Host'].keys()):
                                activedaysinmonth=np.where(Days_Calendar_np==dia)[0]
                                if(len(activedaysinmonth)>0):
                                    self.Days_Calendar_widget[activedaysinmonth[0]].style.button_color='lightblue'
                        '''                
                        # Give green color to open invitations that fits the filtets and the category
                        diasyaenverde=[]
                        for key in (self.DataBaseOwners.keys()):


                            for dia in(self.DataBaseOwners[key]['Host'].keys()):

                                if dia not in diasyaenverde:
                                    activedaysinmonth=np.where(Days_Calendar_np==dia)[0]

                                    if(len(activedaysinmonth)>0):

                                        #if((sameSubDiv and (self.DataBase[key]['Host'][dia][1]==self.WOD_filter.value or self.WOD_filter.value=='All') and (self.DataBase[key]['Definition']['HomeBox']==self.BOX_filter.value or self.BOX_filter.value=='All')) or ((((self.DataBase[key]['Host'][dia][1]==Optionswod[1]==self.WOD_filter.value) or ((self.DataBase[key]['Host'][dia][1]==Optionswod[1]) and (self.WOD_filter.value=='All'))) and (self.DataBase[key]['Definition']['HomeBox']==self.BOX_filter.value or self.BOX_filter.value=='All')))    ):
                                        for horadeldia in self.DataBaseOwners[key]['Host'][dia].keys():
                                            if((self.DataBaseOwners[key]['Host'][dia][horadeldia][1]==self.WOD_filter.value or self.WOD_filter.value=='Cualquiera') and (self.DataBaseOwners[key]['HomeBox']==self.BOX_filter.value or self.BOX_filter.value=='Cualquiera') and (self.Category_filter.value in self.DataBaseOwners[key]['Host'][dia][horadeldia][2]  or self.Category_filter.value=='Cualquiera')):
    
                                                if(self.typeUser=='Atleta'):
    
                                                    #sameDiv=(self.DataBase[self.widgets_dict["UserName"].value]['Definition']['Category'] in self.DataBaseOwners[key]['Host'][dia][2])  
    
                                                    if ((self.widgets_dict["UserName"].value in self.DataBaseOwners[key]['Host'][dia][horadeldia][-1]) or (self.widgets_dict["UserName"].value in self.DataBaseOwners[key]['Host'][dia][horadeldia][-2])):
                                                        self.Days_Calendar_widget[activedaysinmonth[0]].style.button_color='lightblue'
                                                        self.Days_Calendar_widget[activedaysinmonth[0]].layout.border='solid 2px black'
                                                        diasyaenverde.append(dia)
                                                        
                                                    else:
                                                        self.Days_Calendar_widget[activedaysinmonth[0]].layout.border='solid 2px black'
                                                        
                                                    '''
                                                    if not sameDiv:
                                                        #self.Days_Calendar_widget[activedaysinmonth[0]].style.button_color='lightblue'
                                                        self.Days_Calendar_widget[activedaysinmonth[0]].layout.border='solid'
                                                    else:
                                                        self.Days_Calendar_widget[activedaysinmonth[0]].style.button_color='lightgreen'
                                                        diasyaenverde.append(dia)
                                                    '''                            
                                                if(self.typeUser=='Owner'):
                                                    OwnBox=(self.DataBaseOwners[self.widgets_dict["UserName"].value]['HomeBox']==self.DataBaseOwners[key]['HomeBox'])
    
                                                    if OwnBox:
                                                        self.Days_Calendar_widget[activedaysinmonth[0]].style.button_color='lightblue'
                                                        self.Days_Calendar_widget[activedaysinmonth[0]].layout.border='solid 2px black'
                                                        diasyaenverde.append(dia)
                                                    else:
                                                    
                                                    #self.Days_Calendar_widget[activedaysinmonth[0]].style.button_color='lightblue'
                                                        self.Days_Calendar_widget[activedaysinmonth[0]].layout.border='solid 2px black'
                                                    
    
                                            else:
                                                
                                                if(self.typeUser=='Owner'):
                                                    OwnBox=(self.DataBaseOwners[self.widgets_dict["UserName"].value]['HomeBox']==self.DataBaseOwners[key]['HomeBox'])
                                                    if(OwnBox):
                                                        self.Days_Calendar_widget[activedaysinmonth[0]].style.button_color='lightblue'
                                                elif(self.typeUser=='Atleta'):
    
    
    
                                                    if ((self.widgets_dict["UserName"].value in self.DataBaseOwners[key]['Host'][dia][horadeldia][-1]) or (self.widgets_dict["UserName"].value in self.DataBaseOwners[key]['Host'][dia][horadeldia][-2])):
                                                        self.Days_Calendar_widget[activedaysinmonth[0]].style.button_color='lightblue'

                                    
                    if(self.HostorGuest.value=='Crear un HEAT'): 



                        # This part is used to append to the options of creating an invitation the combination of catergories based on the self.sharedWodcaledarOptions(whic defines the wod that are coomo for two categories)
                        if((self.sharedWodcaledarOptions[np.where(np.asarray(list(self.WOD_filter.options))==self.WOD_filter.value)[0][0]])==None):
                            OptionsCategories=self.CategoryList.copy()
                        elif((self.sharedWodcaledarOptions[np.where(np.asarray(list(self.WOD_filter.options))==self.WOD_filter.value)[0][0]])==[0,1]):
                            OptionsCategories=self.CategoryList.copy()
                            OptionsCategories.append(self.CategoryList[0]+'-'+self.CategoryList[1])
                        elif((self.sharedWodcaledarOptions[np.where(np.asarray(list(self.WOD_filter.options))==self.WOD_filter.value)[0][0]])==[1,2]):
                            OptionsCategories=self.CategoryList.copy()
                            OptionsCategories.append(self.CategoryList[1]+'-'+self.CategoryList[2])
                              
                        self.Categories_filter.options=OptionsCategories 
                        self.Categories_filter.value=OptionsCategories[0]
                              
                def ModifyCalendarOptions(b):
                    #print('Ha entrado bnew:',b['new'])
                    for limpiar in (self.Days_Calendar_widget):
                        limpiar.style.button_color=None
                        limpiar.layout.border=None
                    #print(self.Days_Calendar_widget)    
                    if(self.PreviousDaySelected!=None):
                        self.Days_Calendar_widget[self.PreviousDaySelected].style.button_color=None
                    if(b['new']=='Crear un HEAT'):

                        #self.CreateInvitation.description='Crear un HEAT'
                        
                        self.WOD_filter.options=self.WODcaledarOptions
                        self.WOD_filter.value=self.WODcaledarOptions[0]
                        self.BOX_filter.options=self.BoxListHost
                        self.BOX_filter.value=self.BoxListHost[0]
                        self.LeagueCalendarGrid= GridspecLayout(15,7,width='320px',height='auto') 
                        #self.WOD_filter.value=self.WODcaledarOptions[0]
                        self.LeagueCalendarGrid[0,:]=self.HostorGuest
                        self.LeagueCalendarGrid[7,:]=self.NombreMes
                        #self.LeagueCalendarGrid[1,:]=self.DummyWidget 
                        #self.LeagueCalendarGrid[2,:]=self.DummyWidget 
                        #self.LeagueCalendarGrid[3,:]=self.DummyWidget

                        #self.LeagueCalendarGrid[5,:]=self.DummyWidget
                        #self.LeagueCalendarGrid[6,:]=self.AvisoInvitationCreated
                        #self.LeagueCalendarGrid[7,:]=self.NombreMes
                        self.LeagueCalendarGrid[8:13,:]=self.Daysgrid

                        #self.LeagueCalendarGrid[13,:]=self.DummyWidget
                        temp=list(self.grid.children)
                        temp[-1]=self.LeagueCalendarGrid
                        self.grid.children=tuple(temp) # Quitar despues de prueba
                            
                    elif(b['new']=='Ver HEATS'):

                        #self.CreateInvitation.description='Unirse a un Heat'
                        
                        self.AvisoInvitationCreated.value=""
                        self.WOD_filter.options=Optionswod
                        self.WOD_filter.value=Optionswod[0]
                        self.BOX_filter.options=Optionsbox
                        self.BOX_filter.value=Optionsbox[0]
                        Days_Calendar_np=np.asarray(self.Days_Calendar)
                        #active_days=[]

                        ColorActiveFilteredDays(self.DummyWidget)

                        self.LeagueCalendarGrid= GridspecLayout(15,7,width='320px',height='auto') 
                        self.LeagueCalendarGrid[0,:]=self.HostorGuest
                        self.LeagueCalendarGrid[1,:]=self.WOD_filter
                        self.LeagueCalendarGrid[2,:]=self.BOX_filter
                        self.LeagueCalendarGrid[3,:]=self.Category_filter
                        self.LeagueCalendarGrid[4,:]=self.NombreMes
                        self.LeagueCalendarGrid[5:10,:]=self.Daysgrid
                        temp=list(self.grid.children)
                        temp[-1]=self.LeagueCalendarGrid
                        self.grid.children=tuple(temp) # Quitar despues de prueba
                        
                 
                def DeleteGuest(b): 
                    DateOK=self.currentDate<=self.Days_Calendar[self.PreviousDaySelected]
                    if(DateOK):
                        listahora=b.tooltip.split('-|-')[3].split(':')
                        hora=datetime.time(int(listahora[0]),int(listahora[1]))
                        if(self.typeUser=='Atleta'):
                            self.savedeleteControl=True
                            self.pos_textoaviso=int(b.tooltip.split('-|-')[2])
                            if os.path.exists(os.path.join(os.getcwd(),'DataBaseOwners.users')):
                                with open(os.path.join(os.getcwd(),'DataBaseOwners.users'), 'rb') as fin:
                                    self.DataBaseOwners=pickle.load(fin)
                                    
                                    
                                    
                                    
                                    
                                    
                            if(self.DataBaseOwners[b.tooltip.split('-|-')[0]]['HomeBox']==self.DataBase[self.UserName.value]['Definition']['HomeBox']):
                                GuestList=self.DataBaseOwners[b.tooltip.split('-|-')[0]]['Host'][self.Days_Calendar[self.PreviousDaySelected]][hora][-2]
                                Spots=self.DataBaseOwners[b.tooltip.split('-|-')[0]]['Host'][self.Days_Calendar[self.PreviousDaySelected]][hora][-4]
                                if(self.widgets_dict["UserName"].value in GuestList) :
                                    GuestList.pop(np.where(np.asarray(GuestList)==self.widgets_dict["UserName"].value)[0][0])
                                    Spots+=1
                                    self.DataBaseOwners[b.tooltip.split('-|-')[0]]['Host'][self.Days_Calendar[self.PreviousDaySelected]][hora][-4]=Spots
                                    self.textoaviso='Te has borrado del heat'
                                    #if((Spots-1)==0):
                                        #b.style.button_color='red'
                                else:
                                    self.textoaviso='No estabas en el heat'   
                            else:
                                GuestList=self.DataBaseOwners[b.tooltip.split('-|-')[0]]['Host'][self.Days_Calendar[self.PreviousDaySelected]][hora][-1]
                                Spots=self.DataBaseOwners[b.tooltip.split('-|-')[0]]['Host'][self.Days_Calendar[self.PreviousDaySelected]][hora][-3]
                                if(self.widgets_dict["UserName"].value in GuestList):
                                    
                                    GuestList.pop(np.where(np.asarray(GuestList)==self.widgets_dict["UserName"].value)[0][0])
                                    Spots+=1
                                    self.DataBaseOwners[b.tooltip.split('-|-')[0]]['Host'][self.Days_Calendar[self.PreviousDaySelected]][hora][-3]=Spots
                                    self.textoaviso='Te has borrado del heat'
                                else:
                                    self.textoaviso='No estabas en el heat'   
                                        
                                        
                                        
                            with open(os.path.join(os.getcwd(),'DataBaseOwners.users'), 'wb') as fout:
                                        pickle.dump(self.DataBaseOwners, fout)
                            DaySelected(self.globalDaySelectedWidget)
                            self.savedeleteControl=False
                            self.pos_textoaviso=0
                    else:
                        self.textoaviso="Se ha pasado la fecha"
                def SaveGuest(b):
                    
                    DateOK=self.currentDate<=self.Days_Calendar[self.PreviousDaySelected]
                    if(DateOK):
                        listahora=b.tooltip.split('-|-')[3].split(':')
                        hora=datetime.time(int(listahora[0]),int(listahora[1]))
                        '''
                        if(self.typeUser=='Owner'):
                            sameDiv=True # Los owner pueden ver todas las invitacines
                        '''                            
                        if(self.typeUser=='Atleta'):
                            self.savedeleteControl=True
                            self.pos_textoaviso=int(b.tooltip.split('-|-')[2])
                            
                            if os.path.exists(os.path.join(os.getcwd(),'DataBaseOwners.users')):
                                with open(os.path.join(os.getcwd(),'DataBaseOwners.users'), 'rb') as fin:
                                    self.DataBaseOwners=pickle.load(fin)
                                
                            if(self.DataBaseOwners[b.tooltip.split('-|-')[0]]['HomeBox']==self.DataBase[self.UserName.value]['Definition']['HomeBox']):
                                #time.sleep(5)    
                                GuestList=self.DataBaseOwners[b.tooltip.split('-|-')[0]]['Host'][self.Days_Calendar[self.PreviousDaySelected]][hora][-2]
                                Spots=self.DataBaseOwners[b.tooltip.split('-|-')[0]]['Host'][self.Days_Calendar[self.PreviousDaySelected]][hora][-4]
                                if(Spots>=1 and (self.widgets_dict["UserName"].value not in GuestList) ):
                                    GuestList.append(self.widgets_dict["UserName"].value)
                                    Spots-=1
                                    self.DataBaseOwners[b.tooltip.split('-|-')[0]]['Host'][self.Days_Calendar[self.PreviousDaySelected]][hora][-4]=Spots
                                    
                                    self.textoaviso="Te has apuntado en el heat"
                                    #print("Te has apuntado en el heat")
                                elif(self.widgets_dict["UserName"].value in GuestList):
                                    self.textoaviso="Ya estás en el heat"
                                elif(Spots<1):
                                    self.textoaviso="El heat está completo"

                                    #if((Spots-1)==0):
                                        #b.style.button_color='red'
                            else:
                                #time.sleep(15)    
                                GuestList=self.DataBaseOwners[b.tooltip.split('-|-')[0]]['Host'][self.Days_Calendar[self.PreviousDaySelected]][hora][-1]
                                Spots=self.DataBaseOwners[b.tooltip.split('-|-')[0]]['Host'][self.Days_Calendar[self.PreviousDaySelected]][hora][-3]
                                if(Spots>=1 and (self.widgets_dict["UserName"].value not in GuestList) ):
                                    
                                    GuestList.append(self.widgets_dict["UserName"].value)
                                    Spots-=1
                                    self.DataBaseOwners[b.tooltip.split('-|-')[0]]['Host'][self.Days_Calendar[self.PreviousDaySelected]][hora][-3]=Spots
                                    self.textoaviso="Te has apuntado en el heat"
                                elif(self.widgets_dict["UserName"].value in GuestList):
                                    self.textoaviso="Ya estás en el heat"
                                    #if((Spots-1)==0):
                                elif(Spots<1):
                                    self.textoaviso="El heat está completo"

                                    
                            with open(os.path.join(os.getcwd(),'DataBaseOwners.users'), 'wb') as fout:
                                        pickle.dump(self.DataBaseOwners, fout)
                        DaySelected(self.globalDaySelectedWidget)
                        self.savedeleteControl=False
                        self.pos_textoaviso=0
                        
                    else:

                        self.AvisoApuntarse[int(b.tooltip.split('-|-')[2])].value="Se ha pasado la fecha"

                        
                        
                def DaySelected(b):
                    self.globalDaySelectedWidget=b

                    if(self.PreviousDaySelected!=None):
                        #self.Days_Calendar_widget[self.PreviousDaySelected].layout.border = "2px None blue"
                        ColorActiveFilteredDays(self.DummyWidget)

                    self.Days_Calendar_widget[int(b.description)-1].layout.border = "2px solid blue" #.layout=Layout(border='solid')

                    self.PreviousDaySelected=int(b.description)-1
                    if(self.HostorGuest.value=='Crear un HEAT'):
                        self.CreateInvitation.description='Crear invitation'
                        # This part is used to append to the options of creating an invitation the combination of catergories based on the self.sharedWodcaledarOptions(whic defines the wod that are coomo for two categories)
                        if((self.sharedWodcaledarOptions[np.where(np.asarray(list(self.WOD_filter.options))==self.WOD_filter.value)[0][0]])==None):
                            OptionsCategories=self.CategoryList.copy()
                        elif((self.sharedWodcaledarOptions[np.where(np.asarray(list(self.WOD_filter.options))==self.WOD_filter.value)[0][0]])==[0,1]):
                            OptionsCategories=self.CategoryList.copy()
                            OptionsCategories.append(self.CategoryList[0]+'-'+self.CategoryList[1])
                        elif((self.sharedWodcaledarOptions[np.where(np.asarray(list(self.WOD_filter.options))==self.WOD_filter.value)[0][0]])==[1,2]):
                            OptionsCategories=self.CategoryList.copy()
                            OptionsCategories.append(self.CategoryList[1]+'-'+self.CategoryList[2])
                            
                        self.Categories_filter.options=OptionsCategories 
                        self.Categories_filter.value=OptionsCategories[0]
                        self.LeagueCalendarGrid= GridspecLayout(15,7,width='320px',height='auto') 
                        #print('Ha seleccionado un dia en creacion de ivitacion')
                        self.LeagueCalendarGrid[0,:]=self.HostorGuest
                        self.LeagueCalendarGrid[1,:]=self.WOD_filter
                        self.LeagueCalendarGrid[2,:]=self.Categories_filter
                        self.LeagueCalendarGrid[3,:]=Time_picker
                        self.LeagueCalendarGrid[4,0:3]=self.OpenSpots_widget_Locals
                        self.LeagueCalendarGrid[4,3:6]=self.OpenSpots_widget_Visitors
                        self.LeagueCalendarGrid[5,:]=self.CreateInvitation
                        self.LeagueCalendarGrid[6,:]=self.AvisoInvitationCreated
                        self.LeagueCalendarGrid[7,:]=self.NombreMes
                        self.LeagueCalendarGrid[8:13,:]=self.Daysgrid
                        temp=list(self.grid.children)
                        temp[-1]=self.LeagueCalendarGrid
                        self.grid.children=tuple(temp) # Quitar despues de prueba
                        #[14,0:5]=self.DummyWidget # Originalmente activado
                        #self.LeagueCalendarGrid[15,5:]=self.DummyWidget
                        
                    elif(self.HostorGuest.value=='Ver HEATS'):
                        #**********************

                        #print('Ha entrado en day selected, depués de elif Seeopen')
                        
                        if os.path.exists(os.path.join(os.getcwd(),'DataBaseOwners.users')):
                            with open(os.path.join(os.getcwd(),'DataBaseOwners.users'), 'rb') as fin:
                                self.DataBaseOwners=pickle.load(fin)
                        self.Invitations=[]
                        self.InvitationsWidgets=[]
                        self.ApuntarseWidgets=[]
                        self.BorrarseWidgets=[]
                        self.ApuntarseGrid=[]
                        self.GuestsWidgets=[]
                        self.AvisoApuntarse=[]
                        i=0
                        columnas=['Time','Host','Category','HomeBox','WOD','Available spots','Guests']

                        # Curro
                        for key in (self.DataBaseOwners.keys()):


                            if(self.typeUser=='Owner'):
                                #sameDiv=(self.Category_filter.value in self.DataBaseOwners[key]['Host'][dia][2]  or self.Category_filter.value=='All') #True # Los owner pueden ver todas las invitacines
                                CategoOk=False
                                
                            for dia in(self.DataBaseOwners[key]['Host'].keys()):
                                if(self.Days_Calendar[self.PreviousDaySelected]==dia):
                                    for horadeldia in self.DataBaseOwners[key]['Host'][dia].keys():
                                        sameDiv=(self.Category_filter.value in self.DataBaseOwners[key]['Host'][dia][horadeldia][2]  or self.Category_filter.value=='Cualquiera')
                                        if(self.typeUser=='Atleta'):
                
                                            #sameDiv=(self.Category_filter.value in self.DataBaseOwners[key]['Host'][dia][2]  or self.Category_filter.value=='All')
                                            CategoOk=self.DataBase[self.UserName.value]['Definition']['Category'] in self.DataBaseOwners[key]['Host'][dia][horadeldia][2] 
                                        if((sameDiv and (self.DataBaseOwners[key]['Host'][dia][horadeldia][1]==self.WOD_filter.value or self.WOD_filter.value=='Cualquiera') and (self.DataBaseOwners[key]['HomeBox']==self.BOX_filter.value or self.BOX_filter.value=='Cualquiera')) ):
    
                                            
                                            if(CategoOk):
                                                DisabledApuntarse=False
                                            else:
                                                DisabledApuntarse=True
                                            #texto=[str(key),str(self.Categories_filter.value)]
                                            texto=[str(key),str(self.Categories_filter.value),str(i),str(horadeldia)]
                                            texto=('-|-'.join(texto))
                                            self.ApuntarseWidgets.append(widgets.Button(
                                            description='Apuntarse',
                                            disabled=DisabledApuntarse,
                                            button_style='', # 'success', 'info', 'warning', 'danger' or ''
                                            tooltip=texto,
                                            layout=Layout(width='auto',heigth='auto', grid_area='Apuntarse',border='solid'),
                                            icon='' # (FontAwesome names without the `fa-` prefix)
                                            ))
                                            
                                            self.BorrarseWidgets.append(widgets.Button(
                                            description='Borrarse',
                                            disabled=DisabledApuntarse,
                                            button_style='', # 'success', 'info', 'warning', 'danger' or ''
                                            tooltip=texto,
                                            layout=Layout(width='auto', grid_area='Borrarse',border='solid'),
                                            icon='' # (FontAwesome names without the `fa-` prefix)
                                            ))
                                            #print('self.savedeleteControl',self.savedeleteControl)
                                            if (i==self.pos_textoaviso and self.savedeleteControl):
                                                textoaviso=self.textoaviso
                                            else:
                                                textoaviso=''
                                              
                                            self.AvisoApuntarse.append(widgets.HTML(
                                                        value="<b>%s</b>"%textoaviso,
                                                        placeholder='',
                                                        description='',
                                                        indent=False,
                                                        layout=Layout(width='auto', grid_area='AvisoApuntarse'),
                                                        ))
    
                                            self.HeaderBox=widgets.HTML(
                                                        value="<b>%s<b>"%self.DataBaseOwners[key]['HomeBox'],
                                                        placeholder='',
                                                        description='',
                                                        indent=False,
                                                        layout=Layout(width='auto', grid_area='HeaderBox',border='solid'),
                                                        )
    
                                            self.HeaderCategory=widgets.HTML(
                                                        value="<b>%s<b>"%self.DataBaseOwners[key]['Host'][dia][horadeldia][2],
                                                        placeholder='',
                                                        description='',
                                                        indent=False,
                                                        layout=Layout(width='auto', grid_area='HeaderCategory',border='solid'),
                                                        )
                                            self.HeaderTime=widgets.HTML(
                                                        value="<b>%s<b>"%self.DataBaseOwners[key]['Host'][dia][horadeldia][0],
                                                        placeholder='',
                                                        description='',
                                                        indent=False,
                                                        layout=Layout(width='auto', grid_area='HeaderTime',border='solid'),
                                                        )
                                            ApunAnfi=len(self.DataBaseOwners[key]['Host'][dia][horadeldia][-2])
                                            LibresAnfitriones=str(ApunAnfi)+'/'+str(ApunAnfi+self.DataBaseOwners[key]['Host'][dia][horadeldia][-4])
                                            
                                            self.LibresAnfitriones=widgets.HTML(
                                                        value="<b>%s<b>"%LibresAnfitriones,
                                                        placeholder='',
                                                        description='',
                                                        indent=False,
                                                        layout=Layout(width='auto', grid_area='LibresAnfitriones',border='solid'),
                                                        )
                                            
                                            ApunVisi=len(self.DataBaseOwners[key]['Host'][dia][horadeldia][-1])
                                            LibresVisitantes=str(ApunVisi)+'/'+str(ApunVisi+self.DataBaseOwners[key]['Host'][dia][horadeldia][-3])
                                            self.LibresVisitantes=widgets.HTML(
                                                        value="<b>%s<b>"%LibresVisitantes,
                                                        placeholder='',
                                                        description='',
                                                        indent=False,
                                                        layout=Layout(width='auto', grid_area='LibresVisitantes',border='solid'),
                                                        )
                                            self.HeaderWod=widgets.HTML(
                                                        value="<b>%s<b>"%self.DataBaseOwners[key]['Host'][dia][horadeldia][1],
                                                        placeholder='',
                                                        description='',
                                                        indent=False,
                                                        layout=Layout(width='auto', grid_area='HeaderWod',border='solid'),
                                                        )
                                            opciones=[]
                                            if (ApunAnfi==0):
                                                opciones=[]
                                                opciones.insert(0,'None')
                                            else:
                                                opciones=self.DataBaseOwners[key]['Host'][dia][horadeldia][-2]
                                                
                                            self.ListAnfitriones=widgets.Dropdown(
                                            options=opciones,
                                            value=opciones[0],
                                            description='',
                                            #indent=False,
                                            #layout=Layout(width='auto', grid_area='Category'),
                                            layout=Layout(width='max-content', grid_area='ListAnfitriones'),
                                            style=style
                                            )
                                            opciones=[]
                                            if (ApunVisi==0):
                                                opciones=[]
                                                opciones.insert(0,'None')
                                            else:
                                                opciones=self.DataBaseOwners[key]['Host'][dia][horadeldia][-1]
                                            self.ListVisitantes=widgets.Dropdown(
                                            options=opciones,
                                            value=opciones[0],#self.DataBaseOwners[key]['Host'][dia][-1][0],
                                            #indent=False,
                                            #layout=Layout(width='auto', grid_area='Category'),
                                            layout=Layout(width='max-content', grid_area='ListVisitantes'),
                                            style=style
                                            )
                                            
    
                                            self.ApuntarseWidgets[i].on_click(SaveGuest)
                                            self.BorrarseWidgets[i].on_click(DeleteGuest)
                                            self.ApuntarseGrid.append(GridBox(children=[self.HeaderBox,self.HeaderWod,self.HeaderHost,self.HeaderGuest,self.LibresVisitantes,self.LibresAnfitriones,self.ListAnfitriones,self.ListVisitantes,self.HeaderTime,self.HeaderCategory,self.ApuntarseWidgets[i],self.BorrarseWidgets[i],self.AvisoApuntarse[i]],
                                                      layout=Layout(
                                                          border='solid',
                                                          width='auto',
                                                          grid_template_columns='auto auto auto auto',
                                                          grid_template_rows='auto auto auto auto',
                                                          grid_template_areas='''
                                                            "HeaderBox HeaderWod HeaderTime HeaderCategory"
                                                            "Anfitriones LibresAnfitriones ListAnfitriones Apuntarse"
                                                             "Visitantes LibresVisitantes  ListVisitantes Borrarse"
                                                             "AvisoApuntarse AvisoApuntarse AvisoApuntarse AvisoApuntarse"
                                
                                                            '''
                                                          )
                                                     )) 
                                            #InvitationsLayout[i,:]=tempgrid
                                            i+=1
                        
                        numInvis=len(self.ApuntarseGrid)
                        
                        self.CreateInvitation.description='Unirse a un Heat'
                        # Prueba redefinir gridSpecLayout
                        self.LeagueCalendarGrid= GridspecLayout(15+5*numInvis,7,width='320px',height='auto')  
                        if(self.typeUser=='Owner'):
                            self.LeagueCalendarGrid[0,:]=self.HostorGuest
                        elif(self.typeUser=='Atleta'):
                            self.LeagueCalendarGrid[0,:]=self.DummyWidget
                    
                        self.LeagueCalendarGrid[1,:]=self.WOD_filter
                        self.LeagueCalendarGrid[2,:]=self.BOX_filter
                        self.LeagueCalendarGrid[3,:]=self.Category_filter
                        self.LeagueCalendarGrid[4,:]=self.NombreMes
                        self.LeagueCalendarGrid[5:10,:]=self.Daysgrid
                        
                        
                        k=0
                        if(numInvis>0):
                            '''
                            self.InvitationsLayout= GridspecLayout(numInvis, 5)
                            for j in range(numInvis):
                                self.InvitationsLayout[j,:]=self.ApuntarseGrid[j]
                                self.LeagueCalendarGrid[(10+k):14+k,:]=self.InvitationsLayout
                                k+=5
                            #self.LeagueCalendarGrid[14,:]=self.InvitationsLayout
                            '''
                            vbox=VBox(self.ApuntarseGrid)
                            self.LeagueCalendarGrid[11:,:]=vbox
                            
                        else:
                            self.LeagueCalendarGrid[14,:]=self.DummyWidget
                        self.savedeleteControl=False
                        temp=list(self.grid.children)
                        temp[-1]=self.LeagueCalendarGrid
                        self.grid.children=tuple(temp) # Quitar despues de prueba
                def createInvitation(b):
                    #print('Ha entreado a crear una invitacion')
                    if os.path.exists(os.path.join(os.getcwd(),'DataBaseOwners.users')):
                        with open(os.path.join(os.getcwd(),'DataBaseOwners.users'), 'rb') as fin:
                            self.DataBaseOwners=pickle.load(fin)
                    # Agregar aqui condicional para que estén todos los campos rellenados antes de guardas la invitación        
                    if(self.currentDate>self.Days_Calendar[self.PreviousDaySelected]):
                        self.AvisoInvitationCreated.value="Se ha pasado la fecha"
                    elif(Time_picker.value==None):
                        self.AvisoInvitationCreated.value="<b>Selecciona una hora para el heat</b>"

                    elif(self.OpenSpots_widget_Locals.value<=0 or self.OpenSpots_widget_Visitors.value<=0):   

                        self.AvisoInvitationCreated.value="Error: Num plazas<1"

                    else:
                        
                        if(self.Days_Calendar[self.PreviousDaySelected] not in self.DataBaseOwners[self.widgets_dict["UserName"].value]['Host'].keys()):
                            self.DataBaseOwners[self.widgets_dict["UserName"].value]['Host'][self.Days_Calendar[self.PreviousDaySelected]]={}    
                            
                        
                        #self.DataBaseOwners[self.widgets_dict["UserName"].value]['Host'][self.Days_Calendar[self.PreviousDaySelected]]=[Time_picker.value,self.WOD_filter.value,self.Categories_filter.value,self.OpenSpots_widget_Locals.value,self.OpenSpots_widget_Visitors.value,[],[]]
                        self.DataBaseOwners[self.widgets_dict["UserName"].value]['Host'][self.Days_Calendar[self.PreviousDaySelected]][Time_picker.value]=[Time_picker.value,self.WOD_filter.value,self.Categories_filter.value,self.OpenSpots_widget_Locals.value,self.OpenSpots_widget_Visitors.value,[],[]]
                        self.AvisoInvitationCreated.value="Invitación creada correctamente"
                        
                        
                    with open(os.path.join(os.getcwd(),'DataBaseOwners.users'), 'wb') as fout:
                                pickle.dump(self.DataBaseOwners, fout)
                    
                    
                    
                    
                self.HostorGuest=widgets.Dropdown(
                options=['Crear un HEAT','Ver HEATS'],
                value='Ver HEATS',
                description='',
                )
                self.WOD_filter=widgets.Dropdown(
                options=Optionswod,
                value=Optionswod[0],
                description='Wod',
                )
                # This part is used to append to the options of creating an invitation the combination of catergories based on the self.sharedWodcaledarOptions(whic defines the wod that are coomo for two categories)
                if((self.sharedWodcaledarOptions[np.where(np.asarray(list(self.WOD_filter.options))==self.WOD_filter.value)[0][0]])==None):
                    OptionsCategories=self.CategoryList.copy()
                elif((self.sharedWodcaledarOptions[np.where(np.asarray(list(self.WOD_filter.options))==self.WOD_filter.value)[0][0]])==[0,1]):
                    OptionsCategories=self.CategoryList.copy()
                    OptionsCategories.append(self.CategoryList[0]+'-'+self.CategoryList[1])
                elif((self.sharedWodcaledarOptions[np.where(np.asarray(list(self.WOD_filter.options))==self.WOD_filter.value)[0][0]])==[1,2]):
                    OptionsCategories=self.CategoryList.copy()
                    OptionsCategories.append(self.CategoryList[1]+'-'+self.CategoryList[2])
                self.Categories_filter=widgets.Dropdown(
                options=OptionsCategories,
                value=OptionsCategories[0],
                description='Category',
                )
                        
                
                self.BOX_filter=widgets.Dropdown(
                options=Optionsbox,
                value=Optionsbox[0],
                description='Box',
                )
                if(self.typeUser=='Owner'):
                    ini_catefilvalue=Optionscat[0]
                elif(self.typeUser=='Atleta'):
                    ini_catefilvalue=self.ini_catefilvalue=self.DataBase[self.widgets_dict["UserName"].value]['Definition']['Category']
                self.Category_filter=widgets.Dropdown(
                options=Optionscat,
                value=ini_catefilvalue,
                description='Categoría',
                )
                
                
                #self.sharedWodcaledarOptions
                
                

                self.CreateInvitation=widgets.Button(
                            value=False,
                            description='Crear HEAT',
                            disabled=False,
                            indent=False,
                            layout=Layout(width='auto',border='solid'),
                            
                )
                def clearInvitations(b):
                    if(self.HostorGuest.value=='Ver HEATS'):
                        self.LeagueCalendarGrid[10:,:]=self.DummyWidget
 
                    
                
                self.WOD_filter.observe(clearInvitations,'value')
                self.BOX_filter.observe(clearInvitations,'value')
                self.Category_filter.observe(clearInvitations,'value')
                
                self.CreateInvitation.on_click(createInvitation)
                self.HostorGuest.observe(ModifyCalendarOptions,'value')
                self.WOD_filter.observe(ColorActiveFilteredDays,'value')
                self.BOX_filter.observe(ColorActiveFilteredDays,'value')
                self.Category_filter.observe(ColorActiveFilteredDays,'value')


                
                # then must create an object of the Calendar class
                cal = calendar.Calendar(firstweekday=0)
                year = 2022#datetime.date.today().year Volver a poner
                month =11#datetime.date.today().month Volver a poner
                calendario=cal.monthdatescalendar(year, month)
                # Este bucle es para crear los button widget del calendario de invitacione (a la vez se crea el texto para meter en el templateAreas del grid)
                self.string_grid_templaAreas=''+'\n'+' '*35
                self.Days_Calendar_widget=[]
                self.Days_Calendar=[]
                self.children_days=[]
                j=0
                dia=1
                prueba=[["aa","ab","ac","ad","ae","af","ag"],["ba","bb","bc","bd","be","bf","bg"],["ca","cb","cc","cd","ce","cf","cg"],["da","db","dc","dd","de","df","dg"],["ea","eb","ec","ed","ee","ef","eg"],["fa","fb","fc","fd","fe","ff","fg"]]
                Final=False
                # All below is to genrate the calendar
                for semana in range(len(calendario)):
                    if((len(calendario)-semana)==1):
                        Final=True
                    semana_firstEntry=True
                    semana_lastEntry=False
                    for i,fecha in enumerate(calendario[semana]):

                        if((len(calendario[semana])-i)==1):
                            semana_lastEntry=True
                
                        #if(calendario[semana][i].month==datetime.date.today().month): Volver a poner
                        if(calendario[semana][i].month==11):
                            disabledValue=False
                            Description=str(dia)
                            dia+=1
                            if(semana_firstEntry):
                                self.string_grid_templaAreas+=' "'+prueba[semana][i]+' '
                            else:
                                if(semana_lastEntry):
                                    if(Final):
                                        self.string_grid_templaAreas+=prueba[semana][i]+'"'
                                    else:
                                        self.string_grid_templaAreas+=(prueba[semana][i]+'"\n'+' '*35)
                                else:        
                                    self.string_grid_templaAreas+=prueba[semana][i]+' '
                        else:
                            disabledValue=True
                            Description=''
                            if(semana_firstEntry):
                                self.string_grid_templaAreas+=' ". '
                            else:
                                if(semana_lastEntry):
                                    if(Final):
                                        self.string_grid_templaAreas+='."'
                                    else:
                                        self.string_grid_templaAreas+='."\n'+' '*35
                                else:
                                    self.string_grid_templaAreas+='. '
                        #print('String',self.string_grid_templaAreas)
                        semana_firstEntry=False  
                        
                        if(disabledValue==False):
                            self.Days_Calendar.append(calendario[semana][i])
                            self.Days_Calendar_widget.append(widgets.Button(
                                        #value=calendario[semana][i],
                                        description=Description,
                                        disabled=disabledValue,
                                        indent=False,
                                        #layout=Layout(width='auto', grid_area='%s%s'%(str(semana),str(i))),
                                        layout=Layout(width='auto', grid_area=prueba[semana][i]),
                                        
                            ))
                            #self.children_days.append(self.Days_Calendar_widget[j])
                            
                            self.Days_Calendar_widget[j].on_click(DaySelected)
                            j += 1




                self.Daysgrid=widgets.GridBox(children=self.Days_Calendar_widget,
                              layout=widgets.Layout(
                                  width='300px',
                                  grid_template_rows='auto',
                                  grid_template_columns='auto',
                                  grid_template_areas=self.string_grid_templaAreas)
                                        ) 
                
                if(self.typeUser=='Owner'):
                    self.LeagueCalendarGrid[0,:]=self.HostorGuest
                elif(self.typeUser=='Atleta'):
                    self.LeagueCalendarGrid[0,:]=self.DummyWidget
                self.LeagueCalendarGrid[1,:]=self.WOD_filter
                self.LeagueCalendarGrid[2,:]=self.BOX_filter
                self.LeagueCalendarGrid[3,:]=self.Category_filter
                self.LeagueCalendarGrid[4,:]=self.NombreMes
                self.LeagueCalendarGrid[5:10,:]=self.Daysgrid
                #self.LeagueCalendarGrid[14,:]=self.DummyWidget
                if(calendario[semana][i].month==11):
                    titles.append('Calendario')
    
                    children.append(self.LeagueCalendarGrid)    

                
                ColorActiveFilteredDays(self.DummyWidget)
 
    

                self.grid.titles=titles
                self.grid.children=children
    
                for i, title in enumerate(self.grid.titles):
                    self.grid.set_title(i, title)
            
            else:
                self.AvisoLogin.value="<b>Invalid user or password</b>"
                #print('Invalis user or password')
        self.LogIn.on_click(checkAccess)     
        
   
        return self.grid
    def CreateNewUser(self,b):
        #print(b.description)
        owner=(b.description=='Crear Box')
        
        
        
    
        
       #CREACION PERFILES DE USUARIO (DYNAMIC)
        if os.path.exists(os.path.join(os.getcwd(),'DataBase.users')):
            with open(os.path.join(os.getcwd(),'DataBase.users'), 'rb') as fin:
                self.DataBase=pickle.load(fin)
        userNamesList=list(self.DataBase.keys()) 
        
        if os.path.exists(os.path.join(os.getcwd(),'DataBaseOwners.users')):
            with open(os.path.join(os.getcwd(),'DataBaseOwners.users'), 'rb') as fin:
                self.DataBaseOwners=pickle.load(fin)
        ownerNamesList=list(self.DataBaseOwners.keys()) 
        TotalNamesList=userNamesList+ownerNamesList
        
        
        # Check the AccessCode for the selected box
        config_file = configparser.ConfigParser()
        config_file.read('BoxesDataBeta.config')

        codigos= ""
        if(owner):
            codigos = config_file[self.Box.value]['owneraccesscode'].split(",") if string else []
            if(self.AccessCode.value in codigos and self.AccessCode.value!=''):
                AccessCodeok=True
           
            else:
                AccessCodeok=False
        
        else:
            codigos = config_file[self.Box.value]['userAccessCodes'].split(",") if string else []
            if(self.AccessCode.value in codigos and self.AccessCode.value!=''):
                AccessCodeok=True
           
            else:
                AccessCodeok=False


        #UserDefinition_List=list(self.DataBase[userNamesList[0]]['Definition'].keys())
        #UserDefinition_List=self.UserDefinition_List
        # Check ojo format
        l, u, p, d = 0, 0, 0, 0
        ll, uu, pp, dd = 0, 0, 0, 0
        s = self.NewOjo.value
        capitalalphabets="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        smallalphabets="abcdefghijklmnopqrstuvwxyz"
        specialchar="$@_"
        digits="0123456789"
        if (len(s) >= 8 and len(s) <20):
            for i in s:
         
                # counting lowercase alphabets
                if (i in smallalphabets):
                    l+=1           
         
                # counting uppercase alphabets
                if (i in capitalalphabets):
                    u+=1           
         
                # counting digits
                if (i in digits):
                    d+=1           
         
                # counting the mentioned special characters
                if(i in specialchar):
                    p+=1       
        if (l>=1 and u>=1 and p>=1 and d>=1 and l+p+u+d==len(s)):
            ojoformatok=True
        else:
            ojoformatok=False
            
        if (len(self.NewUserName.value) >= 3 and len(self.NewUserName.value) <= 9):
            for i in self.NewUserName.value:
         
                # counting lowercase alphabets
                if (i in smallalphabets):
                    ll+=1           
         
                # counting uppercase alphabets
                if (i in capitalalphabets):
                    uu+=1           
         
                # counting digits
                if (i in digits):
                    dd+=1           
         
                # counting the mentioned special characters
                if(i in specialchar):
                    pp+=1       
        if (ll+pp+uu+dd==len(self.NewUserName.value)):
            usernameformatok=True
        else:
            usernameformatok=False

        #self.UserBenchMarksDict=list(self.DataBase[userNamesList[0]]['BenchMarks'].keys())
        if (((self.NewUserName.value not in TotalNamesList) and (self.DateOfBirth.value!=None) and (self.NewOjo.value==self.ConfirmOjo.value) and ojoformatok and usernameformatok and AccessCodeok) or ((self.NewUserName.value not in TotalNamesList) and (self.NewOjo.value==self.ConfirmOjo.value) and ojoformatok and usernameformatok and AccessCodeok and owner)): #CurroSpot
            
            if(owner):
                self.AvisoUserCreated.value="<b>Usuario creado, bienvenido!</b>"

                config_file[self.Box.value]['owneraccesscode']=','
                conf_file = 'BoxesDataBeta.config'
                with open(conf_file+'.bak', 'w') as configfile:
                    config_file.write(configfile)
                if os.path.exists(conf_file):
                   os.remove(conf_file)  # else rename won't work when target exists
                os.rename(conf_file+'.bak',conf_file)
                
                username=self.NewUserName.value
                ownerNamesList.append(username)
                self.DataBaseOwners[username]={}  
                self.DataBaseOwners[username]['HomeBox']=self.Box.value
                self.DataBaseOwners[username]['Host']={}
                ojos=bytes(self.NewOjo.value,'utf-8')
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(ojos, salt)
                self.DataBaseOwners[username]['ojos']=hashed
                
                with open(os.path.join(os.getcwd(),'DataBaseOwners.users'), 'wb') as fout:
                    pickle.dump(self.DataBaseOwners, fout)
                
            else:
                # Delete the already used code and rewrite the access codes file
                codigos.pop(np.where(np.asarray(codigos)==self.AccessCode.value)[0][0])
                config_file[self.Box.value]['userAccessCodes']=','.join(codigos)
                conf_file = 'BoxesDataBeta.config'
                with open(conf_file+'.bak', 'w') as configfile:
                    config_file.write(configfile)
                if os.path.exists(conf_file):
                   os.remove(conf_file)  # else rename won't work when target exists
                os.rename(conf_file+'.bak',conf_file)
            
            
            
                username=self.NewUserName.value
                
                #print('User created: Welcome to the league (Alpha test)')
                userNamesList.append(username)
                self.DataBase[username]={}  
                self.DataBase[username]['Definition']=dict.fromkeys(self.UserDefinition_List)
                self.DataBase[username]['BenchMarks']=self.UserBenchMarksDict.copy()
                self.DataBase[username]['WODpoints']=dict.fromkeys(self.WodNamesFlat)
                self.DataBase[username]['WODpositions']=dict.fromkeys(self.WodNamesFlat)
                self.DataBase[username]['WodResultsYoutube']=dict.fromkeys(self.WodNamesFlat)
                #self.DataBase[username]['Host']={}
                #self.DataBase[username]['Guest']={}
                
                UserDefinitionEntries=[[int((datetime.date.today()-self.DateOfBirth.value).days/365),self.Gender.value,self.heigth.value,self.weight.value,self.Box.value,self.Category.value]]
                for w4,points in enumerate(self.WodNamesFlat.copy()):
                    self.DataBase[username]['WODpoints'][points]= 0
                    self.DataBase[username]['WODpositions'][points]= '---' 
                    self.DataBase[username]['WodResultsYoutube'][points[0]] = '---'  
                # User definition
                for w2,userEntry in enumerate(zip(self.UserDefinition_List.copy(),UserDefinitionEntries.copy()[0])):
                    self.DataBase[username]['Definition'][userEntry[0]]= userEntry[1]
                # User becnhMarks 
                for key in enumerate(self.UserBenchMarksDict.copy().keys()):
    
                    for w3,activity_value in enumerate(zip(self.DataBase[username]['BenchMarks'][key[1]],self.Inputs_BenchmarksInit.copy()[0][key[0]])):
    
                        self.DataBase[username]['BenchMarks'][key[1]][activity_value[0]]=activity_value[1]
                
                self.DataBase[username]['WODmarks']=dict.fromkeys(self.WodNamesFlat)
                self.DataBase[username]['RawWODmarks']=dict.fromkeys(self.WodNamesFlat)
                self.DataBase[username]['WODmarksCorrected']=dict.fromkeys(self.WodNamesFlat)
                self.DataBase[username]['RawWODmarksCorrected']=dict.fromkeys(self.WodNamesFlat)
                
                
    
                ojos=bytes(self.NewOjo.value,'utf-8')
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(ojos, salt)
    
            
                self.DataBase[username]['ojos']=hashed
    
                
                
                with open(os.path.join(os.getcwd(),'DataBase.users'), 'wb') as fout:
                    pickle.dump(self.DataBase, fout)
                
                self.AvisoUserCreated.value="<b>Usuario creado, bienvenido a la liga!</b>"
        else:
            if owner:
                if(self.NewUserName.value in TotalNamesList):
                    self.AvisoUserCreated.value="<b>El nombre de usuario ya está en uso!</b>"
                elif not(usernameformatok):  
                    self.AvisoUserCreated.value="<b>El nombre de usuario debe de cumplir:<br>Longitud >3 y <10<br> Caracteres especiales aceptados [ _ o @ o $ ]!</b>"
                elif not(ojoformatok):
                    self.AvisoUserCreated.value="<b>La longitud de la contraseña ha de cumplir:<br> Longitud > 8 y <20 <br> Contener1 Maúscula,1 Número y 1 Carácter especial [ _ o @ o $ ]!</b>"
                elif(self.NewOjo.value!=self.ConfirmOjo.value):
                    self.AvisoUserCreated.value="<b>Las contraseñas no coinciden!</b>"

                elif not(AccessCodeok):
                    self.AvisoUserCreated.value="<b>Código no válido para esta cuenta de manager</b>"
                
            else:
                if(self.NewUserName.value in TotalNamesList):
                    self.AvisoUserCreated.value="<b>El nombre de usuario ya está en uso!</b>"
                elif not(usernameformatok):  
                    self.AvisoUserCreated.value="<b>El nombre de usuario debe de cumplir:<br>Longitud >3 y <10<br> Caracteres especiales aceptados [ _ o @ o $ ]!</b>"
                elif not(ojoformatok):
                    self.AvisoUserCreated.value="<b>La longitud de la contraseña ha de cumplir:<br> Longitud > 8 y <20<br> Contener1 Maúscula,1 Número y 1 Carácter especial [ _ o @ o $ ]!</b>"
                elif(self.NewOjo.value!=self.ConfirmOjo.value):
                    self.AvisoUserCreated.value="<b>Las contraseñas no coinciden!</b>"
    
                elif(self.DateOfBirth.value==None):
                    self.AvisoUserCreated.value="<b>Fecha de nacimiento vacía</b>"
                elif not(AccessCodeok):
                    self.AvisoUserCreated.value="<b>El código de acceso utilizado no es correcto o ya ha sido utilizado</b> Revisa que el box elegido corresponde con el código utilizado</b>"
                
                

    # Parte para generar los plot de las estadísticas de Rms etc...
    def plotUserProfile(self,name,benchmarkType):
     
         '''
         Total_DataPlot=[]  
         #for key in enumerate(self.UserBenchMarksDict.copy().keys()):
         for key in enumerate(self.DataBase.keys()):
             #print(key[1])
             Total_DataPlot.append(list(self.DataBase[key[1]]['BenchMarks']['Strength'].values()))
         Total_DataPlot=pd.DataFrame(Total_DataPlot,columns=self.DataBase[key[1]]['BenchMarks']['Strength'].keys(),index=self.DataBase.keys())    
         
         # The attributes we want to use in our radar plot.
         factors = self.DataBase[key[1]]['BenchMarks']['Strength'].keys()
         Total_DataPlot_0to10=Total_DataPlot.copy()
         # New scale should be from 0 to 100.
         new_max = 10
         new_min = 0
         new_range = new_max - new_min
         
         # Do a linear transformation on each variable to change value
         # to [0, 100].
         for factor in factors:
           max_val = Total_DataPlot_0to10[factor].max()
           min_val = Total_DataPlot_0to10[factor].min()
           val_range = max_val - min_val
           Total_DataPlot_0to10[factor] = Total_DataPlot[factor].apply(
               lambda x: (((x - min_val) * new_range) / val_range) + new_min)
         
         '''
         
         #**********************************************************************************
         #**********************************************************************************
         #**********************************************************************************
         #**********************************************************************************
         #**********************************************************************************
         #%%   PRIMER PLOT
         
         #%% 
         #for z,benchmarkType=self.UserBenchMarksDict):
         Total_DataPlot=[]  
         #for key in enumerate(self.UserBenchMarksDict.copy().keys()):
         
         for key in enumerate(self.DataBase.keys()):

             #if((self.DataBase[key[1]]['Definition']['Gender']==self.DataBase[self.widgets_dict["UserName"].value]['Definition']['Gender'])  and (self.DataBase[key[1]]['Definition']['Category']==self.DataBase[self.widgets_dict["UserName"].value]['Definition']['Category'])):
                 
                 #print(key[1])
             Total_DataPlot.append(list(self.DataBase[key[1]]['BenchMarks'][benchmarkType].values()))
         Total_DataPlot=pd.DataFrame(Total_DataPlot,columns=self.DataBase[key[1]]['BenchMarks'][benchmarkType].keys(),index=self.DataBase.keys())    
         self.mirar=Total_DataPlot
         # The attributes we want to use in our radar plot.
         factors = self.DataBase[key[1]]['BenchMarks'][benchmarkType].keys()
         Total_DataPlot_0to10=Total_DataPlot.copy()
         
         # New scale should be from 0 to 100.
         new_max = 10
         new_min = 0
         new_range = new_max - new_min
         
         # Do a linear transformation on each variable to change value
         # to [0, 100].
         #print(Total_DataPlot_0to10)
         for factor in factors:
           max_val = Total_DataPlot_0to10[factor].max()
           min_val = Total_DataPlot_0to10[factor].min()
           new_min = 0
           val_range = max_val - min_val
           #print(val_range)
           if (val_range==0):
               val_range=1
               new_min=10
           Total_DataPlot_0to10[factor] = Total_DataPlot[factor].apply(
               lambda x: (((x - min_val) * new_range) / val_range) + new_min)
         Data_Plot=[Total_DataPlot,Total_DataPlot_0to10]  
         DataPlotName=['','']
         
         self.mirar2=Data_Plot
         #for name in enumerate(self.DataBase.keys()): 
         
         #for i in range(len(Data_Plot)):
         for i in range(1):

             #labels=list(self.DataBase['Asier']['BenchMarks']['Strength'].keys())
             
             #print(list(map(str, Data_Plot[i][0,:].tolist())))
         
             # values=df.iloc[:,-1].tolist()
             '''
             values=Data_Plot[i].loc[name].values.tolist()
             num_vars= len(labels)
             
             # Split the circle into even parts and save the angles
             # so we know where to put each axis.
             angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
             
             # The plot is a circle, so we need to "complete the loop"
             # and append the start value to the end.
             values += values[:1]
             angles += angles[:1]
             MaxValue=np.max(np.asarray(values))
             # ax = plt.subplot(polar=True)
             fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
             '''

             
             #%% SEGUNDO PLOT (GIRAR Y ETIQUETAR)
             '''
             angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
             
             # Fix axis to go in the right order and start at 12 o'clock.
             ax.set_theta_offset(np.pi / 2)
             ax.set_theta_direction(-1)
             # Draw axis lines for each angle and label.
             ax.set_thetagrids(np.degrees(angles), labels)
             #**********************************************************************************
             # Go through labels and adjust alignment based on where
             # it is in the circle.
             
             angles += angles[:1]
             
             for label, angle in zip(ax.get_xticklabels(), angles):
               if angle in (0, np.pi):
                 label.set_horizontalalignment('center')
               elif 0 < angle < np.pi:
                 label.set_horizontalalignment('left')
               else:
                 label.set_horizontalalignment('right')
                 
                 
                 
                 
             #**********************************************************************************
             # Ensure radar goes from 0 to 100.
             ax.set_ylim(0, MaxValue)
             # You can also set gridlines manually like this:
             # ax.set_rgrids([20, 40, 60, 80, 100])
             
             # Set position of y-labels (0-100) to be in the middle
             # of the first two axes.
             ax.set_rlabel_position(180 / num_vars)
             '''
             
             
             # Each attribute we'll plot in the radar chart.
             #labels=list(Data_Plot[i].columns)
             
             # Let's look at the 1970 Chevy Impala and plot it.
             #car = 'Strength'
             #values = dft.loc[car].tolist()
             #values=df.iloc[:,-1].tolist()
             values=Data_Plot[i].loc[name].values.tolist()
             labels=list(Data_Plot[i].columns)
             '''
             if (i==1):     
                 for j,value in enumerate(values):
                    labels[j]=labels[j]+': '+str(round(value,2))
             else:     
             '''    
             for j,value in enumerate(values):
               labels[j]=labels[j]+': '+str(round(value,2))

             MaxValue=np.max(np.asarray(values))
             # Number of variables we're plotting.
             num_vars = len(labels)
             
             # Split the circle into even parts and save the angles
             # so we know where to put each axis.
             angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
             
             # The plot is a circle, so we need to "complete the loop"
             # and append the start value to the end.
             values += values[:1]
             angles += angles[:1]
             
             # ax = plt.subplot(polar=True)
             fig, ax = plt.subplots(figsize=(3, 3), subplot_kw=dict(polar=True))
             
             # Draw the outline of our data.
             ax.plot(angles, values, color='#1aaf6c', linewidth=1)
             # Fill it in.
             ax.fill(angles, values, color='#1aaf6c', alpha=0.25)
             
             # Fix axis to go in the right order and start at 12 o'clock.
             ax.set_theta_offset(np.pi / 2)
             ax.set_theta_direction(-1)
             
             # Draw axis lines for each angle and label.
             ax.set_thetagrids(np.degrees(angles[0:-1]), labels)
             
             # Go through labels and adjust alignment based on where
             # it is in the circle.
             for label, angle in zip(ax.get_xticklabels(), angles):
               if angle in (0, np.pi):
                 label.set_horizontalalignment('center')
               elif 0 < angle < np.pi:
                 label.set_horizontalalignment('left')
               else:
                 label.set_horizontalalignment('right')
             
             # Ensure radar goes from 0 to 100.
             ax.set_ylim(0, MaxValue)
             # You can also set gridlines manually like this:
             # ax.set_rgrids([20, 40, 60, 80, 100])
             
             # Set position of y-labels (0-100) to be in the middle
             # of the first two axes.
             ax.set_rlabel_position(180 / num_vars)
             
             # Add some custom styling.
             # Change the color of the tick labels.
             ax.tick_params(colors='#222222')
             # Make the y-axis (0-100) labels smaller.
             ax.tick_params(axis='y', labelsize=8)
             # Change the color of the circular gridlines.
             ax.grid(color='#AAAAAA')
             # Change the color of the outermost gridline (the spine).
             ax.spines['polar'].set_color('#222222')
             # Change the background color inside the circle itself.
             ax.set_facecolor('#FAFAFA')
             
             # Lastly, give the chart a title and give it some
             # padding above the "Acceleration" label.
             #ax.set_title('%s_%s'%(benchmarkType,name), y=1.08) 
             ax.set_title('%s'%(DataPlotName[i]), y=1.08) 
             self.stafigure[i]=fig
             plt.close(fig)
             #fig.savefig(os.path.join(getcwd(),'PlotsPerfil','%s%s_%s'%(benchmarkType,name,DataPlotName[i])))  
     
     
             #************************************************************************************              
            
        
