#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 21:24:09 2017

@author: cataraucorina
"""

import pandas as pd
import random


#Function that prints the results after each year
#nr of breed c agents
#nr of breed nc agents
#nr of gained,lost,regained agents
def create_out_result(year,model,df):
    
   #by using keys, allows us to add extra breeds to the csv file if needed, without modifying the code 
   for i in range(0,model['Agent_Breed'].value_counts().keys().size):
       df.loc[year,str(model['Agent_Breed'].value_counts().keys()[i])]=model['Agent_Breed'].value_counts()[model['Agent_Breed'].value_counts().keys()[i]]
    
  
   df.loc[year,'Year']=year
   #keys() it's used because we don't always have all the flags 
   for i in range(0,model['Flag'].value_counts().keys().size):
       df.loc[year,str(model['Flag'].value_counts().keys()[i])]=model['Flag'].value_counts()[model['Flag'].value_counts().keys()[i]]
   

#Prints to txt file
def model_output(year,model,file):
    count_breed_c=0
    count_breed_nc=0
    
    file.write("Year:"+str(year)+"\n") 
    for i in range(0,model.shape[0]):
        if (model['Agent_Breed'][i] == 'Breed_C'):
            count_breed_c=count_breed_c+1
        else:
            if (model['Agent_Breed'][i] == 'Breed_NC'):
                count_breed_nc=count_breed_nc+1
    file.write("Number of breed C agents:"+str(count_breed_c)+"\n") 
    file.write("Number of breed NC agents:"+str(count_breed_nc)+"\n") 
    #keys() it's used because we don't always have all the flags 
    for i in range(0,model['Flag'].value_counts().keys().size):
        file.write(str(model['Flag'].value_counts().keys()[i])+":"+str(model['Flag'].value_counts()[model['Flag'].value_counts().keys()[i]])+"\n")
    
    file.write("----------------------------------------------"+"\n")

def breed_nc_switch(model,i):
    model.loc[i,'Agent_Breed']='Breed_NC'
    #changing the flag value to lost in order to mark the change
    if(model.loc[i,'Flag'] == 'Default') or (model.loc[i,'Flag']=='Regained'):
        model.loc[i,'Flag']='Lost'
        
def breed_c_switch(model,i):
     model.loc[i,'Agent_Breed']='Breed_C'
     if(model.loc[i,'Flag'] == 'Default'):
         model.loc[i,'Flag']='Gained'
     if(model['Flag'][i]=='Lost'):
         model.loc[i,'Flag']='Regained'

def switch_breed(condition,consequence,model,i):
    if condition:
        consequence(model,i)
        
    
#Flag element is added to see when changes are made to the breed C            
def initialise_flag(model):
    for i in range(0,model.shape[0]):
        model['Flag']='Default' 

#method is called recursively for 15 years
def run_model(years,model,txt,period):
    #I choose brand_factor randomly from the given interval
    brand_factor = random.uniform( 0.1, 2.9 )
    
    if (years == period):
        print('done')
    else:
        
        for i in range(0,model.shape[0]):
            if (model['Auto_Renew'][i] != 1):
                rand = random.random() * 3
                aux=(rand * model['Attribute_Promotions'][i] * model['Inertia_for_Switch'][i])
                affinity = model['Payment_at_Purchase'][i]/model['Attribute_Price'][i] + aux
                breed = model.loc[i,'Agent_Breed']
                
                condition_breed_nc=(breed == 'Breed_C') and (affinity < model['Social_Grade'][i] * model['Attribute_Brand'][i])
                switch_breed(condition_breed_nc,breed_nc_switch,model,i)
                
                condition_breed_c=(condition_breed_nc == False) and(breed == 'Breed_NC') and (affinity < model['Social_Grade'][i] * model['Attribute_Brand'][i] * brand_factor)
                switch_breed(condition_breed_c,breed_c_switch,model,i)
               
        create_out_result(years,model,txt)
        years=years+1
        run_model(years,model,txt,period)

                   
        

def initialise_parameters(csvIn,csvColumns,period,csvOut):
    file=pd.read_csv(csvIn)
    df = pd.DataFrame(columns=csvColumns)
  
    #adding a flag to determine when the breed of an agent has changed
    initialise_flag(file)
    run_model(0,file,df,period)
    df.to_csv(csvOut)    
        
    
    

def main():
    columns= ['Year', 'Breed_C','Breed_NC','Gained','Lost','Regained']
    initialise_parameters('Simudyne_Backend_Test.csv',columns,15,'result_breeds.csv')
   
    

  

if __name__== '__main__':
    main()
    