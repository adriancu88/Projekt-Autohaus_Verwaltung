from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Datenbank-Konfigurationsdetails
db_config = {
    'user': 'user',
    'password': 'pa$$w0rd',
    'host': 'localhost',
    'database': 'autohaus_verwaltungssystem',
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search_term']
    
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM Kunden WHERE Nachname = %s"
    params = (search_term,)

    cursor.execute(query, params)
    customer_info = cursor.fetchone()

    if customer_info:
        print("Kundendaten abgerufen:")
        print("Vorname:", customer_info[1])
        print("Nachname:", customer_info[2])
        print("Adresse:", customer_info[3])
        print("Telefonnummer:", customer_info[4])
        print("Email:", customer_info[5])
    else:
        print("Kundenname nicht im System zu finden.")

    cursor.close()
    conn.close()

    return render_template('search_results.html', customer_info=customer_info)

if __name__ == '__main__':
    app.run(debug=True)
