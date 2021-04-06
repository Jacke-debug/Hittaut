from xlsxwriter import Workbook
import math

def main(listofdicts):

    #ordered_list=["ort","url","dates","nCheckpts","draws"] #list object calls by index but dict object calls items randomly
    header_names=["Ort","Start","Slut","Antal checkpts","Vinstdragningar","Metod för extraktion av dragningsdatum"]
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

    colummns_per_month = 10
    col=1
    cfm_mon = wb.add_format({'left':1})
    for month in months:
        ws_vis.write(first_row,col,month,cfm_mon)
        col+=colummns_per_month

    ws_raw.set_column(0,0,21.5) # width for ort column
    ws_raw.set_column(4,4,35) # width for draws column

    ws_vis.set_column(0,0,21.5) # width for ort column
    #ws_vis.set_column(1,2,4) # width for empty columns
    ws_vis.set_column(1,12*colummns_per_month,0.9) # width for month columns

    row=1
    for dictEntry in listofdicts:
        ws_raw.write_url(row,0, dictEntry['url'], string=dictEntry['ort'])
        ws_raw.write(row,1, dictEntry['start'])
        ws_raw.write(row,2, dictEntry['end'])
        nCheckpts = dictEntry['nCheckpts']
        if nCheckpts == -1:
            nCheckpts = 'okänt'
        ws_raw.write(row,3, nCheckpts)
        list_str=str(dictEntry['draws'])
        ws_raw.write(row,4, list_str)
        # for _key,_value in dictEntry.items():
        #     col=ordered_list.index(_key)
        #     if type(_value)==list:
        #         _value=str(_value)
        #     ws.write(row,col,_value)
        ws_raw.write(row,5, dictEntry['method'])

        # visualised worksheet
        ws_vis.write_url(row,0, dictEntry['url'], string=dictEntry['ort'])
        start_col = column_from_date(dictEntry['start'],colummns_per_month)
        end_col = column_from_date(dictEntry['end'],colummns_per_month)
        # print('start_col =',start_col)
        # print('end_col =',end_col)
        vinst_cols = []
        for draw in dictEntry['draws']:
            vinst_cols.append(column_from_date(draw,colummns_per_month))
        cfm_on = wb.add_format({'bg_color':'#dd235f','font_color':'#FFFFFF'})
        # cfm_off = wb.add_format({'bg_color':''})
        cfm_on_mon = wb.add_format({'bg_color':'#dd235f','font_color':'#FFFFFF','left':1})
        cfm_off_mon = wb.add_format({'left':1})
        for col in range(1,12*colummns_per_month+1):
            if col in vinst_cols:
                text = 'V'
            else:
                text = ''
            if start_col <= col and col <= end_col:
                if (col-1) % colummns_per_month == 0:
                    ws_vis.write(row, col, text, cfm_on_mon)
                else:
                    ws_vis.write(row, col, text, cfm_on)
            else:
                if (col-1) % colummns_per_month == 0:
                    ws_vis.write(row, col, text, cfm_off_mon)
                else:
                    ws_vis.write(row, col, text)


        row+=1 #enter the next row

    wb.close()

    return filename

def column_from_date(datenumber,colummns_per_month):
    # datenumber: last two digits for day, first two (or one) for month
    month = datenumber // 100
    day = datenumber % 100
    day_col = math.ceil(colummns_per_month*(day/30))
    if day_col>colummns_per_month:
        day_col=colummns_per_month
    elif day_col<1:
        day_col=1
    colnumber = (month-1)*colummns_per_month + day_col
    return colnumber

if __name__ == '__main__': # for testing/debugging

    # testList = [{'ort': 'Aröd','url':'arod.se', 'dates':'','nCheckpts': '60','draws': ['7/8','5/5','9/9']},
    # {'ort': 'kode','url':'kode.se', 'draws': list(), 'dates':'','nCheckpts': '60'},
    # {'ort': 'Kungälv', 'url':'kungalv.se', 'dates': '10 Apr - 11 Oct', 'nCheckpts': '60', 'draws': ['-/8', '-/5', '-/10']}]

    # testList = [{'ort': 'Kalmar', 'url': 'https://www.orientering.se/provapaaktiviteter/hittaut/kalmar/',\
        #  'start': 501, 'end': 1030, 'nCheckpts': '130', 'draws': [104,202,303,625,726,827,928,1029,1130,1231]}]
    testList = [{'ort': 'Stockholm Upplands Väsby', 'url': 'https://www.orientering.se/provapaaktiviteter/hittaut/upplandsvasby/',\
         'start': 501, 'end': 1030, 'nCheckpts': '130', 'draws': [104,202,303,625,726,827,928,1029,1130,1231],'method':'alla'}]

    main(testList)