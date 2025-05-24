import os
import subprocess
import sys

def download_packages():
    # Create packages directory if it doesn't exist
    if not os.path.exists('packages'):
        os.makedirs('packages')
    
    # Read requirements.txt
    with open('requirements.txt', 'r') as f:
        requirements = f.read().splitlines()
    
    # Download each package
    for package in requirements:
        if package.strip():
            print(f"Downloading {package}...")
            subprocess.run([
                sys.executable, 
                '-m', 
                'pip', 
                'download',
                '--dest', 
                './packages',
                package
            ])

if __name__ == '__main__':
    print("Downloading packages for offline installation...")
    download_packages()
    print("Download complete! Copy the 'packages' folder to the target machine.") 