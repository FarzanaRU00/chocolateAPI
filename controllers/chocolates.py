from werkzeug.exceptions import BadRequest

chocolates = [
    {"id": 1, "name": "Snickers", "country": "American"},
    {"id": 2, "name": "Fruit and Nut", "country": "British"},
    {"id": 3, "name": "Kinder Bueno", "country": "Italian"}
]

def index(req):
    return [c for c in chocolates], 200

def create(req):
    new_chocolate = req.get_json()
    new_chocolate['id'] = sorted([c['id'] for c in chocolates]) [-1] +1
    chocolates.append(new_chocolate)
    return new_chocolate, 201

def show(req, id):
    return find_by_id(id), 200

def show_by_country(req, country):
    country = country.lower()
    return find_by_country(country), 200

def update(req, id):
    chocolate = find_by_id(id)
    data = req.get_json()
    print(data)
    for key, val in data.items():
        chocolate[key] = val
    return chocolate, 200

def destroy(req, id):
    chocolate = find_by_id(id)
    chocolate.remove(chocolate)
    return chocolate, 204

def find_by_id(id):
    try:
        return next(chocolate for chocolate in chocolates if chocolate['id'] == id)
    except:
        raise BadRequest(f"No chocolate with id {id} found!")

def find_by_country(country):
    try:
        return next(chocolate for chocolate in chocolates if chocolate['country'] == country)
    except:
        raise BadRequest(f"We don't have a chocolate from {country}")