

'''
Author :  Sujay
Definition : An Automation System to convert PDF's to Data

Data Extracted :

    1. Date (DD/MM/YYYY)	
    2. Max.Demand met during the day (MW)	
    3. Shortage during maximum Demand (MW)	
    4. Energy Met (MU)	
    5. Drawal Schedule(MU)	
    6. OD(+)/UD(-) (MU) 
    7. Max OD (MW)	
    8. Energy Shortage (MU)

'''

# Update - 0.1
'''
    - No need to convert to txt file
    - Extracting Region Data
''' 

import pandas as pd
import numpy as np
import PyPDF2
import os


# Defining File Paths Here
folder_path = "raw_data/"
processed_path = "processed_data/"


# State for which demand can be found
state = "Delhi"


'''
    - Converts the PDFs to .txt files 
    - Only converts 2nd page of PDF to text (less space)
    - Path From  : raw_data/* (all)
    - Path to : processed_data/* (all)
'''
def pdf_conversion(file):
    org_path = folder_path+file
    processing = processed_path+file[0:8]+".txt"
    pdffileobj=open(org_path,'rb')
    pdfreader=PyPDF2.PdfReader(pdffileobj)
    x=len(pdfreader.pages)
    if x>1:
        pageobj=pdfreader.pages[1]
        pageobj1 = pdfreader.pages[0]
        text=pageobj.extract_text()
        text = text + pageobj1.extract_text()
    else:
        pageobj = pdfreader.pages[0]
        text=pageobj.extract_text()
    
    # Make a Txt File
    file1=open(processing ,"a")
    file1.writelines(text)
    file1.close()
    pdffileobj.close()



'''
    - Extract the Data from the .txt files (Constant Time Complexity - reduced file size)
    - Only extracts the particular data from the length from x to x'
    - Path From  : processed_data/* (all)
    - Returns an array of Strings : []
'''
def extract_info(file):
    contents = ""
    file_path = processed_path+file
    myfile = open(file_path, "rt") 
    contents = myfile.read()       
    myfile.close()       
    # Find the Substring index from the file
    x = 0    
    if "Delhi" in contents:
        x = contents.index(state)

    stri = ""
    s = []
    s.append(file[0:8].replace('.','/'))
    sd = ""
    while stri != "\n" and x<len(contents):
        if stri == " ":
            s.append(sd)
            sd = contents[x]
        else:
            sd = sd + contents[x]
        stri = contents[x]
        x = x+1
    sd = sd[:4]
    s.append(sd)
    return s



files = os.listdir(folder_path)
data = []

# This is only for MAC's to remove the .DStore file
files.remove(".DS_Store")

print(len(files))

# # First : Conversion
for file in files:
    pdf_conversion(file)

processed_files = os.listdir(processed_path)

# This is only for MAC's to remove the .DStore file
processed_files.remove(".DS_Store")

# Second : Extraction
for file in processed_files:
    data.append(extract_info(file))


# Check for the length equal to size of the folder
print(len(data),len(files),len(processed_files))
assert len(data) == len(files)

df = pd.DataFrame(data)

df.to_csv("main/ndlc_psp.csv")


