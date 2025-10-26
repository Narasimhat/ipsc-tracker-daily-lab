# iPSC Tracker - Daily Export Configuration
# Edit these settings to customize your daily exports

# Export Schedule
EXPORT_TIME = "09:00"  # 24-hour format (HH:MM)
TASK_NAME = "iPSC_Tracker_Daily_Export"

# File Management
DAYS_TO_KEEP = 30      # Number of days to keep old export files
EXPORT_DIRECTORY = "daily_exports"

# Export Options
INCLUDE_IMAGES = False  # Include image file paths in export
INCLUDE_STATS = True   # Include database statistics in log

# Notification Options (for future enhancement)
EMAIL_NOTIFICATIONS = False
SLACK_NOTIFICATIONS = False

# Log Settings
DETAILED_LOGGING = True
LOG_FILE = "daily_export_log.txt"