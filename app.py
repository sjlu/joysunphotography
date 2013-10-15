__author__ = "sjlu"

import imghdr
from PIL import Image
from os import listdir
from os.path import isdir, isfile, join

from flask import Flask, render_template
from flask.ext.assets import Environment as Assets, Bundle

# Initialize
app = Flask(__name__)

# Assets
assets = Assets(app)
assets.auto_build = True

# Helper functions
def list_projects():
  path = 'static/img/projects/'
  directories = [item for item in listdir(path) if isdir(join(path,item))]
  directories_and_files = []

  projects = []
  for d in directories:
    directory_path = '%s%s' % (path, d)
    files = [f for f in listdir(directory_path) if isfile(join(directory_path, f)) and imghdr.what(join(directory_path, f))]

    vertical = []
    horizontal = []
    for f in files:
      image = Image.open(join(directory_path, f))
      # if width > height
      if image.size[0] > image.size[1]:
        horizontal.append(f)
      else:
        vertical.append(f)

    projects.append({
      'name': d.replace('_', ' ').title(),
      'path': directory_path.replace('static/', ''),
      'files': {
        'horizontal': horizontal,
        'vertical': vertical
      }
    })

  print projects
  return projects

# Define our routes.
@app.route("/")
def index():
  return render_template('homepage.html', projects=list_projects())

# Execute
if __name__ == "__main__":
  app.run(debug=True)
