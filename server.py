from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)
DB_NAME = 'users.db'

# HTML template with aligned forms and JS handling
HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html>
<head>
    <title>CSSE142 CTF</title>
    <style>
        body { font-family: monospace; background-color: #f5f5f5; padding: 20px; }
        input { width: 150px; }
        button { margin-left: 10px; }
    </style>
</head>
<body>
    <h2>Try to log in:</h2>
    <pre>
{% for user in users %}
<form method="POST" action="/login/{{ loop.index }}" onsubmit="return handleSubmit(this);" style="display:inline;">
User {{ "%03d" % loop.index }}: {{ "%-10s" % user }} | Password: <input type="password" name="password" /> <button type="submit">Login</button>
</form>
{% endfor %}
    </pre>

<script src="/static/main.js"></script>
</body>
</html>
"""

def get_users():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('SELECT username FROM users')
    users = [row[0] for row in cur.fetchall()]
    conn.close()
    return users

@app.route("/", methods=["GET"])
def index():
    users = get_users()
    return render_template_string(HTML_TEMPLATE, users=users)

@app.route("/login/<int:index>", methods=["POST"])
def login(index):
    users = get_users()
    if index < 1 or index > len(users):
        return "Invalid index"

    username = users[index - 1]
    password = request.form["password"]
    vuln_index = int(request.args.get("vuln", -1))

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    if index == vuln_index:
        # Vulnerable raw SQL query
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print(f"[VULNERABLE SQL] {query}")
        try:
            cur.execute(query)
        except Exception as e:
            conn.close()
            return f"<script>alert('SQL error: {e}');</script>"
    else:
        # Safe parameterized query
        cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))

    result = cur.fetchone()
    conn.close()

    if result:
        return "<script>alert('FLAG{c4n_y0u_byp4ss_m3}');</script>"
    else:
        return "<script>alert('Incorrect password!');</script>"

if __name__ == "__main__":
    app.run(debug=True)
