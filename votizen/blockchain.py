from pymongo import MongoClient

import json
import hashlib as hasher
import datetime
client = MongoClient('mongodb://localhost:27017/')
db = client['votizen']

reg = db.registration
vot = db.voting


REG_INDEX = 1000000
VOT_INDEX = 2000000


class Block:
    def __init__(self, block, timestamp, previous_hash, transactions=[]):
        self.index = None
        self.transactions = transactions
        if not reg.find({'index': REG_INDEX}).count() and block == 'REG':
            reg_genesis = {
                "index": REG_INDEX,
                "timestamp": datetime.datetime.utcnow(),
                "transactions": [],
                "hash": "ajskd876as87geaq7weva",
                "previous_hash": None
            }
            reg.insert_one(reg_genesis)
            self.index = REG_INDEX

        if not vot.find({'index': VOT_INDEX}).count() and block == 'VOT':
            vot_genesis = {
                "index": VOT_INDEX,
                "timestamp": datetime.datetime.utcnow(),
                "transactions": [],
                "hash": "ajskd876as87geaq7weva",
                "previous_hash": None
            }
            vot.insert_one(vot_genesis)
            self.index = VOT_INDEX

        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update((str(self.index) +
                    str(self.timestamp) +
                    str(self.transactions) +
                    str(self.previous_hash)).encode())
        return sha.hexdigest()

    @staticmethod
    def add_reg_transaction(transaction):
        reg.find_one_and_update({'index': REG_INDEX}, {
                                '$push': {'transactions': transaction}})

    @staticmethod
    def add_vot_transaction(transaction):
        vot.find_one_and_update({'index': VOT_INDEX}, {
                                '$push': {'transactions': transaction}})

    @staticmethod
    def team_registered(id):
        if reg.find({'transactions': {'$elemMatch': {'team_id': id}}}).count() == 0:
            return False
        stored_transactions =  reg.find_one({'transactions': {'$elemMatch': {'team_id': id}}}).get('transactions', None)
        team_hash = None
        for t in stored_transactions:
            if t['team_id'] == id:
                team_hash = t['team_hash']
        return team_hash

    @staticmethod
    def team_voted(team_hash):
        if vot.find({'transactions':{'$elemMatch': {'team_hash': team_hash}}}).count() == 0:
            return False
        return True

