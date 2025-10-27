"""
GitHub Auto-Backup System for iPSC Tracker
Automatically backs up database to GitHub and restores on startup
"""

import os
import subprocess
import streamlit as st
from datetime import datetime
from pathlib import Path
import shutil

class GitHubBackup:
    """Handles automatic GitHub backup and restore for database"""
    
    def __init__(self, db_path: str = "data/ipsc_tracker.db"):
        self.db_path = db_path
        self.backup_branch = "db-backup"
        self.repo_url = "https://github.com/Narasimhat/ipsc-tracker-daily-lab.git"
        
    def is_cloud_environment(self) -> bool:
        """Detect if running on Streamlit Cloud"""
        return os.path.exists("/mount/src") or "STREAMLIT_SHARING_MODE" in os.environ
    
    def get_github_token(self) -> str:
        """Get GitHub token from Streamlit secrets"""
        try:
            if hasattr(st, 'secrets') and 'github' in st.secrets:
                return st.secrets['github']['token']
        except:
            pass
        return os.getenv('GITHUB_TOKEN', '')
    
    def setup_git_auth(self):
        """Configure git with authentication"""
        token = self.get_github_token()
        if not token:
            print("⚠️  No GitHub token found - backup disabled")
            return False
        
        # Set git config
        try:
            subprocess.run(['git', 'config', '--global', 'user.email', 'ipsc-tracker@streamlit.app'], 
                         check=False, capture_output=True)
            subprocess.run(['git', 'config', '--global', 'user.name', 'iPSC Tracker Bot'], 
                         check=False, capture_output=True)
            
            # Set credential helper
            auth_url = self.repo_url.replace('https://', f'https://{token}@')
            subprocess.run(['git', 'remote', 'set-url', 'origin', auth_url], 
                         check=False, capture_output=True)
            return True
        except Exception as e:
            print(f"⚠️  Git auth setup failed: {e}")
            return False
    
    def restore_from_github(self):
        """Download and restore database from GitHub on startup"""
        if not self.is_cloud_environment():
            print("📍 Local environment - skipping restore")
            return
        
        print("🔄 Restoring database from GitHub...")
        
        try:
            # Ensure data directory exists
            os.makedirs("data", exist_ok=True)
            
            # Try to fetch latest backup
            result = subprocess.run(
                ['git', 'fetch', 'origin', f'{self.backup_branch}:{self.backup_branch}'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # Checkout database file from backup branch
                checkout_result = subprocess.run(
                    ['git', 'checkout', self.backup_branch, '--', self.db_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if checkout_result.returncode == 0 and os.path.exists(self.db_path):
                    print(f"✅ Database restored from GitHub: {self.db_path}")
                    return True
                else:
                    print("⚠️  No backup found - starting with fresh database")
            else:
                print(f"⚠️  Backup branch not found - starting fresh")
                
        except subprocess.TimeoutExpired:
            print("⚠️  Restore timeout - using local database")
        except Exception as e:
            print(f"⚠️  Restore failed: {e}")
        
        return False
    
    def backup_to_github(self, force: bool = False):
        """Backup database to GitHub"""
        if not self.is_cloud_environment() and not force:
            print("📍 Local environment - skipping backup")
            return False
        
        if not os.path.exists(self.db_path):
            print(f"⚠️  Database not found: {self.db_path}")
            return False
        
        if not self.setup_git_auth():
            return False
        
        print("💾 Backing up database to GitHub...")
        
        try:
            # Check if backup branch exists, create if not
            subprocess.run(['git', 'fetch', 'origin'], capture_output=True, timeout=30)
            
            branch_check = subprocess.run(
                ['git', 'rev-parse', '--verify', f'origin/{self.backup_branch}'],
                capture_output=True
            )
            
            if branch_check.returncode != 0:
                # Create new orphan branch for backups
                print(f"📝 Creating new backup branch: {self.backup_branch}")
                subprocess.run(['git', 'checkout', '--orphan', self.backup_branch], 
                             capture_output=True)
                subprocess.run(['git', 'rm', '-rf', '.'], capture_output=True)
            else:
                # Switch to backup branch
                subprocess.run(['git', 'checkout', self.backup_branch], capture_output=True)
                subprocess.run(['git', 'pull', 'origin', self.backup_branch], 
                             capture_output=True, timeout=30)
            
            # Copy database to backup location
            backup_dir = Path("data")
            backup_dir.mkdir(exist_ok=True)
            
            # Add and commit database
            subprocess.run(['git', 'add', self.db_path], check=True)
            
            commit_msg = f"Auto-backup: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}"
            result = subprocess.run(
                ['git', 'commit', '-m', commit_msg],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 or 'nothing to commit' in result.stdout:
                # Push to GitHub
                push_result = subprocess.run(
                    ['git', 'push', 'origin', self.backup_branch],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if push_result.returncode == 0:
                    print(f"✅ Database backed up to GitHub: {commit_msg}")
                    
                    # Return to main branch
                    subprocess.run(['git', 'checkout', 'master'], capture_output=True)
                    return True
                else:
                    print(f"⚠️  Push failed: {push_result.stderr}")
            else:
                print("ℹ️  No changes to backup")
            
            # Return to main branch
            subprocess.run(['git', 'checkout', 'master'], capture_output=True)
            
        except subprocess.TimeoutExpired:
            print("⚠️  Backup timeout")
        except Exception as e:
            print(f"⚠️  Backup failed: {e}")
        
        return False
    
    def schedule_backup(self, interval_minutes: int = 60):
        """
        Schedule periodic backups (to be called from main app)
        Note: Streamlit Cloud may restart, so this is best-effort
        """
        import time
        last_backup = getattr(st.session_state, 'last_backup_time', 0)
        current_time = time.time()
        
        if current_time - last_backup > (interval_minutes * 60):
            success = self.backup_to_github()
            if success:
                st.session_state.last_backup_time = current_time
            return success
        
        return False


# Singleton instance
_backup_instance = None

def get_backup_system():
    """Get or create backup system singleton"""
    global _backup_instance
    if _backup_instance is None:
        _backup_instance = GitHubBackup()
    return _backup_instance


def restore_database_on_startup():
    """Call this at app startup to restore from GitHub"""
    backup = get_backup_system()
    return backup.restore_from_github()


def backup_database_now(force: bool = False):
    """Manually trigger a backup"""
    backup = get_backup_system()
    return backup.backup_to_github(force=force)


def auto_backup_if_needed(interval_minutes: int = 60):
    """Call this periodically from your app to trigger auto-backups"""
    backup = get_backup_system()
    return backup.schedule_backup(interval_minutes)
