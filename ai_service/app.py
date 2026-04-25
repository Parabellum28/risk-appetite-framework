from flask import Flask

from routes.categorise import bp as categorise_bp   # ✅ FIXED
from routes.query import bp as query_bp             # ✅ FIXED

app = Flask(__name__)

app.register_blueprint(categorise_bp)
app.register_blueprint(query_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
