__author__ = "sjlu"

import imghdr
import re
import os

from PIL import Image
from flask import Flask, render_template
from flask.ext.assets import Environment as Assets, Bundle

# Initialize
app = Flask(__name__)
app.debug = True

# Assets
assets = Assets(app)
assets.auto_build = True

# Helper functions
def make_layout(images):
  layouts = []
  number_set = range(2, 5)
  currently_at = 0
  while currently_at < len(images):
    layout = []
    num = len(images) if len(images) < 4 else number_set.pop(0)
    for n in range(currently_at, num):
      layout.append(images[n])
    currently_at += num
    number_set.append(num)
    layouts.append(layout)
  return layouts

def list_projects():
  # Look for project folders
  path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/img/projects/')
  directories = [item for item in os.listdir(path) if os.path.isdir(os.path.join(path, item))]
  directories_and_files = []

  # Walk through each directory to find photos
  projects = []
  for d in directories:
    directory_path = os.path.join(path, d)
    files = []
    for f in os.listdir(directory_path):
      is_file = os.path.isfile(os.path.join(directory_path, f))
      is_image = imghdr.what(os.path.join(directory_path, f))
      if is_file and is_image:
        files.append(f)

    # Detect if the photo is vertical or horizontal.
    vertical = []
    horizontal = []
    for f in files:
      image = Image.open(os.path.join(directory_path, f))
      # if width > height
      if image.size[0] > image.size[1]:
        horizontal.append(f)
      else:
        vertical.append(f)

    # Create our layout.
    vertical_layouts = make_layout(vertical)
    horizontal_layouts = make_layout(horizontal)
    layouts = []
    currently_using = True
    while len(vertical_layouts) > 0 and len(horizontal_layouts) > 0:
      if currently_using:
        layouts.append(vertical_layouts.pop(0))
      else:
        layouts.append(horizontal_layouts.pop(0))
      currently_using = not currently_using
    layouts += vertical_layouts + horizontal_layouts

    projects.append({
      'name': d.replace('_', ' ').replace(' and ', ' & ').title(),
      'canonical': d,
      'path': re.sub('.*static/', '', directory_path),
      'thumbnail': horizontal[0],
      'layouts': layouts
    })

  print projects
  return projects

# Preload this data.
projects = list_projects()

# Define our routes.
@app.route("/")
def index():
  return render_template('homepage.html', projects=projects)

@app.route("/<project_id>")
def project(project_id):
  project = next((p for p in projects if p['canonical'] == project_id), None)
  return render_template('project.html', project=project)

# Execute
if __name__ == "__main__":
  app.run()
