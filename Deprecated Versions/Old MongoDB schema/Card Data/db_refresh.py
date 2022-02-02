import csv
import pymongo
from pprint import pprint


# establish handle on db
client = pymongo.MongoClient()
db = client.card_data


def create_new_card(mtgo_id, name, rarity, shortcode, collector_id, premium):
    '''Creates a new card document to be inserted into mongoDB database (collection: card_data.cards).'''
    
    newCard = {
        '_id': mtgo_id,
        'name': name,
        'rarity': rarity,
        'shortcode': shortcode,
        'collector_id': collector_id,
        'premium': premium
    }
    
    return newCard


# currently uses collection conn.card_data.test for testing
def db_refresh(fileName):
    '''
    Refreshes the mongoDB database (collection: card_data.cards).
    Takes a csv filepath ('Wish List.csv' exported from mtgo client).
    Include all cards from mtgo in Wish List.csv, even foils
    '''

    cards = []
    with open(fileName, 'r') as newSet:
        for row in csv.reader(newSet):
            if 'Card Name' not in row:
                # card format: [Card Name,Quantity,ID #,Rarity,Set,Collector #,Premium]
                name = row[0]
                mtgo_id = row[2]
                rarity = row[3]
                shortcode = row[4]
                collector_id = row[5]
                premium = row[6]
                
                # Append card to newCardSet.
                newCard = create_new_card(mtgo_id, name, rarity, shortcode, collector_id, premium)
                cards.append(newCard)

    db.drop_collection('test')
    db.test.insert_many(cards)


# Global variabal setDict. Used for translating shortcode to expansion.
setDict = {
    '10E': 'Core Set Tenth Edition',
    '5DN': 'Fifth Dawn',
    '7E': 'Core Set Seventh Edition',
    '8ED': 'Core Set Eighth Edition',
    '9ED': 'Core Set Ninth Edition',
    'ALA': 'Shards of Alara',
    'AP': 'Apocalypse',
    'ARB': 'Alara Reborn',
    'AVR': 'Avacyn Restored',
    'BNG': 'Born of the Gods',
    'BOK': 'Betrayers of Kamigawa',
    'C13': 'Commander 2013',
    'C14': 'Commander (2014 Edition)',
    'CHK': 'Champions of Kamigawa',
    'CMD': 'Commander',
    'CON': 'Conflux',
    'CSP': 'Coldsnap',
    'DD2': 'Duel Decks: Jace vs. Chandra',
    'DDC': 'Duel Decks: Divine vs. Demonic',
    'DDD': 'Duel Decks: Garruk vs. Liliana',
    'DDE': 'Duel Decks: Phyrexia vs. The Coalition',
    'DDF': 'Duel Decks: Elspeth vs. Tezzeret',
    'DDG': 'Duel Decks: Knights vs. Dragons',
    'DDH': 'Duel Decks: Ajani vs. Nicol Bolas',
    'DDI': 'Duel Decks: Venser vs. Koth',
    'DDJ': 'Duel Decks: Izzet vs. Golgari',
    'DDK': 'Duel Decks: Sorin vs. Tibalt',
    'DDL': 'Duel Decks: Heroes vs. Monsters',
    'DDM': 'Duel Decks: Jace vs. Vraska',
    'DGM': "Dragon's Maze",
    'DIS': 'Dissension',
    'DKA': 'Dark Ascension',
    'DRB': 'From the Vault: Dragons',
    'DST': 'Darksteel',
    'DTK': 'Dragons of Tarkir',
    'EVE': 'Eventide',
    'EVG': 'Duel Decks: Elves vs. Goblins',
    'EX': 'Exodus',
    'FRF': 'Fate Reforged',
    'FUT': 'Future Sight',
    'GPT': 'Guildpact',
    'GTC': 'Gatecrash',
    'H09': 'Premium Deck Series: Slivers',
    'IN': 'Invasion',
    'ISD': 'Innistrad',
    'JOU': 'Journey into Nyx',
    'JUD': 'Judgment',
    'KTK': 'Khans of Tarkir',
    'LGN': 'Legions',
    'LRW': 'Lorwyn',
    'M10': 'Magic 2010 Core Set',
    'M11': 'Magic 2011 Core Set',
    'M12': 'Magic 2012 Core Set',
    'M13': 'Magic 2013 Core Set',
    'M14': 'Magic 2014 Core Set',
    'M15': 'Magic 2015 Core Set',
    'MBS': 'Mirrodin Besieged',
    'ME2': 'Masters Edition II',
    'ME3': 'Masters Edition III',
    'ME4': 'Masters Edition IV',
    'MED': 'Masters Edition',
    'MI': 'Mirage',
    'MM': 'Mercadian Masques',
    'MMA': 'Modern Masters',
    'MM2': 'Modern Masters 2015 Edition',
    'MOR': 'Morningtide',
    'MRD': 'Mirrodin',
    'NE': 'Nemesis',
    'NPH': 'New Phyrexia',
    'OD': 'Odyssey',
    'ONS': 'Onslaught',
    'PC1': 'Planechase',
    'PC2': 'Planechase (2012 Edition)',
    'PD2': 'Premium Deck Series: Fire & Lightning',
    'PD3': 'Premium Deck Series: Graveborn',
    'PLC': 'Planar Chaos',
    'PR': 'Prophecy',
    'PRM': 'Promo',
    'PS': 'Planeshift',
    'RAV': 'Ravnica: City of Guilds',
    'ROE': 'Rise of the Eldrazi',
    'RTR': 'Return to Ravnica',
    'SCG': 'Scourge',
    'SHM': 'Shadowmoor',
    'SOK': 'Saviors of Kamigawa',
    'SOM': 'Scars of Mirrodin',
    'ST': 'Stronghold',
    'TD0': 'Theme Deck Set',
    'TD2': 'Duel Decks: Mirrodin Pure vs. New Phyrexia',
    'TE': 'Tempest',
    'THS': 'Theros',
    'TOR': 'Torment',
    'TPR': 'Tempest Remastered',
    'TSB': 'Timeshifted',
    'TSP': 'Time Spiral',
    'UD': "Urza's Destiny",
    'UL': "Urza's Legacy",
    'UZ': "Urza's Saga",
    'V09': 'From the Vault: Exiled',
    'V10': 'From the Vault: Relics',
    'V11': 'From the Vault: Legends',
    'V12': 'From the Vault: Realms',
    'V13': 'From the Vault: Twenty',
    'V14': 'From the Vault: Annihilation',
    'VI': 'Visions',
    'VMA': 'Vintage Masters',
    'WL': 'Weatherlight',
    'WWK': 'Worldwake',
    'ZEN': 'Zendikar'
}
