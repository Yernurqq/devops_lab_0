from flask import Flask, render_template_string
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# PostgreSQL connection parameters -- UPDATED
DB_CONFIG = {
    "host": "192.168.249.132",
    "port": 5432,
    "dbname": "devops_db",
    "user": "devops_user",
    "password": "StrongP@ssw0rd!",
    "sslmode": "require"  # <-- ADD THIS LINE
}

# Simple HTML template with Bootstrap 5 and error display
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>DevOps Lab</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
        rel="stylesheet">
  <style>
    body {
      background-color: #f8f9fa;
    }
    .container {
      max-width: 960px;
    }
    .table {
      box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
    }
  </style>
</head>
<body>
<div class="container py-5">
  <div class="text-center mb-4">
    <h1 class="display-5">DevOps Lab Database Contents</h1>
    <p class="lead text-muted">A live view of the <code>devops_lab</code> table.</p>
  </div>
  {% if error %}
    <div class="alert alert-danger" role="alert">
      <strong>Error:</strong> {{ error }}
    </div>
  {% elif rows %}
  <div class="table-responsive">
    <table class="table table-striped table-hover table-bordered">
      <thead class="table-dark">
        <tr>
          {% for col in rows[0].keys() %}
          <th>{{ col | capitalize }}</th>
          {% endfor %}
        </tr>
      </thead>
      <tbody>
        {% for row in rows %}
        <tr>
          {% for val in row.values() %}
          <td>{{ val }}</td>
          {% endfor %}
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
  {% else %}
  <div class="alert alert-info" role="alert">
    No data found in the <code>devops_lab</code> table.
  </div>
  {% endif %}
</div>
</body>
</html>
"""

def fetch_data():
    """Return all rows from devops_lab or an error string."""
    query = "SELECT * FROM devops_lab ORDER BY id;"
    try:
        # The **DB_CONFIG unpacks all key-value pairs as arguments
        conn = psycopg2.connect(**DB_CONFIG)
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            data = cur.fetchall()
        conn.close()
        return data, None
    except psycopg2.OperationalError as e:
        # Return a user-friendly error message for connection issues
        return None, f"Could not connect to the database. Please check the network, firewall, and credentials. Details: {e}"
    except Exception as e:
        return None, f"An unexpected error occurred: {e}"


@app.route("/")
def index():
    rows, error = fetch_data()
    return render_template_string(HTML_TEMPLATE, rows=rows, error=error)

if __name__ == "__main__":
    # Listen on all interfaces so the VM’s IP is reachable
    app.run(host="0.0.0.0", port=5000, debug=True) # Set debug=True for better error messages during development
