from datetime import datetime

class Order:
    def __init__(self, number, day, month, year, device, problemtype, description, client, status):
        self.number = number
        self.startDate = datetime(year,month,day)
        self.endDate = None
        self.device = device
        self.problemtype = problemtype
        self.description = description
        self.client = client
        self.status = status
        self.master = "Не назначен"
        self.comments = []

from fastapi import Body, FastAPI
 
repo = [
    Order(1,24,5,2024,"Cyber","Телефон","Leni","Misha","Обнулён"),
    Order(2,21,4,2024,"Noga","Экран","Leni","Lexa","Обнулён"),
    Order(3,20,3,2024,"Ryka","Рука","Leni","Kirill","Обнулён")
] 
 
for order in repo:
    order.endDate = datetime.now()
    order.status ="завершено"
 
app = FastAPI()
 
isUpdatedStatus = False
massage = ""
 
@app.get("/")
def get_orders():
    global isUpdatedStatus
    global massage
    if(isUpdatedStatus):
        buffer = massage
        isUpdatedStatus = False
        massage = ""
        return repo, buffer
    else:
        return repo

@app.post("/")
def create_order(data = Body()):
    order = Order(
        data["number"],                
        data["day"],        
        data["month"],        
        data["year"],        
        data["device"],        
        data["problemtype"],        
        data["description"],        
        data["client"],        
        data["status"],
       
    )
    repo.append(order)
    return order

@app.put("/{number}")
def update_order(number,dto = Body()):
    global isUpdatedStatus
    global massage
    isEmpty = True
    for order in repo:
        if order.number == int(number):
            isEmpty = False
            if(order.status != dto["status"]):
                order.status = dto["status"]
                isUpdatedStatus = True
                massage += "Статус заявки номер " + str(order.number) + " изменён\n"
                if order.status == "завершено":
                    order.endDate == datetime.now()            
            if (order.description != dto["description"]):
                order.description = dto["description"]
            if (order.master != dto["master"]):
                order.master = dto["master"]
            if (dto["comment"] != None):
                order.comments.append(dto["comment"])
            return order
    if isEmpty:
        return "Нет такого"

@app.get("/filter/{param}")
def getByNum(param):
    return [Order for Order in repo if
        Order.device == param or
        Order.problemtype == param or
        Order.description == param or
        Order.client == param or
        Order.status == param or   
        Order.master == param]

@app.get("/stat/completeCount")
def complete_count():
    return len(complete_orders())

@app.get("/stat/problemTypes")
def problem_types():
    result = {}
    for order in repo:
        if order.problemtype in result:
            result[order.problemtype] += 1
        else:
            result[order.problemtype] = 1
    return result

@app.get("/stat/avr")
def average_time():
    completed = complete_orders()
    times = []
    for order in completed:
        times.append(order.endDate-order.startDate)
    timesSum = sum([t.days for t in times])
    ordCount = complete_count()
    result = timesSum/ordCount
    return result

def complete_orders():
    return [order for order in repo if order.status == "завершено"]