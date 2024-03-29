from bson import json_util
from flask import Flask, jsonify, request
from pymongo import MongoClient
import json
import time
import names
import random
import uuid

app = Flask(__name__)
client = MongoClient("mongo_db_url_here")

myDatabase = client['game-x']
myCollection = myDatabase['users']

# this returns the 1.2.3 players with their ranks
def getLeaderBoard():
    leaderboard = []
    myFind = {}
    myFilter = {"_id": 0, "points": 1, "display_name": 1, "country": 1, "timestamp":1}
    for x in myCollection.find(myFind, myFilter).sort("points", -1).limit(10):
        # print(x['user_id'])
        playerScore = x["points"]
        playerTimeStamp = x["timestamp"]
        b = myCollection.find({"points": {"$gt": playerScore}}).count()
        c = myCollection.find({"points": {"$eq": playerScore}, "timestamp": {"$lt": playerTimeStamp}}).count()
        x['rank'] = b+c + 1
        leaderboard.append(x)
    leaderboard.sort(key=sortListFunction)
    if len(leaderboard) == 0:
        leaderboard = {"message" : "Database is empty"}
    else:
        for y in leaderboard:
            y.pop('timestamp', None)    # remove 'timestamp' from dictionary for not showing
    return leaderboard

# this returns for sorting leaderboard list by rank and presenting in sorted
def sortListFunction(e):
    return e["rank"]

# this returns the 1.2.3 players with their ranks by country iso code(country spesific data)
def getLeaderBoardWithCountryIsoCode(country_iso_code):
    leaderboardWithCountryIsoCode = []
    myFind = {"country": country_iso_code}
    myFilter = {"_id": 0, "points": 1, "display_name": 1, "country": 1}
    if country_iso_code is None:
        return
    for x in myCollection.find(myFind, myFilter).sort("points", -1).limit(10):
        agg_result = myCollection.aggregate(
            [
                {
                    "$match": {
                        "points": {
                            "$gte": x['points']
                        }
                    }
                },
                {
                    "$count": "passing_scores"
                }
            ]
        )
        for a in agg_result:
            #print(a)
            x['rank'] = a['passing_scores']
        leaderboardWithCountryIsoCode.append(x)
    if len(leaderboardWithCountryIsoCode) == 0:
        leaderboardWithCountryIsoCode = {"message" : "Country code is invalid"}
    else:
        pass
    return leaderboardWithCountryIsoCode

def parse_json(data):
    return json.loads(json_util.dumps(data))

# this returns user profile finding by GUID and adds its rank
def getUserProfileWithGuid(guid):
    myFind = {"user_id": guid}
    myFilter = {"_id": 0, "points": 1, "display_name": 1, "country": 1}
    userprofileWithGuid = myCollection.find_one(myFind, myFilter)
    #print(userprofileWithGuid)
    if userprofileWithGuid is not None:
        agg_result = myCollection.aggregate(
            [
                {
                    "$match": {
                        "points": {
                            "$gte": userprofileWithGuid['points']
                        }
                    }
                },
                {
                    "$count": "passing_scores"
                }
            ]
        )
        for a in agg_result:
            userprofileWithGuid['rank'] = a['passing_scores']
    else:
        pass
    return userprofileWithGuid

# this returns a epoch time in the type of int
def getTimestamp():
    return int(time.time())

@app.route('/', methods=['GET'])
def landingPage():
    return "The resource cannot be found"

@app.route('/leaderboard', methods=['GET'])
def leaderboardPage():
    return json.dumps(getLeaderBoard(), indent=4, sort_keys=True)

@app.route('/leaderboard/<country_iso_code>', methods=['GET'])
def leaderboardPageWithCountryIsoCode(country_iso_code):
    return jsonify(parse_json(getLeaderBoardWithCountryIsoCode(country_iso_code)))

@app.route('/user/profile/<guid>', methods=['GET'])
def userprofilePageWithGuid(guid):
    result = getUserProfileWithGuid(guid)
    if result is not None:
        return jsonify(parse_json(result))
    else:
        return jsonify(parse_json({"message" : "user doesn't exists"}))

@app.route('/user/create', methods=['POST'])
def usercreatePage():
    # checking the existing guid for preventing collusion
    guid = request.get_json()['user_id']
    myFind = {"user_id": guid}
    myFilter = {"_id": 0, "points": 1, "display_name": 1, "country": 1}
    userprofileWithGuid = myCollection.find_one(myFind, myFilter)
    if userprofileWithGuid is None:
        newUserProfile = {}
        newUserProfile['display_name'] = request.get_json()['display_name']
        newUserProfile['user_id'] = request.get_json()['user_id']
        newUserProfile['points'] = request.get_json()['points']
        newUserProfile['country'] = request.get_json()['country']
        newUserProfile['timestamp'] = getTimestamp()
        #print(newUserProfile)
        myCollection.insert(newUserProfile)
        newUserProfile.pop('_id', None)
        newUserProfile.pop('user_id', None)
        newUserProfile.pop('timestamp', None)
        agg_result = myCollection.aggregate(
            [
                {
                    "$match": {
                        "points": {
                            "$gte": newUserProfile['points']
                        }
                    }
                },
                {
                    "$count": "passing_scores"
                }
            ]
        )
        for a in agg_result:
            newUserProfile['rank'] = a['passing_scores']
        return jsonify(parse_json(newUserProfile))
    else:
        return jsonify(parse_json({"message" : "user exists", "success" : False}))

@app.route('/score/submit', methods=['POST'])
def scoresubmitPage():
    """
    this function can be used for updating a player's score.
    :return:
    """
    #print(request.get_json())
    guid = request.get_json()['user_id']
    scoreWorth = request.get_json()['score_worth']
    myFind = {"user_id": guid}
    myFilter = {"_id": 0, "points": 1, "user_id": 1, "display_name": 1}
    userprofileWithGuid = myCollection.find_one(myFind, myFilter)
    #print(userprofileWithGuid)
    if userprofileWithGuid is not None:
        userprofileWithGuid['points'] += scoreWorth     # increase player score
        myQuery = {"user_id" : userprofileWithGuid["user_id"]}
        myNewValues = {"$set": {"points" : userprofileWithGuid['points'], "timestamp" : int(time.time())}}
        myCollection.update_one(myQuery, myNewValues)

        # find user rank
        agg_result = myCollection.aggregate(
            [
                {
                    "$match": {
                        "points": {
                            "$gte": userprofileWithGuid['points']
                        }
                    }
                },
                {
                    "$count": "passing_scores"
                }
            ]
        )
        for a in agg_result:
            userprofileWithGuid['rank'] = a['passing_scores']
    else:
        userprofileWithGuid = {"message" : "user is not found"}
    return jsonify(parse_json(userprofileWithGuid))

@app.route('/createfields', methods=['GET'])
@app.route('/createfields/', methods=['GET'])
def createFakeFieldsPage():
    """
    this function creates fake fields for testing the Restful API
    sample GET request : localhost:3000/createfields?iteration=5

    sample MongoDB field in JSON
    {
        "_id": {
            "$oid": "600887737718091954842845"
        },
        "user_id": "d28d919b-1f95-4003-a2cf-7ede28279d08",
        "display_name": "Hugh Dach V",
        "points": 875,
        "country": "tr",
        "timestamp": 1611171699
    }
    :param iteration:
    :return:
    """

    iteration = 1000
    countryCodeList = ["tr", "en", "de", "es", "it"]
    for x in range(iteration):
        newField = {
            "user_id": str(uuid.uuid4()),
            "display_name": names.get_full_name().replace(' ', '_'),
            "points": random.randint(1, 1000000),
            "country": countryCodeList[random.randint(0, len(countryCodeList) - 1)],
            "timestamp": random.randint(946688400, 1611427150)
        }
        myCollection.insert_one(newField)
    return jsonify(parse_json({"message" : "fake resources has been inserted"}))

@app.errorhandler(404)
def not_found(*args):
    """Page not found."""
    return jsonify(parse_json({"message":"The resource cannot be found"}))

if __name__ == '__main__':
    app.run(debug=False, threaded=True)
