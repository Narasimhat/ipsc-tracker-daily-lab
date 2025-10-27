# 🐳 iPSC Tracker - Docker Deployment Guide

## Prerequisites

1. **Install Docker Desktop for Windows**
   - Download from: https://www.docker.com/products/docker-desktop
   - Install and restart your computer
   - Ensure Docker Desktop is running (whale icon in system tray)

2. **Verify Docker Installation**
   ```powershell
   docker --version
   docker-compose --version
   ```

## Quick Start Deployment

### Option 1: Using Docker Compose (Recommended)

1. **Build and Start the Application**
   ```powershell
   cd "U:\DATA MANAGMENT\NT_Literature\iPSC_Tracker"
   docker-compose up -d
   ```

2. **Access the Application**
   - Open browser: http://localhost:8080
   - The app will be running in the background

3. **Check Status**
   ```powershell
   docker-compose ps
   docker-compose logs -f ipsc-tracker
   ```

4. **Stop the Application**
   ```powershell
   docker-compose down
   ```

### Option 2: Using Docker Commands Directly

1. **Build the Docker Image**
   ```powershell
   docker build -t ipsc-tracker:latest .
   ```

2. **Run the Container**
   ```powershell
   docker run -d `
     --name ipsc-tracker `
     -p 8080:8080 `
     -v "${PWD}/data:/app/data" `
     -v "${PWD}/backups:/app/backups" `
     --restart unless-stopped `
     ipsc-tracker:latest
   ```

3. **Access the Application**
   - Open browser: http://localhost:8080

4. **Stop and Remove Container**
   ```powershell
   docker stop ipsc-tracker
   docker rm ipsc-tracker
   ```

## Data Persistence

Your data is stored in these directories:
- **Database & Images**: `./data/` - Contains `ipsc_tracker.db` and `images/`
- **Backups**: `./backups/` - Automatic daily backups

These folders are mounted as Docker volumes, so your data persists even if you:
- Stop the container
- Remove the container
- Rebuild the image

## Management Commands

### View Logs
```powershell
# Docker Compose
docker-compose logs -f ipsc-tracker

# Docker directly
docker logs -f ipsc-tracker
```

### Restart Application
```powershell
# Docker Compose
docker-compose restart

# Docker directly
docker restart ipsc-tracker
```

### Update Application
```powershell
# Stop current container
docker-compose down

# Rebuild with latest changes
docker-compose build --no-cache

# Start updated version
docker-compose up -d
```

### Backup Data Manually
```powershell
# Create timestamped backup
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
Compress-Archive -Path ".\data\*" -DestinationPath ".\backups\manual-backup-$timestamp.zip"
```

## Automatic Backups

The docker-compose.yml includes an optional backup service that:
- Creates daily compressed backups
- Stores them in `./backups/`
- Automatically deletes backups older than 30 days

To enable it, the service is already included in docker-compose.yml and will run automatically.

## Troubleshooting

### Container Won't Start
```powershell
# Check container status
docker-compose ps

# View detailed logs
docker-compose logs ipsc-tracker

# Check if port 8080 is already in use
netstat -ano | findstr :8080
```

### Port 8080 Already in Use
Edit `docker-compose.yml` and change the port mapping:
```yaml
ports:
  - "8081:8080"  # Use 8081 instead
```
Then access via http://localhost:8081

### Reset Everything
```powershell
# Stop and remove all containers
docker-compose down -v

# Remove the image
docker rmi ipsc-tracker

# Rebuild from scratch
docker-compose up -d --build
```

### Access Container Shell
```powershell
docker exec -it ipsc-tracker /bin/bash
```

## Production Deployment Tips

### 1. Use a Reverse Proxy (Nginx/Caddy)
For production deployments, use a reverse proxy with SSL:
```yaml
# Add to docker-compose.yml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - ipsc-tracker
```

### 2. Change Default Port
In docker-compose.yml, modify:
```yaml
ports:
  - "80:8080"  # Expose on port 80
```

### 3. Set Resource Limits
```yaml
services:
  ipsc-tracker:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

### 4. Enable Docker Auto-Start
Ensure Docker Desktop starts with Windows:
- Open Docker Desktop settings
- General → "Start Docker Desktop when you log in"

## Network Access

### Allow Access from Other Computers
1. Open Windows Firewall
2. Create inbound rule for port 8080
3. Access via: http://YOUR-COMPUTER-IP:8080

Find your IP:
```powershell
ipconfig | findstr IPv4
```

## Health Checks

The application includes automatic health checks:
- Checks every 30 seconds
- Application is considered unhealthy after 3 failed checks
- Docker will restart unhealthy containers

View health status:
```powershell
docker ps
# Look for "healthy" or "unhealthy" in STATUS column
```

## File Structure After Deployment

```
iPSC_Tracker/
├── Dockerfile                 # Container definition
├── docker-compose.yml         # Multi-container orchestration
├── .dockerignore             # Files to exclude from image
├── app.py                    # Main application
├── db.py                     # Database functions
├── requirements.txt          # Python dependencies
├── data/                     # Persisted data (mounted volume)
│   ├── ipsc_tracker.db      # SQLite database
│   └── images/              # Uploaded images
└── backups/                  # Automatic backups (mounted volume)
    └── *.tar.gz             # Compressed backups
```

## Support

For issues or questions:
1. Check logs: `docker-compose logs -f`
2. Verify Docker is running
3. Ensure ports are not blocked
4. Check firewall settings

---

**Version**: 1.0  
**Last Updated**: October 27, 2025  
**Container**: iPSC Tracker Application
