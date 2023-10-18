import pymysql
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/click.html', methods=['GET', 'POST'])
def click():
    if request.method == 'POST':
        # Get the values from the web form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        cov_id = request.form['id_number']

        # Connect to the database and find the matching value in the specified column
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='Qwer123$',
            database='vaccine_database',
            cursorclass=pymysql.cursors.DictCursor
        )
        cur = conn.cursor()
        query = '''
        SELECT vaccination_information.dose_2 
        FROM vaccination_information 
        INNER JOIN Personal_details 
        ON vaccination_information.vaccine_id = Personal_details.vaccine_id 
        WHERE Personal_details.first_name = %s AND Personal_details.last_name = %s AND Personal_details.Cov_id = %s
        '''
        cur.execute(query, (first_name, last_name, cov_id))
        result = cur.fetchone()
        conn.close()

        if result and result['dose_2']:
            return render_template('vaccination_status.html', vaccinated=True)
        else:
            return render_template('vaccination_status.html', vaccinated=False)
    else:
        return render_template('click.html')

@app.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)