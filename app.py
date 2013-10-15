__author__ = "sjlu"

from flask import Flask, render_template
from flask.ext.assets import Environment as Assets, Bundle

# Initialize
app = Flask(__name__)

# Assets
assets = Assets(app)
assets.auto_build = True

# Define our routes.
@app.route("/")
def index():
  return render_template('homepage.html')

# Execute
if __name__ == "__main__":
  app.run(debug=True)
