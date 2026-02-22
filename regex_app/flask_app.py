from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    matches = []
    error = None

    if request.method == "POST":
        test_string = request.form.get("test_string")
        pattern = request.form.get("pattern")

        try:
            compiled_pattern = re.compile(pattern)
            matches = compiled_pattern.findall(test_string)
        except re.error as e:
            error = f"Invalid Regex: {str(e)}"

    return render_template("index.html", matches=matches, error=error)


if __name__ == "__main__":
    app.run(debug=True)