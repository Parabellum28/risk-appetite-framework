from flask import Flask
from .routes.categorise import bp as categorise_bp

app = Flask(__name__)

app.register_blueprint(categorise_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
