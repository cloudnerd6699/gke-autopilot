from flask import Flask
from flask import Response
import os
import gke_automation

app = Flask(__name__)

@app.route("/", methods=["POST","GET"])
def main():
    gke_automation.main()
    status_code = Response(status=200)
    return status_code

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
