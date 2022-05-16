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
>pip install -r requirements.txt

This will install the necassary packages for Django Marketplace to run:
django == 4.0.4
stripe == 3.0.0
pillow == 9.1.0

Next cd into django_markplace\django_marketplace and run:
>python manage.py runserver 

Finally navigate to http://127.0.0.1:8000 in your browser to view Django market place.