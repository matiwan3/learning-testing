from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    name = request.args.get("name")
    return render_template("index.html")

@app.route("/greet", methods=["POST"])
def greet():
    name = request.form.get("name", default="World")  # request.form for POST method and request.args for GET method
    return render_template("greet.html", name=name)


if __name__ == "__main__":
    app.run(debug=True)
    
    # to run simply use: python "file name"