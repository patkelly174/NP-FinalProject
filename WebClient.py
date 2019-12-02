# Import socket module
from socket import * 
# In order to terminate the program
import sys
import pandas
import lxml.html
import xlwt
from xlwt import Workbook
import pickle
# Assign the IP address of the web server
# Use localhost if run the web server locally
serverName = 'localhost'
# Assign the port number of the web server
serverPort = 1234
# Create a TCP server socket
clientSocket = socket(AF_INET, SOCK_STREAM)
# Connect to the web server
clientSocket.connect((serverName,serverPort))

print ("Enter the following apartment fields. Enter NA if data field does not apply")
city = input("Enter a city (required): ")
clientSocket.send(city.encode())
state = input("Enter a state abbreviation (required): ")
clientSocket.send(state.encode())
minPrice = input("Enter minimum price: ")
clientSocket.send(minPrice.encode())
maxPrice = input("Enter max price: ")
clientSocket.send(maxPrice.encode())
radius = input("Enter search radius in miles: ")
clientSocket.send(radius.encode())

# Get HTTP response from the web server
wb = Workbook()
wb = clientSocket.recv()
file = 'C:\\Users\\stepkak\\NPClient.xls'
wb.save(file)

clientSocket.close()
#Terminate the program after getting the corresponding data
sys.exit() 
