# Docker Revision Guide 🐳

## What is Docker?
Think of Docker as a **shipping container for your code**. Just like shipping containers standardize how goods are transported, Docker containers package your app with everything it needs to run anywhere.

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
```bash
# Format: -p HOST_PORT:CONTAINER_PORT
docker run -d -p 8080:80 --name web nginx     # Access via localhost:8080
docker run -d -p 3000:3000 --name app node    # Port 3000 to 3000
docker run -d -p 80:80 --name site nginx      # Port 80 to 80
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

**Simple Example:**
```dockerfile
FROM nginx:alpine                # Start with nginx
COPY index.html /usr/share/nginx/html/  # Copy your file
EXPOSE 80                        # Document port
```

**Node.js Example:**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
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

**docker-compose.yml:**
```yaml
version: '3.8'
services:
  web:
    image: nginx
    ports:
      - "8080:80"
  
  db:
    image: postgres
    environment:
      POSTGRES_PASSWORD: secret
```

**Commands:**
```bash
docker-compose up -d             # Start all services
docker-compose ps                # Check status
docker-compose logs -f           # View logs
docker-compose down              # Stop & remove all
```

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
