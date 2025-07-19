# Sử dụng Python slim
FROM python:3.13.5

# Cài uv
RUN pip install uv

# Tạo thư mục làm việc
WORKDIR /app

# # Copy toàn bộ project vào container
# COPY . .

# Copy lock files để cài package sớm
COPY pyproject.toml uv.lock ./

# Cài đặt uv nếu bạn dùng lock file
RUN uv sync

# Nếu bạn dùng requirements.txt
# RUN pip install -r requirements.txt


# Khởi động app (ví dụ main.py)
CMD ["python", "main.py"]
