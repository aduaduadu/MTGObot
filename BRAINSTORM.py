'''

shopkeep responsibilities:
	opens the shop
		open mtgo
		requires password authentication from owner
		login
	
	takes inventory
		this is to verify collection stock actually matches inventory databases
		image recognition and GUI manipulation of mtgo collection
			trade binder is the mtgo store inventory

	tends mtg_window
		accepting trade offer
		!STILL NEED PROCEDURE FOR BUYING CARD FROM CUSTOMERS
			is this a separate shopkeep?
		grabbing the pricing guide
		grabbing the customer account
		managing sale process
			interacting with mtg card trade screen
			interacting with mtg chat
				customer conversation
				display customer's credit/deals
				display order total
					dynamically? how quick does this need to be?
						do I need a faster computer?
					calculate mtgo ticket exchange
				checkout
			double checking the transaction screen
			closes sales
			updating inventory database
			receipt of transaction
			update sale history database
			evaluate sales 
				update card pricing guide if necessary
				updates mtgo AD if necessary
			opens sales
	tends mtg_window

	image recognition and gui manipulation
	interacting with mtg card collection screens


GUI responsibilities:
        password authentication
	window1: 
		card pricing list
		also displays both store inventory stock and mtgo collection iventory stock for each card
		toggle between sets
		easy to manipulate pricing
			password required? maybe just at opening time
		can manipulate stock btw mtgo collection and store
			this requires closing sales
			slower than manual pricing list update
	window2:
		generates graphs for visualizing collected card price data over time
		use matplotlib likely
		functionality for displaying multiple graphs side by side for easy comparison
			comparing different vendors of the same card especially
			comparing multiple cards sold by same vendor
		timeline of major MTG events displayed below all graphs 
			this will help me visualize price trends due to tournament activity
				metric for visualizing size of tournament
				include in brief description?
			simple design
			colored dots along a line
			hover over dot displays brief event detail
			click dot to link to event page(s)
	window3:
		sales history data visualizations?
		what else do I need?


spider responsibilities
	libraries to use:
		requests
		requests_html and python 3.7
		beautifulsoup
		selenium if html alone is inadequate for scraping page data
	competitor card price data collection
	web scraping
	cleaning data, this is important for recognizing changes in presentation of data, leads to:
                sending/logging error messages if collected data patterns change
	list of competitors to scrape: [
		clanteam		
			DONEDONEDONE	
			can also scrape quantity in stock with regex parsing of 'bots with stock' column on clanteam pages
		cardhoarder
                        uses Incapsula Bot Detection
                        TODO: how to get around this??
            	tried random user agent with every request
            		behavior was noticed and quickly blocked
		goatbots
			requires advanced image recognition
		wikiprice/mtgoLibrary
			also requires advanced i.r.
		mtgoacademy
			DONEDONEDONE
			could also scrape inventory
		jbStore
		mtgoTraders
                        DONEDONEDONE
                        could also scrape inventory
		supernovabots
			doesn't exist anymore
		mtgoEmpire
			http://mtgoempire.com/pricing.html
			http requests show cloudflare
			worthwhile site, though
		vrtstore
			http://vrtstore.com/
			worthwhile to try
		dojoTrade
			https://www.dojotradebots.com/pricelist
			pricing tables similar to mtgoEmpire
			worthwhile site, though
		any other new ones?
	]


database
	structure:
		table of cards
			unique_id (mtgo_id), name, set, rarity, type, cmc, sell_price, buy_price, mtgo_inventory, shop_inventory
				TODO: get cmc and type for each card
				TODO: instantiate inventory columns
			sell/buy prices
				these prices can be manipulated by GUI interface
				can be manipulated by shopkeep after sale if necessary
					raise price if a card is selling out quickly?
					or hide some of collection from sale inventory
			card inventory
				SQL TABLE
				mtgo account stock
				shop card stock
				eventually this will keep track of inventories for each computer/mtgo account/shopkeep

		shop transaction history
			SQL TABLE or MongoDB doc collection
			example MongoDB structure
			{
				sale_id: 1
				customer_id: 14
				timestamp: datetime object
				transaction_length: datetime object
				bought/received: {
					# card_id: {amount: x, buylist_price (at the time of sale): y}
					12345: {amount: 2, price: 1.2}
					23455: {amount: 4, price: 0.4}
					tix: 24
				}
				sold: {
					# card_id: {amount: x, sell_price (at the time of sale): y}
				}
			}
			example SQL schema
			column headers: order_id, customer_id, timestamp, transaction_time_delta, customer credit delta

		customer Table
			shows credit stored from past transactions


		collected card data
			one SQL table per unique mtgo card
			(datetime, vendor, buy, sell)
			should this be in a SQL table to avoid nesting in MongoDB doc structure?
				nesting structure would make doc structure grow exponentially when adding more collected card data
			specific card prices 
				various mtgo vendor websites
			my pricing guide history
				sell/buy list prices

tasks to stil figure out:
	how to multiprocess tasks
		shopkeep
		spiders
		database server
	can I handle all that on one computer?
		then manage other processes for other screens/shops/computers
		

order to code project:
	table of cards
		unique_id (mtgo_id), name, set, rarity, type, cmc, sell_price, buy_price, mtgo_inventory, shop_inventory
		start with just standard
	table of scraped data for each individual card
		unique_id is table name
		fields: timestamp, my_buy_price, my_sell_price, vendor1_buy, vendor1_sell, vendor2_buy, vendor2_sell, etc...
	spiders
		requests, beautifulsoup
		requests_html and python 3.7
		learned about mtgsdk
			convenient expansion shortcode -> set name function
			limit 5000 requests an hour

'''
