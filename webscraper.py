import requests
from bs4 import BeautifulSoup
import pandas
import lxml.html
import xlwt
from xlwt import Workbook

wb = Workbook()
sheet1 = wb.add_sheet('Sheet 1')
sheet1.write(0,0, 'Number')
sheet1.write(0,1, 'Title')
sheet1.write(0,2, 'Address')
sheet1.write(0,3, 'Price')
sheet1.write(0,4, 'Beds')
sheet1.write(0,5, 'Baths')
sheet1.write(0,6, 'sqft')
sheet1.write(0,7, 'Pets')
counter = 0
t = 0

while t < 4:
    t = t+1
    url = "https://www.realtor.com/apartments/Boston_MA/pg-" + str(t)
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content,"html.parser")

    apartment = soup.find_all('li', {"class" : "component_property-card js-component_property-card"})
    apartmentTitle = soup.find_all('div', {"class" : "address ellipsis"})
    apartmentData = soup.find_all('ul', {"class" : "prop-meta ellipsis"})
    apartmentPrice = soup.find_all('span', {"class" : "data-price"})

    print(apartmentData[13].get_text())
    # To process property by property by looping
    for i in range(43):
        print(i)
        try:
            title = apartmentTitle[i].find('span', {"class" : "listing-community"}).get_text()
            address = apartmentTitle[i].find('span', {"class" : "listing-street-address"}).get_text()
            price = apartmentPrice[i].get_text()
            beds = apartmentData[i].find('li', {"data-label" : "property-meta-beds"}).get_text()
            baths = apartmentData[i].find('li', {"data-label" : "property-meta-baths"}).get_text()
            pets = apartmentData[i].find('li', {"data-label" : "property-meta-pets"}).get_text()
            sqft = apartmentData[i].find('li', {"data-label" : "property-meta-sqft"}).get_text()
        except:
            print("error")

        sheet1.write(i+1+(44*counter), 0, i)
        sheet1.write(i+1+(44*counter), 1, title)
        sheet1.write(i+1+(44*counter), 2, address)
        sheet1.write(i+1+(44*counter), 3, price)
        sheet1.write(i+1+(44*counter), 4, beds)
        sheet1.write(i+1+(44*counter), 5, baths)
        sheet1.write(i+1+(44*counter), 6, sqft)
        sheet1.write(i+1+(44*counter), 7, pets)
    counter = counter + 1

wb.save('NP.xls')

