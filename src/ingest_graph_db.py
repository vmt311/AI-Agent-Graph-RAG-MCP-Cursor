from pymongo import MongoClient
from neo4j import GraphDatabase
import os

# Kết nối MongoDB
mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
mongo = MongoClient(mongo_uri)
db = mongo['smartphones_db']
phones = db['smartphones'].find()

# Kết nối Neo4j
neo4j = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "test12345"))

def create_graph(tx, phone):
    model = phone['model']
    price = phone['price']
    rating = phone['rating']
    sim = phone['sim']
    processor = phone['processor']
    ram = phone['ram']
    battery = phone['battery']
    display = phone['display']
    camera = phone['camera']
    card = phone['card']
    os = phone['os']
    tx.run(
    """
        MERGE (p:Phone {model: $model})
        MERGE (price:Price {value: $price})
        MERGE (rating:Rating {value: $rating})
        MERGE (sim:Sim {value: $sim})
        MERGE (processor:Processor {value: $processor})
        MERGE (ram:RAM {value: $ram})
        MERGE (battery:Battery {value: $battery})
        MERGE (display:Display {value: $display})
        MERGE (camera:Camera {value: $camera})
        MERGE (card:Card {value: $card})
        MERGE (os:OS {value: $os})

        MERGE (p)-[:HAS_PRICE]->(price)
        MERGE (p)-[:HAS_RATING]->(rating)
        MERGE (p)-[:HAS_SIM]->(sim)
        MERGE (p)-[:HAS_PROCESSOR]->(processor)
        MERGE (p)-[:HAS_RAM]->(ram)
        MERGE (p)-[:HAS_BATTERY]->(battery)
        MERGE (p)-[:HAS_DISPLAY]->(display)
        MERGE (p)-[:HAS_CAMERA]->(camera)
        MERGE (p)-[:HAS_CARD]->(card)
        MERGE (p)-[:HAS_OS]->(os)
    """, 
    model=model, 
    price=price, 
    rating=rating, 
    sim=sim, 
    processor=processor, 
    ram=ram, 
    battery=battery, 
    display=display, 
    camera=camera, 
    card=card, 
    os=os)

if __name__ == "__main__":
    # insert data
    with neo4j.session() as session:
        for phone in phones:
            session.execute_write(create_graph, phone)
    
    print("Đã insert dữ liệu vào Neo4j")