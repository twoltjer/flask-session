from flask import Flask, render_template, request
import markdown
from datetime import datetime

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def handle_request():
    if request.method == 'GET':
        return render_template('main.html', md_html="", md_raw="##Click \"Submit\" button below to render this!")
    if request.method == 'POST':
        form_data = request.form
        md_input = ""
        for key, value in form_data.items():
            if key == "md_input":
                md_input = value
        html = markdown.markdown(md_input)
        return render_template('main.html', md_html=html, md_raw=md_input)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
