from flask import Flask, render_template
from flask import request, redirect, url_for, jsonify, flash

from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Items, User
engine = create_engine('sqlite:///catalogitemUser.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

# code for reading client_id.
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# code for connecting with google
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style ="width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# create new user.
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# return user object based on user id.
def getUserInfo(user_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    user = session.query(User).filter_by(id=user_id).one()
    return user


# return user id based on user email
def getUserID(email):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# disconnect applicaiton from google account.
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s' % access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        showAllCat = session.query(Category).all()
        latest = session.query(Items).order_by(Items.id.desc()).all()[1:8]
        return redirect(url_for('showCatalog'))
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Route and method for displaying Categories and latest items
@app.route('/')
@app.route('/catalog')
def showCatalog():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    showAllCat = session.query(Category).all()
    latest = session.query(Items).order_by(Items.id.desc()).all()[1:8]
    if 'username' not in login_session:
        return render_template(
            'publiccatalog.html',
            catalog=showAllCat, items=latest)
    else:
        return render_template(
            'showCatalog.html',
            catalogs=showAllCat, items=latest)


# route for displaying specific catalog item
@app.route('/catalog/<int:cat_id>/items')
def showItems(cat_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    showAllCat = session.query(Category).all()
    selectCat = session.query(Category).filter_by(id=cat_id).one()
    showCatitems = session.query(
        Items).filter_by(category_id=selectCat.id).all()
    return render_template(
        'showCatalogItems.html',
        catalogs=selectCat,
        allcat=showAllCat,  items=showCatitems)


# route for adding new item
@app.route('/catalog/<int:cat_id>/new', methods=['GET', 'POST'])
def createnewItem(cat_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        showAllCat = session.query(Category).filter_by(id=cat_id).one()
        newItem = Items(name=request.form['name'],
                        description=request.form['description'],
                        user_id=showAllCat.user_id, category_id=showAllCat.id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showItems', cat_id=showAllCat.id))
    else:
        return render_template('createnewItem.html', cat_id=cat_id)


# url for adding new categroy
@app.route('/catalog/new', methods=['POST', 'GET'])
def createnewCategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        newCat = Category(
            name=request.form['name'],
            user_id=login_session['user_id'])
        session.add(newCat)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('addnewCat.html')


# route for details of  specific items
@app.route('/catalog/<int:cat_id>/<int:item_id>')
def itemDetail(cat_id, item_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    selectCat = session.query(Category).filter_by(id=cat_id).one()
    itemDetail = session.query(
        Items).filter_by(
        category_id=selectCat.id).filter_by(id=item_id).one()
    return render_template(
        'itemDetails.html',
        catalogs=selectCat, items=itemDetail)


# route for editing item
@app.route('/catalog/<int:cat_id>/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(cat_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    allcat = session.query(Category).all()
    editedCat = session.query(Category).filter_by(id=cat_id).one()
    editedItem = session.query(
        Items).filter_by(
        id=item_id).filter_by(category_id=editedCat.id).one()
    if request.method == 'POST':
        if request.form['name'] and request.form['description'] and request.form['categories']:
            editedItem.name = request.form['name']
            editedItem.category_id = request.form['categories']
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showItems', cat_id=editedCat.id))
    else:
        return render_template(
            'editItem.html', cat_id=editedCat,
            item_id=editedItem, categories=allcat)


# route to delete item
@app.route(
    '/catalog/<int:cat_id>/<int:item_id>/delete',
    methods=['GET', 'POST'])
def deleteItem(cat_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    deleteCat = session.query(Category).filter_by(id=cat_id).one()
    deleteItem = session.query(
        Items).filter_by(id=item_id).filter_by(
            category_id=deleteCat.id).one()
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        return redirect(url_for('showItems', cat_id=deleteCat.id))
    else:
        return render_template(
            'deleteItem.html', catalogs=deleteCat,
            items=deleteItem)


# json end point for specific category
@app.route('/catalog/<int:cat_id>/items/JSON')
def getCategoriesJSON(cat_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    cat = session.query(Category).filter_by(id=cat_id).one()
    itm = session.query(Items).filter_by(category_id=cat.id).all()
    return jsonify(items=[i.serialize for i in itm])


# json end point  for specific item
@app.route('/catalog/<int:cat_id>/<int:item_id>/JSON')
def getItemJSON(cat_id, item_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    item = session.query(Items).filter_by(id=item_id).one()
    return jsonify(item=item.serialize)


# json endpoint for all categories and items
@app.route('/catalog.json')
def getJson():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    getallCat = session.query(Category).all()
    getallItem = session.query(Items).all()
    return jsonify(
        Category=[j.serialize for j in getallCat],
        Items=[i.serialize for i in getallItem])


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'ItemCatalog'
    app.run(host='0.0.0.0', port=8000)
