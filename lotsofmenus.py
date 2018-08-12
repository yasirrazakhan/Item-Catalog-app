from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Items

engine = create_engine('sqlite:///catalogitem.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()



category5 = Category(name = "Base Ball")

session.add(category5)
session.commit()

Item1 = Items(name = "Bat", description = "Made of wood thick at end and thinner at upper end, and usually in cylindrical shap", categories = category5)

session.add(Item1)
session.commit()


Item2 = Items(name = "Ball", description = "Ball made of cork", categories = category5)

session.add(Item2)
session.commit()




# category1 = Category(name = "Circket")

# session.add(category1)
# session.commit()

# Item1 = Items(name = "Bat", description = "Made of wood, usually 2 feet in lenght flat and half and inch thick while half feet in width.", categories = category1)

# session.add(Item1)
# session.commit()


# Item2 = Items(name = "Ball", description = "Made with leather from the outside and hard cork from the inside, the two halfs of leather are stiched together with thread. Two colors are available red and white", categories = category1)

# session.add(Item2)
# session.commit()

# Item3 = Items(name = "Shoes", description = "Sport shoes with spikes are best fit of Circket", categories = category1)

# session.add(Item3)
# session.commit()

# Item4 = Items(name = "Wicket", description = "Three cylindrical shaped wood sticks each of lenght 2 feet and width half inch",  categories = category1)

# session.add(Item4)
# session.commit()

# # Items4 = Items(name = "Sirloin Burger", description = "Made with grade A beef", price = "$7.99", course = "Entree", categories = categories1)

# # session.add(Items4)
# # session.commit()

# # Items5 = Items(name = "Root Beer", description = "16oz of refreshing goodness", price = "$1.99", course = "Beverage", categories = categories1)

# # session.add(Items5)
# # session.commit()

# # Items6 = Items(name = "Iced Tea", description = "with Lemon", price = "$.99", course = "Beverage", categories = categories1)

# # session.add(Items6)
# # session.commit()

# # Items7 = Items(name = "Grilled Cheese Sandwich", description = "On texas toast with American Cheese", price = "$3.49", course = "Entree", categories = categories1)

# # session.add(Items7)
# # session.commit()

# # Items8 = Items(name = "Veggie Burger", description = "Made with freshest of ingredients and home grown spices", price = "$5.99", course = "Entree", categories = categories1)

# # session.add(Items8)
# # session.commit()




# #Menu for Super Stir Fry
# category2 = Category(name = "Hockey")

# session.add(category2)
# session.commit()


# Item1 = Items(name = "Hockey Stick", description = "usually made of wood and 300 cm long, the end part of the Hockey sticks is curved to make contact with the ball ", categories = category2)

# session.add(Item1)
# session.commit()

# Item2 = Items(name = "Ball", description = "The ball used in the game of field hockey is spherical in shape. Made of solid plastic, a hockey ball is very hard, and in some cases, may contain a core made of cork", categories = category2)

# session.add(Item2)
# session.commit()

# Item3 = Items(name = "Jersey", description = "Each team has their own unique Jersey ",  categories = category2)

# session.add(Item3)
# session.commit()

# # Items4 = Items(name = "Nepali Momo ", description = "Steamed dumplings made with vegetables, spices and meat. ", price = "12", course = "Entree", categories = categories2)

# # session.add(Items4)
# # session.commit()

# # Items5 = Items(name = "Beef Noodle Soup", description = "A Chinese noodle soup made of stewed or red braised beef, beef broth, vegetables and Chinese noodles.", price = "14", course = "Entree", categories = categories2)

# # session.add(Items5)
# # session.commit()

# # Items6 = Items(name = "Ramen", description = "a Japanese noodle soup dish. It consists of Chinese-style wheat noodles served in a meat- or (occasionally) fish-based broth, often flavored with soy sauce or miso, and uses toppings such as sliced pork, dried seaweed, kamaboko, and green onions.", price = "12", course = "Entree", categories = categories2)

# # session.add(Items6)
# # session.commit()




# #Menu for Panda Garden
# category3 = Category(name = "Rock Climbing")

# session.add(category3)
# session.commit()


# Item1 = Items(name = "Rope", description = "Saftey is the first priority, so packing rope is the first thing.", categories = category3)

# session.add(Item1)
# session.commit()

# Item2 = Items(name = "Sling", description = "A flexible strap or belt, Saftey is the number first priority", categories = category3)

# session.add(Item2)
# session.commit()

# Item3 = Items(name = "Harnesses", description = "The harness is an attachment between a stationary and non-stationary object and is usually fabricated from rope", categories = category3)

# session.add(Item3)
# session.commit()

# Item4 = Items(name = "Ascenders", description = "An ascender is a device (usually mechanical) used for directly ascending a rope, or for facilitating protection with a fixed rope when climbing on very steep mountain terrain.", categories = category3)

# session.add(Item4)
# session.commit()

# Items2 = Items(name = "Veggie Burger", description = "Juicy grilled veggie patty with tomato mayo and lettuce", price = "$9.50", course = "Entree", categories = categories1)

# session.add(Items2)
# session.commit()


#Menu for Thyme for that
# categories1 = categories(name = "Thyme for That Vegetarian Cuisine ")

# session.add(categories1)
# session.commit()


# Items1 = Items(name = "Tres Leches Cake", description = "Rich, luscious sponge cake soaked in sweet milk and topped with vanilla bean whipped cream and strawberries.", price = "$2.99", course = "Dessert", categories = categories1)

# session.add(Items1)
# session.commit()

# Items2 = Items(name = "Mushroom risotto", description = "Portabello mushrooms in a creamy risotto", price = "$5.99", course = "Entree", categories = categories1)

# session.add(Items2)
# session.commit()

# Items3 = Items(name = "Honey Boba Shaved Snow", description = "Milk snow layered with honey boba, jasmine tea jelly, grass jelly, caramel, cream, and freshly made mochi", price = "$4.50", course = "Dessert", categories = categories1)

# session.add(Items3)
# session.commit()

# Items4 = Items(name = "Cauliflower Manchurian", description = "Golden fried cauliflower florets in a midly spiced soya,garlic sauce cooked with fresh cilantro, celery, chilies,ginger & green onions", price = "$6.95", course = "Appetizer", categories = categories1)

# session.add(Items4)
# session.commit()

# Items5 = Items(name = "Aloo Gobi Burrito", description = "Vegan goodness. Burrito filled with rice, garbanzo beans, curry sauce, potatoes (aloo), fried cauliflower (gobi) and chutney. Nom Nom", price = "$7.95", course = "Entree", categories = categories1)

# session.add(Items5)
# session.commit()

# Items2 = Items(name = "Veggie Burger", description = "Juicy grilled veggie patty with tomato mayo and lettuce", price = "$6.80", course = "Entree", categories = categories1)

# session.add(Items2)
# session.commit()



# #Menu for Tony's Bistro
# categories1 = categories(name = "Tony\'s Bistro ")

# session.add(categories1)
# session.commit()


# Items1 = Items(name = "Shellfish Tower", description = "Lobster, shrimp, sea snails, crawfish, stacked into a delicious tower", price = "$13.95", course = "Entree", categories = categories1)

# session.add(Items1)
# session.commit()

# Items2 = Items(name = "Chicken and Rice", description = "Chicken... and rice", price = "$4.95", course = "Entree", categories = categories1)

# session.add(Items2)
# session.commit()

# Items3 = Items(name = "Mom's Spaghetti", description = "Spaghetti with some incredible tomato sauce made by mom", price = "$6.95", course = "Entree", categories = categories1)

# session.add(Items3)
# session.commit()

# Items4 = Items(name = "Choc Full O\' Mint (Smitten\'s Fresh Mint Chip ice cream)", description = "Milk, cream, salt, ..., Liquid nitrogen magic", price = "$3.95", course = "Dessert", categories = categories1)

# session.add(Items4)
# session.commit()

# Items5 = Items(name = "Tonkatsu Ramen", description = "Noodles in a delicious pork-based broth with a soft-boiled egg", price = "$7.95", course = "Entree", categories = categories1)

# session.add(Items5)
# session.commit()




# #Menu for Andala's
# categories1 = categories(name = "Andala\'s")

# session.add(categories1)
# session.commit()


# Items1 = Items(name = "Lamb Curry", description = "Slow cook that thang in a pool of tomatoes, onions and alllll those tasty Indian spices. Mmmm.", price = "$9.95", course = "Entree", categories = categories1)

# session.add(Items1)
# session.commit()

# Items2 = Items(name = "Chicken Marsala", description = "Chicken cooked in Marsala wine sauce with mushrooms", price = "$7.95", course = "Entree", categories = categories1)

# session.add(Items2)
# session.commit()

# Items3 = Items(name = "Potstickers", description = "Delicious chicken and veggies encapsulated in fried dough.", price = "$6.50", course = "Appetizer", categories = categories1)

# session.add(Items3)
# session.commit()

# Items4 = Items(name = "Nigiri Sampler", description = "Maguro, Sake, Hamachi, Unagi, Uni, TORO!", price = "$6.75", course = "Appetizer", categories = categories1)

# session.add(Items4)
# session.commit()

# Items2 = Items(name = "Veggie Burger", description = "Juicy grilled veggie patty with tomato mayo and lettuce", price = "$7.00", course = "Entree", categories = categories1)

# session.add(Items2)
# session.commit()




# #Menu for Auntie Ann's
# categories1 = categories(name = "Auntie Ann\'s Diner' ")

# session.add(categories1)
# session.commit()

# Items9 = Items(name = "Chicken Fried Steak", description = "Fresh battered sirloin steak fried and smothered with cream gravy", price = "$8.99", course = "Entree", categories = categories1)

# session.add(Items9)
# session.commit()



# Items1 = Items(name = "Boysenberry Sorbet", description = "An unsettlingly huge amount of ripe berries turned into frozen (and seedless) awesomeness", price = "$2.99", course = "Dessert", categories = categories1)

# session.add(Items1)
# session.commit()

# Items2 = Items(name = "Broiled salmon", description = "Salmon fillet marinated with fresh herbs and broiled hot & fast", price = "$10.95", course = "Entree", categories = categories1)

# session.add(Items2)
# session.commit()

# Items3 = Items(name = "Morels on toast (seasonal)", description = "Wild morel mushrooms fried in butter, served on herbed toast slices", price = "$7.50", course = "Appetizer", categories = categories1)

# session.add(Items3)
# session.commit()

# Items4 = Items(name = "Tandoori Chicken", description = "Chicken marinated in yoghurt and seasoned with a spicy mix(chilli, tamarind among others) and slow cooked in a cylindrical clay or metal oven which gets its heat from burning charcoal.", price = "$8.95", course = "Entree", categories = categories1)

# session.add(Items4)
# session.commit()

# Items2 = Items(name = "Veggie Burger", description = "Juicy grilled veggie patty with tomato mayo and lettuce", price = "$9.50", course = "Entree", categories = categories1)

# session.add(Items2)
# session.commit()

# Items10 = Items(name = "Spinach Ice Cream", description = "vanilla ice cream made with organic spinach leaves", price = "$1.99", course = "Dessert", categories = categories1)

# session.add(Items10)
# session.commit()



# #Menu for Cocina Y Amor
# categories1 = categories(name = "Cocina Y Amor ")

# session.add(categories1)
# session.commit()


# Items1 = Items(name = "Super Burrito Al Pastor", description = "Marinated Pork, Rice, Beans, Avocado, Cilantro, Salsa, Tortilla", price = "$5.95", course = "Entree", categories = categories1)

# session.add(Items1)
# session.commit()

# Items2 = Items(name = "Cachapa", description = "Golden brown, corn-based Venezuelan pancake; usually stuffed with queso telita or queso de mano, and possibly lechon. ", price = "$7.99", course = "Entree", categories = categories1)

# session.add(Items2)
# session.commit()


# categories1 = categories(name = "State Bird Provisions")
# session.add(categories1)
# session.commit()

# Items1 = Items(name = "Chantrelle Toast", description = "Crispy Toast with Sesame Seeds slathered with buttery chantrelle mushrooms", price = "$5.95", course = "Appetizer", categories = categories1)

# session.add(Items1)
# session.commit

# Items1 = Items(name = "Guanciale Chawanmushi", description = "Japanese egg custard served hot with spicey Italian Pork Jowl (guanciale)", price = "$6.95", course = "Dessert", categories = categories1)

# session.add(Items1)
# session.commit()



# Items1 = Items(name = "Lemon Curd Ice Cream Sandwich", description = "Lemon Curd Ice Cream Sandwich on a chocolate macaron with cardamom meringue and cashews", price = "$4.25", course = "Dessert", categories = categories1)

# session.add(Items1)
# session.commit()


print "added menu items!"
