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
        BoxList=['PoloBox','White','Independiente']
        BoxList.sort()
        
        self.BoxListHost=['PoloBox','White','Independiente']
        #self.BoxListHostCompetitionHours=
        self.CategoryList=['Scaled-Base','Scaled-Advance','NotScaled-Base','NotScaled-Advance']
        
        
        self.stafigure=[None,None]
        
        # Widgets for the Log In Window
        self.UserName=widgets.Text(
        value='User Name',
        placeholder='Type something',
        description='UserName:',
        disabled=False,
        layout=Layout(width='auto', grid_area='UserName'),
        )
        self.PassWord=widgets.Password(
        value='********',
        description='Password:',
        disabled=False,
        layout=Layout(width='auto', grid_area='PassWord'),
        )
        self.LogIn=widgets.Button(
                    value=False,
                    description='Log in',
                    disabled=False,
                    indent=False,
                    layout=Layout(width='auto', grid_area='LogIn'),
                    
        )
        
        # Widgets to create a new user
        self.NewUserName=widgets.Text(
        value='User Name',
        placeholder='Type something',
        description='UserName:',
        disabled=False,
        layout=Layout(width='auto', grid_area='NewUserName'),
        )
        self.NewPassWord=widgets.Password(
        value='********',
        description='Password:',
        disabled=False,
        layout=Layout(width='auto', grid_area='NewPassWord'),
        
        )
        self.ConfirmPassWord=widgets.Password(
        value='********',
        placeholder='Confirm password',
        description='Confirm Password',
        disabled=False,
        layout=Layout(width='auto', grid_area='ConfirmPassWord'),
        )
        self.Box=widgets.Dropdown(
        options=BoxList,
        value=BoxList[0],
        description='HomeBox',
        layout=Layout(width='auto', grid_area='Box'),
        #layout=Layout(width='max-content', grid_area='Box'),
        )
        self.DateOfBirth=widgets.DatePicker(
        description='Birth date',
        disabled=False,
        layout=Layout(width='auto', grid_area='DateOfBirth'),
        )
        self.Gender=widgets.Dropdown(
        options=[('Female', 'M'),('Male', 'H')],
        value='M',
        description='Gender',
        #layout=Layout(width= 'max-content', grid_area='Gender'),
        layout=Layout(width='auto', grid_area='Gender'),
        #layout=Layout({'width': 'max-content'}, grid_area='Gender'),
        )
        
        self.heigth=widgets.IntText(
        value=0,
        description='Heigth[cm]',
        disabled=False,
        layout=Layout(width='auto', grid_area='heigth'),
        )   
        self.weight=widgets.IntText(
        value=0,
        description='Weight[Kg]',
        disabled=False,
        layout=Layout(width='auto', grid_area='weight'),
        )   
        style = {'description_width': '50px'}
        #Avocado
        self.Category=widgets.Dropdown(
        options=self.CategoryList,
        value=self.CategoryList[0],
        description='Category',
        #indent=False,
        #layout=Layout(width='auto', grid_area='Category'),
        layout=Layout(width='max-content', grid_area='Category'),
        style=style
        )
        
        self.CreateNewUserButton=widgets.Button(
                    value=False,
                    description='Create New User',
                    disabled=False,
                    indent=False,
                    layout=Layout(width='auto', grid_area='CreateNewUser'),
                    
        )
        
        self.CreateNewUserButton.on_click(self.CreateNewUser)
        
        self.WindowToPlot=widgets.Dropdown(
        options=['None','UserProfile', 'LeaderBoard', 'LeagueCalendar'],
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
                        
        
        
        
        
        
        self.check=widgets.Checkbox(
                    value=False,
                    description='Plot Statistics',
                    disabled=True,
                    indent=False
                    
        )
        


        # Widgets for WODs & Callenges
        # TODA ESTA PARTE TIENE QUE QUEDAR COMPLETAMENTE DEFINIDA ANES DEL INICIO DE LA COMPETICIÓN (LOS VIDEO E IMÁGENES ASOCIADAS A LOS WOD CUANDO LLEGUE LA FECHA DEL MES)
        self.CalendarMonths=['Semana1_1','Semana1_2'] # Hay que editar el self.Monthsgrid en consecuencia
        self.currentDate=datetime.date.today()
        self.currentMonth=datetime.date.today().month
        self.StartDate=datetime.date(2022,11,21)
        self.CalendarEndDates=[datetime.date(2022,11,28),datetime.date(2022,12,15)]
        self.WodNames=[ ['AlphaTest-1-PartA','AlphaTest-1-PartB'],
                         ['AlphaTest-2-PartA','AlphaTest-2-PartB'],
                          ]
                        
        
        # Youtube ID video associated to each wod
        self.YoutubeIDs=[ ["B58OYKDwV7w","B58OYKDwV7w"],
                         ["t-eRnB9pRNw","t-eRnB9pRNw"],
                         
                         ]
        
        # Type of mark of every Wod
        self.markType=[ ["Kgs","Time"],
                         ["Reps","Time"],
                         
                         ]
        
        # Active months para ir activando los meses con sus wods etc.. cuando llegue la fecha
        #self.ActiveMonths=['Semana1','Semana2']
        m=0
        for i in range(len(self.CalendarEndDates)):
            if(self.CalendarEndDates[i]<self.currentDate):
                m+=1
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
        self.WODcaledarOptions=self.WodNames[m]

               














               
        #self.WodsDescription=['September2022','October2022','November2022','December2022','January2023','February2023','March2023','April2023']
































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
        self.UserBenchMarksDict={"Strength":dict.fromkeys(self.Strength_BenchM),"Haltero":dict.fromkeys(Haltero_BenchM)}
    
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
            for w4,points in enumerate(zip(self.WodNamesFlat.copy(),UserWodPoints.copy()[w1])):
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
        description='Save new PR',
        disabled=False,
        button_style='', # 'success', 'info', 'warning', 'danger' or ''
        #tooltip='Description',
        layout=Layout(width='auto'),
        icon='' # (FontAwesome names without the `fa-` prefix)
        )
        #print('Ha entrado al widgets_functon')
        self.NewPR=widgets.FloatText(
        value=0.0,
        description='New PR:',
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
            
        self.grid.titles=['Log in','Create New User']

        LogIngrid=GridBox(children=[self.UserName,self.LogIn],
                      layout=Layout(
                          width='auto',
                          grid_template_columns='auto',
                          grid_template_rows='auto auto',
                          grid_template_areas='''
                            "UserName"
                            "LogIn"
                            '''
                          )
                     ) 

        
        NewUsergrid=widgets.GridBox(children=[self.NewUserName,self.CreateNewUserButton,self.DateOfBirth,self.Gender,self.heigth,self.weight,self.Box,self.Category,self.AvisoUserCreated],
                      layout=widgets.Layout(
                          width='auto',
                          grid_template_rows='auto auto auto auto auto auto auto auto auto',
                          grid_template_columns='auto',
                          grid_template_areas='''
                            "NewUserName"
                            "Gender"
                            "DateOfBirth"
                            "heigth"
                            "weight"
                            "Box"
                            "Category"
                            "CreateNewUser"
                            "AvisoUserCreated"
                            ''')
                                ) 
        for i, title in enumerate(self.grid.titles):
            self.grid.set_title(i, title)
        self.grid.children=[LogIngrid,NewUsergrid]
        
        
        #Check if the username is in the DataBase and confirm the password to show the user interface
        def checkAccess(b):
            # FALATA AÑADIR EL CHEQUEO DE PASSWORD, TENGO QUE MIRAR COMO GUARDARLOS DE  FORMA SEGURA Y SIN TEXTO PLANO
            if(self.UserName.value in self.DataBase.keys()):
                titles=[]
                children=[]
                # Defino un gridspeclayout para ahí definir el GridBox, con GridBox sólo no se actualiza
                self.UserProfile_grid = GridspecLayout(2, 8)
                titles.append('UserProfile')
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
                    inicio=time.time()
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
                titles.append('WODs/Challenges')
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
                                  grid_template_columns='auto auto',
                                  grid_template_areas='''
                                    "Semana1_1 Semana1_2"
                                
                                    ''')) 
                                         
                self.WodorChallenge=widgets.RadioButtons(
                options=['Wods', 'Challenges'],
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
                
                
                #self.gridSLMarks= GridspecLayout(3, 3,layout=Layout(width='auto'))   #Avocado
                
                def changeWODorChallenge(valor):
                    style = {'description_width': '35px'}
                    self.AvisoFormato.value="<b></b>"
                    file= open(os.path.join(os.getcwd(),self.WodorChaSelection.value+'_'+self.Category.value+'.png'), "rb")
                    
                    if((self.Category.value==self.DataBase[self.UserName.value]['Definition']['Category']) and ((self.CalendarEndDates[self.indiceMonth]-datetime.date.today()).days>=0) and (datetime.date.today()>=self.StartDate) ):
                    #if((self.Category.value==self.DataBase[self.UserName.value]['Definition']['Category']) and (self.DataBase[self.widgets_dict['UserName'].value]['WODmarks'][self.WodorChaSelection.value]==None) ):
                        Disabled=False
                    else:
                        Disabled=True
                    #Avocado
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
                        #Avocado
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
                
                if(self.Category.value==self.DataBase[self.UserName.value]['Definition']['Category']):
                    Disabled=False
                else:
                    Disabled=True
                #Avocado
                style = {'description_width': '35px'}
                
                #Avocado
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
                    #Avocado
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

                #Avocado
                self.Wods_grid[5,0:7]=widgets.Button(
                                    value=False,
                                    description='Enter result',
                                    disabled=False,
                                    indent=False,
                                    layout=Layout(width='auto', grid_area='LogIn'),
                                    style=style
                                        
                            )
                
                
                #Avocado        
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
                            
                    
                    if((self.CalendarEndDates[self.indiceMonth]-datetime.date.today()).days>=0):
                    #if(self.DataBase[self.widgets_dict['UserName'].value]['WODmarks'][self.WodorChaSelection.value]==None):
                        indice=self.WodNames[self.indiceMonth].index(self.WodorChaSelection.value)
                        
                        if(self.markType[self.indiceMonth][indice]=='Reps'):     
                            self.DataBase[self.widgets_dict['UserName'].value]['WODmarks'][self.WodorChaSelection.value]=self.Wods_grid[3,0:4].value
                            self.DataBase[self.widgets_dict['UserName'].value]['RawWODmarks'][self.WodorChaSelection.value]=str(self.Wods_grid[3,0:4].value)
                            self.AvisoFormato.value="<b>Data saved</b>"
                        if(self.markType[self.indiceMonth][indice]=='Kgs'):     
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
                
                
                self.Category_LeaderBoard=widgets.Dropdown(
                options=self.CategoryList,
                value=self.DataBase[self.UserName.value]['Definition']['Category'],
                description='Category',
                layout=Layout(width='auto', grid_area='Category_LeaderBoard'),
                )
                
                
                self.Gender_LeaderBoard=widgets.Dropdown(
                options=[('Female', 'M'),('Male', 'H')],
                value=self.DataBase[self.UserName.value]['Definition']['Gender'],
                description='Gender',
                layout=Layout(width='auto', grid_area='Gender_LeaderBoard'),
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
                    ResultadosNotScaledBaseMen=[]
                    KeysNotScaledBaseMen=[]
                    Resultados=[]
                    #self.rawMarks=[]
                    Names=[]
                    ResultadosNotScaledBaseWomen=[]
                    ResultadosNotScaledAdvanceMen=[]
                    ResultadosNotScaledAdvanceWomen=[]
                    # Esta parte se llama cuando ploteas leaderboard: Primero se lee el DataBase por is alguien ha metido datos nuevos y se sacan los
                    # resultados por wod y los nombres según categoria y sexo seleccionados
                    keys=self.DataBase.keys()
                    for i in range(len(keys)):
                        temp=[]
                        #temp2=[]
                        
                        if(self.DataBase[list(keys)[i]]['Definition']['Category']==Category):
                    
                            if(self.DataBase[list(keys)[i]]['Definition']['Gender']==Gender):
                                for key in(self.DataBase[list(keys)[i]]['WODmarks']):
                                    if(key in self.ActiveWodNamesFlat):
                                        temp.append(self.DataBase[list(keys)[i]]['WODmarks'][key])
                                    #temp2.append(self.DataBase[list(keys)[i]]['RawWODmarks'][key])
                                #ResultadosNotScaledBaseWomen.append(temp)
                                Resultados.append(temp)
                                #self.rawMarks.append(temp2)
                                Names.append(list(keys)[i])
                            '''
                            elif(self.DataBase[list(keys)[i]]['Definition']['Gender']==Gender):
                                for key in(self.DataBase[list(keys)[i]]['WODmarks']):
                    
                                    temp.append(self.DataBase[list(keys)[i]]['WODmarks'][key])
                                #ResultadosNotScaledBaseMen.append(temp)
                                Resultados.append(temp)
                                #KeysNotScaledBaseMen.append(list(keys)[i])
                                Names.append(list(keys)[i])
                            '''

                    #print('Resultados:',Resultados)
                    self.Names=Names
                    #print(Names) 
                    if(np.shape((np.asarray(Resultados)))[0]>0):   

                        # Una vez sacados estos datos, se realiza la puntuación y ordenación
                        for i in range(np.shape((np.asarray(Resultados)))[1]):
                            wodName=self.WodNamesFlat.copy()[i]
                            #print(wodName)
                            datos=np.asarray(Resultados)[:,i]
                            notnone=np.where(datos!=None)[0].tolist()
                            NombresConResultados=np.asarray(Names)[notnone]
                            #print(NombresConResultados)
                            #print(datos[notnone])
                            orden=[0]*len(datos[notnone])
                            positions=np.argsort(-datos[notnone])
                            for p,pos in enumerate(positions):
                                orden[pos]=p
                            #print(orden)
                            orden=np.asarray(orden)
                            if(len(orden)==1):
                                Puntos=[100]
                            else:
                                #Puntos=100-(orden*(100/(len(orden)-1)))
                                Puntos=(100-(orden*(100/(len(orden)-1))))
                            #print(Puntos)
                            self.datos=datos
                            unique=np.unique(datos[np.where(datos!=None)])
                            if (len(unique)!=len(datos)):
                                for d in range(len(unique)):
                                    donde=np.where(datos==unique[d])
                                    if (len(donde[0])>1):
                                        puntosdonde=Puntos[donde]
                                        ordendonde=orden[donde]
                                        Puntos[donde]=np.ones(len(puntosdonde))*np.max(puntosdonde)
                                        orden[donde]=np.ones(len(ordendonde))*np.min(ordendonde)
                            
                            
                            
                            
                            for j,Nombre in enumerate(NombresConResultados):
                                self.DataBase[Nombre]['WODpoints'][wodName]=Puntos[j]    
                                self.DataBase[Nombre]['WODpositions'][wodName]=orden[j]+1
                            if(i==0):
                                self.positions=positions
                                self.orden=orden
                                self.Puntos=Puntos
                                self.datos=datos
                                
                                
                                
       
                                
                                
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
                        
                                if(self.DataBase[list(keys)[i]]['Definition']['Gender']==Gender):
                                    for key in (self.DataBase[list(keys)[i]]['WODpoints']):
                                        if(key in self.ActiveWodNamesFlat):
                                            temp.append(self.DataBase[list(keys)[i]]['WODpoints'][key])
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
                        
                        '''
    
                        '''
                        
                        
                        
                        self.Points=Points
                        self.Positions=Positions
                        colNames_rawData=[s+'_rawData'for s in self.colNames]
                        colNames_positions=[s+'_positions'for s in self.colNames]
                        colNames_WodResultsYoutube=[s+'_youtube'for s in self.colNames]
                        self.PointsDataFrame=pd.DataFrame(self.Points,columns=self.colNames,index=self.Names)
                        self.IndiceDataFrame=self.PointsDataFrame.sort_values(by='Total', ascending=False)
                        posprueba=[]
                        for i in range(len(self.IndiceDataFrame['Total'].values)):
                            
                            if ((self.IndiceDataFrame['Total'].values[i]!=self.IndiceDataFrame['Total'].values[i-1]) or i==0):
                                posprueba.append(i+1)
                                
                            else:
                                posprueba.append(posprueba[i-1])
                        self.posprueba=posprueba
                                
                        Indice=pd.Index([j+' ('+str(posprueba[i])+')' for i,j in enumerate(self.IndiceDataFrame.index)])
                        #Indice=pd.Index([j+' ('+str(i+1)+')' for i,j in enumerate(self.IndiceDataFrame.index)]) Formato anterior de Indice, no ponía la misma posición a dos eprsonas con los mismos puntos globales
                        #self.PointsDataFrame=self.PointsDataFrame.set_index(self.Names)
                        
                        
                        
                        rawMarksDataFrame=pd.DataFrame(self.rawMarks,columns=colNames_rawData,index=self.Names)
                        PositionsDataFrame=pd.DataFrame(self.Positions,columns=colNames_positions,index=self.Names)
                        self.colNames_WodResultsYoutubeDataFrame=pd.DataFrame(WodResultsYoutube,columns=colNames_WodResultsYoutube,index=self.Names)
                        

                        self.prueba3=pd.concat([self.PointsDataFrame.round(2),PositionsDataFrame,rawMarksDataFrame,self.colNames_WodResultsYoutubeDataFrame], axis=1)
                        self.prueba3=self.prueba3.sort_values(by='Total', ascending=False)
                        self.prueba3=self.prueba3.set_index(Indice)
                        # Aquí se ordenan los dos dataframe por puntos totales o por mwod antes de unirlos
                        
                        #self.PointsDataFrame=self.PointsDataFrame.sort_values(by=self.WOD_LeaderBoard.value, ascending=False)

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
                    #self.final=self.final.sort_values(by='Total', ascending=False)
                    if(video):
                        export=self.final2
                    else:
                        export=self.final
                    
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
                
                
                
                LeaderBoardgrid=widgets.GridBox(children=[self.Video_LeaderBoard,self.Category_LeaderBoard,self.Gender_LeaderBoard,self.WOD_LeaderBoard,self.wid_LeaderBoard],
                              layout=widgets.Layout(
                                  width='auto',
                                  grid_template_rows='auto auto auto',
                                  grid_template_columns='auto auto auto auto',
                                  grid_template_areas='''
                                    "Video_LeaderBoard Category_LeaderBoard Gender_LeaderBoard WOD_LeaderBoard"
                                    "LeaderBoard LeaderBoard LeaderBoard LeaderBoard"
                                    "LeaderBoard LeaderBoard LeaderBoard LeaderBoard"
                                    ''')
                                        ) 
                
                
                #self.LeaderBoard_grid = GridspecLayout(2, 3,width='auto',height='700px')
                #self.LeaderBoard_grid = GridspecLayout(2, 3,width='auto',height='auto')
                #self.LeaderBoard_grid[1,0:2]=self.wid_LeaderBoard
                titles.append('LeaderBoard')
                #children.append(self.LeaderBoard_grid)
                children.append(LeaderBoardgrid)
                

#***************************************************************************************************************
#***************************************************************************************************************
#***************************************************************************************************************
#***************************************************************************************************************







                # TODO ESTO QUEDA PENDIENTE, QUIERO HACER UN CALENDARIO DE BOTONES PARA QUE DESPLIEGUEN LAS INVITACIONES CREADAS
                Optionswod=self.WODcaledarOptions.copy()
                Optionswod.insert(0,'All')
                Optionsbox=self.BoxListHost.copy()
                Optionsbox.insert(0,'All')
                self.PreviousDaySelected=None
                LeagueCalendarGrid= GridspecLayout(13,7,width='320px',height='auto')  
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
                self.OpenSpots_widget=widgets.IntText(
                    value=0,
                    description='Available spots',
                    disabled=False
                )
                self.AvailableInvitations=widgets.Output(layout={'border': '1px none black'})


                Time_picker = ipydatetime.TimePicker()
                def ColorActiveFilteredDays(b):
                    
                    if os.path.exists(os.path.join(os.getcwd(),'DataBase.users')):
                        with open(os.path.join(os.getcwd(),'DataBase.users'), 'rb') as fin:
                            self.DataBase=pickle.load(fin)
                    
                    for limpiar in (self.Days_Calendar_widget):
                        limpiar.style.button_color=None
                        Days_Calendar_np=np.asarray(self.Days_Calendar)
                        #active_days=[]
                    if(self.HostorGuest.value=='Join an invitation'):
                        for key in (self.DataBase.keys()):
                            sameBaseDiv=(self.DataBase[key]['Definition']['Category'].split('-')[0]==self.DataBase[self.widgets_dict["UserName"].value]['Definition']['Category'].split('-')[0] )
                            sameSubDiv=(self.DataBase[key]['Definition']['Category'].split('-')[1]==self.DataBase[self.widgets_dict["UserName"].value]['Definition']['Category'].split('-')[1])
                            if(sameBaseDiv): 
                                
                                
                                for dia in(self.DataBase[key]['Host'].keys()):
                                    activedaysinmonth=np.where(Days_Calendar_np==dia)[0]
                                    if(len(activedaysinmonth)>0):
                                        if((sameSubDiv and (self.DataBase[key]['Host'][dia][1]==self.WOD_filter.value or self.WOD_filter.value=='All') and (self.DataBase[key]['Definition']['HomeBox']==self.BOX_filter.value or self.BOX_filter.value=='All')) or ((((self.DataBase[key]['Host'][dia][1]==Optionswod[1]==self.WOD_filter.value) or ((self.DataBase[key]['Host'][dia][1]==Optionswod[1]) and (self.WOD_filter.value=='All'))) and (self.DataBase[key]['Definition']['HomeBox']==self.BOX_filter.value or self.BOX_filter.value=='All')))    ):
                                            self.Days_Calendar_widget[activedaysinmonth[0]].style.button_color='lightgreen'
                                
                                    '''    
                                        if((self.DataBase[key]['Host'][dia][1]==self.WOD_filter.value or self.WOD_filter.value=='All') and (self.DataBase[key]['Definition']['HomeBox']==self.BOX_filter.value or self.BOX_filter.value=='All')) :
                                            #print('dias activos',np.where(Days_Calendar_np==dia)[0][0])
                                            self.Days_Calendar_widget[np.where(Days_Calendar_np==dia)[0][0]].style.button_color='lightgreen'
                                    else:        
                                        if((self.DataBase[key]['Host'][dia][1]==Optionswod[0]) and (self.DataBase[key]['Definition']['HomeBox']==self.BOX_filter.value or self.BOX_filter.value=='All')) :
                                            #print('dias activos',np.where(Days_Calendar_np==dia)[0][0])
                                            self.Days_Calendar_widget[np.where(Days_Calendar_np==dia)[0][0]].style.button_color='lightgreen'
                                    '''    
                def ModifyCalendarOptions(b):
                    
                    for limpiar in (self.Days_Calendar_widget):
                        limpiar.style.button_color=None
                    #print(self.Days_Calendar_widget)    
                    if(self.PreviousDaySelected!=None):
                        self.Days_Calendar_widget[self.PreviousDaySelected].style.button_color=None
                    if(b['new']=='Create an invitation'):
                        
                        self.WOD_filter.options=self.WODcaledarOptions
                        self.WOD_filter.value=self.WODcaledarOptions[0]
                        self.BOX_filter.options=self.BoxListHost
                        self.BOX_filter.value=self.BoxListHost[0]
                        
                        
                        #self.WOD_filter.value=self.WODcaledarOptions[0]
                        LeagueCalendarGrid[0,:]=self.HostorGuest
                        LeagueCalendarGrid[6:11,:]=self.Daysgrid
                        LeagueCalendarGrid[2,:]=self.DummyWidget
                        LeagueCalendarGrid[3,:]=self.DummyWidget
                        LeagueCalendarGrid[4,:]=self.DummyWidget
                        LeagueCalendarGrid[5,0]=self.DummyWidget
                        LeagueCalendarGrid[12,:]=self.DummyWidget

                    elif(b['new']=='Join an invitation'):

                        self.WOD_filter.options=Optionswod
                        self.WOD_filter.value=Optionswod[0]
                        self.BOX_filter.options=Optionsbox
                        self.BOX_filter.value=Optionsbox[0]
                        Days_Calendar_np=np.asarray(self.Days_Calendar)
                        #active_days=[]
                        '''
                        for key in (self.DataBase.keys()):
                            if(self.DataBase[key]['Definition']['Category']==self.DataBase[self.widgets_dict["UserName"].value]['Definition']['Category']): 

                                for dia in(self.DataBase[key]['Host'].keys()):
                                    #if(self.DataBase[key]['Host'][dia][1]==self.WOD_filter.value):
                                    #print('dias activos',np.where(Days_Calendar_np==dia)[0][0])
                                    self.Days_Calendar_widget[np.where(Days_Calendar_np==dia)[0][0]].style.button_color='lightgreen'
                        '''
                        ColorActiveFilteredDays(self.DummyWidget)
                        '''
                        for key in (self.DataBase.keys()):
                            if(self.DataBase[key]['Definition']['Category'].split('-')[0]==self.DataBase[self.widgets_dict["UserName"].value]['Definition']['Category'].split('-')[0] ): 
                                
                                for dia in(self.DataBase[key]['Host'].keys()):
                                    if(self.DataBase[key]['Definition']['Category'].split('-')[1]==self.DataBase[self.widgets_dict["UserName"].value]['Definition']['Category'].split('-')[1] ):
                                        if((self.DataBase[key]['Host'][dia][1]==self.WOD_filter.value or self.WOD_filter.value=='All') and (self.DataBase[key]['Definition']['HomeBox']==self.BOX_filter.value or self.BOX_filter.value=='All')) :
                                            #print('dias activos',np.where(Days_Calendar_np==dia)[0][0])
                                            self.Days_Calendar_widget[np.where(Days_Calendar_np==dia)[0][0]].style.button_color='lightgreen'
                                    else:        
                                        if((self.DataBase[key]['Host'][dia][1]==Optionswod[0]) and (self.DataBase[key]['Definition']['HomeBox']==self.BOX_filter.value or self.BOX_filter.value=='All')) :
                                            #print('dias activos',np.where(Days_Calendar_np==dia)[0][0])
                                            self.Days_Calendar_widget[np.where(Days_Calendar_np==dia)[0][0]].style.button_color='lightgreen'
                        '''
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        

                        LeagueCalendarGrid[0,:]=self.HostorGuest
                        LeagueCalendarGrid[1,:]=self.WOD_filter
                        LeagueCalendarGrid[2,:]=self.BOX_filter
                        LeagueCalendarGrid[6:11,:]=self.Daysgrid
                        LeagueCalendarGrid[3,0]=self.DummyWidget
                        LeagueCalendarGrid[4,0]=self.DummyWidget
                        LeagueCalendarGrid[5,0]=self.DummyWidget
                        LeagueCalendarGrid[12,:]=self.DummyWidget
                        
                        
                def SaveGuest(b):
                    #print('Ha entrado a guardas un guest')

                    
                    
                    if os.path.exists(os.path.join(os.getcwd(),'DataBase.users')):
                        with open(os.path.join(os.getcwd(),'DataBase.users'), 'rb') as fin:
                            self.DataBase=pickle.load(fin)
                    # Agregar aqui condicional para que estén todos los campos rellenados antes de guardas la invitación        
                    

                    GuestList=self.DataBase[b.description.split('-|-')[1]]['Host'][self.Days_Calendar[self.PreviousDaySelected]][-1]
                    Spots=self.DataBase[b.description.split('-|-')[1]]['Host'][self.Days_Calendar[self.PreviousDaySelected]][-2]
                    if(Spots>=1 and (self.widgets_dict["UserName"].value not in GuestList) and (self.widgets_dict["UserName"].value!=b.description.split('-|-')[1])):
                        
                        self.DataBase[b.description.split('-|-')[1]]['Host'][self.Days_Calendar[self.PreviousDaySelected]][-2]=Spots-1
                        self.DataBase[b.description.split('-|-')[1]]['Host'][self.Days_Calendar[self.PreviousDaySelected]][-1].append(self.widgets_dict["UserName"].value)
                        if((Spots-1)==0):
                            b.style.button_color='red'
                        with open(os.path.join(os.getcwd(),'DataBase.users'), 'wb') as fout:
                                    pickle.dump(self.DataBase, fout)
                        
                        
                        
                        
                def DaySelected(b):
                    if(self.PreviousDaySelected!=None):
                        self.Days_Calendar_widget[self.PreviousDaySelected].layout.border = "2px None blue"

                    self.Days_Calendar_widget[int(b.description)-1].layout.border = "2px solid blue" #.layout=Layout(border='solid')
                    self.PreviousDaySelected=int(b.description)-1
                    if(self.HostorGuest.value=='Create an invitation'):


                        #print('Ha seleccionado un dia en creacion de ivitacion')
                        LeagueCalendarGrid[0,:]=self.HostorGuest
                        LeagueCalendarGrid[6:11,:]=self.Daysgrid
                        LeagueCalendarGrid[1,:]=self.WOD_filter
                        LeagueCalendarGrid[3,:]=Time_picker
                        LeagueCalendarGrid[4,:]=self.OpenSpots_widget
                        LeagueCalendarGrid[5,:]=self.CreateInvitation
                        LeagueCalendarGrid[12,0:5]=self.DummyWidget
                        LeagueCalendarGrid[12,5:]=self.DummyWidget
                        
                    elif(self.HostorGuest.value=='Join an invitation'):
                        
                        if os.path.exists(os.path.join(os.getcwd(),'DataBase.users')):
                            with open(os.path.join(os.getcwd(),'DataBase.users'), 'rb') as fin:
                                self.DataBase=pickle.load(fin)
                        self.Invitations=[]
                        self.InvitationsWidgets=[]
                        self.GuestsWidgets=[]
                        i=0
                        columnas=['Time','Host','Category','HomeBox','WOD','Available spots','Guests']
                        '''
                        for key in (self.DataBase.keys()):
                            if(self.DataBase[key]['Definition']['Category']==self.DataBase[self.widgets_dict["UserName"].value]['Definition']['Category']):   
                        '''       
                        for key in (self.DataBase.keys()):
                            sameBaseDiv=(self.DataBase[key]['Definition']['Category'].split('-')[0]==self.DataBase[self.widgets_dict["UserName"].value]['Definition']['Category'].split('-')[0] )
                            sameSubDiv=(self.DataBase[key]['Definition']['Category'].split('-')[1]==self.DataBase[self.widgets_dict["UserName"].value]['Definition']['Category'].split('-')[1])
                            #print('sameSubDiv: ',sameSubDiv)
                            if(sameBaseDiv): 
                                
                                
                                for dia in(self.DataBase[key]['Host'].keys()):
                                    if(self.Days_Calendar[self.PreviousDaySelected]==dia):
                                        
                                        if((sameSubDiv and (self.DataBase[key]['Host'][dia][1]==self.WOD_filter.value or self.WOD_filter.value=='All') and (self.DataBase[key]['Definition']['HomeBox']==self.BOX_filter.value or self.BOX_filter.value=='All')) or ( ((self.DataBase[key]['Host'][dia][1]==Optionswod[1]) and (self.DataBase[key]['Definition']['HomeBox']==self.BOX_filter.value or self.BOX_filter.value=='All')))    ):
                                            #self.Days_Calendar_widget[np.where(Days_Calendar_np==dia)[0][0]].style.button_color='lightgreen'
                                    
                                    
                                    
                                    
        
                                            #self.DataBase[key]['Host'][self.Days_Calendar[self.PreviousDaySelected]].insert(0,key)
                                            temp=self.DataBase[key]['Host'][self.Days_Calendar[self.PreviousDaySelected]].copy()
                                            temp[1:1]=([key,self.DataBase[key]['Definition']['Category'],self.DataBase[key]['Definition']['HomeBox']])
                                            
                                            self.Invitations.append(temp)
                                            texto=[str(s) for s in self.Invitations[i][0:-1]]
                                            texto=('-|-'.join(texto))
                                            self.InvitationsWidgets.append(widgets.Button(
                                                        description=texto,
                                                        disabled=False,
                                                        indent=False,
                                                
                                                        layout=Layout(width='auto')))
                                            
                                            if(len(self.Invitations[i][-1])>0):
                                                opciones=self.Invitations[i][-1]
                                                valor=self.Invitations[i][-1][0]
                                            else:
                                                
                                                opciones=['None']
                                                valor=opciones[0]
                                                
                                            self.GuestsWidgets.append(widgets.Dropdown(
                                            options=opciones,
            
                                            value=valor,
                                            description='',
                                            disabled=False,
                                            layout=Layout(width='auto')))
                                            
                                            
                                            self.InvitationsWidgets[i].on_click(SaveGuest)
                                            i+=1
                        self.InvitationsLayout= GridspecLayout(len(self.Invitations)+1, 5)
                        self.GuestsLayout= GridspecLayout(len(self.Invitations)+1, 1)
                        for j in range(len(self.Invitations)+1):
                            if (j==0):
                                self.InvitationsLayout[j,:]=widgets.Button(
                                            description=('-|-'.join(columnas[0:-1])),
                                            disabled=True,
                                            indent=False,
                                    
                                            layout=Layout(width='auto'))
                                
                                self.GuestsLayout[j,:]=widgets.Button(
                                            description=(columnas[-1]),
                                            disabled=True,
                                            indent=False,
                                    
                                            layout=Layout(width='auto'))
                                
                                
                            else:
                                self.InvitationsLayout[j,:]=self.InvitationsWidgets[j-1]
                                self.GuestsLayout[j,:]=self.GuestsWidgets[j-1]
                            
                        self.Invitations=sorted(self.Invitations, key=itemgetter(0))
                        #Probando=pd.DataFrame(self.Invitations,columns=columnas,index=None)
                        
                        self.AvailableInvitations.clear_output()
                        with self.AvailableInvitations:
                            #display(Probando)  
                            display(self.InvitationsLayout)
                        
                        

                        LeagueCalendarGrid[12,0:5]=self.AvailableInvitations
                        LeagueCalendarGrid[12,5:]=self.GuestsLayout
                        #print('Ha seleccionado un dia en UNIRSE a una invitacion')
                        
                        
                def createInvitation(b):
                    #print('Ha entreado a crear una invitacion')
                    if os.path.exists(os.path.join(os.getcwd(),'DataBase.users')):
                        with open(os.path.join(os.getcwd(),'DataBase.users'), 'rb') as fin:
                            self.DataBase=pickle.load(fin)
                    # Agregar aqui condicional para que estén todos los campos rellenados antes de guardas la invitación        
                    if(4>2):
                        self.DataBase[self.widgets_dict["UserName"].value]['Host'][self.Days_Calendar[self.PreviousDaySelected]]=[Time_picker.value,self.WOD_filter.value,self.OpenSpots_widget.value,[]]
                    

                    with open(os.path.join(os.getcwd(),'DataBase.users'), 'wb') as fout:
                                pickle.dump(self.DataBase, fout)
                    
                    
                    
                    
                self.HostorGuest=widgets.Dropdown(
                options=['Create an invitation','Join an invitation'],
                value='Join an invitation',
                description='Create or join',
                )
                self.WOD_filter=widgets.Dropdown(
                options=Optionswod,
                value=Optionswod[0],
                description='Wod',
                )
                self.BOX_filter=widgets.Dropdown(
                options=Optionsbox,
                value=Optionsbox[0],
                description='Box',
                )
                self.CreateInvitation=widgets.Button(
                            value=False,
                            description='Create Invitation',
                            disabled=False,
                            indent=False,
                            layout=Layout(width='auto'),
                            
                )
                
                self.CreateInvitation.on_click(createInvitation)
                self.HostorGuest.observe(ModifyCalendarOptions,'value')
                self.WOD_filter.observe(ColorActiveFilteredDays,'value')
                self.BOX_filter.observe(ColorActiveFilteredDays,'value')
                
                # then must create an object of the Calendar class
                cal = calendar.Calendar(firstweekday=0)
                year = datetime.date.today().year
                month =datetime.date.today().month
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
                for semana in range(len(calendario)):
                    if((len(calendario)-semana)==1):
                        Final=True
                    semana_firstEntry=True
                    semana_lastEntry=False
                    for i,fecha in enumerate(calendario[semana]):

                        if((len(calendario[semana])-i)==1):
                            semana_lastEntry=True
                
                        if(calendario[semana][i].month==datetime.date.today().month):
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
       
                
                LeagueCalendarGrid[0,:]=self.HostorGuest
                LeagueCalendarGrid[1,:]=self.WOD_filter
                LeagueCalendarGrid[2,:]=self.BOX_filter
                LeagueCalendarGrid[6:11,:]=self.Daysgrid
                LeagueCalendarGrid[12,:]=self.DummyWidget

                titles.append('LeagueCalendar')

                children.append(LeagueCalendarGrid)    

                
                ColorActiveFilteredDays(self.DummyWidget)
 
    
 
    
 
    
 
    
 
    
 
    
 
    
 
    
                self.grid.titles=titles
                self.grid.children=children
    
                for i, title in enumerate(self.grid.titles):
                    self.grid.set_title(i, title)
            
       
        self.LogIn.on_click(checkAccess)     
        
   
        return self.grid
    def CreateNewUser(self,b):

        
        
        
    
        
       #CREACION PERFILES DE USUARIO (DYNAMIC)
        if os.path.exists(os.path.join(os.getcwd(),'DataBase.users')):
            with open(os.path.join(os.getcwd(),'DataBase.users'), 'rb') as fin:
                self.DataBase=pickle.load(fin)
        userNamesList=list(self.DataBase.keys()) 
        #UserDefinition_List=list(self.DataBase[userNamesList[0]]['Definition'].keys())
        UserDefinition_List=self.UserDefinition_List
        #self.UserBenchMarksDict=list(self.DataBase[userNamesList[0]]['BenchMarks'].keys())
        if ((self.NewUserName.value not in userNamesList) and (self.DateOfBirth.value!=None)):
            username=self.NewUserName.value
            self.AvisoUserCreated.value="<b>User created, welcome to the league!</b>"
            #print('User created: Welcome to the league (Alpha test)')
            userNamesList.append(username)
            self.DataBase[username]={}  
            self.DataBase[username]['Definition']=dict.fromkeys(self.UserDefinition_List)
            self.DataBase[username]['BenchMarks']=self.UserBenchMarksDict.copy()
            self.DataBase[username]['WODpoints']=dict.fromkeys(self.WodNamesFlat)
            self.DataBase[username]['WODpositions']=dict.fromkeys(self.WodNamesFlat)
            self.DataBase[username]['WodResultsYoutube']=dict.fromkeys(self.WodNamesFlat)
            self.DataBase[username]['Host']={}
            self.DataBase[username]['Guest']={}
            
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
            
            
            with open(os.path.join(os.getcwd(),'DataBase.users'), 'wb') as fout:
                pickle.dump(self.DataBase, fout)
            
            
        else:
            print('User name already exists or Birth date is empty')
       
       
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
         DataPlotName=['RawData','ScaledData']
         
         self.mirar2=Data_Plot
         #for name in enumerate(self.DataBase.keys()): 
         
         for i in range(len(Data_Plot)):

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
            
        
