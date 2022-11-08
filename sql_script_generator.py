

# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 15:42:02 2020

@author: u6029558
"""
#importing libraies and classes 
import pandas as pd
from nltk.corpus import stopwords
from textblob import TextBlob
import re
from nltk.corpus import stopwords
import os


#definng function that will return list of diagnosis code for exclusion 
def excl(a):
       
    for index, value in df3.items():
        if index == a:
            econtent =TextBlob(value)
            ewordlist = []
            ewordlists =[]
            ewordlist = econtent.words
            ewordlists =  [ex for exs in ewordlist for ex in exs.split(',')]
    
            ewordlist2 = []
            ep = re.compile('([\d]|[A-Z\d]{1,})([\-]|[\–])')
                        
            ep2 = re.compile('([A-Z]|[A-Z0-9]{1,})(x)')
    
            enew_lists = []
            efinal_list = []
        
            for word in reversed(ewordlists):
                if len(word) >= 3:
                    word = word.replace('.', '')
                    ewordlist2.append(word)
            
            exlist = []
            for word in reversed(ewordlist2):       
                if ep2.match(word):
                    exlist.append(word)
                    ewordlist2.remove(word)
            
            for word in reversed(ewordlist2):
                if ep.match(word):
                    enew_lists.append(word)
                    ewordlist2.remove(word)
            
            enew = []
            for el in enew_lists:
                em = re.match(r'^([A-Z]*)(\d+)[\-|\–]\1*(\d+)$', el)
                if em:
                    enew += [em.group(1) + str(i) for i in range(int(em.group(2)), int(em.group(3))+1)]
                else:
                    enew += [el]

            efinal_list = ewordlist2 + enew
        
            return efinal_list, exlist
        else: pass
   
#defining function that will return list of procedure code for exclusion
def exclproc(a):
    for index, value in df4.items():
        eprocs  = TextBlob(df4.iloc[a])
        eproc_list = eprocs.words
        eproc_list = [x for xs in eproc_list for x in xs.split(',')]
        return eproc_list

#getting current working directory path
path = os.getcwd()

#assigning variable to analytical file name @inputfilename
input_filename = 'mental_health_codes.xlsx'
input_filetype = 'case'

#joinng working directory path and analytical file name @inputsheetname
df_path = os.path.join(path, input_filename)

#reading excel file        
df = pd.read_excel(df_path, 'Sheet2', dtype = {'variable':str, 'inc_icd9':str, 'inc_icd10':str, 'inc_proc':str, 'exc_icd9':str, 'exc_icd10':str, 'exc_proc':str})

#table name @inpat @outpat
table_used = 'service'


#extracting multiple dataframes from single dataframe and convering rows into string
df0 = df['variable'].map(str)
df1 = df['inc_icd9'].map(str) + ' ' + df['inc_icd10'].map(str)
df2 = df['inc_proc'].map(str)
df3 = df['exc_icd9'].map(str) + ' ' + df['exc_icd10'].map(str)
df4 = df['exc_proc'].map(str)



#assigning output file name based on inputfile name
if  input_filetype == 'case': 
    filename = os.path.splitext(input_filename)[0] + '_case_when_script'
else:
    filename = os.path.splitext(input_filename)[0] + '_cohort_script'


#opening of text file for truncating all the exisitng content
with open("%s.txt" % filename, "a+") as f:
    # Always clear content before writing
    f.truncate(0)
    
# looping over all the items in df1 dataframe for extracting list of icd9 and icd10 code    
for index, value in df1.items():
    
#extracting code from df1 separeted by comma and space    
    content =TextBlob(value)
    wordlist = []
    wordlists =[]
    wordlist = content.words

    wordlists =  [x for xs in wordlist for x in xs.split(',')]


#creating empty list   
    wordlist2 = []
    new_lists = []
    final_list = []
    
#creating regex function to find code that has range    
    p = re.compile('([\d]|[A-Z\d]{1,})([\-]|[\–])')
    
    p1 = re.compile('([A-Za-z]{1,})[\-]')
    
    p2 = re.compile('([A-Z]|[A-Z0-9]{1,})(x)')
    
    
    

#removing dot(.) from all the codes 
    for word in reversed(wordlists):
        
        if len(word) >= 3:
            word = word.replace('.', '')
            wordlist2.append(word)
   
#separating code that need wildcard to be use     
    xlist = []
    for word in reversed(wordlist2):
        
        if p2.match(word):
            xlist.append(word)
            wordlist2.remove(word)

       
#seperating codes that required convertion of range        
    for word in reversed(wordlist2):
        if p.match(word):
            new_lists.append(word)
            wordlist2.remove(word)
        
        
       
#converting range of codes to distinct code    
    new = []
    for l in new_lists:
        m = re.match(r'^([A-Z]*)(\d+)[\-|\–]\1*(\d+)$', l)
        if m:
            new += [m.group(1) + str(i) for i in range(int(m.group(2)), int(m.group(3))+1)]
        else:
            new += [l]

#creating list with all icd9 and icd10 code except wildcard codes    
    final_list = wordlist2 + new
    final_list = [x for x in final_list if str(x) != 'nan']

#using same index number to extract procurement code from df2    
    procs  = TextBlob(df2.iloc[index])
    proc_list = []
    proc_list = procs.words
    proc_list = [x for xs in proc_list for x in xs.split(',')]
    
    
#creating empty list   
    proc_list2 = []
    new_plists = []
    final_plist = []
    xplist = []
    
#removing dot(.) from all the codes 
    for word in reversed(proc_list):
        
        if len(word) >= 3:
            word = word.replace('.', '')
            proc_list2.append(word)
            
#separating code that need wildcard to be use     
    for word in reversed(proc_list2):
        
        if p2.match(word):
            xplist.append(word)
            proc_list2.remove(word)
            
            
#seperating codes that required convertion of range        
    for word in reversed(proc_list2):
        if p.match(word):
            new_plists.append(word)
            proc_list2.remove(word)
            
#converting range of codes to distinct code    
    pnew = []
    for l in new_plists:
        m = re.match(r'^([A-Z]*)(\d+)[\-|\–]\1*(\d+)$', l)
        if m:
            pnew += [m.group(1) + str(i) for i in range(int(m.group(2)), int(m.group(3))+1)]
        else:
            pnew += [l]
 
#creating list with all codes except  wildcard codes    
    final_plist = proc_list2 + pnew
    final_plist = [x for x in final_plist if str(x) != 'nan']   
    
#database column that will be used while generating sql script @inpat @outpat
#these below string and list can be change as per the requiremnet
    
    if table_used == 'outpat':
        diag_code = '(dx1, dx2, dx3, dx4)'
        proc_code = '(proc1)'  
        diag_list = ['dx1', 'dx2', 'dx3', 'dx4']
        proc_list = ['proc1']
    elif table_used == 'inpat':
        diag_code = '(pdx, dx1, dx2, dx3, dx4, dx5, dx6, dx7, dx8, dx9, dx10, dx11, dx12, dx13, dx14, dx15)'
        proc_code = '(pproc, proc1, proc2, proc3, proc4, proc5, proc6, proc7, proc8, proc9, proc10, proc11, proc12, proc13, proc14, proc15)'
        diag_list = ['pdx', 'dx1', 'dx2', 'dx3', 'dx4', 'dx5', 'dx6', 'dx7', 'dx8', 'dx9', 'dx10', 'dx11', 'dx12', 'dx13', 'dx14', 'dx15']
        proc_list = ['pproc', 'proc1', 'proc2', 'proc3', 'proc4', 'proc5', 'proc6', 'proc7', 'proc8', 'proc9', 'proc10', 'proc11', 'proc12', 'proc13', 'proc14', 'proc15']
    else:
        diag_code = '(pdx, dx1, dx2, dx3, dx4)'
        proc_code = '(pproc, proc1)'
        diag_list = ['pdx', 'dx1', 'dx2', 'dx3', 'dx4']
        proc_list = ['pproc', 'proc1']
    
    if  input_filetype == 'case':
        with open("%s.txt" % filename, "a+") as f:
            f.write("\ncase when\n")
            
    else:
        with open("%s.txt" % filename, "a+") as f:
            f.write("\n where \n")
    
    
    
#writing sql script into text file
        
#inclusion @diagnosis code without wildcard
    if 'nan' in final_list:
        pass
    else:
        if  xlist == []:
            if  final_plist == [] and  xplist == []:
                for idx,word in enumerate(final_list):
                    with open("%s.txt" % filename, "a+") as f:
                        f.write("\'{}\' in {}\n".format(word, diag_code))
                    if (idx+1) < len(final_list):
                        with open("%s.txt" % filename, "a+") as f:
                            f.write(" or ")
            else:
                for idx,word in enumerate(final_list):
                    with open("%s.txt" % filename, "a+") as f:
                        f.write("\'{}\' in {}\n or ".format(word, diag_code))
       
        else:
            if final_plist == [] and  xplist == []:
                for idx,word in enumerate(final_list):
                    with open("%s.txt" % filename, "a+") as f:
                        f.write("\'{}\' in {}\n or ".format(word, diag_code))
                    
            else:
                for idx,word in enumerate(final_list):
                    with open("%s.txt" % filename, "a+") as f:
                        f.write("\'{}\' in {}\n or ".format(word, diag_code))
        
    
    
            

    
    
#inclusion @diagnosis code with wildcard       
    if final_plist == [] and  xplist == []:
        if len(xlist) > 1:
            for jdx, word in enumerate(xlist):
                for idx, w in enumerate(diag_list):
                    word = str(word).replace('x', '%')
                    with open("%s.txt" % filename, "a+") as f:
                        f.write("{} like \'{}\'\n".format(w, word))
                    if (idx+1) < len(diag_list):
                        with open("%s.txt" % filename, "a+") as f:
                            f.write(" or ")
                if (jdx +1) < len(xlist):
                    with open("%s.txt" % filename, "a+") as f:
                        f.write(" or ")
        else:
            
            for jdx, word in enumerate(xlist):    
                for idx, w in enumerate(diag_list):
                    word = str(word).replace('x', '%')
                    with open("%s.txt" % filename, "a+") as f:
                        f.write("{} like \'{}\'\n".format(w, word))
                    if (idx+1) < len(diag_list):
                        with open("%s.txt" % filename, "a+") as f:
                            f.write(" or ")
                            
    else:
        for idx, word in enumerate(xlist):
            for w in diag_list:
                word = str(word).replace('x', '%')
                with open("%s.txt" % filename, "a+") as f:
                    f.write("{} like \'{}\' or\n".format(w, word))
        
                    
                
                    

            
        
#inclusion @procedure code    
    if xplist == []:
        
        if final_plist == []:
            pass
        else:
        
            for idx, word in enumerate(final_plist):
                with open("%s.txt" % filename, "a+") as f:
                    f.write(" \'{}\' in {}\n".format(word, proc_code))
                if (idx+1) < len(final_plist):
                    with open("%s.txt" % filename, "a+") as f:
                        f.write(" or ")
                            
    else:
        if final_plist == []:
            pass
        else:
        
            for idx, word in enumerate(final_plist):
                with open("%s.txt" % filename, "a+") as f:
                    f.write("\'{}\' in {} or \n".format(word, proc_code))
                    
                    
                    
#inclusion @procedure code wildcard
    if len(xplist) > 1:
            
        
            for jdx, word in enumerate(xplist):
                for idx, w in enumerate(proc_list):
                    word = str(word).replace('x', '%')
                    with open("%s.txt" % filename, "a+") as f:
                        f.write("{} like \'{}\'\n".format(w, word))
                    if (idx+1) < len(proc_list):
                        with open("%s.txt" % filename, "a+") as f:
                            f.write(" or ")
                if (jdx +1) < len(xplist):
                    with open("%s.txt" % filename, "a+") as f:
                        f.write(" or ")
    else:
            
        for jdx, word in enumerate(xplist):    
            for idx, w in enumerate(proc_list):
                word = str(word).replace('x', '%')
                with open("%s.txt" % filename, "a+") as f:
                    f.write("{} like \'{}\'\n".format(w, word))
                if (idx+1) < len(proc_list):
                    with open("%s.txt" % filename, "a+") as f:
                        f.write(" or ")

#assigning index to a variable    @exclusion
    a = index
    
#calling above function to get the list of diagnosis code and writing  @exclusion @diagnosis code
    exclist, dxclist = excl(a)
    if 'nan' in exclist:
        pass
    else:
        for word in exclist:
            with open("%s.txt" % filename, "a+") as f:
                f.write(" and \'{}\' not in {}\n".format(word,diag_code))
                
    if 'nan' in dxclist:
        pass
    else:
        for idx, word in enumerate(dxclist):
            for w in diag_list:
                word = str(word).replace('x', '%')
                with open("%s.txt" % filename, "a+") as f:
                    f.write(" and {} not like \'{}\' \n".format(w, word))


                
    
 
#calling above function to get the list of procedure code and writing @exclusion @procedure code
    exclproc_list = exclproc(a)
    if 'nan' in (exclproc_list):
        pass
    else:
        for word in exclproc_list:
            with open("%s.txt" % filename, "a+") as f:
                f.write(" and \'{}\' not in {}\n".format(word, proc_code))
    
        
        
#extracting condition name from df0 to give column name in sql script         
    condition = TextBlob(df0.iloc[index])
    related_word = condition.words
    related_word =  [w.replace('/', '_') for w in related_word]    
    #nltk.download('stopwords')
    stop_words = stopwords.words("english")
    related_words = [w for w in related_word if w not in stop_words]
    listostr = '_'.join([str(w) for w in related_words]) 
    
    
    #@condition
    if  input_filetype == 'case': 
        with open("%s.txt" % filename, "a+")as f:
            f.write("\nthen 1 else 0 end as {}, \n\n\n".format(listostr[0:20]))
        
        
#counting number of codes and printing in console
    
    diag_num = len(final_list) + len(xlist)
    proc_num = len(final_plist) + len(xplist)
    
    print("\n for \'{}\' number of dx code is  {} and number of proc code is {} ".format(listostr[0:15], diag_num, proc_num))
        
        

   
    
    
    

        
   
            
    

        
        
    
