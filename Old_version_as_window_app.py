from tkinter.ttk import Combobox
from tkinter import *
import requests
from bs4 import BeautifulSoup as BSop
import time
from datetime import date, datetime, timedelta
import xlsxwriter


today = date.today().strftime("%d-%m-%Y")
now = datetime.now()
sdate = datetime(2010, 1, 1)  # data startowa
edate = datetime(2022, 1, 10)  # data koncowa

window = Tk()


def gpwlink(sdate):
    res = requests.get(
        'https://www.gpw.pl/archiwum-notowan-full?type=10&instrument=&date={}'.format(sdate.strftime("%d-%m-%Y")))
    return res


# Funckja do zdobycia nazw z linku
def create_custom_nalist(names):
    nameslist = []
    i = 0
    for name in range(round((len(names)-2)/2)):
        nameslist.append((names[i+2]).getText())
        i += 2
    return nameslist


def total_set_VAlue():
    Value = set_OpeningPrice() + set_MinimumPrice() + \
        set_MaximumPrice() + set_ClosingPrice() + \
        set_PriceChange() + set_TradeVolumen() + \
        set_NumOfTransactions() + set_TumoverVolumen()
    return Value


# Funckja do zdobycia wartości
def create_custom_nrlist(numbers):
    nrlist = []
    nrlist2 = []
    for nr in numbers:
        nrlist.append(nr.getText().replace(
            '\xa0', '').replace('\n', '').replace(' ', ''))

    for nr in nrlist:
        if nr.find(",") != -1 or nr.isnumeric():
            nrlist2.append(nr)

    thisPostion = 8
    correction = 0
    if total_set_VAlue != 8:
        if not set_TumoverVolumen():
            del nrlist2[thisPostion-1+correction::thisPostion]
            thisPostion -= 1
            correction += 1
        if not set_NumOfTransactions():
            del nrlist2[thisPostion-2+correction::thisPostion]
            thisPostion -= 1
            correction += 1
        if not set_TradeVolumen():
            del nrlist2[thisPostion-3+correction::thisPostion]
            thisPostion -= 1
            correction += 1
        if not set_PriceChange():
            del nrlist2[thisPostion-4+correction::thisPostion]
            thisPostion -= 1
            correction += 1
        if not set_ClosingPrice():
            del nrlist2[thisPostion-5+correction::thisPostion]
            thisPostion -= 1
            correction += 1
        if not set_MaximumPrice():
            del nrlist2[thisPostion-6+correction::thisPostion]
            thisPostion -= 1
            correction += 1
        if not set_MinimumPrice():
            del nrlist2[thisPostion-7+correction::thisPostion]
            thisPostion -= 1
            correction += 1
        if not set_OpeningPrice():
            del nrlist2[thisPostion-8+correction::thisPostion]
            thisPostion -= 1
            correction += 1
    return nrlist2


# funckja do łączenia nazw i wartości spółek (dodam możliwość zarządzania tym)
def scal(names, numbers):
    datalist = []
    i = 0
    stotal_set_VAlue = total_set_VAlue()
    for name in range(len(names)):
        # datalist += [[names[i], *numbers[(i*8):((i*8)+8)]]]
        datalist += [[names[i], *
                      numbers[(i*stotal_set_VAlue):((i*stotal_set_VAlue)+stotal_set_VAlue)]]]
        i += 1
    return datalist


def scrapper():
    day = 1
    start_time = time.time()
    rec = 0
    sdate = datetime(*insert_Startdate())
    loopdate = sdate
    edate = datetime(*insert_ENDdate())

    total = (edate-sdate).days
    workbook = xlsxwriter.Workbook(
        'gpwbigdata2{}.xlsx'.format(now.strftime('_%d-%m-%Y_%H-%M-%S')))
    worksheet = workbook.add_worksheet()

    cell_format1 = workbook.add_format()
    cell_format1.set_rotation(90)
    cell_format1.set_align('center')
    # Program
    txtlabel2 = Label(window, text='')
    txtlabel2.place(x=210, y=200)
    while loopdate <= edate:
        txtlabel2.config(text=str('loading {} / {}').format(day, total+1))
        loading()

        soup = BSop(gpwlink(loopdate).text, 'html.parser')
        names2 = soup.select('.left')
        numbers2 = soup.select('.text-right')
        Value = total_set_VAlue()

        datalistloop = scal(create_custom_nalist(
            names2), create_custom_nrlist(numbers2))

        row = 1  # wiersze w excel
        if len(datalistloop) != 0:

            for nr in range(len(datalistloop)):
                col = 0+((rec)*Value)  # columny excel
                worksheet.write_string(
                    0, col+1, str(loopdate.strftime("%d-%m-%Y")))
                # choose_brands =
                if (datalistloop[nr][0]) in brands_list():  # warunek wyboru listy
                    namecol = Value

                    # warunki ktore wedle wyboru z konsoli nanoszą wybrane dane dane
                    if set_TumoverVolumen():
                        worksheet.write_string(
                            1, namecol+((rec)*Value), 'Wartość obrotu', cell_format1)
                        namecol -= 1
                    if set_NumOfTransactions():
                        worksheet.write_string(
                            1, namecol+((rec)*Value), 'Lista transkacji', cell_format1)
                        namecol -= 1
                    if set_TradeVolumen():
                        worksheet.write_string(
                            1, namecol+((rec)*Value), 'Wolumen obrotu', cell_format1)
                        namecol -= 1
                    if set_PriceChange():
                        worksheet.write_string(
                            1, namecol+((rec)*Value), 'Zmiana Kursu ', cell_format1)
                        namecol -= 1
                    if set_ClosingPrice():
                        worksheet.write_string(
                            1, namecol+((rec)*Value), 'Kurs zamknięcia', cell_format1)
                        namecol -= 1
                    if set_MaximumPrice():
                        worksheet.write_string(
                            1, namecol+((rec)*Value), 'Kurs max', cell_format1)
                        namecol -= 1
                    if set_MinimumPrice():
                        worksheet.write_string(
                            1, namecol+((rec)*Value), 'Kurs min', cell_format1)
                        namecol -= 1
                    if set_OpeningPrice():
                        worksheet.write_string(
                            1, namecol+((rec)*Value), 'Kurs Otwarcia ', cell_format1)
                        namecol -= 1

                    row += 1
                    if col == 0:
                        for element in datalistloop[nr][0:1]:
                            worksheet.write_string(row, col, element)
                            col += 1

                        for element in datalistloop[nr][1:]:
                            x = (element.replace(' ', '').replace(',', '.'))
                            x = float(x)
                            worksheet.write(
                                row, col, x)
                            col += 1

                    else:
                        for element in datalistloop[nr][1:]:
                            x = (element.replace(' ', '').replace(',', '.'))
                            x = float(x)
                            worksheet.write(
                                row, col+1, x)
                            col += 1

            rec += 1  # record jako jedne caly rejestr danych z pojedynczej strony
        # podniesienie daty o 1 dzien wartoscio staartowej
        loopdate += timedelta(days=1)
        day += 1
    workbook.close()
    brands_list_clear()
    # choose_brands = []
    timespend = time.time() - start_time
    txtlabel3 = Label(window, text='')
    txtlabel3.config(text=str('Program zajął: {}').format(round(timespend, 4)))
    txtlabel3.place(x=210, y=200)
    btnend = Button(window, text="Ponownie", fg='black',
                    command=lambda: [txtlabel3.destroy(), btnend.destroy(), txtlabel2.destroy()])
    btnend.place(x=210, y=260)


# scrapper()


namesListg = []


def insert_Startdate():
    sdate = (cb3v.get(), cb2v.get(), cb1v.get())
    return sdate


def insert_ENDdate():
    edate = (cb6v.get(), cb5v.get(), cb4v.get())
    return edate


def brands_list():
    for i in lb2.get(0, END):
        namesListg.append(i)
    if len(namesListg) > 0:
        return namesListg
    else:
        return spdata


def brands_list_clear():
    global namesListg
    namesListg = []


def scp():
    txtlabel = Label(window, text='')
    txtlabel.place(x=210, y=130)
    txtlabel.config(text=str(
        'Pobrano\n od: {}\n do: {}\n {} spółek\n'.format(insert_Startdate(), insert_ENDdate(), len(brands_list()))))
    window.update()


def search(event):
    val = event.widget.get()

    if val == '':
        data = spdata
    else:
        data = []
        for item in spdata:
            if val.lower() in item.lower():
                data.append(item)

    Update(data)


def Update(data):

    lb.delete(0, 'end')
    # put new data
    for item in data:
        lb.insert('end', item)


def LB2remove():
    if not lb2.curselection():
        lb2.delete(0, 'end')
    else:
        for name in lb2.curselection():
            lb2.delete(name)


def UpdateLB2(dataLB2):
    for item in dataLB2:
        if item not in lb2.get(0, END):
            lb2.insert('end', item)


def insertlb2():
    jd = []
    for name in lb.curselection():
        if lb.get(name) not in jd:
            jd.append(lb.get(name))

    UpdateLB2(jd)


def loading():
    window.update()


def set_OpeningPrice():
    output_OpeningPrice = v1.get()
    return output_OpeningPrice


def set_MinimumPrice():
    output_MinimumPrice = v2.get()
    return output_MinimumPrice


def set_MaximumPrice():
    output_MaximumPrice = v3.get()
    return output_MaximumPrice


def set_ClosingPrice():
    output_ClosingPrice = v4.get()
    return output_ClosingPrice


def set_PriceChange():
    output_PriceChange = v5.get()
    return output_PriceChange


def set_TradeVolumen():
    output_TradeVolumen = v6.get()
    return output_TradeVolumen


def set_NumOfTransactions():
    output_NumOfTransaction = v7.get()
    return output_NumOfTransaction


def set_TumoverVolumen():
    output_TumoverVolumen = v8.get()
    return output_TumoverVolumen


'''///////////////////////'''
xx = 500
yy = 300

aglingCBy = 20
aglingCBx = -10
lblSTARTdates = Label(window, text="Dane do pobrania",
                      fg='Black', font=("Helvetica", 10))
lblSTARTdates.place(x=50+aglingCBx, y=20)

v1 = IntVar()
v2 = IntVar()
v3 = IntVar()
v4 = IntVar()
v5 = IntVar()
v6 = IntVar()
v7 = IntVar()
v8 = IntVar()
C1 = Checkbutton(window, text="Kurs otwarcia", variable=v1)
C2 = Checkbutton(window, text="Kurs min", variable=v2)
C3 = Checkbutton(window, text="Kurs max", variable=v3)
C4 = Checkbutton(window, text="Kurs zamkniecia", variable=v4)
C5 = Checkbutton(window, text="Zmiana kursu", variable=v5)
C6 = Checkbutton(window, text="Wolumen obrotu", variable=v6)
C7 = Checkbutton(window, text="Liczba transakcji", variable=v7)
C8 = Checkbutton(window, text="Wartość obrotu", variable=v8)


C1.place(x=50+aglingCBx, y=25+aglingCBy)
C2.place(x=50+aglingCBx, y=50+aglingCBy)
C3.place(x=50+aglingCBx, y=75+aglingCBy)
C4.place(x=50+aglingCBx, y=100+aglingCBy)
C5.place(x=50+aglingCBx, y=125+aglingCBy)
C6.place(x=50+aglingCBx, y=150+aglingCBy)
C7.place(x=50+aglingCBx, y=175+aglingCBy)
C8.place(x=50+aglingCBx, y=200+aglingCBy)

'''///////////////////////'''

lblSTARTdates = Label(window, text="Data początkowa",
                      fg='Black', font=("Helvetica", 10))
lblSTARTdates.place(x=200, y=20)


cbsdalg = 20
cb1v = IntVar(value=1)
dayList = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
           18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31)
cb1 = Combobox(window, state="readonly", values=dayList,
               width=4,  textvariable=cb1v)
cb1.place(x=200-cbsdalg, y=25+20)

cb2v = IntVar(value=1)
dayList = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
cb2 = Combobox(window, state="readonly", values=dayList,
               width=4, textvariable=cb2v)
cb2.place(x=250-cbsdalg, y=25+20)

cb3v = IntVar(value=2010)
yrList = (2010, 2011, 2012, 2013, 2014, 2015,
          2016, 2017, 2018, 2019, 2020, 2021, 2022)
cb3 = Combobox(window, state="readonly", values=yrList,
               width=5, textvariable=cb3v)
cb3.place(x=300-cbsdalg, y=25+20)


lblENDdates = Label(window, text="Data końcowa",
                    fg='Black', font=("Helvetica", 10))
lblENDdates.place(x=210, y=70)

cb4v = IntVar(value=1)
eday = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
        18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31)
cb4 = Combobox(window, state="readonly", values=eday,
               width=4, textvariable=cb4v)
cb4.place(x=200-cbsdalg, y=75+20)

cb5v = IntVar(value=1)
emon = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
cb5 = Combobox(window, state="readonly", values=emon,
               width=4, textvariable=cb5v)
cb5.place(x=250-cbsdalg, y=75+20)

cb6v = IntVar(value=2010)
eyr = (2010, 2011, 2012, 2013, 2014, 2015,
       2016, 2017, 2018, 2019, 2020, 2021, 2022)
cb6 = Combobox(window, state="readonly", values=eyr,
               width=5, textvariable=cb6v)
cb6.place(x=300-cbsdalg, y=75+20)


'''////////////////////'''
entry = Entry(window)
entry.pack()
entry.bind('<KeyRelease>', search)
entry.place(x=350, y=42)
varsp = StringVar()
# spdata = ['06MAGNA', '08OCTAVA', 'ABPL', 'ACTION', 'AGORA', 'AMBRA', 'AMICA', 'AMPLI', 'AMREST', 'APATOR', 'APLISENS', 'ARCTIC', 'ARTERIA', 'ASBIS', 'ASSECOBS', 'ASSECOPOL', 'ASSECOSEE', 'ASTARTA', 'ATLANTAPL', 'ATLANTIS', 'ATLASEST', 'ATMGRUPA', 'ATREM', 'BEDZIN',
#           'BEST', 'BETACOM', 'BIOTON', 'BOGDANKA', 'BORYSZEW', 'BOS', 'BUDIMEX', 'BUMECH', 'CAPITAL', 'CCC', 'CEZ', 'CIECH', 'COGNOR', 'COMARCH', 'COMP', 'CORMAY', 'CYFRPLSAT', 'DEBICA', 'DECORA', 'DELKO', 'DGA', 'DOMDEV', 'DREWEX', 'DROZAPOL', 'ECHO', 'EFEKT', 'ELEKTROTI', 'ELKOP', 'ELZAB', 'EMCINSMED', 'ENAP', 'ENEA', 'ENERGOINS', 'ERBUD', 'ERG', 'EUROCASH', 'EUROTEL', 'FAMUR', 'FASING', 'FERRUM', 'FON', 'FORTE', 'GETIN', 'GETINOBLE', 'GROCLIN', 'GTC', 'HANDLOWY', 'HELIO', 'HYDROTOR', 'IDMSA', 'INGBSK', 'INSTALKRK',
#           'INTERCARS', 'INTERFERI', 'INTERSPPL', 'INTROL', 'IPOPEMA', 'IZOLACJA', 'KERNEL', 'KETY', 'KGHM', 'KOGENERA', 'KOMPAP', 'KOMPUTRON', 'KPPD', 'KRAKCHEM', 'KREDYTIN', 'LENA', 'LENTEX', 'LOTOS', 'LPP', 'LSISOFT', 'LUBAWA', 'MAKARONPL', 'MARVIPOL', 'MCI', 'MENNICA', 'MERCOR', 'MILLENNIUM', 'MIRBUD', 'MOJ', 'MOL', 'MONNARI', 'MOSTALPLC', 'MOSTALWAR', 'MOSTALZAB', 'MUZA', 'MWTRADE', 'NETIA', 'NEUCA', 'NOVITA', 'NTTSYSTEM', 'ODLEWNIE', 'OPONEO.PL', 'ORCOGROUP', 'ORZBIALY', 'PAMAPOL', 'PANOVA', 'PATENTUS', 'PBG', 'PCGUARD', 'PEKAO', 'PEP', 'PEPEES', 'PGE', 'PGNIG', 'PKNORLEN', 'PKOBP', 'PLASTBOX', 'PLAZACNTR', 'POLICE', 'POLIMEXMS', 'POZBUD', 'PRIMAMODA', 'PROCAD', 'PROCHEM', 'PROJPRZEM', 'PROTEKTOR', 'PULAWY', 'QUANTUM', 'RADPOL', 'RAFAKO', 'RAFAMET', 'RAINBOW', 'REDAN', 'REINHOLD', 'RELPOL', 'REMAK', 'RESBUD', 'RONSON', 'ROPCZYCE', 'SANOK', 'SANWIL', 'SECOGROUP', 'SEKO', 'SELENAFM', 'SFINKS', 'SILVANO', 'SIMPLE', 'SKOTAN', 'SKYLINE', 'SNIEZKA', 'SONEL', 'STALEXP', 'STALPROD', 'STALPROFI', 'STAPORKOW', 'SUWARY', 'SWISSMED', 'SYGNITY', 'TALEX', 'TIM', 'TRAKCJA', 'TRITON', 'ULMA', 'UNIBEP', 'UNICREDIT', 'UNIMA', 'VINDEXUS', 'WARIMPEX', 'WASKO', 'WAWEL', 'WIELTON', 'WIKANA', 'WOJAS', 'ZPUE', 'ZREMB', 'ZYWIEC']\

spdata = ['KGHM',
          'PKOBP',
          'PKNORLEN',
          'PEKAO',
          'PGE',
          'PGNIG',
          'LOTOS',
          'CCC',
          'EUROCASH',
          'CYFRPLSAT',
          'ASSECOPOL',
          'ENEA',
          'MILLENNIUM',
          'LPP',
          'KERNEL',
          'POLIMEXMS',
          'BORYSZEW',
          'HANDLOWY',
          'CIECH',
          'BOGDANKA',
          'GETIN',
          'GETINOBLE',
          'PBG',
          'GTC',
          'AMREST',
          'BIOTON',
          'TRAKCJA',
          'BUDIMEX',
          'RAFAKO',
          'CORMAY',
          'ASBIS',
          'INGBSK',
          'SKOTAN',
          'FAMUR',
          'LUBAWA',
          'BUMECH',
          'KETY',
          'IDMSA',
          'GROCLIN',
          'MCI',
          'MONNARI',
          'NETIA',
          'MIRBUD',
          'COGNOR',
          'AMICA',
          'MOSTALZAB',
          'NEUCA',
          'ARCTIC',
          'WIELTON',
          'ACTION',
          'ECHO',
          'STALEXP',
          'ATLANTIS',
          'AGORA',
          'FORTE',
          'SYGNITY',
          'STALPROD',
          'ASTARTA',
          'CEZ',
          'FON',
          'WASKO',
          'PCGUARD',
          'RESBUD',
          'POLICE',
          'SFINKS',
          '06MAGNA',
          'KOMPUTRON',
          'INTERCARS',
          'PEP',
          'BOS',
          'ELKOP',
          'RAINBOW',
          'MOSTALWAR',
          'TIM',
          'SANWIL',
          'DOMDEV',
          'LENTEX',
          'PULAWY',
          'COMARCH',
          'APATOR',
          'PLAZACNTR',
          'SANOK',
          'OPONEO.PL',
          'REDAN',
          'AMBRA']
# spdata = ['01NFI', '04PRO', '05VICT', '06MAGNA', '08OCTAVA', '11 NFI', '13FORTUNA', '14ZACH',
#           '4MEDIA', 'ABG', 'ADVADIS', 'AGORA', 'AGROS', 'ALCHEMIA', 'ALMA', 'AMICA', 'AMPLI', 'AMS',
#           'ANIMEX', 'APATOR', 'APEXIM', 'ASSECOPOL', 'ATLANTIS', 'BAKOMA', 'BANKBPH', 'BBICAPNFI',
#           'BBIDEVNFI', 'BBIZENNFI', 'BCZ', 'BEDZIN', 'BELCHATOW', 'BEST', 'BETONSTAL', 'BICK', 'BIELBAW',
#           'BORYSZEW', 'BOS', 'BRE', 'BROK', 'BUDIMEX', 'BUDOPOL', 'BYTOM', 'CENSTALGD', 'CENTROZAP', 'CERSANIT',
#           'CLIF', 'COMARCH', 'COMPENSA', 'CSS', 'DBPBC', 'DEBICA', 'DELIA', 'DROSED', 'DZPOLSKA', 'EBI', 'ECHO',
#           'EFEKT', 'EKODROB', 'ELBUDOWA', 'ELEKTRIM', 'ELEKTROEX', 'ELZAB', 'ENAP', 'ENERGOPLD', 'ENERGOPN',
#           'ENERGOPOL', 'ESPEBEPE', 'EXBUD', 'FAMOT', 'FARMACOL', 'FARMFOOD', 'FERRUM', 'FON', 'FORTE', 'FORTISPL',
#           'GANT', 'GPRD', 'GRAJEWO', 'GROCLIN', 'GRUPAONET', 'HANDLOWY', 'HOWELL', 'HUTMEN', 'HYDROBUD', 'HYDROGD',
#           'HYDROTOR', 'IBSYSTEM', 'ICOPAL', 'IGROUP', 'IMPEXMET', 'INDYKPOL', 'INGBSK', 'INSTAL', 'INSTALKRK', 'IRENA',
#           'JAROS£AW', 'JELFA', 'JUPITER', 'JUTRZENKA', 'KABLE', 'KABLEHOLD', 'KETY', 'KGHM', 'KOMPAP', 'KOPEX', 'KREDYTB',
#           'KREZUS', 'KROSNO', 'KRUSZWICA', 'KZWM', 'LDASA', 'LENTEX', 'LETA', 'LGPETRO', 'LTL', 'LUBAWA', 'LUKBUT', 'LZPS',
#           'MANOMETRY', 'MASTERS', 'MENNICA', 'MIDAS', 'MIESZKO', 'MILLENNIUM', 'MILMET', 'MITEX', 'MNI', 'MORLINY', 'MOSTALEXP',
#           'MOSTALGD', 'MOSTALPLC', 'MOSTALWAR', 'MOSTALZAB', 'MOSTOSTAL KRAKÓW', 'MUZA', 'NAFTA', 'NFIEMF', 'NOMI', 'NORDEABP',
#           'NOVITA', 'OBORNIKI', 'OCEAN', 'ODLEWNIE', 'OKOCIM', 'OLAWA', 'ORBIS', 'ORFE', 'PAGED', 'PAZUR', 'PBK', 'PEKABEX',
#           'PEKAO', 'PEMUG', 'PEPEES', 'PERMEDIA', 'PGF', 'PIASECKI', 'PKNORLEN', 'POINTGROUP', 'POLAR', 'POLFKUTNO',
#           'POLIFARB DÊBICA', 'POLIFARBC', 'POLIGR', 'POLIMEXMS', 'POLISA', 'POLLENAE', 'POLNA', 'POLNORD',
#           'PONARFEH', 'POZMEAT', 'PPLHOLD', 'PPWK', 'PROCHEM', 'PROCHNIK', 'PROJPRZEM', 'PROKOM', 'PROSPER',
#           'PROVIMROL', 'RAFAKO', 'RELPOL', 'REMAK', 'ROPCZYCE', 'SANOK', 'SANWIL', 'SKOTAN', 'SOKOLOW', 'STALEXP',
#           'STALPROD', 'STGROUP', 'STOMIL', 'STORMM', 'SUWARY', 'SWARZEDZ', 'SWIECIE', 'SYGNITY', 'TIM', 'TONSIL',
#           'TPSA', 'TRITON', 'TUEUROPA', 'TUP', 'ULMA', 'UNIBUD', 'UNIMIL', 'VISCO', 'VISTULA', 'WAFAPOMP', 'WARTA',
#           'WAWEL', 'WBK', 'WILBO', 'WISTIL', 'WKSM', 'WOLCZANKA', 'YAWAL', 'ZASADA', 'ZEG', 'ZEW', 'ZREW', 'ZYWIEC',
#           'BEEFSAN', 'FORTWRO', 'EFL', 'STALPROFI', 'KOGENERA', 'MCLOGIC', 'NETIA', 'ZPUE', 'FASING', 'KRAKBROK', 'TALEX',
#           'WANDALEX', 'SIMPLE', '10FOKSAL', 'MCI', 'ELKOP', 'INTERIA.PL', 'GETIN', 'GKI', 'LPP', 'BZWBK', 'TRASINTUR', 'WASKO',
#           'EMPERIA', 'OPTIMUS', 'SPIN', 'KRUK', 'EMAX', 'DUDA', 'NETIA2', 'HOOP', 'BACA', 'IMPEL', 'REDAN', 'SNIEZKA', 'ATMGRUPA',
#           'BETACOM', 'PLASTBOX', 'DGA', 'GTC', 'INTERCARS', 'TECHMEX', 'ARTMAN', 'JCAUTO', 'ELSTAROIL', 'HYGIENIKA', 'MEDIATEL',
#           'NOWAGALA', 'RMFFM', 'CAPITAL', 'PBG', 'ATM', 'BCHEM', 'FAM', 'SWISSMED', 'WSIP', 'CCC', 'KOELNER', 'PEKAES', 'PKOBP',
#           'TORFARM', 'BMPAG', 'DROZAPOL', 'IVAXCORP', 'MOL', 'POLCOLOR', 'PRATERM', 'SYNTHOS', 'TVN', 'ATLANTAPL', 'COMP', 'EUROFAKTR',
#           'CIECH', 'EUROCASH', 'SRUBEX', 'ZELMER', 'GRAAL', 'POLMOSLBN', 'BIOTON', 'AMREST', 'ZETKAMA', 'ZTSERG', 'PEP', 'POLMOSBIA',
#           'DECORA', 'LENA', 'LOTOS', 'OPOCZNO', 'TRAVELPL', 'AMBRA', 'VARIANT', 'EMCINSMED', 'IDMSA', 'POLICE', 'SPRAY', 'BARLINEK',
#           'PCGUARD', 'SKYEUROPE', 'PGNIG', 'JAGO', 'PULAWY', 'TELL', 'NOVITUS', 'TETA', 'TOORA', 'NORTCOAST', 'BANKIER.PL', 'ERGIS',
#           'MISPOL', 'SFINKS', 'ECARD', 'CASHFLOW', 'FAMUR', 'GINOROSSI', 'INWESTCON', 'PAMAPOL', 'QUMAKSEK', 'ACTION', 'ASTARTA',
#           'HYPERION', 'INTERFERI', 'INTERSPPL', 'ABPL', 'EUROMARK', 'ASSECOSLO', 'CEZ', 'DOMDEV', 'ONE2ONE', 'UNIMA', 'HTLSTREFA',
#           'MMPPL', 'NETMEDIA', 'BAKALLAND', 'CCIINT', 'ARTERIA', 'CEDC', 'FOTA', 'MEWA', 'PEGAS', 'ZURAWIE', 'B3SYSTEM', 'EUROTEL',
#           'IVMX', 'RUCH', 'WARIMPEX', 'HAWE', 'LSISOFT', 'MONNARI', 'ORZEL', 'ESSYSTEM', 'GADUGADU', 'PROCAD', 'KOLASTYNA', 'SEKO',
#           'ELEKTROTI', 'HELIO', 'RADPOL', 'TFONE', 'ACE', 'IMMOEAST', 'JWCONSTR', 'MAKARONPL', 'NOBLEBANK', 'BUDVARCEN', 'ERBUD',
#           'KAREN', 'KREDYTIN', 'LCCORP', 'ORCOGROUP', 'RAFAMET', 'MERCOR', 'NTTSYSTEM', 'POLAQUA', 'POLREST', 'PRONOX', 'SILVANO',
#           'STAPORKOW', 'ABMSOLID', 'ARMATURA', 'BOMI', 'GFPREMIUM', 'KOMPUTRON', 'MAKRUM', 'MOJ', 'PANOVA', 'PETROLINV', 'ZASTAL',
#           'HBWLOCLAW', 'OLYMPIC', 'QUANTUM', 'RESBUD', 'IZOLACJA', 'KPPD', 'KRAKCHEM', 'MAGELLAN', 'PLAZACNTR', 'ASBIS', 'ASSECOBS',
#           'ENERGOINS', 'OPONEO', 'RONSON', 'ZNTKLAPY', 'ALTERCO', 'BLACKLION', 'CALATRAVA', 'COGNOR', 'COMPLEX', 'CPENERGIA',
#           'ERG', 'GASTELZUR', 'GETINOBLE', 'HBPOLSKA', 'INTEGERPL', 'INVESTCON', 'KERNEL', 'KOFOLA', 'MIT', 'NEUCA', 'OPONEO.PL',
#           'ORZBIALY', 'POLCOLORIT', 'PONAR', 'PROTEKTOR', 'RAINBOW', 'REINHOLD', 'RUBICON', 'SECOGROUP', 'TERESA', 'TRION', 'WIKANA',
#           'WOLAINFO', 'CITYINTER', 'PRIMAMODA', 'UNICREDIT', 'DROP', 'EFH', 'INTROL', 'KONSSTALI', 'NEPENTES', 'WARFAMA', 'ATLASEST', 'BIPROMET',
#           'WIELTON', 'HERMAN', 'OPTOPOL', 'SKYLINE', 'SOBIESKI', 'TRAKCJA', 'CYFRPLSAT', 'NEWWORLDR', 'PWRMEDIA', 'UNIBEP', 'CAMMEDIA', 'K2INTERNT',
#           'SELENAFM', 'WOJAS', 'ZREMB', 'ARCUS', 'AZOTYTARNOW', 'DREWEX', 'MARVIPOL', 'SKOK', 'HARDEX', 'POLJADLO', 'SONEL', 'POZBUD', 'DRAGOWSKI',
#           'CORMAY', 'CHEMOS', 'IZNS', 'MIRBUD', 'MWTRADE', 'ATREM', 'CENTKLIMA', 'ENEA', 'BUMECH', 'ANTI', 'VINDEXUS', 'IPOPEMA', 'APLISENS', 'BOGDANKA',
#           'ARCTIC', 'ASSECOSEE', 'PATENTUS', 'DELKO', 'PGE', 'PCCINTER', 'EKO', 'FASTFIN', 'INTAKUS', 'BERLING', 'FERRO', 'KOV', 'LSTCAPITA', 'PRAGMAINK',
#           'PZU', 'ABCDATA', 'DSS', 'HARPER', 'RANKPROGR', 'TAURONPE', 'TESGAS', 'OTMUCHOW', 'FORTUNA', 'KCI', 'KREC', 'OPTEAM', 'AGROTON', 'GPW',
#           'INTERBUD', 'TRANSPOL', 'ZUE', '4FUNMEDIA', 'CELTIC', 'EDINVEST', 'MILKILAND', 'POLMED', 'PTI', 'ROBYG', 'EKOEXPORT', 'EUCO', 'MIRACULUM',
#           'PBSFINANSE', 'SADOVAYA', 'VOTUM', 'WADEX', 'BSCDRUK', 'CCENERGY', 'AVIASG', 'AWBUD', 'IDEATFI', 'IZOSTAL', 'ESTAR', 'EUIMPLANT', 'INPRO',
#           'OPENFIN', 'QUERCUS', 'ADVGRUPA', 'BENEFIT', 'BNPPL', 'IMCOMPANY', 'LIBET', 'PRAGMAFA', 'BGZ', 'KINOPOL', 'KSGAGRO', 'MEGARON', 'NEWWORLDN',
#           'NOVAKBM', 'WESTAISIC', 'AGROWILL', 'DMWDM', 'ENELMED', 'JSW', 'OVOSTAR', 'PBOANIOLA', 'ACAUTOGAZ', 'CDRED', 'COALENERG', 'COLIAN', 'JHMDEV',
#           'TOYA', 'PRESCO', 'IQP', 'PGODLEW', 'ZAMET', 'SOPHARMA', 'EUROHOLD', 'HERKULES', 'PELION', 'BOWIM', 'GETBANK', 'ROVESE', 'GREMISLTN',
#           'IFCAPITAL', 'KANIA', 'NOKAUT', 'VANTAGE', 'KRKA', 'MOBRUK', 'SOLAR', 'IDEON', 'MEXPOLSKA', 'WORKSERV', 'ATMSI', 'KBDOM', 'REGNON', 'URSUS',
#           'DUON', 'KDMSHIPNG', 'LIBRA', 'GREENECO', 'PCCEXOL', 'TATRY', 'VOXEL', 'EXILLON', 'ZEPAK', 'ALIOR', 'CDPROJEKT', 'INTERAOLT', 'BALTONA',
#           'GREMMEDIA', 'CZTOREBKA', 'IMPERA', 'PHN', 'QUMAK', 'CNT', 'PROVIDENT', 'SMT', 'ATENDE', 'MABION', 'BBIZEN', 'GLOBALNRG', 'IIAAV', 'FEERUM',
#           'SCOPAK', 'AVIAAML', 'PPG', 'RAWLPLUG', 'SERINUS', 'TARCZYNSKI', 'WINVEST', 'BBIDEV', 'GLCOSMED', 'OTLOG', 'CIGAMES', 'EKANCELAR', 'GRUPAAZOTY',
#           'INVISTA', 'ALTA', 'PEIXIN', 'MLPGROUP', 'PKPCARGO', 'SKYSTONE', 'ENERGA', 'MBANK', 'NEWAG', 'ELEMENTAL', 'GORENJE', 'MFO', 'VISTAL', 'INDYGO',
#           'MEDICALG', 'MERCATOR', 'ORANGEPL', 'COMPERIA', 'CPGROUP', 'DTP', 'GLOBCITYHD', 'INC', 'CUBEITG', 'IMMOBILE', 'LIVECHAT', 'PCM', 'BUWOG',
#           'TALANX', 'BRIJU', 'MSXRESOUR', 'REDWOOD', 'JJAUTO', 'PCCROKITA', 'TELEPOLSKA', 'ALUMETAL', 'IFSA', 'STARHEDGE', 'ALTUSTFI', 'TERMOREX', 'TORPOL',
#           'IMS', 'INVENTUM', 'POLWAX', 'SYNEKTIK', 'FENGHUA', 'KERDOS', 'SANTANDER', 'SKARBIEC', 'VIGOSYS', 'WDMCP', 'CDRL', 'SELVITA', 'AURUM', 'BIOMEDLUB',
#           'DEKPOL', 'EVEREST', 'CFI', 'PMPG', 'INDATA', 'PEMANAGER', 'IBSM', 'IDEABANK', 'IZOBLOK', 'UNIWHEELS', 'WIRTUALNA', 'BGZBNPP', 'BRASTER', 'SOHODEV',
#           'ATAL', 'ESOTIQ', 'PLATYNINW', 'SUNEX', 'HUBSTYLE', 'POLYMETAL', 'PRAIRIE', 'PSG', 'AATHOLD', 'ADIUVO', 'APSENERGY', 'GRODNO', 'INPOST', 'WDX',
#           'WINDMOBIL', 'AILLERON', 'GRAVITON', 'LARQ', 'WITTCHEN', 'CITYSERV', 'MBWS', '11BIT', 'KOFOL', 'KRVITAMIN', 'LABOPRINT', 'LOKUM', 'MDIENERGIA', 'ORION',
#           'TOPMEDICA', 'APLITT', 'ENTER', 'GREMINWES', 'OEX', 'KGL', 'LARK', 'SARE', 'BACD', 'IALBGR', 'MASTERPHA', 'PBKM', 'XTRADEBDM', 'AIRWAY',
#           'ARCHICOM', 'GEKOPLAST', 'I2DEV', 'XTB', 'ABADONRE', 'AUTOPARTN', 'FMG', 'MEDIACAP', 'PGSSOFT', 'ASMGROUP', 'MANGATA', 'VIVID', 'GOBARTO',
#           'PFLEIDER', 'PLAYWAY', 'STELMET', 'ARTIFEX', 'YOLO', 'BIK', 'CLNPHARMA', 'SETANTA', 'TXM', 'UNIMOT', 'JWWINVEST', 'DINOPL', 'GPRE', 'IFIRMA',
#           'GETBACK', 'MAXCOM', 'MORIZON', 'PLAY', 'SLEEPZAG', 'PGO', 'AUGA', 'ITMTRADE', 'VENTUREIN', 'BAHOLDING', 'BZWBK2', 'HOLLYWOOD', 'NANOGROUP',
#           'R22', 'TOWERINVT', 'NOVATURAS', 'SESCOM', 'OAT', 'TSGAMES', 'MLSYSTEM', 'SILVAIR-REGS', 'TBULL', 'SANPL', 'SANPL2', 'PRIMETECH', 'REINO',
#           'DATAWALK', 'XTPL', 'BNPPPL', 'PHARMENA', 'BOOMBIT', 'VRG', 'HMINWEST', 'ULTGAMES', 'DEVELIA', 'RYVU', 'DIGITREE', 'GAMEOPS', 'PUNKPIRAT',
#           'AIGAMES', 'GAMFACTOR', 'ALLEGRO', 'NOVAVISGR', 'NEXITY', 'MEDINICE', 'PCFGROUP', 'PURE', '3RGAMES', 'ANSWEAR', 'PHOTON', 'HUUUGE-S144',
#           'K2HOLDING', 'PGFGROUP', 'DADELO', 'CREEPYJAR', 'BRAND24', 'CAPTORTX', 'SATIS', 'VERCOM', 'PEPCO', 'IMPERIO', 'ONDE', 'SHOPER', 'CAVATINA',
#           'ALTUS', 'MANYDEV', 'GIGROUP', 'POLTREG', 'BIGCHEESE', 'BIOPLANET', 'GREENX', 'GRUPRACUJ', 'STSHOLDING']\

spdata = sorted(spdata)


szukaj = Label(window, text="Szukaj:",
               fg='Black', font=("Helvetica", 10))
szukaj.place(x=350, y=20)

lb = Listbox(window, height=5, selectmode='multiple')
lb.pack()
for num in spdata:
    lb.insert(END, num)
lb.place(x=350, y=60)

btn = Button(window, text="Download", fg='black',
             command=lambda: [scp(), scrapper()])
btn.place(x=210, y=250)


btn2 = Button(window, text="   Add    ", fg='black', command=insertlb2)
btn2.place(x=350, y=145)

btn3 = Button(window, text="  Remove  ", fg='black', command=LB2remove)
btn3.place(x=407, y=145)

wybrane = Label(window, text="Wybrane spółki:",
                fg='Black', font=("Helvetica", 10))
wybrane.place(x=350, y=172)

lb2 = Listbox(window, height=5, selectmode='multiple')
lb2.place(x=350, y=192)

window.title('GPW Scrapper by AD v3')
window.geometry(f"{xx}x{yy}+10+20")
window.mainloop()
