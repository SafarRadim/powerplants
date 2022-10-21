# Powerplants  
A flask app to support my small project to encourage attendance in my freetime 
thing.  
Is it pretty? No.  
Does it work? Kinda.  
Do I try to upgrade it over time? Definitely.  

## Install  
The `install.sh` script creates virtual env for the app and pip-s all the required libraries.  
Then you just need to link the database to the app:
```
python3  
from app import db  
db.create_all()
```
