__author__ = "sjlu"

import imghdr
import re
import os
import PIL
from PIL import Image

from flask import Flask, render_template
from flask.ext.assets import Environment as Assets, Bundle

# Config
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/img/projects/')

# Initialize
app = Flask(__name__)
app.debug = True

# Assets
assets = Assets(app)
assets.auto_build = True

# Helper functions
def make_layout(images, path):
  layouts = []
  number_set = range(2, 5)
  while len(images):
    layout = {
      "width": 0,
      "height": 0,
      "images": []
    }
    num = len(images) if len(images) < 4 else number_set.pop(0)
    dimensions = []
    for n in range(0, num):
      image = images.pop(0)
      layout['images'].append(image)

      # calculating averages
      image_details = Image.open(os.path.join(path, image))
      dimensions.append({
        'width': image_details.size[0],
        'height': image_details.size[1]
      })

      average_width = sum(x['width'] for x in dimensions) / len(dimensions)
      average_height = sum(x['height'] for x in dimensions) / len(dimensions)

      key = 'height'
      if average_width > average_height:
        key = 'width'

      min_dimension = min(dimensions, key=lambda x: x[key])

      layout['width'] = min_dimension['width']
      layout['height'] = min_dimension['height']

    for image in layout['images']:
      image_handler = Image.open(os.path.join(path, image))

      if image_handler.size[0] == layout['width'] and image_handler.size[1] == layout['height']:
        continue

      resized_image_handler = image_handler.resize((layout['width'], layout['height']), Image.ANTIALIAS)
      resized_image_handler.save(os.path.join(path, image))

    number_set.append(num)
    layouts.append(layout)

  return layouts

def list_projects():
  # Look for project folders
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
    vertical_layouts = make_layout(vertical[:], directory_path)
    horizontal_layouts = make_layout(horizontal[:], directory_path)
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
