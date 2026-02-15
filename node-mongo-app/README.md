# Node.js + MongoDB Docker Practical Example 🚀

## 📋 What This Demo Shows

This practical example demonstrates:
1. **MongoDB and Mongo Express running in Docker** (inside Docker network)
2. **Node.js app running locally on your computer** (outside Docker network)
3. **How Node.js (outside) connects to MongoDB (inside Docker)**
4. **How browser accesses both local app and Docker services**
5. **How Docker Compose simplifies setup**

---

## 🎯 The Setup

### What's Running Where:

```
┌─────────────────────────────────────────────────────────┐
│              Your Computer (Outside Docker)             │
│                                                         │
│  ┌──────────────┐         ┌──────────────────────┐    │
│  │   Browser    │         │  Node.js App         │    │
│  │              │         │  (localhost:3000)    │    │
│  └──────┬───────┘         └──────────┬───────────┘    │
│         │                            │                 │
│         │                            │                 │
│         │ Access via                 │ Connects via    │
│         │ localhost:8081             │ localhost:27017 │
│         │ localhost:3000             │                 │
└─────────┼────────────────────────────┼─────────────────┘
          │                            │
          │ Port Binding               │ Port Binding
          │ (8081→8081)                │ (27017→27017)
          ↓                            ↓
┌─────────────────────────────────────────────────────────┐
│         Docker Network (mongo-network)                  │
│         Created by Docker Compose!                      │
│                                                         │
│  ┌──────────────────┐         ┌──────────────────┐    │
│  │  mongo-express   │────────→│      mongo       │    │
│  │    :8081         │         │     :27017       │    │
│  └──────────────────┘         └──────────────────┘    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Key Points:**
- ✅ **MongoDB** runs in Docker (inside network)
- ✅ **Mongo Express** runs in Docker (inside network)
- ✅ **Node.js app** runs on your computer (outside Docker)
- ✅ **Port binding** (`-p 27017:27017`) allows Node.js to connect via `localhost:27017`
- ✅ **Browser** accesses everything via `localhost`

---

## 🚀 Quick Start

### Step 1: Start MongoDB and Mongo Express with Docker Compose
```bash
# Navigate to this directory
cd node-mongo-app

# Start MongoDB and Mongo Express
docker-compose up -d
```

**What this does:**
- ✅ Creates Docker network automatically
- ✅ Starts MongoDB on port 27017
- ✅ Starts Mongo Express on port 8081
- ✅ Both containers can talk to each other inside Docker network
- ✅ Port binding allows external access

### Step 2: Install Node.js Dependencies
```bash
npm install
```

### Step 3: Run Node.js App Locally
```bash
node server.js
```

**Output:**
```
✅ Connected to MongoDB successfully!
📍 MongoDB URL: mongodb://admin:password@localhost:27017/mydb?authSource=admin
🚀 Server running on http://localhost:3000
```

### Step 4: Access the Services

Open your browser:
- **Node.js App**: http://localhost:3000
- **Mongo Express**: http://localhost:8081 (login: admin/pass)

---

## 🔍 How It Works

### Connection Explained:

**Node.js connects to MongoDB using `localhost:27017`:**
```javascript
// In server.js
const MONGO_URL = 'mongodb://admin:password@localhost:27017/mydb?authSource=admin';
//                                          ^^^^^^^^^
//                                    Uses localhost because
//                                    Node.js is OUTSIDE Docker
```

**Why `localhost` works:**
1. MongoDB container exposes port 27017 with `-p 27017:27017`
2. This creates a bridge: `localhost:27017` → `mongo container:27017`
3. Node.js (running on your computer) connects via `localhost:27017`
4. Docker forwards the connection to MongoDB inside the container

**Inside Docker network:**
- Mongo Express connects to MongoDB using container name: `mongo:27017`
- Containers use DNS to resolve container names

---

## 🧪 Testing the Application

### 1. Check Docker Containers:
```bash
docker-compose ps
```

You should see:
```
NAME            IMAGE           STATUS    PORTS
mongo           mongo           Up        0.0.0.0:27017->27017/tcp
mongo-express   mongo-express   Up        0.0.0.0:8081->8081/tcp
```

### 2. Test Node.js App:
Open browser: http://localhost:3000

### 3. Add a User:
Click "Add sample user" or visit: http://localhost:3000/add-user

### 4. View All Users:
Visit: http://localhost:3000/users

### 5. Check MongoDB in Mongo Express:
- Open: http://localhost:8081
- Login: admin / pass
- Navigate to: mydb → users collection
- You'll see the users created by Node.js app!

### 6. View MongoDB Logs:
```bash
docker-compose logs -f mongo
```

---

## 📁 Project Structure

```
node-mongo-app/
├── docker-compose.yml    # Defines MongoDB and Mongo Express
├── package.json          # Node.js dependencies
├── server.js             # Node.js app (runs locally)
├── .dockerignore         # Files to exclude
└── README.md             # This file
```

**Note:** No Dockerfile needed! Node.js runs directly on your computer.

---

## 🎓 Understanding the Difference

### Manual Way (Without Docker Compose):

```bash
# Step 1: Create network manually
docker network create mongo-network

# Step 2: Run MongoDB
docker run -d \
  -p 27017:27017 \
  --network mongo-network \
  --name mongo \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  mongo

# Step 3: Run Mongo Express
docker run -d \
  -p 8081:8081 \
  --network mongo-network \
  --name mongo-express \
  -e ME_CONFIG_MONGODB_ADMINUSERNAME=admin \
  -e ME_CONFIG_MONGODB_ADMINPASSWORD=password \
  -e ME_CONFIG_MONGODB_SERVER=mongo \
  -e ME_CONFIG_BASICAUTH_USERNAME=admin \
  -e ME_CONFIG_BASICAUTH_PASSWORD=pass \
  mongo-express

# Step 4: Run Node.js locally
npm install
node server.js
```

**Problems:**
- ❌ Must create network manually
- ❌ Long docker run commands
- ❌ Easy to make mistakes
- ❌ Hard to remember all the flags

### Docker Compose Way:

```bash
# One command does everything!
docker-compose up -d

# Run Node.js locally
npm install
node server.js
```

**Benefits:**
- ✅ Network created automatically
- ✅ All configuration in one file
- ✅ Easy to share with team
- ✅ Simple to start/stop everything

---

## 🛠️ Useful Commands

### Docker Compose Commands:
```bash
# Start services
docker-compose up -d

# View status
docker-compose ps

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f mongo

# Stop services
docker-compose down

# Stop and remove data
docker-compose down -v
```

### Node.js Commands:
```bash
# Install dependencies
npm install

# Run the app
node server.js

# Stop the app
Ctrl + C
```

---

## 🔑 Key Takeaways

1. **Node.js runs on your computer** (outside Docker)
2. **MongoDB runs in Docker** (inside Docker network)
3. **Port binding** (`-p 27017:27017`) allows Node.js to connect via `localhost:27017`
4. **Inside Docker network**, containers use container names (`mongo`, `mongo-express`)
5. **Outside Docker network**, we use `localhost` + port number
6. **Docker Compose** automates network creation and container management
7. **Browser** accesses both local Node.js app and Docker services via `localhost`

---

## 🎯 Real-World Use Case

This setup is perfect for:
- **Development**: Run databases in Docker, code locally
- **Testing**: Easy to start/stop databases without installing them
- **Team collaboration**: Share docker-compose.yml, everyone has same setup
- **Multiple projects**: Different databases for different projects, no conflicts

---

## 🚀 Next Steps

Try modifying the code:
1. Add more routes to `server.js`
2. Create more MongoDB collections
3. Add more fields to the User schema
4. Experiment with MongoDB queries

---

## 🐛 Troubleshooting

### Can't connect to MongoDB?
```bash
# Check if MongoDB is running
docker-compose ps

# Check MongoDB logs
docker-compose logs mongo

# Make sure port 27017 is not used by another app
netstat -ano | findstr :27017
```

### Mongo Express not loading?
```bash
# Check logs
docker-compose logs mongo-express

# Make sure it's running
docker-compose ps
```

### Node.js connection error?
- Make sure MongoDB is running: `docker-compose ps`
- Check the connection URL in `server.js`
- Verify port 27017 is exposed: `docker-compose ps`

---

**Congratulations! You now understand how applications outside Docker connect to services inside Docker! 🎉**
