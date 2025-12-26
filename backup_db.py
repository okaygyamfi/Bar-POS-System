import os
import subprocess
from datetime import datetime

def run_backup():
    # Configuration
    db_name = "bar_pos_system"
    db_user = "your_username"
    db_password = "your_password"
    
    # Create a 'backups' folder if it doesn't exist
    backup_folder = "backups"
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
    
    # Generate filename with date and time (e.g., Akropong_Backup_2023-10-27_10-30.sql)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"Akropong_Backup_{timestamp}.sql"
    filepath = os.path.join(backup_folder, filename)
    
    # Command to run mysqldump
    
    dump_command = [
        "mysqldump",
        f"-u{db_user}",
        f"-p{db_password}",
        db_name
    ]
    
    print(f"--- Starting Backup for {db_name}... ---")
    
    try:
        with open(filepath, "w") as output_file:
            subprocess.run(dump_command, stdout=output_file, check=True)
        print(f"--- Success! Backup saved to: {filepath} ---")
    except Exception as e:
        print(f"!!! Backup Failed: {e}")

if __name__ == "__main__":
    run_backup()
