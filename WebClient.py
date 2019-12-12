# Import socket module
from socket import * 
# In order to terminate the program
import sys
import webbrowser
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
print(clientSocket.recv(1024).decode())

response = clientSocket.recv(1024).decode()
html_name = "client_" + city + "_" + state + "_" + minPrice + "_" + maxPrice + "_" + radius + ".html"
f =  open(html_name, 'w')
while len(response):
	f.write(response)
	response = clientSocket.recv(1024).decode()
webbrowser.open(html_name)
clientSocket.close()
#Terminate the program after getting the corresponding data
sys.exit() 
