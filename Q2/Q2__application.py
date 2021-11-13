import PyPDF2 
import tabula
import tika
from tika import parser
import numpy as np
import csv
import warnings
warnings.filterwarnings("ignore")

def extract(filepath):

    # get total number of pages in pdf file
    pdfFileObj = open(filepath, 'rb') 
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
    num_pages = pdfReader.numPages

    # read the table from pdf file
    print("Reading data from pdf file... (Its gonna take about 1 minute)")
    dfs = []
    for i in range (1,num_pages+1):
       df = tabula.read_pdf(
            filepath,
            pages=i,
            lattice=True,
            silent=True
            )
       dfs.append(df)

    # extract "description" & "possible root cause" from the table
    print("Extracting information...")
    descs = []
    prcs = []
    for i in range (num_pages):
       dum = dfs[i][0]
       dum = dum.dropna(axis = 0, how = 'all')
       dum = dum.dropna(axis = 1, how = 'all')
       dum.reset_index(drop=True, inplace=True)
       dum = dum.T.reset_index(drop=True).T
       is_contain = dum[0].str.contains('Description')
       if not np.any(is_contain) :
         dum = dum.drop(0, axis=1) 
         dum = dum.T.reset_index(drop=True).T
       desc = dum[dum[0]=="Description"]
       desc = desc.iloc[0,1]
       prc = dum[dum[0]=="Possible Root\rcause"]
       prc = prc.iloc[0,1]
       descs.append(desc)
       prcs.append(prc)

    # get the page number from each page
    PDF_Parse = parser.from_file(filepath)
    content = PDF_Parse ['content']
    clue = content.split("Service Diagnosis")
    clue = np.array(clue)
    page_numbers = []
    for i in range (1,len(clue)):
       page_number = clue[i][3:5]
       page_numbers.append(page_number)

    # transform list into numpy array
    prcs = np.array(prcs)
    descs = np.array(descs)
    page_numbers = np.array(page_numbers)

    # reshape array from 1D to 2D
    page_numbers = page_numbers.reshape(-1,1)
    descs = descs.reshape(-1,1)
    prcs = prcs.reshape(-1,1)

    # concate page_numbers, description, and possible root cause
    content = np.concatenate((page_numbers, descs,prcs), axis=1)
    header = np.array([["Page numbers", "Description", "Possible root cause"]])
    Q2 = np.concatenate((header,content),axis=0)

    # Import data to csv file
    print("Importing data to csv file...")
    with open('Q2.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(Q2)

    print("DONE!")
    print("Press ctrl+c to exit the application")
    print("-------------------------------------------------------------------------------------")

while True : 

    print("Please Input File path, Example : Q2.pdf (if the application and the file is in the same directory)")
    filepath = input("Filepath :")
    extract(filepath)