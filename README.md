# 🧬 iPSC Tracker v1.0 - Docker Edition# 🧬 iPSC Tracker - Daily Lab Work System# 🧬 iPSC Tracker v1.0



**Laboratory Information Management System for iPSC Culture Tracking**



A production-ready, containerized system for tracking induced Pluripotent Stem Cell (iPSC) culture workflows in laboratory environments.**Laboratory Information Management System for iPSC Culture Tracking**Laboratory Information Management System for induced Pluripotent Stem Cell (iPSC) culture tracking with team collaboration features.



---



## 🚀 Quick StartA production-ready, team-collaborative system for tracking induced Pluripotent Stem Cell (iPSC) culture workflows in laboratory environments.## ✨ Features



### 1. Deploy with Docker

```bash

docker-compose up -d## ✨ Features- 📊 **Cell Culture Logging** - Track passages, media changes, observations, and experimental workflows

```

- 🔗 **Thaw ID System** - Link related culture events and track cell lineage

### 2. Access the Application

- **Local**: http://localhost:8080- 📊 **Cell Culture Logging** - Track passages, media changes, observations- 👥 **Multi-User Support** - Real-time team collaboration with user filtering and assignment

- **Network**: http://YOUR-IP:8080

- 🔗 **Thaw ID System** - Link related culture events and track lineage- 📋 **Lab Book Export** - Multiple formatting options (detailed, compact, table, simple list)

### 3. Share with Team

Run: `🌐 SHARE WITH TEAM 🌐.bat`- 👥 **Multi-User Support** - Real-time team collaboration- 📅 **Daily Automation** - Automated Excel exports and scheduled backups



---- 📋 **Lab Book Export** - Multiple formatting options for documentation- 🌐 **Web Interface** - Browser-based access requiring no software installation on user computers



## ✨ Features- 📅 **Automated Backups** - Daily Excel exports and data protection- 🧪 **Experimental Tracking** - Protocol management and success rate analytics



- 📊 **Cell Culture Logging** - Track passages, media changes, observations, and experimental workflows- 🌐 **Web Interface** - Browser-based, no software installation required- 📱 **Enhanced UI** - Emoji-enhanced launchers and intuitive interface

- 🔗 **Thaw ID System** - Link related culture events and track cell lineage

- 👥 **Multi-User Support** - Real-time team collaboration with user filtering- 🛠️ **Smart Launchers** - Conflict-free startup system- 🔧 **Diagnostic Tools** - Built-in troubleshooting and setup assistance

- 📋 **Lab Book Export** - Multiple formatting options for documentation

- 📅 **Daily Automation** - Automated Excel exports and scheduled backups

- 🌐 **Web Interface** - Browser-based access requiring no software installation

- 🐳 **Dockerized** - Consistent environment, easy deployment, automatic backups## 🚀 Quick Start## 🚀 Quick Start



---



## 📁 Essential Files### For Team Use:### Simple 3-Step Launch:



### Docker Configuration1. **Double-click**: `🌐 TEAM ACCESS MANAGER 🌐.bat`1. **Double-click**: `🌐 TEAM ACCESS MANAGER 🌐.bat`

- `Dockerfile` - Container image definition

- `docker-compose.yml` - Multi-container orchestration2. **Follow prompts** (detects existing instances or starts new one)2. **Follow prompts** (detects existing instances or starts new one)

- `.dockerignore` - Build optimization

3. **Start logging** your cell culture data3. **Start logging** your cell culture data!

### Application Core

- `app.py` - Main Streamlit application

- `db.py` - Database operations

- `requirements.txt` - Python dependencies### System Requirements:### Team Access:



### Data & Persistence- **Python 3.8+** (3.11 recommended)- **First person**: Uses Team Access Manager to start server

- `data/` - Database and images (persisted)

- `backups/` - Automatic daily backups- **Windows** (primary), macOS/Linux compatible- **Team members**: Use same launcher to connect to existing server

- `exports/` - Generated exports

- **Network access** for team collaboration- **Access URL**: Typically `http://localhost:8501` or `http://[COMPUTER-NAME]:8501`

### Documentation

- `DOCKER_DEPLOYMENT.md` - Complete deployment guide

- `DOCKER_QUICKSTART.md` - Quick reference

- `TEAM_SHARING_GUIDE.md` - Team access instructions## 📁 Project Structure## 📁 Project Structure

- `iPSC_Tracker_User_Guide.pdf` - Comprehensive PDF manual



### Utilities

- `🐳 DOCKER DEPLOY 🐳.bat` - Interactive deployment tool### Core Application:### Core Application:

- `🌐 SHARE WITH TEAM 🌐.bat` - Team access setup

- `📖 CREATE USER GUIDE PDF 📖.bat` - Regenerate PDF guide- `app.py` - Main Streamlit application- `app.py` - Main Streamlit application (236KB)

- `team-access.html` - Quick access page for team

- `open-firewall.ps1` - Network access configuration- `db.py` - Database operations and analytics- `db.py` - Database operations, schema, and analytics (88KB)



---- `requirements.txt` - Python dependencies- `requirements.txt` - Python dependencies



## 🛠️ Common Commands



```bash### Team Launchers:### Launcher System:

# Start application

docker-compose up -d- `🌐 TEAM ACCESS MANAGER 🌐.bat` - **Primary launcher** (recommended)- `🌐 TEAM ACCESS MANAGER 🌐.bat` - **Primary launcher** (recommended for all users)



# Stop application- `🚀 SMART LAUNCHER 🚀.bat` - Advanced with port detection- `🚀 SMART LAUNCHER 🚀.bat` - Advanced launcher with port detection

docker-compose down

- `🛠️ SETUP ASSISTANT 🛠️.bat` - First-time setup helper- `🧬 START iPSC TRACKER 🧬.bat` - Simple direct launcher

# View logs

docker-compose logs -f- `🔧 DIAGNOSTIC LAUNCHER 🔧.bat` - Troubleshooting tools- `🛠️ SETUP ASSISTANT 🛠️.bat` - First-time setup and package installation



# Restart- `🔄 VERSION UPGRADE HELPER 🔄.bat` - Python version management

docker-compose restart

## 👥 Team Collaboration- `🔧 DIAGNOSTIC LAUNCHER 🔧.bat` - Troubleshooting and system testing

# Check status

docker-compose ps



# Update after changes### Multi-User Features:### Documentation:

docker-compose up -d --build

```- **Concurrent access** - Multiple users can work simultaneously- `📋 START HERE - CLEAN SETUP 📋.txt` - Quick start guide



---- **Real-time data entry** - Each person's entries appear immediately- `📚 GITHUB SETUP GUIDE 📚.md` - Version control setup



## 📖 Documentation- **Personal filtering** - "My entries only" for focused work- `🏷️ VERSION 1.0 - PRODUCTION 🏷️.txt` - Version information



- **New User?** Start with: `iPSC_Tracker_User_Guide.pdf`- **Operator tracking** - All entries tagged with user information

- **Deploying?** Read: `DOCKER_DEPLOYMENT.md`

- **Quick Start?** See: `DOCKER_QUICKSTART.md`- **Manual refresh** - F5 to see team updates## 🔧 Installation Requirements

- **Team Setup?** Check: `TEAM_SHARING_GUIDE.md`



---

### Network Setup:### System Requirements:

## 🔒 Data Persistence

- **Server address**: Accepts connections from any network computer- **Python 3.8+** (3.11 or 3.12 recommended)

Your data is safe and persistent:

- **Database**: `./data/ipsc_tracker.db`- **Access URLs**: `http://[COMPUTER-NAME]:8501` for team members- **Windows** (primary), macOS/Linux compatible

- **Images**: `./data/images/`

- **Backups**: `./backups/` (automatic daily)- **No client software** required - browser-based interface- **Network access** for team collaboration



Data persists even when:

- Container is stopped

- Container is removed## 📊 Laboratory Data Management### Dependencies:

- Image is rebuilt

```

---

### Features:streamlit>=1.24

## 🌐 Team Access

- **SQLite database** with WAL mode for concurrent accesspandas>=1.5

Share your tracker with colleagues in 3 easy ways:

- **Thaw ID linking** for culture lineage trackingpillow>=10

1. **Send the link**: `http://YOUR-IP:8080`

2. **Send file**: `team-access.html`- **Experimental workflow** support and analyticsopenpyxl>=3.0

3. **Use tool**: `🌐 SHARE WITH TEAM 🌐.bat`

- **Image upload** for colony documentationmatplotlib>=3.5

**Requirements for team members:**

- Same network/WiFi- **Export capabilities** for external analysispyperclip>=1.8.2

- Any web browser

- The access link```



**No installation needed** - Just open the link!### Data Security:



---- **Local storage** - sensitive data stays on your network### Automated Installation:



## 🆘 Troubleshooting- **Automatic backups** - daily Excel exportsUse `🛠️ SETUP ASSISTANT 🛠️.bat` for automatic dependency installation and system verification.



### Can't access the application?- **User access control** through operator management

```bash

# Check if running- **Database protection** - excluded from version control## 👥 Team Usage & Collaboration

docker ps



# Check logs

docker-compose logs -f## 🎯 Production Ready### Multi-User Architecture:



# Restart- **Concurrent users**: Unlimited (tested with 5-15 users)

docker-compose restart

```### Tested & Validated:- **Database**: SQLite with WAL mode for concurrent access



### Port 8080 already in use?- ✅ **Multi-user collaboration** (5-15 concurrent users)- **Network**: Server accessible via computer name or IP

Edit `docker-compose.yml`:

```yaml- ✅ **Production database** with 1000+ entries- **Data sync**: Manual refresh (F5) to see team updates

ports:

  - "8090:8080"  # Use different port- ✅ **Team workflows** in active laboratory use

```

- ✅ **Cross-platform** compatibility### User Management:

### Need to reset everything?

```bash- ✅ **Diagnostic tools** for troubleshooting- **Operator tracking** in all entries

docker-compose down -v

docker-compose up -d --build- **Personal filtering** with "My entries only"

```

### Performance:- **Task assignment** system with due dates

---

- **Page load**: < 2 seconds- **Template sharing** across team members

## 📦 What's in ARCHIVE/

- **Data entry**: Immediate response- **Weekend scheduling** and workload management

Old deployment files and legacy launchers:

- Previous setup scripts- **Filtering**: < 1 second for large datasets

- Non-Docker launchers

- Legacy batch files- **Export generation**: < 10 seconds### Collaboration Features:

- Historical documentation

- **Real-time data entry** by multiple users

**Note:** Only use files from the main folder for Docker deployment.

## 🔧 Installation- **Individual user calibers** and performance tracking

---

- **Shared experimental protocols**

## 🔧 System Requirements

### Automated Setup:- **Team analytics** and reporting

- **Docker Desktop** (latest version)

- **Windows 10/11** or **Linux** or **macOS**Use `🛠️ SETUP ASSISTANT 🛠️.bat` for automatic installation of:

- **2GB RAM** minimum

- **1GB disk space** for application- Python dependencies## 📊 Data Management

- **Network access** for team sharing

- System verification

---

- Database initialization### Database:

## 📊 Technology Stack

- **SQLite** for reliable local storage

- **Frontend**: Streamlit

- **Backend**: Python 3.11### Manual Setup:- **Automatic schema migration** for updates

- **Database**: SQLite

- **Container**: Docker```bash- **WAL mode** for concurrent access

- **Web Server**: Streamlit built-in

- **Backup**: Automated dailypip install -r requirements.txt- **Foreign key constraints** for data integrity



---python -m streamlit run app.py



## 🎯 Version Information```### Backup & Export:



- **Version**: 1.0 - Docker Edition- **Daily automated exports** to Excel

- **Release Date**: October 2025

- **Deployment**: Docker Compose## 📋 Documentation- **Manual backup** functionality in Settings

- **Python**: 3.11

- **Architecture**: Web-based, containerized- **Data export** with filtering options



---- `📋 START HERE - CLEAN SETUP 📋.txt` - Quick start guide- **Image storage** with timestamped naming



## 📝 Quick Tips- `🏷️ VERSION 1.0 - PRODUCTION 🏷️.txt` - Version information



✅ Keep Docker running for team access  - Built-in diagnostic tools for troubleshooting### Data Security:

✅ Bookmark the access URL  

✅ Use `docker-compose logs -f` to monitor  - **Local storage** - sensitive data stays on your network

✅ Data is automatically backed up daily  

✅ Multiple users can access simultaneously  ## 🔒 Data Protection- **User access control** through operator management

✅ Share `team-access.html` for easy access  

- **Backup encryption** options available

---

### Included in Repository:- **Audit trail** for all data modifications

## 🌟 Getting Help

- ✅ Application code and launchers

1. Check the PDF guide: `iPSC_Tracker_User_Guide.pdf`

2. Review deployment docs: `DOCKER_DEPLOYMENT.md`- ✅ Documentation and setup guides## 🧪 Experimental Workflow Support

3. Check logs: `docker-compose logs -f`

4. Run diagnostic: Review container status- ✅ System configuration files



---### Research Features:



**Made with 🧬 for iPSC Research**### Protected (Not Included):- **Experiment type categorization** (Genome Editing, Differentiation, etc.)



*Containerized for easy deployment and team collaboration*- ❌ Database files with lab data- **Protocol reference tracking** (DOIs, SOPs, internal docs)


- ❌ Personal images and exports- **Success metrics** and outcome status

- ❌ Sensitive configuration files- **Multi-stage experiment** progression tracking

- **Success rate analytics** across protocols

## 📈 Laboratory Impact

### Laboratory Integration:

### Workflow Benefits:- **Vial lifecycle tracking** from thaw to cryopreservation

- **Streamlined data entry** replacing paper logs- **Passage prediction** based on historical data

- **Improved data consistency** across team members- **Culture alerts** and recommendations

- **Enhanced traceability** through thaw ID linking- **Weekend work planning** and assignment

- **Automated reporting** reducing manual work

- **Team coordination** through shared access## 🌐 Network Configuration



### Research Applications:### Server Setup:

- **iPSC culture maintenance** tracking- **Address**: `0.0.0.0` (accepts connections from any network computer)

- **Experimental workflow** management- **Ports**: Auto-detection from 8501-8510 range

- **Quality control** and reproducibility- **Access**: Browser-based, no client software required

- **Data analysis** and export capabilities- **Firewall**: May require Windows Firewall configuration



## 🎉 Ready for Production### Team Access URLs:

- **Local**: `http://localhost:[PORT]`

This system is actively used in laboratory environments for daily iPSC culture tracking. The clean, focused codebase represents a stable production release suitable for team deployment.- **Network**: `http://[COMPUTER-NAME]:[PORT]`

- **IP Address**: `http://[IP-ADDRESS]:[PORT]`

---

## 🔒 Security & Privacy

**🔬 Developed for laboratory teams requiring robust, collaborative cell culture tracking with professional-grade features.**
### Data Protection:
- **No cloud storage** - all data remains local
- **Database exclusion** from version control
- **Image privacy** - personal lab photos protected
- **Export control** - manual data sharing only

### Access Control:
- **Network-based** access (same network required)
- **User identification** through operator names
- **Session management** through browser sessions
- **Data visibility** controlled by user filters

## 🎯 Version 1.0 Features Summary

### Core Functionality:
✅ **Cell culture event logging** with comprehensive metadata  
✅ **Thaw ID linking** for culture lineage tracking  
✅ **Multi-user collaboration** with real-time access  
✅ **Lab book formatting** in 4 different styles  
✅ **Automated daily backups** and exports  
✅ **Enhanced user interface** with emoji navigation  
✅ **Diagnostic and troubleshooting** tools  
✅ **Experimental workflow** tracking and analytics  
✅ **Smart launcher system** with conflict resolution  
✅ **Team management** and task assignment  

### Technical Achievements:
✅ **Clean, organized codebase** with modular design  
✅ **Robust error handling** and user guidance  
✅ **Performance optimization** for team use  
✅ **Cross-platform compatibility**  
✅ **Professional deployment** tools and documentation  

## 📈 Performance Metrics

### Tested Capacity:
- **Concurrent users**: 5-15 (optimal), up to 50+ (technical limit)
- **Database entries**: Tested with 1000+ entries
- **File uploads**: Support for standard lab image formats
- **Export size**: Handles large datasets efficiently

### Response Times:
- **Page load**: < 2 seconds typical
- **Data entry**: Immediate response
- **Filtering**: < 1 second for 1000+ entries
- **Export generation**: < 10 seconds for typical datasets

## 🔄 Future Development

This is Version 1.0 - a stable production release. Version 2.0 development environment is prepared for:
- **Blockchain integration** for data integrity
- **Advanced analytics** and reporting
- **Mobile responsiveness** improvements
- **Real-time notifications** and alerts
- **Enhanced collaboration** features

## 📄 License

[Add your preferred license - MIT, GPL, Apache, etc.]

## 🤝 Contributing

Version 1.0 is stable and feature-complete. For suggestions and improvements, please:
1. Use the application and collect feedback
2. Document enhancement requests
3. Consider contributing to Version 2.0 development

## 📞 Support & Documentation

- **Setup Guide**: `📚 GITHUB SETUP GUIDE 📚.md`
- **Quick Start**: `📋 START HERE - CLEAN SETUP 📋.txt`
- **Troubleshooting**: Use `🔧 DIAGNOSTIC LAUNCHER 🔧.bat`
- **Version Info**: `🏷️ VERSION 1.0 - PRODUCTION 🏷️.txt`

## 🏆 Acknowledgments

Developed for laboratory teams requiring robust, collaborative cell culture tracking with professional-grade features and team-ready deployment.

---

**🔬 Ready for production laboratory use - tested, documented, and team-validated.**