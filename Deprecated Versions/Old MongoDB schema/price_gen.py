import pymongo
from pprint import pprint


# establish connection to db
conn = pymongo.MongoClient()
db = conn.card_data


def decode_id(mtgo_id):
    '''
    takes a mtgo_id [str] (_id for cards collection) and returns a
    tuple of respective (name, shortcode, premium)
    '''
    
    card = db.cards.find_one({'_id': mtgo_id})

    return card['name'], card['shortcode'], card['premium']


def find_id(name, shortcode, premium):
    '''
    takes a name, shortcode, premium and returns the respective mtgo_id [str]
    '''

    card = db.cards.find_one({'name': name,
                              'shortcode': shortcode,
                              'premium': premium})

    return card['_id']


def price_history(mtgo_id):
    '''
    takes a mtgo_id and shows latest price history from all vendors
    '''

    card = db.cards.find_one({'_id': mtgo_id})

    agg = db.pricePoints.aggregate([
        
	{'$match': {
            'name': card['name'],
            'shortcode': card['shortcode'],
            'premium': card['premium']
            }
         },
        
        # sort by vendor and timestamp descending
	{'$sort': {
             'vendor': 1,
             'timestamp': -1
             }
         },

        # clean up format
        {'$project': {
            '_id': 0,
            'vendor': 1,
            'sell': 1,
            'buy': 1,
            'timestamp': 1
            }
         }
        ])

    for line in agg:
        pprint(line)


def vendors_snapshot(mtgo_id):
    '''
    takes a mtgo_id (_id) and returns the most recent pricePoint for all vendors
    '''

    card = db.cards.find_one({'_id': mtgo_id})

    agg = db.pricePoints.aggregate([
        
	{'$match': {
            'name': card['name'],
            'shortcode': card['shortcode'],
            'premium': card['premium']
            }
         },
        
        # sort by vendor and timestamp descending
	{'$sort': {
             'vendor': 1,
             'timestamp': -1
             }
         },
        
        # most recent data with $first
	{'$group': {
            '_id': '$vendor',
            'sell': {'$first': '$sell'},
            'buy': {'$first': '$buy'}
            }
	 }
        ])

    for line in agg:
        pprint(line)    
        

def agg_sell_price(mtgo_id):
    '''
    takes a mtgo_id and returns a sellPrice for price list
    '''

    card = db.cards.find_one({'_id': mtgo_id})

    agg = db.pricePoints.aggregate([
        
	{'$match': {
            'name': card['name'],
            'shortcode': card['shortcode'],
            'premium': card['premium']
            }
         },
        
        # sort by vendor and timestamp descending
	{'$sort': {
             'vendor': 1,
             'timestamp': -1
             }
         },
        
        # most recent data with $first
	{'$group': {
            '_id': '$vendor',
            'sell': {'$first': '$sell'}
            }
	 },
        
        # avg vendor prices for market price
	{'$group': {
            # generic 'market' _id to display single answer '$sell'
             '_id': 'market',
             'sell': {'$avg': '$sell'}
             }
	 }
        
	])

    # ie. {'sell': 5.805}
    sell = agg.next()['sell']

    return sell

def owr_to_invoice(owrlist):
    '''
    This takes an owrList and print a cards order invoice for demonstration
    '''
    
    total = 0
    
    for quantity, name, shortcode in owrlist:
        
        mtgo_id = find_id(name, shortcode, 'No')
        sell = agg_sell_price(mtgo_id)

        # print '# x name (sell) = line total
        print('{} x {} ({:.4f}) = {:.4f}'.format(quantity, name, sell, quantity*sell))
        total += quantity*sell

    print('\n')
    print('Total = {:.4f}'.format(total))


def owr_to_chat_message(owrlist):
    '''
    This takes an owrList and prints a cards order invoice to be typed in chat
    '''

    # initialize variables
    invoiceMessage = ''
    total = 0

    i = 1
    
    for quantity, name, shortcode in owrlist:
        
        mtgo_id = find_id(name, shortcode, 'No')
        sell = agg_sell_price(mtgo_id)

        lineItem = '{}:{}x {}({:.4f}) '.format(i,quantity,name,sell)
        invoiceMessage += lineItem

        total += quantity*sell
        i += 1

    invoiceMessage += '= {:.2f} tix'.format(total)

    return invoiceMessage
              
