from flask import Flask, render_template, send_file, make_response, request
from flask_mysqldb import MySQL
import pandas as pd
from sklearn.svm import SVR
from io import BytesIO
import base64
import pymysql
from sqlalchemy import create_engine
import numpy as np
import matplotlib.pyplot as plt


app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'skripsi'
mysql.init_app(app)


@app.route("/")
def main():
    cur = mysql.connection.cursor()
    cur.execute('''INSERT IGNORE INTO travel(day,arrival,departure,time,elapsed,distance)
                    SELECT DISTINCT 
                        a.day as day, 
                        b.time as arrival, 
                        a.time as departure, 
                        TIME_TO_SEC(TIMEDIFF(MAX(a.time),MAX(b.time))) as time, 
                        TIME_TO_SEC(TIMEDIFF(MAX(a.time),MAX(b.time)))/3600 as elapsed, 
                        111.111 
                        * DEGREES(ACOS(COS(RADIANS(a.Latitude)) 
                        * COS(RADIANS(b.Latitude)) 
                        * COS(RADIANS(a.Longitude - b.Longitude)) 
                        + SIN(RADIANS(a.Latitude)) 
                        * SIN(RADIANS(b.Latitude)))) 
                        AS distance_in_km 
                    FROM logger AS a 
                    JOIN logger AS b ON a.id_logger <> b.id_logger 
                    WHERE a.aid=b.aid AND b.time <= a.time AND a.day=b.day;''')
    mysql.connection.commit()
    return render_template('index.html')

@app.route("/build_plot",methods=['POST'])
def build_plot():
    engine = create_engine('mysql+pymysql://root:@localhost/skripsi')
    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
    if request.method == 'POST':
        if (request.form['hari']) == "Senin":    
            x = pd.read_sql_query('''SELECT day,arrival FROM travel where day=1''', engine)
            x = x.as_matrix()
            y = pd.read_sql_query('''SELECT elapsed FROM travel where day=1''', engine)
            y = y.as_matrix()
            y_rbf = svr_rbf.fit(x, y.ravel()).predict(x)
            img = BytesIO()
            plt.plot(y_rbf, y_rbf, color='navy', label='Prediksi Waktu Tempuh')
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return '<img src="data:image/png;base64,{}">'.format(plot_url)


        elif (request.form['hari']) == "Selasa":
            x = pd.read_sql_query('''SELECT day,arrival FROM travel where day=2''', engine)
            x = x.as_matrix()
            y = pd.read_sql_query('''SELECT elapsed FROM travel where day=2''', engine)
            y = y.as_matrix()
            y_rbf = svr_rbf.fit(x, y.ravel()).predict(x)
            plt.plot(x, y_rbf, color='navy', label='Prediksi Waktu Tempuh')
            img = BytesIO()
            plt.plot(x, y_rbf, color='navy', label='Prediksi Waktu Tempuh')
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return '<img src="data:image/png;base64,{}">'.format(plot_url)

        elif (request.form['hari']) == "Rabu":
            x = pd.read_sql_query('''SELECT day,arrival FROM travel where day=3''', engine)
            x = x.as_matrix()
            y = pd.read_sql_query('''SELECT elapsed FROM travel where day=3''', engine)
            y = y.as_matrix()
            y_rbf = svr_rbf.fit(x, y.ravel()).predict(x)
            plt.plot(x, y_rbf, color='navy', label='Prediksi Waktu Tempuh')
            img = BytesIO()
            plt.plot(x, y_rbf, color='navy', label='Prediksi Waktu Tempuh')
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return 'index.html, <img src="data:image/png;base64,{}">'.format(plot_url)

        elif (request.form['hari']) == "Kamis":
            x = pd.read_sql_query('''SELECT day,arrival FROM travel where day=4''', engine)
            x = x.as_matrix()
            y = pd.read_sql_query('''SELECT elapsed FROM travel where day=4''', engine)
            y = y.as_matrix()
            y_rbf = svr_rbf.fit(x, y.ravel()).predict(x)
            plt.plot(x, y_rbf, color='navy', label='Prediksi Waktu Tempuh')
            img = BytesIO()
            plt.plot(x, y_rbf, color='navy', label='Prediksi Waktu Tempuh')
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return '<img src="data:image/png;base64,{}">'.format(plot_url)

        elif (request.form['hari']) == "Jumat":
            x = pd.read_sql_query('''SELECT day,arrival FROM travel where day=5''', engine)
            x = x.as_matrix()
            y = pd.read_sql_query('''SELECT elapsed FROM travel where day=5''', engine)
            y = y.as_matrix()
            y_rbf = svr_rbf.fit(x, y.ravel()).predict(x)
            plt.plot(x, y_rbf, color='navy', label='Prediksi Waktu Tempuh')
            img = BytesIO()
            plt.plot(x, y_rbf, color='navy', label='Prediksi Waktu Tempuh')
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return '<img src="data:image/png;base64,{}">'.format(plot_url)
        else:
            return render_template('index.html')

if __name__ == "__main__":
    app.run()
