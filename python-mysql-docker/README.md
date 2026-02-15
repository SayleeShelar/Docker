# Python + MySQL Docker Example 🐍🐳

## 🎯 What Are We Building?

A **super simple** example to understand Docker networking:

- **Part 1 (Outside Docker)**: Python script running on your computer
- **Part 2 (Inside Docker)**: MySQL database running in a Docker container

This shows how applications **outside Docker** connect to services **inside Docker**.

---

## 🤔 Why This Example?

### Real-World Scenario:
When you're developing:
- You write code on your computer (Python, Node.js, Java, etc.)
- You don't want to install databases (MySQL, MongoDB, PostgreSQL) on your computer
- **Solution**: Run databases in Docker, code runs locally!

### Benefits:
✅ **No installation mess** - Don't install MySQL on your computer  
✅ **Easy cleanup** - Delete container, database is gone  
✅ **Multiple projects** - Different databases for different projects  
✅ **Team consistency** - Everyone uses same database version  
✅ **Quick start** - One command to start database  

---

## 📊 The Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Your Computer (Outside Docker)             │
│                                                         │
│              ┌──────────────────────────┐              │
│              │   Python Script          │              │
│              │   (app.py)               │              │
│              └──────────┬───────────────┘              │
│                         │                               │
│                         │ Connects to                   │
│                         │ localhost:3306                │
│                         │                               │
└─────────────────────────┼───────────────────────────────┘
                          │
                          │ Port Binding
                          │ (-p 3306:3306)
                          ↓
┌─────────────────────────────────────────────────────────┐
│              Docker Network                             │
│                                                         │
│              ┌──────────────────────────┐              │
│              │   MySQL Container        │              │
│              │   Port: 3306             │              │
│              └──────────────────────────┘              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🔍 Understanding Each Part

### Part 1: Python Script (app.py)

**What it does:**
- Runs on your computer (not in Docker)
- Connects to MySQL database
- Creates a table
- Inserts data
- Reads data

**Why localhost?**
```python
connection = mysql.connector.connect(
    host='localhost',      # ← Why localhost?
    port=3306,
    user='root',
    password='rootpassword',
    database='testdb'
)
```

**Answer:** 
- Python is running **outside Docker** on your computer
- MySQL is running **inside Docker** 
- Port binding `-p 3306:3306` creates a bridge
- Your computer's `localhost:3306` → MySQL container's port 3306
- So Python uses `localhost:3306` to connect!

---

### Part 2: Docker Compose (docker-compose.yml)

**What it does:**
- Defines MySQL container
- Exposes port 3306
- Sets up database credentials
- Creates persistent storage

**Let's break it down:**

```yaml
version: '3.8'              # Docker Compose version

services:                   # List of containers to run
  mysql:                    # Service name (you choose this)
    image: mysql:8.0        # Use official MySQL 8.0 image
    container_name: mysql-db  # Container name (optional)
    ports:
      - "3306:3306"         # Port binding: YOUR_COMPUTER:CONTAINER
    environment:            # Environment variables
      MYSQL_ROOT_PASSWORD: rootpassword  # MySQL root password
      MYSQL_DATABASE: testdb             # Create this database
    volumes:
      - mysql-data:/var/lib/mysql  # Persist data

volumes:
  mysql-data:               # Named volume for data persistence
```

**Why each part?**

1. **`image: mysql:8.0`**
   - Downloads MySQL 8.0 from Docker Hub
   - No need to install MySQL on your computer!

2. **`ports: - "3306:3306"`**
   - **Left side (3306)**: Port on your computer
   - **Right side (3306)**: Port inside container
   - Creates bridge so Python can connect via `localhost:3306`

3. **`environment:`**
   - Sets MySQL password and creates database
   - Like running `CREATE DATABASE testdb;` automatically

4. **`volumes:`**
   - Saves data even after container stops
   - Without this, data is lost when container is deleted

---

## 🚀 Step-by-Step Guide

### Step 1: Start MySQL with Docker Compose

```bash
# Navigate to project folder
cd python-mysql-docker

# Start MySQL container
docker-compose up -d
```

**What happens:**
1. ✅ Docker downloads MySQL image (if not already downloaded)
2. ✅ Creates a container named `mysql-db`
3. ✅ Starts MySQL on port 3306
4. ✅ Creates database `testdb`
5. ✅ Sets root password to `rootpassword`
6. ✅ Creates volume for data persistence

**Check if it's running:**
```bash
docker-compose ps
```

You should see:
```
NAME       IMAGE       STATUS    PORTS
mysql-db   mysql:8.0   Up        0.0.0.0:3306->3306/tcp
```

---

### Step 2: Install Python Dependencies

```bash
# Install MySQL connector
pip install -r requirements.txt
```

**What this does:**
- Installs `mysql-connector-python` library
- Allows Python to talk to MySQL

---

### Step 3: Run Python Script

```bash
python app.py
```

**Expected Output:**
```
🐍 Python Script (Running on your computer)
🐳 MySQL Database (Running in Docker)
==================================================
✅ Successfully connected to MySQL database!
📍 MySQL Server version: 8.0.35
✅ Table 'users' created successfully!
✅ Inserted user: Alice

📊 All users in database:
--------------------------------------------------
ID: 1, Name: Alice, Email: alice@example.com
--------------------------------------------------

✅ MySQL connection closed
```

---

### Step 4: Verify Data Persists

**Stop and restart MySQL:**
```bash
docker-compose down
docker-compose up -d
```

**Run Python script again:**
```bash
python app.py
```

**You'll see:**
- Alice is still there! (Data persisted)
- A new Alice is added (script inserts data each time)

---

## 🔑 Key Concepts Explained

### 1. Port Binding (`-p 3306:3306`)

**Without port binding:**
```
Your Computer          Docker Network
     ❌ ──────────────→  MySQL :3306
   (Can't connect!)
```

**With port binding:**
```
Your Computer          Docker Network
localhost:3306 ──────→  MySQL :3306
     ✅ (Connected!)
```

**How it works:**
1. MySQL runs inside Docker on port 3306
2. Docker maps your computer's port 3306 to container's port 3306
3. Python connects to `localhost:3306`
4. Docker forwards connection to MySQL container
5. MySQL responds back through the same path

---

### 2. Why Docker Compose?

**Without Docker Compose (Manual way):**
```bash
# Create volume
docker volume create mysql-data

# Run MySQL
docker run -d \
  --name mysql-db \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=rootpassword \
  -e MYSQL_DATABASE=testdb \
  -v mysql-data:/var/lib/mysql \
  mysql:8.0
```

**Problems:**
- ❌ Long command to remember
- ❌ Easy to make mistakes
- ❌ Hard to share with team
- ❌ Must remember all flags

**With Docker Compose:**
```bash
docker-compose up -d
```

**Benefits:**
- ✅ One simple command
- ✅ All config in one file
- ✅ Easy to share (just share docker-compose.yml)
- ✅ Version control friendly
- ✅ Easy to modify

---

### 3. Data Persistence (Volumes)

**Without volumes:**
```bash
docker-compose down    # Data is LOST! ❌
```

**With volumes:**
```bash
docker-compose down    # Data is SAVED! ✅
docker-compose up -d   # Data is still there!
```

**How it works:**
- Docker stores data in a special location on your computer
- Even if container is deleted, data remains
- Next container uses the same data

---

## 🧪 Experiment & Learn

### Experiment 1: Check MySQL Directly

```bash
# Connect to MySQL container
docker exec -it mysql-db mysql -uroot -prootpassword testdb

# Inside MySQL, run:
SELECT * FROM users;

# Exit MySQL
exit
```

### Experiment 2: View Logs

```bash
# See what MySQL is doing
docker-compose logs -f mysql
```

### Experiment 3: Stop Everything

```bash
# Stop MySQL (data persists)
docker-compose down

# Stop MySQL and delete data
docker-compose down -v
```

---

## 📁 Project Structure

```
python-mysql-docker/
├── docker-compose.yml    # Defines MySQL container
├── app.py                # Python script (runs locally)
└── requirements.txt      # Python dependencies
```

**Note:** No Dockerfile! Python runs on your computer, not in Docker.

---

## 🎓 What You Learned

1. ✅ **Port Binding** - How to connect from outside Docker to inside Docker
2. ✅ **Docker Compose** - Easy way to manage containers
3. ✅ **Volumes** - How to persist data
4. ✅ **Environment Variables** - How to configure containers
5. ✅ **Real-world workflow** - Code locally, database in Docker

---

## 🐛 Troubleshooting

### Error: "Can't connect to MySQL server"

**Check if MySQL is running:**
```bash
docker-compose ps
```

**Check MySQL logs:**
```bash
docker-compose logs mysql
```

**Wait a few seconds:**
MySQL takes 10-20 seconds to start. Try again!

---

### Error: "Port 3306 already in use"

**Solution 1: Stop local MySQL**
```bash
# Windows
net stop MySQL80

# Mac/Linux
sudo service mysql stop
```

**Solution 2: Use different port**
```yaml
ports:
  - "3307:3306"  # Use 3307 on your computer
```

Then in Python:
```python
port=3307  # Change to 3307
```

---

### Error: "Access denied for user 'root'"

**Check password in docker-compose.yml:**
```yaml
MYSQL_ROOT_PASSWORD: rootpassword
```

**Make sure Python uses same password:**
```python
password='rootpassword'
```

---

## 🚀 Quick Start (TL;DR)

```bash
# 1. Start MySQL
docker-compose up -d

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Run Python script
python app.py

# 4. Stop MySQL
docker-compose down
```

---

## 🎯 Next Steps

Try modifying the code:
1. Add more columns to the users table
2. Create a new table
3. Add UPDATE and DELETE operations
4. Try connecting with a GUI tool (MySQL Workbench)

---

## 💡 Key Takeaway

**This is how real developers work:**
- Write code on your computer (fast, easy to debug)
- Run databases in Docker (clean, isolated, easy to manage)
- Port binding connects them together!

**No need to install MySQL, PostgreSQL, MongoDB, Redis on your computer!**
**Just use Docker! 🐳**

---

**Congratulations! You now understand Docker networking and Docker Compose! 🎉**
