"""Generate the images of the gallery."""
import os
import subprocess

os.chdir('docs/gallery')

for script in ('logo.py', 'colorbar.py', 'legend.py', 'cmaps.py'):
    subprocess.call(['python', script])

os.chdir('../../')
