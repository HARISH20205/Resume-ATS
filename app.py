# This is a bridging file for Hugging Face Spaces
# It ensures that when the container starts, your Django app will run correctly

import os
import sys
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Make sure we're using the correct port
    port = os.environ.get("PORT", "7860")
    logger.info(f"Starting Django server on port {port}")
    
    try:
        # Start the Django development server
        # For better production deployment, consider using gunicorn
        subprocess.run(
            ["python", "manage.py", "runserver", f"0.0.0.0:{port}"],
            check=True
        )
    except Exception as e:
        logger.error(f"Error starting Django server: {e}")
        sys.exit(1)
