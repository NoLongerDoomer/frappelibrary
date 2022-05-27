import MySQLdb.cursors
from matplotlib.pyplot import get
import requests
from flask import Flask, jsonify, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Swarup@4202'
app.config['MYSQL_DB'] = 'frappelibrary'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/home')
def homeagain():
    return jsonify({"data": render_template("home.html")})


@app.route('/insertintodb')
def getdata():
    response_arary = request.form.get("data")
    # request.
    # api_url = "https://frappe.io/api/method/frappe-library"
    # response = requests.get(api_url)
    # response_array = response.json().get("message")
    putdata(response_arary)
    return "yooo"

def putdata(response):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    for x in response:
        # cursor.callproc('insertbooks', [x['bookID'], x['title'], x['authors'], x['average_rating'], x['isbn'],
        #                                 x['isbn13'], x['language_code'], x['num_pages'], x['ratings_count'],
        #                                 x['text_reviews_count'], x['publication_date'], x['publisher']])
        cursor.callproc('insertbooks',)
        mysql.connection.commit()
    cursor.close()

@app.route('/importbooks', methods=['POST'])
def importbooks(): 
    response_arary = request.get_json("rowArray")
    response_array = response_arary['rowArray']
    importbooksmethod(response_array)
    return "Success"

def importbooksmethod(x):
    print(x[0])
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.callproc('insertbooks',[x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11],x[12]])
    mysql.connection.commit()
    cursor.close()

@app.route('/getbooksfromfrappe', methods=['POST'])
def getbooksfromapi() :
    url = request.form.get("apiurl")
    response = requests.get("https://frappe.io/api/method/frappe-library?"+url)
    response_array = response.json().get("message")
    return jsonify({"data": render_template("books-table-api.html", books = response_array)})

@app.route('/getbooks')
def books():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from books")
    list = cursor.fetchall()
    return jsonify({"data": render_template("books-table.html", books=list)})


@app.route('/delete')
def deletebooks():
    id = request.args.get('bookID')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('delete from books where bookID = {0}'.format(id))
    mysql.connection.commit()
    return render_template("ind ex.html")


@app.route('/updatebooks', methods=['POST'])
def updatebooks():
    column = request.form.get("column")
    value = request.form.get("value")
    id = request.form.get("id")
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("update books set {0} = '{1}' where bookID = {2}".format(column, value, id))
    mysql.connection.commit()
    return jsonify({"data": "Updated"})


@app.route('/footerenable')
def footercheck():
    return render_template("index.html", siteinclude="footer.html")


if __name__ == "__main__":
    app.run(debug=True)
