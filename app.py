from flask import Flask, render_template, request, send_file, redirect
from utils import main, remove_trash

app = Flask(__name__)


def redirect_to_main():
    return redirect('/')

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def download():
    main(request.form["input"])
    file = send_file(
        "/home/andersen/Documents/projects/shar/announcement.pdf", as_attachment=True
    )
    remove_trash()
    # request.form["input"] = ""
    return file


if __name__ == "__main__":
    app.run()
