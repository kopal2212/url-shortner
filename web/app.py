
from flask import Flask, request, abort, jsonify
import pymongo,pyshorteners,re
from datetime import datetime

app = Flask(__name__)
URL = 'https://tinyurl.com/'


myclient = pymongo.MongoClient("mongodb://db:27017/") # making a mongo connection. 
db = myclient['shortUrls'] # shortUrls is the name of the database we would be using
objects = db['urls'] #urls is the name of the collection

#introductory route bounded with welcome function
@app.route('/', methods=['GET'])
def welcome():
    return 'Welcome to URL Shortner made with Python,Flask and MongoDb!'

#route for original URL look up with identifier(url_id) bounded with lookup function
@app.route('/api/v1/lookup/<url_id>', methods=['GET'])
def lookup(url_id=None):
    if url_id:
        url = objects.find_one({'url_id': url_id})
        if url:
            url['id'] = str(url['_id'])
            url['added'] = date_to_str(url['added'])
            del url['_id']
            return jsonify({'lookup': url}),200
    abort(404)

#route to fetch the original web link from the user and return the shortened URL
@app.route('/api/v1/shorten/', methods=['POST'])
def original_to_shorten_url():
    link = request.form.get('link')
    if isValidURL(link) == False:
        return abort(400)
    url = objects.find_one({'link': link})
    if url:
        return jsonify({'url': URL + url['url_id']}),200
    else:
        return jsonify({'url': shorten_url(link)}),200

#function to verify if the entered URL is valid or not
def isValidURL(string):
    regex = ("((http|https)://)(www.)?" +"[a-zA-Z0-9@:%._\\+~#?&//=]" +"{2,150}\\.[a-z]" +"{2,6}\\b([-a-zA-Z0-9@:%" +"._\\+~#?//&=]*)")
    a = re.compile(regex)
    if (string == None):
        return False
    if(re.search(a, string)):
        return True
    else:
        return False

#function to shorten the any given URL
def shorten_url(link) :
    shortener = pyshorteners.Shortener()
    url = shortener.tinyurl.short(link)
    url_id=str(url[20:])
    objects.insert_one({'url_id': url_id, 'link': link, 'shortened_url': URL+url_id, 'added': datetime.utcnow()})
    return url

#function to convert date to string
def date_to_str(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%d-%m-%Y- %H:%M:%S')


if __name__ == '__main__':
    app.run(host='0.0.0.0')