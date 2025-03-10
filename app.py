from flask import Flask, jsonify,  request,flash
from flask_cors import CORS
from admin import init_admin
from config import Config
from flask_mongoengine import MongoEngine
from tslib import twiiter
import re

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
app.config["MONGO_URI"] = Config.MONGO_URI

app.config["MONGODB_SETTINGS"] = {
    "host": Config.MONGO_URI
}

mongo = MongoEngine(app)



@app.route("/", methods=["GET", "POST"])
def home():
    return "hello"



@app.route("/admin/start_process", methods=["POST"])
def start_process():
    post_link = request.form.get("post_link")

    if not post_link:
        flash("Please enter the link.", "danger")
        return jsonify({"status": "error", "message": "Start date is required."}), 400

    if not re.match(r"^https://x\.com/.+/status/\d+$", post_link):
        flash("Invalid post link format.", "danger")
        return jsonify({"status": "error", "message": "Invalid post link format."}), 400

    try:
        twiiter.main(post_link=post_link)
    except Exception as e:
        flash(f"Error processing post_link for {post_link}: {e}", "danger")
        return jsonify({"status": "error", "message": str(e)}), 500

    flash(f"Process Done for {post_link}.", "success")
    return jsonify(
        {"status": "success", "message": f"Process Done for {post_link}."}
    ), 200

init_admin(app)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
