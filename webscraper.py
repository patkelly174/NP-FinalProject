# Usage: Open terminal/cmd and run "python WebServer.py"
import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml.html
import xlwt
from xlwt import Workbook

#imports for sending email with attachment
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders

# Import socket module
from socket import *
# Import Thread
from threading import Thread
# In order to terminate the program
import sys


# Handles incomming connections
def accept_incoming_connections(serverSocket):
    while True:
        # Set up a new connection from the client
        connectionSocket, addr = serverSocket.accept()
        print("%s:%s has connected." % addr)
        # Start client thread to handle the new connection
        Thread(target=handle_client, args=(connectionSocket,)).start()


# Handles a single client connection, taking connection socket as argument
def handle_client(connectionSocket):
    # If an exception occurs during the execution of try clause
    # the rest of the clause is skipped
    # If the exception type matches the word after except
    # the except clause is executed
    try:
        # Receives the request message from the client
        city = connectionSocket.recv(1024).decode()
        state = connectionSocket.recv(1024).decode()
        minPrice = connectionSocket.recv(1024).decode()
        maxPrice = connectionSocket.recv(1024).decode()
        radius = connectionSocket.recv(1024).decode()
        url =   "https://www.realtor.com/apartments/"
        url = url + city + "_" + state + "/price-" + minPrice + "-" + maxPrice + "/radius-" + radius
        connectionSocket.send("Compiling spreadsheet now... (will open in browser when done)".encode())

        wb = Workbook()
        sheet1 = wb.add_sheet('Sheet 1')
        sheet1.write(0, 0, 'Title')
        sheet1.write(0, 1, 'Address')
        sheet1.write(0, 2, 'Price')
        sheet1.write(0, 3, 'Beds')
        sheet1.write(0, 4, 'Baths')
        sheet1.write(0, 5, 'sqft')
        sheet1.write(0, 6, 'Pets')
        counter = 0
        t = 0

        while t < 4:
            t = t + 1
            url = url + "pg-" + str(t)
            response = requests.get(url)
            content = response.content
            soup = BeautifulSoup(content, "html.parser")

            apartment = soup.find_all('li', {"class": "component_property-card js-component_property-card"})
            apartmentTitle = soup.find_all('div', {"class": "address ellipsis"})
            apartmentData = soup.find_all('ul', {"class": "prop-meta ellipsis"})
            apartmentPrice = soup.find_all('span', {"class": "data-price"})

            # To process property by property by looping
            for i in range(43):
                try:
                    title = apartmentTitle[i].find('span', {"class": "listing-community"}).get_text()
                    address = apartmentTitle[i].find('span', {"class": "listing-street-address"}).get_text()
                    price = apartmentPrice[i].get_text()
                    beds = apartmentData[i].find('li', {"data-label": "property-meta-beds"}).get_text()
                    baths = apartmentData[i].find('li', {"data-label": "property-meta-baths"}).get_text()
                    pets = apartmentData[i].find('li', {"data-label": "property-meta-pets"}).get_text()
                    sqft = apartmentData[i].find('li', {"data-label": "property-meta-sqft"}).get_text()
                except:
                    continue

                sheet1.write(i + 1 + (44 * counter), 0, title)
                sheet1.write(i + 1 + (44 * counter), 1, address)
                sheet1.write(i + 1 + (44 * counter), 2, price)
                sheet1.write(i + 1 + (44 * counter), 3, beds)
                sheet1.write(i + 1 + (44 * counter), 4, baths)
                sheet1.write(i + 1 + (44 * counter), 5, sqft)
                sheet1.write(i + 1 + (44 * counter), 6, pets)
            counter = counter + 1
        excel_file = "ApartmentSearch_" + city + "_" + state + "_" + minPrice + "_" + maxPrice + "_" + radius +".xls"
        wb.save(excel_file)
        wb1 = pd.read_excel(excel_file)
        html_file = "server_" + city + "_"+ state + "_" + minPrice + "_" + maxPrice + "_" + radius + ".html"
        f =  open(html_file, 'w')
        f.write(wb1.to_html())
        x = open(html_file, 'rb')
        data = x.read()
        connectionSocket.send(data)



        # Close the client connection socket
        print("Table computed. Closing connection for search of: " + url)
        connectionSocket.close()

    except IOError:
        # Send HTTP response message for file not found
        connectionSocket.send("Error".encode())
        # Close the client connection socket
        connectionSocket.close()


def main():
    # Create a TCP server socket
    # (AF_INET is used for IPv4 protocols)
    # (SOCK_STREAM is used for TCP)
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Assign a port number
    serverPort = 1234

    # Bind the socket to server address and server port
    serverSocket.bind(('', serverPort))

    # Listen to at most 5 connections at a time
    serverSocket.listen(5)

    # Server should be up and running and listening to the incoming connections
    print('The server is ready to receive')

    # Start the accepting connections thread
    acceptThread = Thread(target=accept_incoming_connections, args=(serverSocket,))
    acceptThread.start()
    # Wait for the accepting connections thread to stop
    acceptThread.join()

    # Close the server socket
    serverSocket.close()
    # Terminate the program after sending the corresponding data
    sys.exit()


if __name__ == "__main__":
    main()





