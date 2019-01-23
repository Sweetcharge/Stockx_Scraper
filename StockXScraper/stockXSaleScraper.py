import requests, time, math, csv

domain = "https://stockx.com"
def welcome():
	print('''
		~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		Welcome to stockX sales scraper! 
		Make sure you have your username and password correctly! 
		Author: Samuel Belarmino

		NOTE: Your sales will be saved in a file called "StockX_Sales.csv"
		~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		''')
	print("[1] Yes")
	print("[2] No")
	user_choice = input("Ready to continue? ")

	if(user_choice == "1"):
		login()
	else:
		print("Goodbye!")

def login():
	pageNumber = 1
	# Set the headers for requesting to login
	header = {
		'user-agent':			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
		'content-type':			'application/json',
		'appversion':			'0.1',
		'appos':				'web',
		'x-requested-with':		'XMLHttpRequest',
		'jwt-authorization':	'false',
		'accept':				'*/*',
		'referer':				'https://stockx.com/signup',
		'accept-encoding':		'gzip, deflate, br',
		'accept-language':		'en-GB,en-US;q=0.9,en;q=0.8'
	}

	# User info here
	accInfo = {
		'email': "", ### YOUR USERNAME HERE
		'password': "" ### YOUR PASSWORD HERE
	}

	print("Loggin in...")
	time.sleep(3)

	postReq = requests.post(url="https://stockx.com/api/login", headers=header, json=accInfo)
	# Convert to JSON object
	siteJSON = postReq.json()
	# Check to see if the connection was successful
	status = postReq.status_code
	# Get the customer ID; will be used for getting sales history
	customerID = siteJSON['Customer']['id']
	if(status == 200):
		print("\nLogged in!")
		jwt = postReq.headers["jwt-authorization"]
		# Call the function to scrape sales from the user's account
		saleHistory(jwt, customerID, pageNumber)

def saleHistory(theJWT, userID, page_num):
	print("\nGetting sales...")
	profit = 0.0

	header = {
		'user-agent':			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
		'content-type':			'application/json',
		'appversion':			'0.1',
		'appos':				'web',
		'x-requested-with':		'XMLHttpRequest',
		'jwt-authorization':	theJWT,
		'accept':				'*/*',
		'referer':				'https://stockx.com/selling',
		'accept-encoding':		'gzip, deflate, br',
		'accept-language':		'en-GB,en-US;q=0.9,en;q=0.8'
	}

	url = domain+"/api/customers/"+str(userID)+"/selling/history?sort=matched_with_date&order=DESC&limit=20&page="+str(page_num)
	getReq = requests.get(url=url, headers=header)
	siteJSON = getReq.json()
	totalItems = siteJSON["Pagination"]['total']
	maxPages = math.ceil(totalItems / 20)

	# Create a csv file with the appropriate headers
	with open("StockX_Sales.csv", "w") as csvfile:
				csv_file = csv.writer(csvfile)
				csv_file.writerow(["Date Sold", "Product", "Size", "Buy Price ($)", "Sell Price ($)"])

	for j in range(page_num, maxPages+1):
		# Sleeps every 2 seconds to avoid bans
		time.sleep(2)
		url = domain+"/api/customers/"+str(userID)+"/selling/history?sort=matched_with_date&order=DESC&limit=20&page="+str(page_num)
		getReq = requests.get(url=url, headers=header)
		siteJSON = getReq.json()

		# Start scraping the other pages
		for i in range(0, len(siteJSON["PortfolioItems"])):
			productName = siteJSON["PortfolioItems"][i]["product"]["title"]
			buyPrice = siteJSON["PortfolioItems"][i]["purchasePrice"]
			soldPrice = siteJSON["PortfolioItems"][i]["localTotal"]
			shoeSize = siteJSON["PortfolioItems"][i]["product"]["shoeSize"]
			soldDate = siteJSON["PortfolioItems"][i]["matchedWithDate"].split("T")[0]

			# Write each item on it's own separate row
			with open("StockX_Sales.csv", "a") as csvfile:
				csv_file = csv.writer(csvfile)
				csv_file.writerow([soldDate, productName, shoeSize, buyPrice, soldPrice])
			
			profit += soldPrice
		page_num = page_num+1

	print("\nSuccess!")
	print('''
		Created by: Samuel Belarmino
		Check out my reselling profits tracker on Twitter! @theBoominApp
		''')
	print("Total profit after fees: $" + str(profit))	


# Start here
welcome()

