#%%
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 7 

@author: bcubrich
"""



import pandas as pd
import numpy as np
import seaborn as sns
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt

#These global vars are useful inside of some functions
global keep_oil
global keep_gas
global keep_water
global keep_facility
global keep_dict


'''--------------------------------------------------------------------------
GUI
---------------------------------------------------------------------------'''
from tkinter import *

master = Tk()

variable = StringVar(master)
variable.set("Oil") # default value

w = OptionMenu(master, variable, "Oil", "Gas", "facility_count", 'Condensate')
w.grid(row=1, sticky=W, column=0, columnspan=3)




def quit():
    global tp
    global var1
    global var2
    global var3
    global var4
    global var5
    global var6
    global var7
    var1=var1.get()
    var2=var2.get()
    var3=var3.get()
    var4=var4.get()
    var5=var5.get()
    var6=var6.get()
    var7=var7.get()
    tp=variable.get()
    master.destroy()
    

button = Button(master, text="OK", command=quit)
button.grid(row=10, sticky=W, column=2)

labelText=StringVar()
labelText.set("Choose TP")
label1=Label(master, textvariable=labelText, height=4)
label1.grid(row=0, sticky=W, column=1, columnspan=2)

labelText=StringVar()
labelText.set("Choose Ems")
label1=Label(master, textvariable=labelText, height=4)
label1.grid(row=2, sticky=W, column=1)


var1 = IntVar()
Checkbutton(master, text="PM10", variable=var1).grid(row=3, sticky=W, column=1)
var2 = IntVar()
Checkbutton(master, text="PM25", variable=var2).grid(row=4, sticky=W, column=1)
var3 = IntVar()
Checkbutton(master, text="SOX", variable=var3).grid(row=5, sticky=W, column=1)
var4 = IntVar()
Checkbutton(master, text="NOX", variable=var4).grid(row=6, sticky=W, column=1)
var5 = IntVar()
Checkbutton(master, text="VOC", variable=var5).grid(row=3, sticky=W, column=2)
var6 = IntVar()
Checkbutton(master, text="CO", variable=var6).grid(row=4, sticky=W, column=2)
var7 = IntVar()
Checkbutton(master, text="CH20", variable=var7).grid(row=5, sticky=W, column=2)


mainloop()


#The following function is just used to get filepaths
#I usually just run it once to get the path, and then leave this 
#fucntion so that I can get othe rpaths if needed
def get_dat():
    root = Tk()
    root.withdraw()
    root.focus_force()
    root.attributes("-topmost", True)      #makes the dialog appear on top
    filename = askopenfilename()      # Open single file
    
    return filename



'''----------------------------------------------------------------------------
                                 2014 Data
----------------------------------------------------------------------------'''

#next 14 lines import the data
api_id=pd.read_csv('U:/PLAN/BCUBRICH/Small OG Operators/Data/apis_2014.csv',
                   usecols=['api', 'operator_id'])
operator_id_2014 = pd.read_csv(r'U:/PLAN/BCUBRICH/Small OG Operators/Data'\
                               r'/company_info_with_assoc_2014.csv')
facility_id_2014 = pd.read_csv(r'U:/PLAN/BCUBRICH/Small OG Operators/Data/'\
                               r'facility_summary_2014.csv'''
                               ,usecols=['facility_id', 'operator_id'])
company_emit_2014 = pd.read_csv(r'U:/PLAN/BCUBRICH/Small OG Operators/Data/'\
                               r'company_summary_2014.csv''')
dogm_production_2014 = pd.read_csv(r'U:/PLAN/BCUBRICH/Small OG Operators/'\
                                   r'Data/2014Producing_Shutin_'\
                                   r'OilandGasWells_Python.csv',
                                   usecols=['API', 'Oil','Gas',
                                            'Water', 'Condensate'])

    
api_dict=api_id.set_index('api').T.to_dict('list')       #create a dict to assign operators to apis
facility_count_2014 = facility_id_2014.groupby('operator_id').count()   #get facility count from dict
count_dict_2014 = facility_count_2014.T.to_dict('list')
facility_dict_2014=facility_id_2014.set_index('facility_id').T.to_dict('list')

    
'''The following is helpful if you have data for a range of years,
 which I no longer have, but did before'''
#dogm_production_2014['ReportPeriod']=pd.to_datetime(dogm_production_2014['ReportPeriod'])
#dogm_production_2014=dogm_production_2014[dogm_production_2014['ReportPeriod'].dt.year>=2014]
#dogm_production_2014=dogm_production_2014[dogm_production_2014.ReportPeriod.str.contains('2014')]    #get only 2014 data
#dogm_production_2014['API']=dogm_production_2014['API'].astype(str)                                   #convert API to str

dogm_production_2014['operator_id']=dogm_production_2014['API'].map(api_dict).str[0]                 #map the operator ID to the API no
company_tp_2014=dogm_production_2014.groupby('operator_id').agg({'Oil':'sum',
                                        'Gas':'sum',
                                        'Water':'sum',
                                        'Condensate':'sum',
                                        'API':'count'}).reset_index().rename({
                                                'API':'well_count'}, axis='columns')
company_tp_2014['data_year']=2014
company_tp_2014=pd.merge(company_tp_2014,operator_id_2014,how='outer',on='operator_id')


    
company_tp_2014['facility_count']=company_tp_2014['operator_id'].map(count_dict_2014).str[0]   #add facility count data
company_tp_2014=company_tp_2014[company_tp_2014['operator_id']<32]   #only want 2014 operators

'''----------------------------------------------------------------------------
                                 2017 Data
----------------------------------------------------------------------------'''


operator_id_2017 = pd.read_csv(r'U:/PLAN/BCUBRICH/Small OG Operators/Data'\
                               r'/company_info_with_assoc_2017.csv')
company_emit_2017 = pd.read_csv(r'U:/PLAN/BCUBRICH/Small OG Operators/'\
                                r'Data/company_summary_2017.csv')

data_year_id=pd.read_csv(r'U:/PLAN/BCUBRICH/Small OG Operators'\
                         r'/Data/operator_info.csv',
                         usecols=['data_year','operator_id'])
facility_tp_2017 = pd.read_csv('U:/PLAN/BCUBRICH/Small OG Operators/Data/facilities_list_2017.csv').fillna(0)
company_tp_2017=facility_tp_2017.groupby('operator_id').agg({'facility_prod_oil':'sum',
                                        'facility_prod_gas':'sum',
                                        'facility_prod_water':'sum',
                                        'facility_prod_condensate':'sum',
                                        'facility_id':'count'}).reset_index().rename({
                                                'facility_id':'facility_count',
                                                'facility_prod_oil':'Oil',
                                                'facility_prod_gas':'Gas',
                                                'facility_prod_water':'Water',
                                                'facility_prod_condensate':'Condensate'
                                                }, axis='columns')
                                                
company_tp_2017=pd.merge(company_tp_2017,data_year_id,how='outer')
company_tp_2017=pd.merge(company_tp_2017,operator_id_2017,how='outer')
company_tp_2017=company_tp_2017[company_tp_2017['data_year']==2017]
company_tp_2017['well_count']='?'

final_tp_2017=facility_tp_2017[['facility_name','facility_prod_water',
                               'facility_prod_oil', 'facility_prod_gas', 
                               'facility_prod_condensate', 'operator_id']]
tp_2017=pd.merge(final_tp_2017,data_year_id,how='inner')
tp_2017=pd.merge(final_tp_2017,operator_id_2017,how='inner')
#tp_2017.to_csv('U:/PLAN/BCUBRICH/Small OG Operators/Facility_TP_2017.csv')

'''-------------------------------------------------------------------------'''
'''---------------2017QC----------------------------------------------------'''

'''The following section qcs DOGM vs Inventory data, but it's a bit slow due
to all the entries, uncomment ot run '''

#api_id_2017=pd.read_csv('U:/PLAN/BCUBRICH/Small OG Operators/Data/apis.csv',
#                   usecols=['api', 'operator_id'])
#api_dict_2017=api_id_2017.set_index('api').T.to_dict('list')       #create a dict to assign operators to apis
#dogm_production_2017 = pd.read_csv(r'U:/PLAN/BCUBRICH/Small OG Operators/'\
#                                   r'Data/Production2015To2020.csv',
#                                   usecols=['API', 'Oil','Gas',
#                                            'Water', 'ReportPeriod'])
#
#
#'''The following is helpful if you have data for a range of years,
# which I no longer have, but did before'''
#dogm_production_2017=dogm_production_2017[dogm_production_2017.ReportPeriod.str.contains('2017')]    #get only 2014 data
#dogm_production_2017['API']=dogm_production_2017['API'].astype(str)                                   #convert API to str
#
##next, map the operator ID to the API no. the '.str[0]' 
##bit makes the outcome a number instead of a list
#
#condensate=False
#if condensate==True: 
#    dogm_production_2017=dogm_production_2017.groupby('API').agg({'Oil':'sum',
#                                            'Gas':'sum',
#                                            'Water':'sum'}).reset_index() 
#    dogm_production_2017['Condensate']=np.where(dogm_production_2017['Gas']>dogm_production_2017['Oil'],dogm_production_2017['Oil'],0)    
#    dogm_production_2017['Oil']=np.where(dogm_production_2017['Condensate']>0,0,dogm_production_2017['Oil'])  
#else:
#    dogm_production_2017['Condensate']=0
#    
#dogm_production_2017['operator_id']=dogm_production_2017['API'].map(api_dict_2017).str[0]
#
#qc_tp_2017=dogm_production_2017.groupby('operator_id').agg({'Oil':'sum',
#                                        'Gas':'sum',
#                                        'Water':'sum',
#                                        'Condensate':'sum',
#                                        'API':'count'}).reset_index().rename({
#                                                'API':'well_count'}, axis='columns')  
#
#
#    
##Add compaany name and id to df
#qc_tp_2017=pd.merge(qc_tp_2017,operator_id_2017,how='outer', on='operator_id')             
#
##combine companies who have two operator ids (one from 2014)
#company_tp_2017_qc=qc_tp_2017.groupby('company_id').agg({'Oil':'sum',
#                                        'Gas':'sum',
#                                        'Water':'sum',
#                                        'Condensate':'sum',
#                                        'well_count':'sum'}).reset_index()
#
#if condensate==False: company_tp_2017_qc['Condensate']='Not Calculated'
##Add compaany name and id to df (lost in last line)
#company_tp_2017_qc=pd.merge(company_tp_2017_qc,company_tp_2017,how='outer', on='company_id') 
#    
##uncommment next line if you want to write 2017 inventory vs DOGM data to file
#company_tp_2017_qc.to_csv('U:/PLAN/BCUBRICH/Small OG Operators/Data/Company_TP_2017_QC.csv')


'''----------------------------------------------------------------------------
                                    Data Join/Merge
----------------------------------------------------------------------------'''

#simplify df for pairplot
plot_data_2017=company_tp_2017[['facility_count','Water',
                               'Oil', 'Gas', 
                               'Condensate']].copy()
#simplify df for pairplot
plot_data_2014=company_tp_2014[['facility_count','Water',
                               'Oil', 'Gas', 
                               'Condensate']].copy()

combined_tp=pd.concat([company_tp_2014, company_tp_2017], sort=False).dropna()

#next, if there are 2014 and 2017 entries for a company keep only 2017
combined_tp_trim=combined_tp.sort_values(['company_id',
                                          'data_year']).drop_duplicates(subset='company_name', keep='last')

combined_plot_dat=combined_tp_trim[['facility_count','Water',
                               'Oil', 'Gas']].copy()


tp_emission_all=pd.merge(combined_tp,company_emit_2017,how='outer',on='operator_id')



def quantiles(data, q):
    for col in data.columns:
        print(col)
        test=np.percentile(data[col], q)
        print(test)
'''uncomment for a qauntiles assesment'''
#quantiles(combined_plot_dat, 50)




'''----------------------------------------------------------------------------
                      Plotting to Determine "Small Company'
----------------------------------------------------------------------------'''


'''Plot a pairwise correlation crossplot'''
#sns.pairplot(combined_plot_dat,  kind='reg', plot_kws={'line_kws':{'color':'red'}, 'scatter_kws': {'alpha': 0.1}})
#sns.pairplot(combined_plot_dat,  kind='scatter', plot_kws={'alpha': 0.4, 'edgecolor':"0.5"})
#sns.pairplot(plot_data_2014)
#sns.pairplot(plot_data_2017)
'''plot histograms of each important column'''
#plot_data_2017.plot.hist(subplots=True)
#combined_plot_dat.plot.hist(subplots=True)
'''plot kernal density estimates of each important column'''
#plot_data_2017.plot.kde(subplots=True)
#combined_plot_dat.facility_count.plot.kde(subplots=True)




def plot_facility_count(combined_plot_dat):
    f, (ax1, ax2) = plt.subplots(2, 1)
    sns.kdeplot(combined_plot_dat['facility_count'], ax=ax1)
    ax1.axvline(np.percentile(combined_plot_dat['facility_count'], 50), c='0')
    f.text(0.15, 0.9, s=str(np.percentile(combined_plot_dat['facility_count'],50)))
    
    sns.kdeplot(np.log10(combined_plot_dat['facility_count']), ax=ax2)
    #ax2.axvline(np.percentile(np.log10(combined_plot_dat['facility_count']), 50), c='orange')
    #f.text(0.4, 0.25, s=str(np.around(10**np.percentile(np.log10(combined_plot_dat['facility_count']),50),0)))
    sns.kdeplot(np.log(combined_plot_dat['facility_count']), ax=ax2)

'''uncomment for histograms of facility count'''
#plot_facility_count(combined_plot_dat)

small_company_data=tp_emission_all.copy().dropna()
len_total=len(small_company_data)

keep_oil=2.1e6
keep_gas=4.4e6
keep_water=3.5e6
keep_facility=30
keep_dict={'Oil':keep_oil,'Gas':keep_gas,'Water':keep_water, 
           'facility_count':keep_facility,
           'Condensate':0}   #use this dict later to plot cuttoffs

small_company_data['company_size']=np.where((small_company_data['facility_count']<keep_facility) &
                            (small_company_data['Gas']<keep_gas) &
                            (small_company_data['Oil']<keep_oil) &
                            (small_company_data['Water']<keep_water), 
                            'Minor', 'Major')

'''Write results to output csv on next line, commented out to nut rewrite'''
#print(small_company_data.columns)
#small_company_data.to_csv('U:/PLAN/BCUBRICH/Small OG Operators/Combined_TP_Emissions_2014_2017.csv')
len_final=len(small_company_data[small_company_data['company_size']=='Minor'])
percent_kept=len_final/len_total

#Plot the relationship between number of facilities and percentiles
def percentile_plot(combined_plot_dat):
    qs=np.arange(0,max(combined_plot_dat['facility_count']))
    qp=qs/max(combined_plot_dat['facility_count'])*100
    percentiles=np.percentile(combined_plot_dat['facility_count'],q=qp)
    f, (ax1, ax2) = plt.subplots(2, 1)
    ax1.plot(percentiles,qp)
    ax1.set_ylabel('Percentile')
    ax1.axvline(30, c='0')
    percentile_df=pd.DataFrame([qs,qp, percentiles], index=['counts','linear_percent', 'percentile']).T
    percentile_df['binned']=pd.cut(percentile_df['percentile'], qs, labels=qs[1:])
    percentile_df=percentile_df.groupby('binned').agg({'linear_percent':'min'}).reset_index().dropna()
    percentile_df['change']=percentile_df['linear_percent']-percentile_df['linear_percent'].shift(1)
    ax2.plot(percentile_df['binned'].astype(int),percentile_df['change'])
    ax2.set_ylabel('Percent change')
    ax2.set_xlabel('Number of Facilities')
    ax2.axvline(30, c='0')
    
#turn the above plotting on or off with comment    
#percentile_plot(combined_plot_dat)
'''----------------------------------------------------------------------------
                         Emission Analyses
----------------------------------------------------------------------------'''
def abline(slope, intercept):
    """Plot a line from slope and intercept"""
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + slope * x_vals
    plt.plot(x_vals, y_vals, '--')



#Plot emissions vs any of the production types

def plot_emit(tp,df):
    count=0
    
    
    keep=keep_dict.get(tp)
    rhos=[]
    
    if len(df.columns)==2: 
        emit=df.columns[1]
        f, ax = plt.subplots(1, 1)
        x=df[tp]             #use throughput as independent variable
        y=df[emit]           #use each emmisions in loop to get dependent var
        ax.scatter(x,y, alpha=0.6)
        ax.set_ylabel(emit[3:], fontsize=12)
        m,b=np.polyfit(x,y,1)
        corr=np.corrcoef(x,y)
        x_vals = np.arange(0,max(x), step=max(x)/10)
        y_vals = b + m * x_vals
        ax.plot(x_vals, y_vals, '-',c='0')
        ax.text(100,max(y)/10*8, s=('slope = {:.2e}'.format(m)), fontsize=8)
#        ax.text(100,max(y)/10*6, s=np.around(b,2), fontsize=8)
        ax.text(100,max(y)/10*6, s=('rho = ' 
                + str(np.around(corr[0,1],2))), fontsize=8)
#        ax.axvline(keep, c='r')             #turn this back on if you wnat to see small company cutoff
        if count<6: ax.set_xticklabels([])  
        count+=1
        rhos.append(corr[0,1])
    
    
    
    else:
        f, axs = plt.subplots(len(df.columns)-1, 1)
        axs = axs.reshape(-1)
        for ax,emit in zip(axs,df.columns[1:]):
            x=df[tp]             #use throughput as independent variable
            y=df[emit]           #use each emmisions in loop to get dependent var
            ax.scatter(x,y, alpha=0.6)
            ax.set_ylabel(emit[3:], fontsize=12)
            m,b=np.polyfit(x,y,1)
            corr=np.corrcoef(x,y)
            x_vals = np.arange(0,max(x), step=max(x)/10)
            y_vals = b + m * x_vals
            ax.plot(x_vals, y_vals, '-',c='0')
            ax.text(100,max(y)/10*8, s=('slope = {:.2e}'.format(m)), fontsize=8)
    #        ax.text(100,max(y)/10*6, s=np.around(b,2), fontsize=8)
            ax.text(100,max(y)/10*6, s=('rho = ' 
                    + str(np.around(corr[0,1],2))), fontsize=8)
#            ax.axvline(keep, c='r')        #turn this back on if you wnat to see small company cutoff
            if count<6: ax.set_xticklabels([])  
            count+=1
            rhos.append(corr[0,1])
        
    rhos=np.asarray(rhos)
    f.text (0.75,0.9,'Average rho = {:.2}'.format(np.mean(rhos)))    
    f.text(0.5, 0.06, s=tp, fontsize=16)
#    f.text(keep/max(x)+0.03,0.9,'Small Company Cuttoff = {:.2e}'.format(keep))
    prod_=' Production'
    if tp == 'facility_count': prod_=''
    f.suptitle('Emissions Vs '+ tp + prod_, fontsize=18, weight='bold')
    
#    plt.show()

'''---------------------------------------------------------------------------
                                    Analysis
----------------------------------------------------------------------------'''

'''---                                                                   -----
This part is the interactive analysis. A gui here would really help this be an 
analysis tool. You can choose what production type and what emissions 
you want to plot, and it will fit a regression and plot them automatically
---                                                                      ---'''

#Plot Oil vs Emissions
#tp='Oil'
#analysis_cols=[tp,'em_pm10','em_pm25', 'em_sox',
#               'em_voc','em_nox', 'em_co','em_ch2o']
#df=tp_emission_all[analysis_cols].dropna()
##plot_emit(tp, df)     #uncomment to plot oil
#
##Plot Gas vs Emissions
#tp='Gas'
#analysis_cols=[tp,'em_pm10','em_pm25', 'em_sox',
#               'em_voc','em_nox', 'em_co','em_ch2o']
#df=tp_emission_all[analysis_cols].dropna()
##plot_emit(tp, df)               #uncomment to plot gas
#
#
##Plot Water vs Emissions
#tp='Water'
#analysis_cols=[tp,'em_pm10','em_pm25', 'em_sox',
#               'em_voc','em_nox', 'em_co','em_ch2o']
#df=tp_emission_all[analysis_cols].dropna()
##plot_emit(tp, df)               #uncomment to plot water
#
#
##Plot Condensate vs Emissions
#tp='Condensate'
#analysis_cols=[tp,'em_pm10','em_pm25', 'em_sox',
#               'em_voc','em_nox', 'em_co','em_ch2o']
#df=tp_emission_all[analysis_cols].dropna()
##plot_emit(tp, df)          #uncomment to plot condensate
#
#
##Plot facility_count vs Emissions
#tp='facility_count'
#analysis_cols=[tp,'em_pm10','em_pm25', 'em_sox',
#               'em_voc','em_nox', 'em_co','em_ch2o']
#df=tp_emission_all[analysis_cols].dropna()
#plot_emit(tp, df)          #uncomment to plot facility_count


var1='em_pm10' if var1==1 else ''
var2='em_pm25' if var2==1 else ''
var3='em_voc' if var3==1 else ''  
var4='em_sox' if var4==1 else ''
var5='em_nox' if var5==1 else ''
var6='em_co' if var6==1 else ''
var7='em_ch2o' if var7==1 else ''

list_var=var1+' '+var2+' '+var3+' '+var4+' '+var5+' '+var6+' '+var7
list_split=list_var.split()
analysis_cols=[tp]
for item in list_split:
    analysis_cols.append(item)

df=tp_emission_all[analysis_cols].dropna()
plot_emit(tp, df)

































