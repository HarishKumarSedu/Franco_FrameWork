
import pandas as pd
import numpy as np

def writeInExcel(filename,sheet,*args,**kwargs):
    df = {}
    for colname, data in kwargs.items():
        df.update(
            {
                colname:data
            }
        )
    df = pd.DataFrame(df)
    print(df)
    try:
        writer=  pd.ExcelWriter(filename, mode="a",if_sheet_exists="replace", engine="openpyxl")
        df.to_excel(writer, sheet_name=sheet, index=False)
        print('.................')
        writer.close()
    except:
        writer = pd.ExcelWriter(filename,  engine="openpyxl")
        df.to_excel(writer, sheet_name=sheet, index=False)
        writer.close()
