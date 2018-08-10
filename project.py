from flask import Flask, render_template
app= Flask(__name__)



catalog = {'name': 'The CRUDdy Crab', 'id': '1'}

catalogs = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [{'name':'Cheese Pizza', 'description':'made with fresh cheese' ,'id': '1'},
		  {'name':'Chocolate Cake','description':'made with Dutch Chocolate','id':'2'},
		  {'name':'Caesar Salad', 'description':'with fresh organic vegetables','id':'3'},
		  {'name':'Iced Tea', 'description':'with lemon','id':'4'},
		  {'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','id':'5'}
		]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese'}


#route for displaying all categories
@app.route('/')
@app.route('/catalog')
def showCatalog():
	return render_template('showCatalog.html',catalogs = catalogs)



#route for displaying specific catalog item
@app.route('/catalog/<string:cat_name>/items')
def showItems(cat_name):
	return render_template('showCatalogItems.html', catalogs=catalogs, items = items)


#route for adding new item
@app.route('/catalog/item/new')
def createnewItem():
	return render_template('createnewItem.html')

#route for details of  specific items
@app.route('/catalog/<string:cat_name>/<string:item_name>')
def itemDetail(cat_name, item_name):
	return "catalog destail"

#route for editing item
@app.route('/catalog/<string:cat_name>/<string:item_name>/edit')
def editItem(cat_name, item_name):
	return "page for editing catalog %s item" %cat_name

#route to delete item
@app.route('/catalog/<string:cat_name>/<string:item_name>/delete')
def  deleteItem(cat_name, item_name):
	return "page to delete item"


#json endpoint
@app.route('/catalog.json')
def getJson():
	return "page to display Json for catalog"


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port=8000)