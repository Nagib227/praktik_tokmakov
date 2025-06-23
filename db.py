from tinydb import TinyDB, Query


PATH = "db/db.json"


def create_db():
    open(PATH, 'w').close()
    db = TinyDB(PATH)
        
    db.insert({ 
        "name": "Test1", 
        "username": "text", 
        "email": "email" 
    })
    db.insert({ 
        "name": "Test2", 
        "username": "text", 
        "phone": "phone" 
    })
    db.insert({ 
        "name": "Test3", 
        "username": "text",
        "date": "date" 
    })
    return 


def find_matching_patterns(template):
    db = TinyDB(PATH)
    Pattern = Query()
    
    query = None
    
    for key, template_value in template.items():
        condition = (
            Pattern[key].exists() & 
            (Pattern[key] == template_value)
            )
        if query is None:
            query = condition
        else:
            query &= condition
    
    results = db.search(query) if query is not None else db.all()
    db.close()
    return results



if __name__ == "__main__":
    create_db()
