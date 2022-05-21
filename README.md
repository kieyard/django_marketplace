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

