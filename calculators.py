from flask import Flask
from gail import gail

app = Flask(__name__)


@app.route('/')
def index():
    return "Test Flask Project"

if __name__ == "__main__":
    app.run(debug=True)