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

    
#Flag element is added to see when changes are made to the breed C            
def initialise_flag(model):
    for i in range(0,model.shape[0]):
        model['Flag']='Default' 

#method is called recursively for 15 years
def run_model(years,model,txt):
    #I choose brand_factor randomly from the given interval
    brand_factor = random.uniform( 0.1, 2.9 )
    
    if years == 15:
        print("done")
    else:
        years=years+1
        for i in range(0,model.shape[0]):
            if (model['Auto_Renew'][i] == 1):
                rand = random.random() * 3
                aux=(rand * model['Attribute_Promotions'][i] * model['Inertia_for_Switch'][i])
                affinity = model['Payment_at_Purchase'][i]/model['Attribute_Price'][i] + aux
                breed = model.loc[i,'Agent_Breed']
                if (breed == 'Breed_C') and (affinity < model['Social_Grade'][i] * model['Attribute_Brand'][i]):
                    model.loc[i,'Agent_Breed']='Breed_NC'
                    #changing the flag value to lost in order to mark the change
                    if(model.loc[i,'Flag'] == 'Default') or (model.loc[i,'Flag']=='Regained'):
                        model.loc[i,'Flag']='Lost'
                    
                    
                else:
                    if (breed == 'Breed_NC') and (affinity < model['Social_Grade'][i] * model['Attribute_Brand'][i] * brand_factor):
                        model.loc[i,'Agent_Breed']='Breed_C'
                        if(model.loc[i,'Flag'] == 'Default'):
                            model.loc[i,'Flag']='Gained'
                        if(model['Flag'][i]=='Lost'):
                            model.loc[i,'Flag']='Regained'
        model_output(years,model,txt)
        run_model(years,model,txt)

                   
        
        
        
    
    

def main():
    file=pd.read_csv('Simudyne_Backend_Test.csv')
    txt = open("symudine_results.txt","w") 
    #adding a flag to determine when the breed of an agent has changed
    initialise_flag(file)
    run_model(0,file,txt)
    txt.close() 
    

  

if __name__== '__main__':
    main()
    