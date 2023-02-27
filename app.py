from flask import Flask, render_template, request, send_file
from result import main

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def download():
    main(request.form['input'])

    return send_file('/home/andersen/Documents/projects/shar/result_test_html.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run()
