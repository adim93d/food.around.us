# 🌿 Plant Identifier Web App

Welcome to the **Plant Identifier Web App**! This application allows users to upload 1-5 images of a plant and receive information about its name, edibility, and how to prepare it for consumption.

---

## 🚀 Features
- 📷 Upload 1-5 images of a plant
- 🌱 Identify the plant species
- 🍽️ Determine if the plant is edible
- 📝 Get details on which parts are edible and how to prepare them
- 🔐 User authentication system (CRUD operations for users)
- 🗄️ PostgreSQL database for storing plant and user data
- 📡 FastAPI-based backend with Docker support

---

## 🛠️ Tech Stack
- **Backend**: FastAPI
- **Database**: PostgreSQL
- **Authentication**: JWT (to be added)
- **Deployment**: Docker & Docker Compose
- **ORM**: SQLAlchemy
- **Environment Variables**: Managed with `dotenv`

---

## 📂 Project Structure
```bash
📦 project-root
├── app
│   ├── api
│   │   ├── routers
│   │   │   ├── plant_routes.py  # Plant API
│   │   │   ├── user_routes.py   # User API
│   ├── database
│   │   ├── database.py         # Database configuration
│   │   ├── models.py           # Database models
│   │   ├── schemas.py          # Pydantic schemas
├── main.py                      # FastAPI main app
├── Dockerfile                    # Docker setup
├── docker-compose.yml             # Multi-container setup
├── requirements.txt              # Python dependencies
└── .env                          # Environment variables
```

---

## 📦 Installation & Setup
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/your-repo-name.git
cd your-repo-name
```

### **2️⃣ Set Up Environment Variables**
Create a `.env` file in the root directory and add:
```ini
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_db_name
POSTGRES_HOST=db
POSTGRES_PORT=5432
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=admin_password
```

### **3️⃣ Build and Run the Application with Docker**
```sh
docker-compose up --build -d
```

This will:
- Start a PostgreSQL database
- Start the FastAPI backend
- Start pgAdmin for database management

---

## 🔥 Usage
### **API Documentation**
Once the app is running, you can access the interactive API documentation at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### **User Endpoints**
- Create a user: `POST /users/`
- Get all users: `GET /users/`
- Get a user by ID: `GET /users/{user_id}`
- Update a user: `PUT /users/{user_id}`
- Delete a user: `DELETE /users/{user_id}`

### **Plant Endpoints**
- Upload plant images & identify: `POST /plants/`
- Get all plants: `GET /plants/`
- Get plant by ID: `GET /plants/{plant_id}`
- Update plant info: `PUT /plants/{plant_id}`
- Delete a plant: `DELETE /plants/{plant_id}`

---

## 🛠️ Development Mode (Without Docker)
1. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
2. **Run the application**
   ```sh
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

---

## 🤝 Contributing
We welcome contributions! Feel free to submit an issue or a pull request.

---

## 📜 License
This project is licensed under the MIT License.

---

🌱 **Happy Plant Identifying!** 🌿
