from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def index():
    name = request.args.get("name")
    return render_template("index.html")


# app.config['TESTING'] = True

# app.testing = True

# app.config.update(
#     TESTING=True,
#     SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
# )

# flask --app hello --debug run  # to debug
# use mongoDB

