import pandas as pd

#(reading unformatted data)
df_input = pd.read_excel(r"Filepath\Unformatted.xlsx")

#Creating an output df with empty headers for class and training status
column_names = ["Class", "TrainingStatus"]
df_empty = pd.DataFrame(columns = column_names)
#print(df_empty)


#Creating a client vendor data_frame with just the client 
null_values = pd.notnull(df_input["s.no"])
df_Client_Vendor = df_input[null_values]
#dropping the s.no column
df_Client_Vendor = df_Client_Vendor.drop('s.no', 1)
#resetting the index
df_Client_Vendor = df_Client_Vendor.reset_index(drop=True)
#print(df_Client_Vendor)


#Separating the document ID's into multiple sublists
m = df_input['s.no'].isna()
r = [[*g['client-vendor combination']] for _, g in df_input[m].groupby((~m).cumsum())]


#Creating an empty matrix and looping through using counter to get all the correct document ids less the NaNs and emptys
# while is < len(r) because count starts at 0 and there are 12 elements not 13.
matrix = []
i = 0
while i < len(r):
    matrix.append([])
    
    for x in r[i]:
        if pd.isnull(x) == False and len(str(x)) == 10:
            matrix[i].append(x)
    i = i + 1    
#Removing any "falsey" values in the matrix e.g. empty strings, empty tuples, zeros etc.    
matrix = [x for x in matrix if x]
#print (matrix)


#Turning sublists into new single column doc id dataframe
documents = pd.DataFrame([i] for i in matrix)

#resetting the index
documents = documents.reset_index(drop=True)
#print(documents)

#concat the documents and the vendors and empty columns df
df_output = pd.concat([df_Client_Vendor, documents, df_empty], axis=1)
#df_output
#name all 4 columns to the correct 4 names:
df_output.columns = ['Client_Vendor', 'DocumentIDs', 'Class', 'TrainingStatus']
#Changing the Document ID column from list to strings (NOTE! THIS IS CHANGING XL STRINGS TO Scientific notation might comment out)
df_output['DocumentIDs'] = [','.join(map(str, l)) for l in df_output['DocumentIDs']]
#printing the output
print(df_output)


#generating csv with filepath
#df_output.to_csv("C:/Users/kabir/Desktop/Xtracta work/outputfile3.csv", index=False)
#generating excel with filepath
df_output.to_excel("Filepath/Formatted.xlsx", index = False, header=True)