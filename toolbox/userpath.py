import os
import sys

"""
Path for determining the path of the user running the script. 
There are three potential users: 
- Local test runs
- Runs on remote server by user ubuntu
- Runs by cronjob on remote server
"""

def get_path():
    if 'ubuntu' in os.path.abspath('.'):
        
        # Test whether cron is running the script, or not
        if os.isatty(sys.stdout.fileno()):
            # It is not cron
            path = ''
        else:
            # it is cron
            path = '/home/ubuntu/projects/p03-tilsynsbot/'
    else:
        
        if os.isatty(sys.stdout.fileno()):
            # It is not cron
            path = ''
        else:
            # it is cron
            path = '/Users/oivind/Library/CloudStorage/OneDrive-Deltebiblioteker–UniversityofBergen/Samarbeidsdesken - Dokumenter/Prosjekter/Mulige prosjekter/brreg/'
            
    return path
