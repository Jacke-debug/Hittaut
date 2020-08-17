from xlsxwriter import Workbook

def main(ortList):

    ordered_list=["name","draws"] #list object calls by index but dict object calls items randomly

    wb=Workbook("hittaut - dragningar.xlsx")
    ws=wb.add_worksheet() #or leave it blank, default name is "Sheet 1"

    first_row=0
    for header in ordered_list:
        col=ordered_list.index(header) # we are keeping order.
        ws.write(first_row,col,header) # we have written first row which is the header of worksheet also.

    row=1
    for ort in ortList:
        for _key,_value in ort.items():
            col=ordered_list.index(_key)
            ws.write(row,col,_value)
        row+=1 #enter the next row
    wb.close()

if __name__ == '__main__': # for testing/debugging

    testList = [{'name': 'aröd', 'draws': '7/8,5/5,9/9'},
    {'name': 'kode', 'draws': 'fr'}]

    main(testList)