# **Plan API** 

**Plan API** is a Flask-based REST API that allows users to store, retrieve, update, and delete plan records efficiently. It is backed by **MongoDB** as a key-value store and follows RESTful best practices for structured JSON data handling.

---

## **⚡ Features**
- **CRUD operations**: Create, Read, Update, and Delete plans  
- **JSON-based key-value storage** using **MongoDB**  
- **Schema validation** to ensure structured data  
- **Versioned API** (`/api/v1/`) for future enhancements  

---

## ** Prerequisites**
Ensure you have the following installed before running the application:  
1. **Python 3.8+**  
2. **MongoDB 8** (Installation guide below)  
3. **Virtual environment (venv)** for package management  

---

## ** Step 1: Install MongoDB**
To install MongoDB **on macOS**, follow the official guide:  
🔗 [MongoDB Installation for macOS](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x/)  

Or install MongoDB using **Homebrew**:  
```sh
brew tap mongodb/brew
brew install mongodb-community@8.0
```
To start MongoDB, run:  
```sh
brew services start mongodb-community@8.0
```
Verify MongoDB is running:  
```sh
mongosh
```

Create Database:  
```sh
use plan_api_db (Or any name you'd like)
```

---

## ** Step 2: Set Up and Run the Flask Application**
### **1️⃣ Clone the Repository**
```sh
git clone <your-repo-url>
cd plan-api
```

### ** Create a Virtual Environment**
```sh
python3 -m venv venv
source venv/bin/activate  # For Mac/Linux
venv\Scripts\activate  # For Windows
```

### ** Install Dependencies**
```sh
pip install -r requirements.txt
```

### ** Configure MongoDB Connection**
Ensure MongoDB is **running locally** on `mongodb://localhost:27017`. You can modify database settings in **config.py** if needed.

### ** Run the Flask Application**
```sh
python3 run.py
```

---

## ** API Endpoints**
| Method | Endpoint | Description |
|--------|---------|-------------|
| **POST** | `/api/v1/plans` | Store a new plan |
| **GET** | `/api/v1/plans/{plan_id}` | Retrieve a plan |
| **DELETE** | `/api/v1/plans/{plan_id}` | Delete a plan |
| **PATCH** | `/api/v1/plans/{plan_id}` | Update a plan conditionally |

Example **POST** request:
```json
{
    "planCostShares": {
        "deductible": 2000,
        "_org": "example.com",
        "copay": 23,
        "objectId": "1234vxc2324sdf-501",
        "objectType": "membercostshare"
    },
    "linkedPlanServices": [
        {
            "linkedService": {
                "_org": "example.com",
                "objectId": "1234520xvc30asdf-502",
                "objectType": "service",
                "name": "Yearly physical"
            },
            "planserviceCostShares": {
                "deductible": 10,
                "_org": "example.com",
                "copay": 0,
                "objectId": "1234512xvc1314asdfs-503",
                "objectType": "membercostshare"
            },
            "_org": "example.com",
            "objectId": "27283xvx9asdff-504",
            "objectType": "planservice"
        }
    ],
    "_org": "example.com",
    "objectId": "12xvxc345ssdsds-508",
    "objectType": "plan",
    "planType": "inNetwork",
    "creationDate": "12-12-2017"
}
```

---

## ** Testing the API**
Use **Postman** or **cURL** to test the API.  

Example **GET request using cURL**:
```sh
curl -X GET http://127.0.0.1:8000/api/v1/plans/12xvxc345ssdsds-508
```

---

## ** Contributors**
Feel free to fork and contribute! 🚀

---

