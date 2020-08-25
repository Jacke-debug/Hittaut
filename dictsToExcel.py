from xlsxwriter import Workbook

def main(listofdicts):

    #ordered_list=["ort","url","dates","nCheckpts","draws"] #list object calls by index but dict object calls items randomly
    header_names=["Ort","Start","Slut","Antal","Dragningar"]

    filename="hittaut - dragningar.xlsx"
    wb=Workbook("hittaut - dragningar.xlsx")
    ws=wb.add_worksheet("Raw info") #or leave it blank, default name is "Sheet 1"

    first_row=0
    for header in header_names:
        col=header_names.index(header) 
        ws.write(first_row,col,header_names[col]) 

    ws.set_column(0,0,15) # width for ort column
    ws.set_column(1,1,15) # width for date column

    row=1
    for dictEntry in listofdicts:
        ws.write_url(row,0, dictEntry['url'], string=dictEntry['ort'])
        ws.write(row,1, dictEntry['start'])
        ws.write(row,2, dictEntry['end'])
        ws.write(row,3, dictEntry['nCheckpts'])
        list_str=str(dictEntry['draws'])
        ws.write(row,4, list_str)
        # for _key,_value in dictEntry.items():
        #     col=ordered_list.index(_key)
        #     if type(_value)==list:
        #         _value=str(_value)
        #     ws.write(row,col,_value)
        row+=1 #enter the next row
    wb.close()

    return filename

if __name__ == '__main__': # for testing/debugging

    testList = [{'ort': 'Aröd','url':'arod.se', 'dates':'','nCheckpts': '60','draws': ['7/8','5/5','9/9']},
    {'ort': 'kode','url':'kode.se', 'draws': list(), 'dates':'','nCheckpts': '60'},
    {'ort': 'Kungälv', 'url':'kungalv.se', 'dates': '10 Apr - 11 Oct', 'nCheckpts': '60', 'draws': ['-/8', '-/5', '-/10']}]

    main(testList)