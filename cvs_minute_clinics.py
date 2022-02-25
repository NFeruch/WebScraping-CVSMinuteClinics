import xlsxwriter
import os
import re
import http.client
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from win32com.client import Dispatch
from time import sleep

http.client._MAXHEADERS = 1000

workbook = xlsxwriter.Workbook('CVS.xlsx')
worksheet = workbook.add_worksheet()

wrap_format = workbook.add_format({'text_wrap': True})
worksheet.write(0, 0, 'Address')
worksheet.write(0, 1, 'Services')

URL = 'https://www.cvs.com/minuteclinic/clinic-locator/clinic-directory'
session = HTMLSession()
response = session.get(URL)
response.html.render(wait=2, timeout=100)
soup = BeautifulSoup(response.html.html, 'lxml')

states = [
    x.attrs['href'][-3:-1] for x in soup.find_all(
        'a', {'href': re.compile(r"https://www.cvs.com/minuteclinic/clinic-locator/clinic-directory/\w{2}/")}
    )
]
# df = []
row = 1
# break_bool = False

for state in states:
    # if break_bool:
    #     break
    print('\n' + state)
    current_state_url = f"https://www.cvs.com/minuteclinic/clinic-locator/clinic-directory/{state}/"
    response = session.get(current_state_url)
    response.html.render(wait=2, timeout=100)
    current_state_soup = BeautifulSoup(response.html.html, 'lxml')

    cities = [
        x.attrs['href'][68:-1] for x in current_state_soup.find_all(
            'a', {'href': re.compile(f"https://www.cvs.com/minuteclinic/clinic-locator/clinic-directory/{state}/.")}
        )
    ]

    for city in cities:
        current_city_url = f"https://www.cvs.com/minuteclinic/clinic-locator/clinic-directory/{state}/{city}"
        response = session.get(current_city_url)
        response.html.render(wait=2, timeout=100)
        current_city_soup = BeautifulSoup(response.html.html, 'lxml')

        clinics_list = current_city_soup.find('div', {'class': 'col-md-17'})

        try:
            while True:
                clinics_list.div.contents.remove('\n')
        except ValueError:
            pass

        address = ''
        for i, clinic in enumerate(clinics_list.div.contents):
            if i % 2 == 0:
                address = clinic.text[:-12]
                worksheet.write(row, 0, address)
            else:
                services = '\n'.join([x.text for x in clinic.find_all('a')])
                # df.append([address, services])
                worksheet.write(row, 1, services, wrap_format)
                row += 1

        print(city, end=', ')
        # if len(df) > 200:
        #     break_bool = True
        #     worksheet.set_column(1, 1, 100)
        #     workbook.close()
        #     break
        sleep(0.5)
    sleep(1)

worksheet.set_column(1, 1, 100)
workbook.close()

excel = Dispatch('Excel.Application')
wb = excel.Workbooks.Open(fr"{os.path.abspath(os.getcwd())}/CVS.xlsx")

excel.Worksheets(1).Activate()
excel.ActiveSheet.Columns.AutoFit()
wb.Save()

wb.Close()
