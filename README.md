# Docker Revision Guide

## What is Docker?
Docker is a platform for developing, shipping, and running applications in containers. Containers package software with all dependencies, ensuring consistency across environments.

## Core Concepts

### Images
- Read-only templates containing application code, runtime, libraries, and dependencies
- Built from Dockerfile instructions
- Stored in registries (Docker Hub, private registries)

### Containers
- Running instances of images
- Isolated, lightweight, and portable
- Share host OS kernel

### Dockerfile
- Text file with instructions to build an image
- Each instruction creates a layer

### Volumes
- Persist data outside container lifecycle
- Share data between containers

### Networks
- Enable container communication
- Types: bridge, host, overlay, none

## Essential Commands

### Image Commands
```bash
docker pull <image>              # Download image
docker images                    # List images
docker rmi <image>               # Remove image
docker build -t <name> .         # Build image from Dockerfile
docker tag <image> <new-name>    # Tag image
```

### Container Commands
```bash
docker run <image>               # Create and start container
docker run -d <image>            # Run in detached mode
docker run -d --name <name> <image>  # Run with custom name
docker run -d --rm --name <name> <image>  # Run with auto-remove on stop
docker run -d -p 8080:80 --name <name> <image>  # With port binding
docker run -p 8080:80 <image>    # Port mapping (host:container)
docker run -v /host:/container   # Volume mount
docker run -it <image> /bin/bash # Interactive terminal

docker ps                        # List running containers
docker ps -a                     # List all containers
docker start <container>         # Start stopped container
docker stop <container>          # Stop container
docker restart <container>       # Restart container
docker rm <container>            # Remove stopped container
docker rm -f <container>         # Forcefully remove container
docker exec -it <container> bash # Execute command in running container
docker logs <container>          # View logs
docker logs -f <container>       # View live logs (follow)
docker inspect <container>       # Detailed info
```

### System Commands
```bash
docker version                   # Docker version
docker info                      # System info
docker system prune              # Remove unused data
docker system df                 # Disk usage
```

### Docker Compose Commands
```bash
docker-compose up                # Start services
docker-compose up -d             # Start in detached mode
docker-compose down              # Stop and remove services
docker-compose ps                # List services
docker-compose logs              # View logs
docker-compose build             # Build services
```

## Dockerfile Instructions

```dockerfile
FROM <image>                     # Base image
WORKDIR /app                     # Set working directory
COPY <src> <dest>                # Copy files
ADD <src> <dest>                 # Copy files (supports URLs, tar)
RUN <command>                    # Execute command during build
CMD ["executable", "param"]      # Default command (overridable)
ENTRYPOINT ["executable"]        # Main command (not overridable)
ENV KEY=value                    # Environment variable
EXPOSE <port>                    # Document port
VOLUME ["/data"]                 # Create mount point
USER <username>                  # Set user
ARG <name>=<default>             # Build-time variable
LABEL key="value"                # Metadata
```

## Example Dockerfile

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

## Docker Compose Example

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - .:/app
    environment:
      - NODE_ENV=development
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=secret
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
```

## Best Practices

1. **Use official base images** - More secure and maintained
2. **Minimize layers** - Combine RUN commands with &&
3. **Use .dockerignore** - Exclude unnecessary files
4. **Don't run as root** - Use USER instruction
5. **Use specific tags** - Avoid 'latest' tag
6. **Multi-stage builds** - Reduce final image size
7. **One process per container** - Follow single responsibility
8. **Use volumes for data** - Don't store in container
9. **Keep images small** - Use alpine variants
10. **Cache dependencies** - Copy package files before source code

## Container Status Meanings

- **Up** - Container is running
- **Exited** - Container stopped (check logs to see why)
- **Created** - Container created but not started
- **Restarting** - Container is restarting
- **Paused** - Container is paused
- **Dead** - Container is dead (non-recoverable state)

## Common Flags

- `-d` - Detached mode (run in background)
- `-it` - Interactive terminal
- `-p` - Port mapping (host:container)
- `-v` - Volume mount
- `--name` - Container name
- `--rm` - Auto-remove container on stop
- `-e` - Environment variable
- `--network` - Network connection
- `--restart` - Restart policy
- `-f` - Follow/force (for logs/remove)

## Quick Reference

### Remove Everything
```bash
docker stop $(docker ps -aq)     # Stop all containers
docker rm $(docker ps -aq)       # Remove all containers
docker rmi $(docker images -q)   # Remove all images
```

### View Resource Usage
```bash
docker stats                     # Live resource usage
docker top <container>           # Running processes
```

### Network Commands
```bash
docker network ls                # List networks
docker network create <name>     # Create network
docker network connect <net> <container>  # Connect container
```

### Volume Commands
```bash
docker volume ls                 # List volumes
docker volume create <name>      # Create volume
docker volume rm <name>          # Remove volume
docker volume prune              # Remove unused volumes
```

## Troubleshooting

- **Container exits immediately**: Check logs with `docker logs <container>`
- **Port already in use**: Change host port or stop conflicting service
- **Permission denied**: Check file permissions or run with sudo
- **Image not found**: Pull image first or check name/tag
- **Out of disk space**: Run `docker system prune -a`

## Resources

- Official Docs: https://docs.docker.com
- Docker Hub: https://hub.docker.com
- Best Practices: https://docs.docker.com/develop/dev-best-practices
