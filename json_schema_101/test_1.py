from jsonschema import validate

schema = {
    "type" : "object",
    "properties" : {
        "price" : {"type" : "number"},
        "name" : {"type" : "string"},
    },
}
# content of test_sample.py
def func(x):
    return x + 1


def test_answer():
    assert func(3) == 4
    

def test_validate():
    assert validate_wrapper(instance={"name" : "Eggs", "price" : 34.99}, schema=test_answer)) == True
    

def test_validate_fail():
    assert validate_wrapper(instance={"name" : "Eggs", "price" : "ciao"}, schema=test_answer)) == False
    
def validate_wrapper(instance, schema):
    try:
        validate(instance = schema, schema = schema)
        return True #None -> True
    except:
        return False #errore -> False