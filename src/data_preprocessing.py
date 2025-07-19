import os
import pandas as pd
from pymongo import MongoClient

def load_and_clean_data():
    # Lấy thư mục chứa file script hiện tại
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Xây dựng đường dẫn tới file dữ liệu
    data_path = os.path.join(current_dir, '..', 'smartphones_data', 'smartphones - smartphones.csv')

    # Đọc file dữ liệu
    df = pd.read_csv(data_path)
    

    # Làm sạch dữ liệu
    df['price'] = df['price'].str.replace('₹', '').str.replace(',', '').astype(float)
    df['rating'] = df['rating'].fillna(0)
    df = df.fillna('unknown')
    
    # Kết nối MongoDB từ biến môi trường
    mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
    client = MongoClient(mongo_uri)
    db = client['smartphones_db']
    collection = db['smartphones']

    # Xóa dữ liệu cũ và insert dữ liệu mới
    collection.delete_many({})
    collection.insert_many(df.to_dict(orient='records'))

    print(f"Đã insert {len(df)} bản ghi vào MongoDB")

if __name__ == "__main__":
    load_and_clean_data()


