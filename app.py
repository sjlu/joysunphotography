__author__ = "sjlu"

import imghdr
import re
from PIL import Image
from os import listdir
from os.path import isdir, isfile, join, abspath, dirname

from flask import Flask, render_template
from flask.ext.assets import Environment as Assets, Bundle

# Initialize
app = Flask(__name__)
app.debug = True

# Assets
assets = Assets(app)
assets.auto_build = True

# Helper functions
def list_projects():
  path = join(dirname(abspath(__file__)), 'static/img/projects/')
  directories = [item for item in listdir(path) if isdir(join(path, item))]
  directories_and_files = []

  projects = []
  for d in directories:
    directory_path = join(path, d)
    files = []
    for f in listdir(directory_path):
      is_file = isfile(join(directory_path, f))
      is_image = imghdr.what(join(directory_path, f))
      if is_file and is_image:
        files.append(f)

    vertical = []
    horizontal = []
    for f in files:
      image = Image.open(join(directory_path, f))
      # if width > height
      if image.size[0] > image.size[1]:
        horizontal.append(f)
      else:
        vertical.append(f)

    print re.sub('.*static/', '', directory_path)
  
    projects.append({
      'name': d.replace('_', ' ').title(),
      'path': re.sub('.*static/', '', directory_path),
      'files': {
        'horizontal': horizontal,
        'vertical': vertical
      }
    })

  return projects

# Define our routes.
@app.route("/")
def index():
  return render_template('homepage.html', projects=list_projects())

# Execute
if __name__ == "__main__":
  app.run()
