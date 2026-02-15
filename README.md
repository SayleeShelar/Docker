# Docker Revision Guide 🐳

## What is Docker?
Think of Docker as a **shipping container for your code**. Just like shipping containers standardize how goods are transported, Docker containers package your app with everything it needs to run anywhere.

---

## 🏗️ Docker Architecture Explained

### The Big Picture
Think of Docker like a **car**:
- **Docker CLI** = Steering wheel (what you control)
- **Docker Engine** = The entire car
- **dockerd** = The engine (does the work)
- **containerd** = Transmission (manages containers)
- **Dockerfile** = Blueprint to build your car

### Components Breakdown

**1. Dockerfile 📄**
- Text file with instructions to build an image
- Like a recipe for cooking
- You write it to define what goes into your container

```dockerfile
FROM node:18-alpine          # Start with base
WORKDIR /app                 # Set workspace
COPY package*.json ./        # Copy files
RUN npm install              # Install dependencies
COPY . .                     # Copy source code
EXPOSE 3000                  # Document port
CMD ["npm", "start"]         # Start command
```

**2. Docker CLI 💻**
- The commands you type (`docker run`, `docker ps`, etc.)
- Your interface to talk to Docker
- Sends commands to dockerd

**3. dockerd (Docker Daemon) 🔧**
- Background service that does the actual work
- Listens to Docker CLI commands
- Manages images, containers, networks, volumes
- You never interact with it directly

**4. containerd 📦**
- Low-level container runtime
- Actually creates and runs containers
- Manages container lifecycle (start, stop, pause)

**5. Docker Engine 🚂**
- The complete package (CLI + dockerd + containerd)
- Everything needed to run Docker

### How They Work Together 🔄

```
You type command
      ↓
Docker CLI (receives your command)
      ↓
dockerd (processes request)
      ↓
containerd (manages container)
      ↓
Container runs!
```

**Example Flow:**
```bash
docker run -d -p 8080:80 nginx
```
1. You type the command
2. Docker CLI sends it to dockerd
3. dockerd checks if nginx image exists
4. dockerd tells containerd to create container
5. containerd starts the container
6. Container runs nginx

| Component | What It Is | What You Do |
|-----------|-----------|-------------|
| **Dockerfile** | Recipe/Blueprint | Write it |
| **Docker CLI** | Your commands | Use it daily |
| **dockerd** | Background worker | Runs automatically |
| **containerd** | Container manager | Runs automatically |
| **Docker Engine** | Complete system | Install once |

---

## 📊 Docker Lifecycle Flowcharts

### Flow 1: Dockerfile → Image → Container

```
Dockerfile (recipe)  →  docker build  →  Image (template)  →  docker run  →  Container (running app)
     📄                      🔨                  📦                   ▶️              🚀
```

**Detailed Flow:**
```
1. Write Dockerfile
        ↓
2. docker build -t myapp .
        ↓
3. Image created (myapp)
        ↓
4. docker run -d -p 8080:80 myapp
        ↓
5. Container running!
```

### Flow 2: Complete Docker Workflow

```
┌─────────────┐
│  Dockerfile │  (You write this)
└──────┬──────┘
       │
       │ docker build -t myapp .
       ↓
┌─────────────┐
│    Image    │  (Template/Blueprint)
└──────┬──────┘
       │
       │ docker run -d -p 8080:80 --name app myapp
       ↓
┌─────────────┐
│  Container  │  (Running application)
└──────┬──────┘
       │
       ├→ docker logs app      (View logs)
       ├→ docker exec -it app bash  (Get inside)
       ├→ docker stop app     (Stop it)
       └→ docker rm app       (Remove it)
```

### Flow 3: Image Sources

```
Option 1: Docker Hub          Option 2: Build Your Own
       ↓                              ↓
  docker pull nginx            docker build -t myapp .
       ↓                              ↓
   Image (nginx)                 Image (myapp)
       ↓                              ↓
  docker run nginx             docker run myapp
       ↓                              ↓
   Container                      Container
```

---

## 🎯 The Docker Workflow (Start Here!)

### Step 1: Get an Image
```bash
docker pull nginx                # Download nginx from Docker Hub
docker images                    # See all downloaded images
```

### Step 2: Run a Container
```bash
# Basic run
docker run nginx                 # Runs but blocks terminal

# Better: Run in background with name
docker run -d --name myapp nginx

# Best: With port binding + auto-cleanup
docker run -d --rm --name myapp -p 8080:80 nginx
```
**Now visit:** `http://localhost:8080` 🎉

### Step 3: Check What's Running
```bash
docker ps                        # Running containers
docker ps -a                     # All containers (including stopped)
```

### Step 4: See What's Happening Inside
```bash
docker logs myapp                # View logs
docker logs -f myapp             # Follow logs live (like tail -f)
docker inspect myapp             # Detailed container info (JSON)
```

### Step 5: Interact with Container
```bash
docker exec -it myapp bash       # Jump inside container
docker exec -it myapp sh         # Use sh if bash not available
```

### Step 6: Stop & Clean Up
```bash
docker stop myapp                # Graceful stop
docker rm myapp                  # Remove stopped container
docker rm -f myapp               # Force remove (stop + remove)
```

---

## 🔑 Essential Commands (Memorize These!)

> **Pro Tip:** Don't stress about memorizing everything! Use `docker --help` or `docker <command> --help` anytime.

```bash
docker --help                    # See all commands
docker run --help                # Help for specific command
docker ps --help                 # Help for ps command
```

### The Big 5 (Most Used)
```bash
docker ps                        # What's running?
docker logs <name>               # What's happening?
docker exec -it <name> bash      # Get inside
docker stop <name>               # Stop it
docker rm -f <name>              # Delete it
```

### Container Lifecycle
```bash
# Create & Start
docker run -d --name web nginx

# Stop & Start
docker stop web
docker start web
docker restart web

# Remove
docker rm web                    # Remove stopped container
docker rm -f web                 # Force remove running container
```

### Port Binding (Critical!)

**Why Port Binding?**
Containers run in an isolated Docker network. Your browser/apps on your computer can't directly access them. Port binding creates a "bridge" between your computer and the container.

**Think of it like this:**
- Container is a house with address `172.17.0.2:80` (inside Docker network)
- Your browser is outside and can't reach that address
- Port binding `-p 8080:80` creates a door at `localhost:8080` that forwards to the container's port 80

```
Your Browser (localhost:8080)
        ↓
   Port Binding (-p 8080:80)
        ↓
Container (172.17.0.2:80)
```

**How it works:**
```bash
# Format: -p HOST_PORT:CONTAINER_PORT
docker run -d -p 8080:80 --name web nginx

# What happens:
# 1. Container runs nginx on port 80 (inside Docker network)
# 2. Docker maps your computer's port 8080 to container's port 80
# 3. You access localhost:8080 in browser
# 4. Docker forwards request to container's port 80
# 5. Container responds back through the same path
```

**Examples:**
```bash
docker run -d -p 8080:80 --name web nginx     # Access via localhost:8080
docker run -d -p 3000:3000 --name app node    # Port 3000 to 3000
docker run -d -p 80:80 --name site nginx      # Port 80 to 80
```

**Without port binding:**
```bash
docker run -d --name web nginx               # ❌ Can't access from browser!
# Container runs but isolated in Docker network
```

**With port binding:**
```bash
docker run -d -p 8080:80 --name web nginx    # ✅ Access at localhost:8080
# Bridge created between your computer and container
```

### Flags You'll Use Daily
```bash
-d                               # Detached (background)
--name myapp                     # Give it a name
-p 8080:80                       # Port mapping
--rm                             # Auto-remove when stopped
-it                              # Interactive terminal
-v /host:/container              # Volume mount
-e KEY=value                     # Environment variable
```

---

## 📊 Container Status Explained

| Status | Meaning | What to Do |
|--------|---------|------------|
| **Up** | Running normally | ✅ All good |
| **Exited** | Stopped/crashed | Check logs: `docker logs <name>` |
| **Created** | Not started yet | Run: `docker start <name>` |
| **Restarting** | Keeps crashing | Check logs, fix issue |

---

## 🏗️ Working with Images

### Download & Manage
```bash
docker pull nginx                # Download image
docker pull nginx:1.25           # Specific version
docker images                    # List all images
docker rmi nginx                 # Remove image
docker rmi -f nginx              # Force remove
```

### Build Your Own
```bash
docker build -t myapp .          # Build from Dockerfile
docker build -t myapp:v1 .       # With tag
docker tag myapp myapp:latest    # Add tag to existing image
```

---

## 📝 Dockerfile Basics

### How to Write a Dockerfile (Simple Template)

**Don't worry about remembering everything! Follow this simple pattern:**

```dockerfile
# 1. Start with a base image
FROM <base-image>:<tag>

# 2. Set working directory (optional but recommended)
WORKDIR /app

# 3. Copy dependency files first (for caching)
COPY package*.json ./           # For Node.js
COPY requirements.txt ./         # For Python
COPY pom.xml ./                  # For Java

# 4. Install dependencies
RUN npm install                  # For Node.js
RUN pip install -r requirements.txt  # For Python
RUN mvn install                  # For Java

# 5. Copy your application code
COPY . .

# 6. Expose the port your app uses
EXPOSE <port-number>

# 7. Define how to start your app
CMD ["command", "to", "start", "app"]
```

**Quick Examples by Language:**

**Node.js:**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

**Python:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

**Static Website (HTML/CSS/JS):**
```dockerfile
FROM nginx:alpine
COPY . /usr/share/nginx/html
EXPOSE 80
```

**Java (Spring Boot):**
```dockerfile
FROM openjdk:17-slim
WORKDIR /app
COPY target/*.jar app.jar
EXPOSE 8080
CMD ["java", "-jar", "app.jar"]
```

### All Dockerfile Instructions Explained

```dockerfile
# FROM - Base image (REQUIRED - must be first)
FROM node:18-alpine              # Start with Node.js on Alpine Linux
FROM ubuntu:22.04                # Or use Ubuntu
FROM nginx:latest                # Or nginx

# WORKDIR - Set working directory inside container
WORKDIR /app                     # All commands run from /app
WORKDIR /usr/src/app             # Creates directory if doesn't exist

# COPY - Copy files from host to container (PREFERRED)
COPY package.json /app/          # Copy single file
COPY . .                         # Copy everything from current dir
COPY src/ /app/src/              # Copy directory

# ADD - Copy files with extra features (use only when needed)
ADD https://example.com/file.tar.gz /app/  # Download from URL
ADD archive.tar.gz /app/         # Auto-extracts tar/zip files

# RUN - Execute commands during BUILD (creates layers)
RUN apt-get update               # Update packages
RUN npm install                  # Install dependencies
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y curl  # Combine to reduce layers

# CMD - Default command when container STARTS (only one)
CMD ["npm", "start"]             # Start Node app
CMD ["python", "app.py"]         # Run Python script
CMD ["nginx", "-g", "daemon off;"]  # Start nginx

# ENTRYPOINT - Main executable (not easily overridden)
ENTRYPOINT ["python"]            # Always run python
CMD ["app.py"]                   # Default argument (can override)

# EXPOSE - Document which port app uses (doesn't publish)
EXPOSE 3000                      # App listens on port 3000
EXPOSE 80 443                    # Multiple ports

# ENV - Set environment variables
ENV NODE_ENV=production          # Set Node environment
ENV PORT=3000                    # Set port variable
ENV DB_HOST=localhost DB_PORT=5432  # Multiple variables

# ARG - Build-time variables (only during build)
ARG VERSION=1.0                  # Default value
RUN echo "Building version $VERSION"

# VOLUME - Create mount point for persistent data
VOLUME ["/data"]                 # Data persists here
VOLUME ["/var/log", "/var/db"]   # Multiple volumes

# USER - Set user for running commands
USER node                        # Run as 'node' user (not root)
USER 1001                        # Or use UID

# LABEL - Add metadata to image
LABEL version="1.0"              # Version info
LABEL description="My app"       # Description
```

### COPY vs ADD

| Feature | COPY | ADD |
|---------|------|-----|
| **Basic copying** | ✅ Yes | ✅ Yes |
| **Copy from URL** | ❌ No | ✅ Yes |
| **Auto-extract tar** | ❌ No | ✅ Yes |
| **Best practice** | ✅ Preferred | ⚠️ Use only when needed |

```dockerfile
# COPY - Simple and predictable (USE THIS)
COPY index.html /app/
COPY package*.json ./

# ADD - Has extra features
ADD https://example.com/file.tar.gz /app/  # Downloads from URL
ADD archive.tar.gz /app/                   # Auto-extracts tar files
```

**Rule:** Use COPY unless you need ADD's special features.

### RUN vs CMD

| Feature | RUN | CMD |
|---------|-----|-----|
| **When executed** | During image build | When container starts |
| **Purpose** | Install/setup | Start application |
| **Can have multiple** | ✅ Yes | ❌ No (last one wins) |
| **Can override** | ❌ No | ✅ Yes (with docker run) |

```dockerfile
# RUN - Executes during BUILD (creates layers)
RUN apt-get update
RUN npm install
RUN pip install -r requirements.txt

# CMD - Executes when CONTAINER STARTS (only one CMD)
CMD ["npm", "start"]           # Starts your app
CMD ["python", "app.py"]       # Runs Python script
CMD ["nginx", "-g", "daemon off;"]  # Starts nginx
```

**Simple Rule:**
- **RUN** = Build time (install stuff)
- **CMD** = Runtime (start app)

### Complete Dockerfile Example

**Simple Example:**
```dockerfile
FROM nginx:alpine                # Start with nginx
COPY index.html /usr/share/nginx/html/  # Copy your file
EXPOSE 80                        # Document port
CMD ["nginx", "-g", "daemon off;"]  # Start nginx
```

**Node.js Example:**
```dockerfile
FROM node:18-alpine              # Base image
WORKDIR /app                     # Set working directory
COPY package*.json ./            # Copy package files
RUN npm install                  # Install dependencies (BUILD TIME)
COPY . .                         # Copy source code
EXPOSE 3000                      # Document port
CMD ["npm", "start"]             # Start app (RUN TIME)
```

**Build & Run:**
```bash
docker build -t myapp .
docker run -d -p 3000:3000 --name app myapp
```

---

## 🎓 Common Scenarios

### Scenario 1: Quick Test an App
```bash
docker run -d --rm -p 8080:80 --name test nginx
# Test it...
docker stop test                 # Auto-removed due to --rm
```

### Scenario 2: Debug Why Container Stopped
```bash
docker ps -a                     # Find stopped container
docker logs <name>               # See what went wrong
docker start <name>              # Try starting again
```

### Scenario 3: Access Container Files
```bash
docker exec -it <name> bash      # Get shell access
ls                               # Browse files
cat /var/log/app.log            # Read logs
exit                             # Leave container
```

### Scenario 4: Clean Everything
```bash
docker stop $(docker ps -aq)     # Stop all
docker rm $(docker ps -aq)       # Remove all containers
docker rmi $(docker images -q)   # Remove all images
docker system prune -a           # Nuclear option (removes everything)
```

---

## 🐛 Troubleshooting

### "Can't see anything on port 8080"
```bash
# Check if container is running
docker ps

# Check logs for errors
docker logs <name>

# Verify port mapping (should show 0.0.0.0:8080->80/tcp)
docker ps

# Common fix: Port flag BEFORE image name
docker run -d -p 8080:80 --name web nginx  ✅
docker run -d --name web nginx -p 8080:80  ❌ WRONG!
```

### "Container exits immediately"
```bash
docker logs <name>               # See why it crashed
docker run -it <image> bash      # Run interactively to debug
```

### "Port already in use"
```bash
# Use different port
docker run -d -p 8081:80 --name web nginx

# Or find what's using it (Windows)
netstat -ano | findstr :8080
```

### "Permission denied"
```bash
# Linux/Mac: Add sudo or add user to docker group
sudo docker ps
```

---

## 🔄 Docker Compose (Multi-Container Apps)

### The Problem: Running Multiple Containers Manually

**Imagine you have a Node.js app that needs MongoDB and Mongo Express:**

```bash
# Step 1: Create network (MANUAL!)
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
  mongo-express

# Step 4: Run your Node.js app
docker run -d \
  -p 3000:3000 \
  --network mongo-network \
  --name node-app \
  -e MONGO_URL=mongodb://admin:password@mongo:27017 \
  my-node-app
```

**Problems:**
- Too many commands to remember
- Easy to make mistakes
- Hard to share with team
- Difficult to start/stop everything together
- **Must manually create network first!**

### The Solution: Docker Compose

**Docker Compose lets you define all containers in ONE file!**

**✨ No need to create network manually - Docker Compose does it automatically!**

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  # MongoDB Database
  mongo:
    image: mongo
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password
    volumes:
      - mongo-data:/data/db

  # Mongo Express (Database UI)
  mongo-express:
    image: mongo-express
    ports:
      - "8081:8081"
    environment:
      ME_CONFIG_MONGODB_ADMINUSERNAME: admin
      ME_CONFIG_MONGODB_ADMINPASSWORD: password
      ME_CONFIG_MONGODB_SERVER: mongo
    depends_on:
      - mongo

  # Your Node.js Application
  node-app:
    build: .
    ports:
      - "3000:3000"
    environment:
      MONGO_URL: mongodb://admin:password@mongo:27017/mydb
    depends_on:
      - mongo
    volumes:
      - .:/app
      - /app/node_modules

volumes:
  mongo-data:

# Network is created automatically by Docker Compose!
# All services are connected to the same network by default
networks:
  default:
    name: mongo-network
```

### How Containers Connect in Docker Network

**Inside Docker Network:**
```
┌─────────────────────────────────────────┐
│         Docker Network                  │
│                                         │
│  ┌──────────┐      ┌──────────────┐   │
│  │  mongo   │◄─────│  node-app    │   │
│  │  :27017  │      │  :3000       │   │
│  └──────────┘      └──────────────┘   │
│       ▲                                │
│       │                                │
│  ┌────┴─────────┐                     │
│  │ mongo-express│                     │
│  │    :8081     │                     │
│  └──────────────┘                     │
└─────────────────────────────────────────┘
         │              │
         │              │
    Port Binding   Port Binding
         │              │
         ▼              ▼
   localhost:8081  localhost:3000
   (Your Browser)  (Your Browser)
```

**How Node.js App Connects to MongoDB:**

```javascript
// In your Node.js app
const mongoose = require('mongoose');

// Use container name 'mongo' instead of 'localhost'
// Docker network resolves 'mongo' to the MongoDB container's IP
const mongoURL = 'mongodb://admin:password@mongo:27017/mydb';

mongoose.connect(mongoURL)
  .then(() => console.log('Connected to MongoDB!'))
  .catch(err => console.error('Connection failed:', err));
```

**Why use 'mongo' instead of 'localhost'?**
- Inside Docker network, containers use **container names** to find each other
- `mongo` = MongoDB container
- `mongo-express` = Mongo Express container
- Docker's internal DNS resolves these names to container IPs

**From outside (your browser):**
- Access Mongo Express: `http://localhost:8081`
- Access Node.js app: `http://localhost:3000`
- Port binding makes them accessible from your computer

### Docker Compose Commands

```bash
# Start all services (creates network automatically!)
docker-compose up -d

# View running services
docker-compose ps

# View logs from all services
docker-compose logs -f

# View logs from specific service
docker-compose logs -f node-app

# Stop all services
docker-compose down

# Stop and remove volumes (deletes data)
docker-compose down -v

# Rebuild and start
docker-compose up -d --build
```

**What happens when you run `docker-compose up`:**
1. ✅ Creates network automatically (no `docker network create` needed!)
2. ✅ Pulls/builds all images
3. ✅ Creates volumes
4. ✅ Starts containers in correct order (based on `depends_on`)
5. ✅ Connects all containers to the same network

### Benefits of Docker Compose

✅ **One command** to start everything: `docker-compose up -d`
✅ **Automatic networking** - containers can talk to each other
✅ **Easy to share** - just share the `docker-compose.yml` file
✅ **Version control** - track changes in git
✅ **Environment variables** - manage configs easily
✅ **Dependencies** - `depends_on` ensures correct startup order
✅ **Volumes** - persist data even after containers stop

### Complete Example: Node.js + MongoDB + Mongo Express

**Project Structure:**
```
my-project/
├── docker-compose.yml
├── Dockerfile
├── package.json
├── server.js
└── .dockerignore
```

**Dockerfile:**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

**server.js:**
```javascript
const express = require('express');
const mongoose = require('mongoose');

const app = express();

// Connect to MongoDB using container name
mongoose.connect(process.env.MONGO_URL)
  .then(() => console.log('Connected to MongoDB'))
  .catch(err => console.error('MongoDB connection error:', err));

app.get('/', (req, res) => {
  res.send('Hello from Node.js + Docker!');
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

**Start everything:**
```bash
docker-compose up -d
```

**Access:**
- Node.js app: http://localhost:3000
- Mongo Express: http://localhost:8081 (admin/pass)

**Stop everything:**
```bash
docker-compose down
```

**That's it! No manual network creation, no long docker run commands!** 🎉

---

## 💡 Pro Tips

1. **Always name your containers** - Easier than using IDs
2. **Use --rm for testing** - Auto-cleanup saves time
3. **Check logs first** - Most issues are visible in logs
4. **Port flag position matters** - Always before image name
5. **Use specific tags** - Avoid `latest` in production

---

## 🚀 Quick Command Reference

```bash
# Run container
docker run -d -p 8080:80 --name web nginx

# Check status
docker ps

# View logs
docker logs -f web

# Get inside
docker exec -it web bash

# Stop & remove
docker rm -f web

# Clean up
docker system prune
```

---

## 📚 Resources

- [Docker Docs](https://docs.docker.com)
- [Docker Hub](https://hub.docker.com) - Find images
- [Play with Docker](https://labs.play-with-docker.com) - Free online practice

---

## 🎯 Practice Exercise

Try this workflow:
```bash
# 1. Pull nginx
docker pull nginx

# 2. Run with port binding
docker run -d -p 8080:80 --name myweb nginx

# 3. Check it's running
docker ps

# 4. View in browser: http://localhost:8080

# 5. See logs
docker logs myweb

# 6. Get inside
docker exec -it myweb bash
ls /usr/share/nginx/html
exit

# 7. Clean up
docker rm -f myweb
```

**Congratulations! You just mastered the Docker basics! 🎉**
