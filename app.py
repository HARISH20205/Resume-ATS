# This is a bridging file for Hugging Face Spaces
# It ensures that when the container starts, your Django app will run correctly

import os
import sys
import subprocess
import logging
import traceback

# Configure more detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        # Make sure we're using the correct port
        port = os.environ.get("PORT", "7860")
        logger.info(f"Starting Django server on port {port}")
        
        # Check environment
        logger.info(f"Python version: {sys.version}")
        logger.info(f"Working directory: {os.getcwd()}")
        
        # Start the Django development server
        # For better production deployment, consider using gunicorn
        logger.info("Launching Django server")
        subprocess.run(
            ["python", "manage.py", "runserver", f"0.0.0.0:{port}"],
            check=True
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"Django server failed with exit code {e.returncode}")
        logger.debug(f"Command output: {e.output if hasattr(e, 'output') else 'No output captured'}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error starting Django server: {e}")
        logger.debug(traceback.format_exc())
        sys.exit(1)
