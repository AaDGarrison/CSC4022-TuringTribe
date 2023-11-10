#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

#DECLARE MODULES/LIBRARIES
import os
import sys

def main():
    """Run administrative tasks."""
    #CONFIGURATION - SET DEFAULT DJANGO SETTINGS MODULE
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FinApp.settings')

    try:
        #IMPORT FUNCTION
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        #ERROR HANDLING - HANDLE IMPORTERROR BY PROVIDING ERROR MESSAGE TO USER
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    #PROCESS - EXECUTE DJANGO COMMANDS FROM CMD LINE    
    execute_from_command_line(sys.argv)

#EXECUTE MAIN CALL
if __name__ == '__main__':
    main()
