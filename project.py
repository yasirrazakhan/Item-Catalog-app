from flask import Flask, render_template, request, redirect, url_for, jsonify
app= Flask(__name__)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Items
engine = create_engine('sqlite:///catalogitem.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


@app.route('/test')
def test():
	DBSession = sessionmaker(bind = engine)
	session = DBSession()
	showAllCat = session.query(Category).all()
	latest = session.query(Items).order_by(Items.id.desc()).all()[1:8]
	return render_template('index.html', catalogs = showAllCat, items = latest)


@app.route('/')
@app.route('/catalog')
def showCatalog():
	DBSession = sessionmaker(bind = engine)
	session = DBSession()
	showAllCat = session.query(Category).all()
	latest = session.query(Items).order_by(Items.id.desc()).all()[1:8]
	return render_template('showCatalog.html',catalogs = showAllCat, items = latest)



#route for displaying specific catalog item
@app.route('/catalog/<string:cat_name>/items')
def showItems(cat_name):
	DBSession = sessionmaker(bind = engine)
	session = DBSession()
	#new_name = cat_name.replace(' ', ' ')
	showAllCat = session.query(Category).all()
	selectCat = session.query(Category).filter_by(name=cat_name).one()
	showCatitems = session.query(Items).filter_by(category_id = selectCat.id).all()
	return render_template('showCatalogItems.html', catalogs=selectCat, allcat = showAllCat, cat_name = selectCat.name, items = showCatitems)


#route for adding new item
@app.route('/catalog/<string:cat_name>/new', methods = ['GET', 'POST'])
def createnewItem(cat_name):

	if request.method == 'POST':
		DBSession = sessionmaker(bind = engine)
		session = DBSession()
		showAllCat = session.query(Category).filter_by(name = cat_name).one()
		newItem = Items(name = request.form['name'], description = request.form['description'],
                         category_id = showAllCat.id)
		session.add(newItem)
		session.commit()
		return redirect(url_for('showItems', cat_name = showAllCat.name))
	else:
		return render_template('createnewItem.html' ,cat_name = cat_name)

#url for adding new categroy
@app.route('/catalog/new', methods = ['POST', 'GET'])
def createnewCategory():
	if request.method == 'POST':
		DBSession = sessionmaker(bind = engine)
		session = DBSession()
		newCat = Category(name = request.form['name'])
		session.add(newCat)
		session.commit()
		return redirect(url_for('showCatalog'))
	else:
		return render_template('addnewCat.html')

#route for details of  specific items
@app.route('/catalog/<string:cat_name>/<string:item_name>')
def itemDetail(cat_name, item_name):
	DBSession = sessionmaker(bind = engine)
	session = DBSession()
	selectCat = session.query(Category).filter_by(name=cat_name).one()
	itemDetail = session.query(Items).filter_by(category_id = selectCat.id).filter_by(name = item_name).one()
	return render_template('itemDetails.html', catalogs=selectCat, items= itemDetail)

#route for editing item
@app.route('/catalog/<string:cat_name>/<string:item_name>/edit', methods = ['GET', 'POST'])
def editItem(cat_name, item_name):
	DBSession = sessionmaker(bind = engine)
	session = DBSession()
	editedCat = session.query(Category).filter_by(name = cat_name).one()
	editedItem = session.query(Items).filter_by(name = item_name).filter_by(category_id = editedCat.id).one()
	if request.method == 'POST':
		if request.form['name'] and request.form['description']:
			editedItem.name = request.form['name']
			editedItem.description = request.form['description']
		session.add(editedItem)
		session.commit()
		return redirect(url_for('showItems', cat_name = editedCat.name))
	else:
		return render_template('editItem.html', cat_name = editedCat, item_name = editedItem)

#route to delete item
@app.route('/catalog/<string:cat_name>/<string:item_name>/delete', methods = ['GET', 'POST'])
def  deleteItem(cat_name, item_name):
	DBSession = sessionmaker(bind = engine)
	session = DBSession()
	deleteCat = session.query(Category).filter_by(name = cat_name).one()
	deleteItem = session.query(Items).filter_by(name = item_name).filter_by(category_id = deleteCat.id).one()
	if request.method == 'POST':
		session.delete(deleteItem)
		session.commit()
		return redirect(url_for('showItems', cat_name = deleteCat.name))
	else:
		return render_template('deleteItem.html', catalogs=deleteCat, items= deleteItem)


#json endpoint
@app.route('/catalog.json')
def getJson():
	DBSession = sessionmaker(bind = engine)
	session = DBSession()
	getallCat = session.query(Category).all()
	return jsonify(Categories=[ i.serialize for i in getallCat])


# @app.route('/category/<string:cat_name>/items/JSON')
# def getCategoriesJSON(cat_id):
# 	DBSession = sessionmaker(bind = engine)
# 	session = DBSession()
#     cat = session.query(Category).filter_by(id=cat_name).one()
#     itm = session.query(Items).filter_by(category_id = cat.id).all()
#     return jsonify(items=itm.serialize)


# @app.route('/category/<string:cat_name>/<string:item_name>/JSON')
# def getItemJSON():
# 	DBSession = sessionmaker(bind = engine)
# 	session = DBSession()
#     item = session.query(Items).filter_by(name = item_name).one()
#     return jsonify(item=item.serialize)

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port=8000)