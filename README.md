# Online shop
## Table of contents
* General info
* Functionalities
* Technologies
## General info
The purpose was to create shop where producents could register and sell their products to users. When product is added to a cart, it is added to a section of a producent it belongs to. User can then select which producent products he is buying and process to payment. 
## Functionalities
* Registration as a producent or user
* Login as a producent or user and logout
* Main page view of all products
* Category page view of products which belong to it
* Detailed view of a product
#### Producent can:
* Add a new product to a database and add it to chosen category
* Change product visibility in a shop
* Edit product description
* See history of orders: client id, order status, was it payed, shipment detail, cost
#### User can:
* Add a product to cart
* Remove a product from cart
* Remove a specific producent's products from cart
* Process to order 
* See his history of orders: producent id, order status, was it payed, shipment detail, cost
## Technologies
* Django
* Postgresql
* venv
## Todo
* Lookup of a product by name
* Message module
* Reclamation