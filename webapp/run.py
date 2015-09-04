from flask import Flask, request
app = Flask(__name__)

@app.route("/deploy")
def hello():
    environment = request.args.get("environment") #"production"
    home = request.args.get("home") #"/tmp/target"
    url = request.args.get("url") #"svn://localhost/repos/SAMPLE"
    project = request.args.get("project") #"sample"
    key = request.args.get("key") #"smp"
    version = request.args.get("version") #"trunk"

    return  "ole"

if __name__ == "__main__":
    app.run()