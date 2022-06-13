# Django Marketplace
Django Marketplace is a market place like ebay/amazon run on a django server.
Using stripe as a payment processor you can create a buyer or seller account with verified bank details.
As a seller you can list your products with Title, Description, Price and everything else you would expect of a market place. 
As a buyer you can add stuff to your basket and checkout to make your basket into an order. 



## How to setup 

First you will need python 3
If you don't already have it go to https://www.python.org/ download and install python 3
The latest version this was tested on was 3.10.4

If you havent already clone this repo to your local machine.
From you CMD prompt cd into django_marketplace and run the following 
`pip install -r requirements.txt`

This will install the necassary packages for Django Marketplace to run:
django == 4.0.4
stripe == 3.0.0
pillow == 9.1.0

Next cd into django_markplace\django_marketplace and run:
`python manage.py runserver` 

Finally navigate to http://127.0.0.1:8000 in your browser to view Django market place.


## How to use

### Home/Product page
The first page to load is http://localhost:8000/products/product_list/ Which shows a list of products for sale on the site.

You can filter though this page using the 'Title', 'Price Min:Max' input boxes and the 'Catagory' dropdown list.
Remember to press 'Search'

From this screen you can add one unit of the product to your basket by clicking 'Add to Basket' on the listing or you can view the listing in full by clicking its title.
>NOTE: You have to be logged in to add items to your basket. 
>      A test buyer account is 
>      Username: buyer@test.test
>      Password: Buy3r***
>
>      Or alternativly create your own test accounts (you will need stripe test card details at checkout, found on stripes website)


### Basket and Checkout
Once you have added items to you basket it is time to view your basket and checkout.

You can view your basket by clicking 'Basket' in the top right of any page.
Here you can remove any products you don't want to buy if needed.
Once you have checked your basket and confimed everything you want to buy you can then click the 'checkout' button at the bottom of the page.

After you click 'Checkout' you will be redirected to a page asking you to select the delivery address and purchase card.
>NOTE: if you don't use the buyer@test.test login you will have to add your own delivery address and card (test card details can be found on stripes website) 

Finally to finish processing your order click the 'Complete transaction' button at the bottom of the checkout page.
This will take you to your orders page where you can see a list of all previous orders and there status's. (you can also navigate to this page using by clicking 'orders' on the top left menu bar.)

### Becoming a seller
You can make your test account into a seller by clicking 'Sell' on the top right menu bar. (Please do not make buyer@test.test a seller)

The form you get prompted to fill in will send off to stripe so you will need stripes test details to create an account (these can be found on stripes website)

If the stripe checks are all good then congrats you are now a seller.

Alternativly you can log into our test seller account:
Username: seller@test.test
Password: S3ll3r***

Once you are a seller or have logged into seller@test.test you will have extra links avaliable to you within the 'sell' page. 

#### My Products 
This page shows a list of all the products you currently have listed for sale

#### Create a listing
Fill in the presented form with all the required details and click 'save' to make a new product listing. Its that simple 

#### Sold
From this page you can see all the items you have sold. From here you can update the status of the order to say you have shipped the order.

### Settings
The final page to look at as a user is the settings page.
You can navigate to the settings page by clicking 'Settings' on the top right menu.

From this page you can update you login details, add a delivery address and add another payment card.

## Admin mode
To go into admin mode, with the server running navigate to http://127.0.0.1:8000/admin in your browser
log in using:
Username: admin@admin.admin
Passeword: admin

Inside the admin portal you can access the differnt users, orders, products catagories and users baskets 

### Custom users
In the customer users menu on the admin portal you can see a list of all the users and wether they are a buyer or seller.

By clicking into a user you can: 
-Reset there password if needed
-Update there email, first name and last name.
-View the date they joined and their stripe information 
-modifiy there permission
-See there associated card and address details
-See there current basket
-See all there orders new and old
-See all the products they have for sale

### Groups
Currently this is unused but will be for grouping users and assigning them permissions in bulk. 

### Orders
Within the orders menu you can see all the orders made, who ceated the order and what they brought.

Inside each order you can see:
-The order ID
-Buyer info
-Seller info
-Delivery address
-Purchase card
-Product details
-Order total
-Payment and shipping status

### Basket 
Inside the basket menu you can see a list of users with a basket.
You can click on the user and see what is in there basket.
You can also see this info via the custom users menu

### catagories
Inside the catagories menu you can see all the catagory options and make new ones if needed

### Products
Inside the products menu you can see a list of all the products listed on the site.

If you click on the product you can update:
-ID
-Title
-Image
-description 
-price
-catagory
-summary 
-quantity 
-featured status
-seller info 
