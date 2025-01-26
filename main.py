from flask import Flask, render_template, request, jsonify
import hashlib

app = Flask(__name__)

# Predefined password list
PASSWORD_LIST = [
    "123456", "password", "123456789", "12345678", "12345",
    "1234567", "qwerty", "abc123", "password1", "letmein",
    "welcome", "admin", "iloveyou", "sunshine", "monkey", "hello"
]

def convert_text_to_hash(text, algorithm):
    """Converts plaintext into the specified hash."""
    if algorithm == "SHA1":
        return hashlib.sha1(text.encode()).hexdigest()
    elif algorithm == "MD5":
        return hashlib.md5(text.encode()).hexdigest()
    else:
        raise ValueError("Unsupported algorithm")

def crack_password(hash_to_crack, algorithm):
    """Attempts to find the plaintext password for the given hash."""
    for password in PASSWORD_LIST:
        converted_hash = convert_text_to_hash(password, algorithm)
        if hash_to_crack == converted_hash:
            return password  # Return the found password
    return None  # Return None if no match is found

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crack', methods=['POST'])
def crack():
    try:
        data = request.json
        hash_to_crack = data.get('hash').strip().lower()
        algorithm = data.get('algorithm')

        if not hash_to_crack or not algorithm:
            return jsonify({"error": "Hash and algorithm are required"}), 400

        password = crack_password(hash_to_crack, algorithm)
        if password:
            return jsonify({"password": password})
        else:
            return jsonify({"password": None})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
