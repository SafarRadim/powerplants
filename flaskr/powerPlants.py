from sys import argv
from database import *
from app import *

app = create_app()
app.app_context().push()

# User funcs

def addUser(name):
    user = User(name = name, finance = 0)
    db.session.add(user)

def removeUser(name):
    user = User.query.filter_by(name = name).first()
    db.session.delete(user)

def changeFinanceUser(user, change):
    user = User.query.filter_by(name = user).first()
    user.finance += change
    db.session.merge(user)

def assignPlantUser(user, plantId):
    plant = Plant.query.filter_by(id = plantId).first()
    user = User.query.filter_by(name = user).first()
    plant.owner_id = user.id
    db.session.merge(plant)

# Company funcs

def addCompany(name):
    company = Company(name = name, finance = 0)
    db.session.add(company)

def removeCompany(name):
    company = Company.query.filter_by(name = name).first()
    db.session.delete(company)

def changeFinanceCompany(company, change):
    company = Company.query.filter_by(name = company).first()
    company.finance += change
    db.session.merge(company)

def assignUserCompany(company, user):
    user = User.query.filter_by(name = user).first()
    company = Company.query.filter_by(name = company).first()
    user.company_id = company.id
    db.session.merge(user)

def assignPlantCompany(company, plantId):
    plant = Plant.query.filter_by(id = plantId).first()
    company_obj = Company.query.filter_by(name = company).first()
    plant.company_id = company_obj.id
    db.session.merge(plant)
    print(plant.cost)

# Plant funcs

    # 0 - foto, 1 - water, 2 - heat, 3 - nuclear
def addPlant(type, cost):
    plant = Plant(type = type, cost = cost, age = 0, active = True)
    db.session.add(plant)

def removePlant(id):
    plant = Plant.query.filter_by(id = id).first()
    db.session.delete(plant)

multipliers = [
        [4, 4, 3, 2, -1],
        [0, 1, 2, 3, 4, 4, 3, 2, -1],
        [0, 0, 1, 2, 3, 3, 4, 4, 3, 2, 2, 1, -1],
        [0, 0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 4, 4, 3, 3, 2, 1, 1, 1, -1]
        ]

def advanceYear(plant_id):
    plant = Plant.query.get(plant_id)
    if not plant.active:
      return

    multiplier = multipliers[plant.type][plant.age]
    print(multiplier)
    if (multiplier == -1):
        plant.active = False
        return        

    if plant.owner_id is not None:
        print("owner")
        plant.owner.finance += (plant.cost * multiplier / 10)
        db.session.merge(plant.owner)
    else:
        print("company")
        plant.company.finance += (plant.cost * multiplier / 10)
        db.session.merge(plant.company)

    plant.age += 1
    db.session.merge(plant)

def listPlants():
    plants = Plant.query.all()
    print("ID\ttype\tcost\tage\tactive")
    for plant in plants:
        print("{}\t{}\t{}\t{}\t{}".format(plant.id, plant.type, plant.cost, plant.age, plant.active)) 

# Combo funcs

def transferUserCompany(user, company, amount):
    user = User.query.filter_by(name = user).first()
    company = Company.query.filter_by(name = company).first()
    company.finance += amount
    user.finance -= amount
    db.session.merge(user)
    db.session.merge(company)


# Call tree
def parseArgs():
    if argv[1] == "user":
        if argv[2] == "add":
            addUser(argv[3])
        elif argv[2] == "remove":
            removeUser(argv[3])
        elif argv[2] == "changeFinance":
            changeFinanceUser(argv[3], int(argv[4]))
        elif argv[2] == "assignPlant":
            assignPlantUser(argv[3], argv[4])
        elif argv[2] == "transfer":
            transferUserCompany(argv[3], argv[4], int(argv[5]))
    elif argv[1] == "company":
        if argv[2] == "add":
            addCompany(argv[3])
        elif argv[2] == "remove":
            removeCompany(argv[3])
        elif argv[2] == "changeFinance":
            changeFinanceCompany(argv[3], int(argv[4]))
        elif argv[2] == "assignPlant":
            assignPlantCompany(argv[3], argv[4])
        elif argv[2] == "assignUser":
            assignUserCompany(argv[3], argv[4])
    elif argv[1] == "plant":
        if argv[2] == "add":
            addPlant(argv[3], argv[4])
        elif argv[2] == "remove":
            removePlant(argv[3])
        elif argv[2] == "advance":
            advanceYear(argv[3])
        elif argv[2] == "list":
            listPlants()
    db.session.commit()


# main == main

if __name__ == "__main__":
    parseArgs()
