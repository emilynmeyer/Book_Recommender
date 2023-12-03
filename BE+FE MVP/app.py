from flask import Flask, render_template, request
import requests
from helpers import get_book_description, get_book_data
from retrieval import get_top_five

app = Flask(__name__)


    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/retrieve')
def retrieve():
    query = request.args.get('query')
    description = get_book_description(query)
    isbns = get_top_five(description)
    print(isbns)
    book_data = get_book_data(isbns)
    return render_template('book-list.html', books=book_data)
    

if __name__ == '__main__':
    app.run(debug=True)