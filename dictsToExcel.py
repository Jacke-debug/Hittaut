from xlsxwriter import Workbook

def main(listofdicts):

    #ordered_list=["ort","url","dates","nCheckpts","draws"] #list object calls by index but dict object calls items randomly
    header_names=["Ort","Start","Slut","Antal","Dragningar"]
    months = ['januari','februari','mars','april','maj','juni','juli','augusti','september','oktober','november','december']

    filename="hittaut - dragningar.xlsx"
    wb=Workbook("hittaut - dragningar.xlsx")

    # worksheet with raw data
    ws_raw=wb.add_worksheet("Raw data") #or leave it blank, default name is "Sheet 1"
    # worksheet with visualized data
    ws_vis=wb.add_worksheet("Grafisk")

    first_row=0
    for header in header_names:
        col=header_names.index(header) 
        ws_raw.write(first_row,col,header_names[col]) 

    col=1
    for month in months:
        ws_vis.write(first_row,col,month)
        col+=1

    ws_raw.set_column(0,0,15) # width for ort column
    ws_raw.set_column(4,4,20) # width for draws column

    ws_vis.set_column(0,0,15) # width for ort column
    #ws_vis.set_column(1,2,4) # width for empty columns
    ws_vis.set_column(1,12,8) # width for month columns

    row=1
    for dictEntry in listofdicts:
        ws_raw.write_url(row,0, dictEntry['url'], string=dictEntry['ort'])
        ws_raw.write(row,1, dictEntry['start'])
        ws_raw.write(row,2, dictEntry['end'])
        ws_raw.write(row,3, dictEntry['nCheckpts'])
        list_str=str(dictEntry['draws'])
        ws_raw.write(row,4, list_str)
        # for _key,_value in dictEntry.items():
        #     col=ordered_list.index(_key)
        #     if type(_value)==list:
        #         _value=str(_value)
        #     ws.write(row,col,_value)

        # visualised worksheet
        ws_vis.write_url(row,0, dictEntry['url'], string=dictEntry['ort'])
        start_month = dictEntry['start'] // 100
        end_month = dictEntry['end'] // 100
        cell_format = wb.add_format({'bg_color':'#dd235f'})
        for monthCol in range(start_month,end_month):
            ws_vis.write(row, monthCol, '', cell_format)


        row+=1 #enter the next row

    

    wb.close()

    return filename

if __name__ == '__main__': # for testing/debugging

    # testList = [{'ort': 'Aröd','url':'arod.se', 'dates':'','nCheckpts': '60','draws': ['7/8','5/5','9/9']},
    # {'ort': 'kode','url':'kode.se', 'draws': list(), 'dates':'','nCheckpts': '60'},
    # {'ort': 'Kungälv', 'url':'kungalv.se', 'dates': '10 Apr - 11 Oct', 'nCheckpts': '60', 'draws': ['-/8', '-/5', '-/10']}]

    testList = [{'ort': 'Kalmar', 'url': 'https://www.orientering.se/provapaaktiviteter/hittaut/kalmar/', 'start': 501, 'end': 1030, 'nCheckpts': '130', 'draws': [1030]}]

    main(testList)