import pandas as pd
data = []

file_path = "C:\\Users\\Hp\\Desktop\\easyStorage-Test-Automation\\TestCases\\Easystorage.xlsx"

# Load the Excel file with all sheets
df = pd.read_excel(file_path, sheet_name=None) 

# Iterate over the sheets and print their names and content
for sheet_name, sheet_data in df.items():
    categories=[]
    for type_, quantity in zip(sheet_data["Type"], sheet_data["Quantity"]):
        categories.append({
            "Type":type_,
            "Quantity":quantity
        })
    data.append({sheet_name:categories})

