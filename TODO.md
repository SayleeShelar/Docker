# TODO - Update README.md with Additional Docker Content

## Task: Add new Docker learning content to README.md

### Steps:
- [ ] 1. Add Docker Networking section after "Container Status Explained" (after line ~200)
      - Explanation of Docker networks
      - Flow diagram showing container communication
      - MongoDB + Mongo Express example with commands

- [ ] 2. Expand docker exec -it explanation in "Interact with Container" section

- [ ] 3. Add Learning Summary section at the end of the file
      - docker run vs docker start
      - Command order matters
      - Why containers stop automatically
      - Why Ubuntu container exited
      - Correct way to run Ubuntu
      - docker exec rule
      - Container status meanings

### New Content to Add:

#### Docker Networking:
```
When two containers are in the same Docker network, they can communicate with each other using container names as hostnames.

Flow:
[Container A] → Docker Network → [Container B]
     ↓                                    ↓
  mongodb:27017                    mongo-express
```

#### MongoDB + Mongo Express Example:
```
bash
# Step 1: Create network
docker network create my-network

# Step 2: Run MongoDB
docker run -d --name mongodb --network my-network -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=password mongo

# Step 3: Run Mongo Express (UI)
docker run -d --name mongo-express --network my-network -p 8081:8081 -e ME_CONFIG_MONGODB_SERVER=mongodb mongo-express

# Now mongo-express can reach mongodb using hostname "mongodb"
```

#### Learning Summary:
- docker run vs docker start
- Command order (options before image)
- Why containers stop (main process stops)
- docker exec -it rules
