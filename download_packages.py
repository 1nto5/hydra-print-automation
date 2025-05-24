import os
import subprocess
import sys

def download_packages():
    """Download all required packages for offline installation."""
    print("Downloading packages for offline installation...")
    
    # Create deps directory if it doesn't exist
    if not os.path.exists('deps'):
        os.makedirs('deps')
    
    # Download packages
    try:
        subprocess.run([
            sys.executable, 
            '-m', 
            'pip', 
            'download',
            '-r', 
            'requirements.txt',
            '-d', 
            'deps'
        ], check=True)
        print("Packages downloaded successfully to 'deps' directory.")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading packages: {e}")
        sys.exit(1)

if __name__ == '__main__':
    download_packages() 