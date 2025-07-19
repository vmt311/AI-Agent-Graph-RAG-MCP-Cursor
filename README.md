Dự án graph rag + mcp + cursor

docker-compose up --build

1. Tạo file `.env` trong thư mục gốc dự án, dựa trên file mẫu `.env.example`:
```bash
cp .env.example .env
```
2. Chạy data_preprocessing.py để làm sạch dữ liệu và thêm vào mongodb
3. Chạy ingest_graph_db.py để khởi tạo graph database (Neo4j)
4. Trong cursor, cài đặt mcp-server như sau: (Xem [link](https://www.youtube.com/watch?v=_Qr0WTgR5EM&t=879s) để biết chi tiết)
    ```bash
    {
        "mcpServers": {
            
            "smart_chat": {
            "command": "path/to/file/uv.exe",
            "args": [
                "run",
                "--directory",
                "path/to/project",
                "main.py"
            ],
            "description": "A simple MCP server to query top chatters from a community database"
            }
        }
    }
    ```
5. Kiểm thử với cursor chat

