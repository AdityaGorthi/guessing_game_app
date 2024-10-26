from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a random secret key for session management

@app.route("/", methods=["GET", "POST"])
def guessing_game():
    if request.method == "POST":
        # Check if the user wants to start a new game
        if "start_game" in request.form:
            # Starting a new game
            lower_bound = int(request.form["lower_bound"])
            upper_bound = int(request.form["upper_bound"])

            # Store game data in session
            session["lower_bound"] = lower_bound
            session["upper_bound"] = upper_bound
            session["number_to_guess"] = random.randint(lower_bound, upper_bound)
            session["attempts"] = 0  # Initialize attempts count
            return redirect(url_for("guessing_game"))

        elif "guess" in request.form:
            # Process the user's guess
            guess = int(request.form["guess"])
            lower_bound = session.get("lower_bound")
            upper_bound = session.get("upper_bound")
            number_to_guess = session.get("number_to_guess")

            # Check if session["attempts"] is already set; initialize it if not
            if "attempts" not in session:
                session["attempts"] = 0
            session["attempts"] += 1

            # Evaluate the guess
            if guess < lower_bound or guess > upper_bound:
                message = "Your guess is out of bounds. Try again!"
            elif guess < number_to_guess:
                message = "Your guess is too low. Try again!"
            elif guess > number_to_guess:
                message = "Your guess is too high. Try again!"
            else:
                message = f"Congratulations! You guessed the number in {session['attempts']} attempts."
                session.clear()  # Clear the session for a new game

            return render_template("index.html", message=message, lower_bound=lower_bound, upper_bound=upper_bound, attempts=session.get("attempts"))

    # GET request - Show the initial form
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
