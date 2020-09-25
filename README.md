# OnlineFarmerMarket

OnlineFarmerMarket is a Django application that allows a farm to offer its products for direct saling. 
Customers can browse a product catalog, add products to their cart and order depending to the available withdrawal slots.
Several options are available : withdrawal, lockers or delivery.

To download app project :

- In a local folder, create a virtual environment and activate it.
  In Ubuntu you can do that by the following commands :
  - sudo apt install virtualenv
  - virtualenv env -p python3
  - source env/bin/activate
  

- Make sure you have PostgreSQL on your device. If not, please, install it.


- In postgresSQL, create a DATABASE with the user of your choice.


- fork and clone this repository in your local folder


- install requirements for this app with the command : pip install -r OnlineFarmerMarket/requirements.txt


- In OnlineFarmerMarket/marche_en_ligne/settings/__ init __.py, you 'll have to change 'NAME' and 'USER' in 'DATABASES' configuration :
  - 'NAME': 'name of your created database',
  - 'USER': 'name of the user in postgreSQL',

- Now, make sure you're in OnlineFarmerMarket directory in your console and type :
  - ' ./manage.py migrate '
  - ' ./manage.py loaddata store/dumps/db.json ' to load initial dataset into your database
  
  - You can run the app in development mode with ' ./manage.py runserver '
