#!/usr/bin/env python3

from pytm import (
    TM,
    Actor,
    Boundary,
    Classification,
    Data,
    Dataflow,
    Datastore,
    Lambda,
    Server,
    DatastoreType,
)

tm = TM("Jade Delight TM")
tm.description = " Jade Delight is a basic website that allows users to order Chinese food. The functionality is limited, with users only being able to enter their contact information and select items to order."
tm.version = 2.0
tm.isOrdered = False
tm.mergeResponses = True
tm.assumptions = [
"InfintyFree servers are not hardened and do not sanitize input.",
"Communication over HTTP is not encrypted."
]

# create user
# trust level for user [1] =  anonymous web user
user = Actor("User")
user.levels = [1]

owner = Actor("Site Owner")
owner.levels = [2]

# create databse
db = Datastore("SQL Product Database")
db.controls.isHardened = False
db.levels = [2]


# create web server
web = Server("InfinityFree Server")
web.OS = "Linux"
web.controls.isHardened = False
web.controls.sanitizesInput = False
web.controls.encodesOutput = True
web.sourceFiles = ["pytm/json.py", "docs/template.md"]

# dataflows
# owner <-> db
products = Data("SQL queries that edit product database")
owner_to_db = Dataflow(owner, db, "Owner edits product database")
owner_to_db.data = products
owner_to_db.protocol = "MySQL"
owner_to_db.dstPort = 3306

# web <-> user
contact = Data("User-entered contact information and order details")
user_to_web = Dataflow(user, web, "User enters order information")
user_to_web.data = contact
user_to_web.protocol = "HTTP"
user_to_web.dstPort = 80

confirmation = Data("Order confirmation alert", classification=Classification.PUBLIC)

web_to_user = Dataflow(web, user, "Confirm Order")
web_to_user.protocol = "HTTP"
web_to_user.dstPort = 80
web_to_user.data = confirmation

# web <-> db
query = Data("Request for product information")
web_to_db = Dataflow(web, db, "Show product data")
web_to_db.protocol = "MySQL"
web_to_db.dstPort = 3306
web_to_db.data = query

product_price = Data("Product Names and Prices", classification=Classification.PUBLIC)
db_to_web = Dataflow(db, web, "Retrieve product data")
db_to_web.data = product_price
db_to_web.protocol = "MySQL"
db_to_web.dstPort = 80

if __name__ == "__main__":
    tm.process()