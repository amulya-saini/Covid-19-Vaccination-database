import pymysql
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the values from the web form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        cov_id = request.form['cov_id']

        # Connect to the database and find the matching value in the specified column
        conn = pymysql.connect(
            host='localhost',
            user='***',
            password='***',
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
            return 'Vaccinated'
        else:
            return 'Not Vaccinated'
    else:
        return '''
        <form method="post">
            <label>First Name:</label><br>
            <input type="text" name="first_name"><br>
            <label>Last Name:</label><br>
            <input type="text" name="last_name"><br>
            <label>Cov ID:</label><br>
            <input type="text" name="cov_id"><br><br>
            <input type="submit" value="Submit">
        </form>
        '''

if __name__ == '__main__':
    app.run(debug=True)
