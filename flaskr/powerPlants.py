#!/usr/bin/env python3

from sys import argv
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
    plant = Plant.query.get(plantId)
    user = User.query.filter_by(name = user).first()
    plant.owner_id = user.id
    user.finance -= plant.cost
    db.session.merge(plant)

def listUsers():
    users = User.query.all()
    print("{:<5}{:<10}{:<5}{}".format("ID", "Name", "C_ID", "Finance"))
    for user in users:
        print("{:<5}{:<10}{:<5}{}".format(user.id, user.name, str(user.company_id), user.finance))

# Company funcs

def addCompany(name):
    company = Company(name = name, finance = 0)
    db.session.add(company)

def removeCompany(name):
    company = Company.query.filter_by(name = name).first()
    db.session.delete(company)

def changeFinanceCompany(companyId, change):
    company = Company.query.get(companyId)
    company.finance += change
    db.session.merge(company)

def assignUserCompany(companyId, user):
    user = User.query.filter_by(name = user).first()
    company = Company.query.get(companyId)
    user.company_id = company.id
    db.session.merge(user)

def assignPlantCompany(companyId, plantId):
    plant = Plant.query.get(plantId)
    company = Company.query.get(companyId)
    plant.company_id = company.id
    company.finance -= plant.cost
    db.session.merge(plant)

def listCompanies():
    companies = Company.query.all()
    print("{:<5}{:<25}{}".format("ID", "Name", "Finance"))
    for company in companies:
        print("{:<5}{:<25}{}".format(company.id, company.name, company.finance))


# Plant funcs

    # 0 - foto, 1 - water, 2 - heat, 3 - nuclear
def addPlant(type, cost):
    plant = Plant(type = type, cost = cost, age = 0, active = True)
    db.session.add(plant)
    print(plant.id)

def removePlant(plantId):
    plant = Plant.query.get(plantId)
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
    print("{:<5}{:<5}{:<6}{:<5}{}".format("ID", "Type", "Cost", "Age", "Active"))
    for plant in plants:
        print("{:<5}{:<5}{:<6}{:<5}{}".format(plant.id, plant.type, plant.cost, plant.age, plant.active)) 

# Combo funcs

def transferUserCompany(user, companyId, amount):
    user = User.query.filter_by(name = user).first()
    company = Company.query.get(companyId)
    company.finance += amount
    user.finance -= amount
    db.session.merge(user)
    db.session.merge(company)

def transferUserCurrentCompany(user, amount):
    user = User.query.filter_by(name = user).first()
    user.finance -= amount
    user.company.finance += amount
    db.session.merge(user)
    db.session.merge(user.company)

def buyPlantCompany(company_id, plant_type, plant_cost):
    plant = Plant(type = plant_type, cost = plant_cost, age = 0, active = True)
    plant.company_id = company_id
    db.session.add(plant)
    company = Company.query.get(company_id)
    company.finance -= plant_cost

def buyPlantUser(user, plant_type, plant_cost):
    plant = Plant(type = plant_type, cost = plant_cost, age = 0, active = True)
    user = User.query.filter_by(name = user).first()
    plant.user_id = user.id
    user.finance -= plant_cost
    db.session.add(plant)

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
            if len(argv) == 6:
                transferUserCompany(argv[3], argv[4], int(argv[5]))
            else:
                transferUserCurrentCompany(argv[3], int(argv[4]))
        elif argv[2] == "buy":
            buyPlantUser(argv[3], int(argv[4]), int(argv[5]))
        elif argv[2] == "list":
            listUsers()
        else:
            print("I dont know what {} is".format(argv[2]))
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
        elif argv[2] == "buy":
            buyPlantCompany(argv[3], int(argv[4]), int(argv[5]))
        elif argv[2] == "list":
            listCompanies()
        else:
            print("I dont know what {} is".format(argv[2]))
    elif argv[1] == "plant":
        if argv[2] == "add":
            addPlant(argv[3], argv[4])
        elif argv[2] == "remove":
            removePlant(argv[3])
        elif argv[2] == "advance":
            advanceYear(argv[3])
        elif argv[2] == "list":
            listPlants()
        else:
            print("I dont know what {} is".format(argv[2]))
    else:
        print("I dont know what {} is".format(argv[1]))
    db.session.commit()


# __name__:== main
if __name__ == "__main__":
    parseArgs()
