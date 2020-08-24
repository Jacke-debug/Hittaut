from xlsxwriter import Workbook

def main(ortList):

    ordered_list=["ort","dates","nCheckpts","draws"] #list object calls by index but dict object calls items randomly
    header_names=["Namn","Datum","Antal","Dragningar"]

    filename="hittaut - dragningar.xlsx"
    wb=Workbook("hittaut - dragningar.xlsx")
    ws=wb.add_worksheet("Information") #or leave it blank, default name is "Sheet 1"

    first_row=0
    for header in ordered_list:
        col=ordered_list.index(header) 
        ws.write(first_row,col,header_names[col]) 

    ws.set_column(1,1,16)

    row=1
    for ort in ortList:
        for _key,_value in ort.items():
            col=ordered_list.index(_key)
            if type(_value)==set:
                _value=str(_value)
            ws.write(row,col,_value)
        row+=1 #enter the next row
    wb.close()

    return filename

if __name__ == '__main__': # for testing/debugging

    testList = [{'ort': 'Aröd', 'draws': {'7/8','5/5','9/9'}},
    {'ort': 'kode', 'draws': set()},
    {'ort': 'Kungälv', 'dates': '10 Apr - 11 Oct', 'nCheckpts': '60', 'draws': {'-/8', '-/5', '-/10'}}]

    main(testList)