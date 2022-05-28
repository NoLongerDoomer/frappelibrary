import MySQLdb.cursors
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
    cursor.execute("select b.book_id, b.title, b.authors, b.average_rating, b.isbn, b.isbn13, b.language_code, b.num_page, b.ratings_count," +
    "b.text_reviews_count, b.publication_date, b.publisher, bc.count from books b inner join books_count bc on b.book_id = bc.book_id")
    list = cursor.fetchall()
    return jsonify({"data": render_template("books-table.html", books=list)})


@app.route('/deletebooks', methods=['POST'])
def deletebooks():
    response_arary = request.get_json("arrayOfValues")
    response_array = response_arary['arrayOfValues']
    print(response_array)
    for item in response_array:
        deletebooksmethod(item)
    return "Success"

def deletebooksmethod(id):
    print(id)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.callproc('deletebooks',[id])
    mysql.connection.commit()
    cursor.close()

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
