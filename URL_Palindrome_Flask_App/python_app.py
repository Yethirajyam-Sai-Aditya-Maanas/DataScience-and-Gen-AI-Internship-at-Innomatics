from flask import Flask, request, render_template_string
import datetime

app = Flask(__name__)

# ---------- Utility Functions ----------

def to_uppercase(name):
    return name.upper()

def reverse_name(name):
    return name[::-1]

def count_vowels(name):
    vowels = "aeiouAEIOU"
    return sum(1 for char in name if char in vowels)

def name_length(name):
    return len(name)

def is_palindrome(name):
    cleaned = name.lower().replace(" ", "")
    return cleaned == cleaned[::-1]

def greeting_by_time():
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        return "Good Morning ☀️"
    elif 12 <= current_hour < 17:
        return "Good Afternoon 🌤️"
    elif 17 <= current_hour < 21:
        return "Good Evening 🌇"
    else:
        return "Good Night 🌙"


# ---------- Routes ----------

@app.route("/")
def home():
    username = request.args.get("username")

    if not username:
        return """
        <h2>Welcome to the Cool Name App 😎</h2>
        <p>Use the below URL to access the cool flask application :</p>
        <code>http://127.0.0.1:5000/?username=Sai</code>
        """

    upper_name = to_uppercase(username)
    reversed_name = reverse_name(username)
    vowels = count_vowels(username)
    length = name_length(username)
    palindrome = is_palindrome(username)
    greeting = greeting_by_time()

    html_template = """
    <html>
    <head>
        <title>Cool Name Transformer</title>
        <style>
            body {
                background: linear-gradient(135deg, #1f4037, #99f2c8);
                font-family: Arial, sans-serif;
                text-align: center;
                padding-top: 80px;
                color: white;
            }
            .card {
                background-color: rgba(0,0,0,0.5);
                padding: 30px;
                border-radius: 15px;
                display: inline-block;
                box-shadow: 0px 8px 20px rgba(0,0,0,0.4);
            }
            h1 {
                font-size: 40px;
                margin-bottom: 10px;
            }
            p {
                font-size: 18px;
                margin: 5px;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>{{ greeting }}</h2>
            <h1>{{ upper_name }}</h1>
            <p><strong>Reversed:</strong> {{ reversed_name }}</p>
            <p><strong>Length:</strong> {{ length }}</p>
            <p><strong>Vowel Count:</strong> {{ vowels }}</p>
            <p><strong>Palindrome:</strong> {{ palindrome }}</p>
        </div>
    </body>
    </html>
    """

    return render_template_string(
        html_template,
        greeting=greeting,
        upper_name=upper_name,
        reversed_name=reversed_name,
        vowels=vowels,
        length=length,
        palindrome="Yes ✅" if palindrome else "No ❌"
    )


# ---------- Run App ----------

if __name__ == "__main__":
    app.run(debug=True)