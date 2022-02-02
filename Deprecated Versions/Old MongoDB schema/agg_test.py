import pymongo
from pprint import pprint


# establish connection to db
conn = pymongo.MongoClient()
db = conn.card_data

card = db.cards.find_one({'shortcode': 'DTK'})

agg = db.pricePoints.aggregate([
	{'$match': {
            'name': card['name'],
            'shortcode': card['shortcode'],
            'premium': card['premium']
            }
	},
        
        # sort by vendor and timestamp descending
	{'$sort': {
             'vendor': pymongo.ASCENDING,
             'timestamp': pymongo.DESCENDING
             }
        },

        # most recent data with $first
	{'$group': {
            '_id': '$vendor',
            'sell': {'$first': '$sell'}
            }
	}
])

'''
        {'$project': {
            '_id': 0,
            'vendor': 1,
            'timestamp': 1,
            'sell': 1
            }
         }
'''

'''
        # avg vendor prices for market price
	{'$group': {
            # generic 'market' _id to display single answer '$sell'
             '_id': 'market',
             'sell': {'$avg': '$sell'}
             }
	 }
'''

for result in agg:
    pprint(result)
