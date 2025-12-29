from flask import Flask, render_template, request
from zxcvbn import zxcvbn
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

@app.route("/", methods=["GET", "POST"])
def index():
    strength = None
    crack_time = None
    status = None

    if request.method == "POST":
        password = request.form.get("password", "")

        result = zxcvbn(password)
        score = result["score"]

        crack_time = result["crack_times_display"][
            "offline_fast_hashing_1e10_per_second"
        ]

        levels = ["Very Weak", "Weak", "Medium", "Strong", "Very Strong"]
        strength = levels[score]

        status_map = {
            0: "weak",
            1: "weak",
            2: "medium",
            3: "strong",
            4: "verystrong"
        }
        status = status_map[score]

    return render_template(
        "index.html",
        strength=strength,
        crack_time=crack_time,
        status=status
    )

if __name__ == "__main__":
    app.run(debug=True)
