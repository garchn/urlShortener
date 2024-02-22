from flask import Flask, json, jsonify, request, g, make_response
from sqlitedict import SqliteDict
import webbrowser
import string
import random
from datetime import datetime, timedelta
from bisect import bisect

api = Flask(__name__)
BASE62 = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
SHORT_TO_LONG_FILE = 'short2long.sqlite'
URL_STATS_FILE = 'urlStats.sqlite'

short2long = SqliteDict(SHORT_TO_LONG_FILE)
urlStats = SqliteDict(URL_STATS_FILE)

@api.route('/encode', methods=['POST'])
def encode():
    data = request.get_json()
    long_url = data['longUrl']

    if not isinstance(long_url, str):
        resp = make_response("Invalid URL Formatting", 400)
        return resp

    # using base62 and a shortUrl of 7 characters allows us to support 62^7 ~= 3.5 trillion URLs.
    def randomBase62IdGen(size=7, chars = string.ascii_uppercase + string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    # simply rehashing on hash collision because with URLs on the scale of millions, collisions will be unlikely.
    short_url = randomBase62IdGen()
    while short_url in short2long:
        short_url = randomBase62IdGen()

    short2long[short_url] = long_url
    short2long.commit()
    return jsonify({"shortUrl": short_url})

@api.route('/decode', methods=['GET'])
def decode():
    data = request.get_json()
    short_url = data['shortUrl']

    if not isinstance(short_url, str):
        resp = make_response("Invalid URL", 400)
        return resp

    for c in short_url:
        if c not in BASE62:
            resp = make_response("Invalid URL: shortUrl is not of base 62 format.", 400)
            return resp

    if len(short_url) != 7:
        resp = make_response("Invalid URL: shortUrl must be 7 characters long.", 400)
        return resp

    if short_url not in short2long:
        resp = make_response("Short URL not found", 404)
        return resp

    long_url = short2long[short_url]
    webbrowser.open(long_url)

    visits = urlStats.get(short_url, json.dumps([]))
    visits = json.loads(visits)

    now = (datetime.utcnow()).isoformat()
    # Simulating 2 days ago
    # now = (datetime.utcnow() - timedelta(days=2)).isoformat()
    # Uncommenting this to simulate a visit from 2 weeks ago
    # now = (datetime.utcnow() - timedelta(weeks=2)).isoformat()

    visits.append(now)
    urlStats[short_url] = json.dumps(visits)
    urlStats.commit()

    return jsonify({"longUrl": long_url})

@api.route('/stats', methods=['GET'])
def stats():
    data = request.get_json()
    short_url = data['shortUrl']

    for c in short_url:
        if c not in BASE62:
            resp = make_response("Invalid URL: shortUrl is not of base 62 format.", 400)
            return resp

    if len(short_url) != 7:
        resp = make_response("Invalid URL: shortUrl must be 7 characters long.", 400)
        return resp

    visits = urlStats.get(short_url, json.dumps([]))
    visits = json.loads(visits)
    now = datetime.now()
    past24h = now - timedelta(days=1)
    past7d = now - timedelta(weeks=1)

    visits_past_day, visits_past_week = 0, 0

    for dt in visits:
        dt = datetime.fromisoformat(dt)
        if dt > past7d:
            visits_past_week += 1
        if dt > past24h:
            visits_past_day += 1

    return jsonify({"shortUrl": short_url, "visits": len(visits), "visits_within_past_day": visits_past_day, "visits_within_past_week": visits_past_week})


if __name__ == '__main__':
    api.run()
