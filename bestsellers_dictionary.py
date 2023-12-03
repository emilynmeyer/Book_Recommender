'''The get_NYT_BookList() function reads in json data from the NYT Bestsellers API
    it then stores information from that data in a nested dictionary,
    which includes ['isbn']['title', 'author', and 'description'].
    
    The google_Description(isbn) function calls the google books api and returns the
    books description if there is one, otherwise it returns an empty string'''

import requests
import json
import config
import pickle

def get_NYT_BookList():

    NYT_API = requests.get('https://api.nytimes.com/svc/books/v3/lists/full-overview/current.json?api-key=' + config.api_key)
    nyt = NYT_API.text
    nyt_data = json.loads(nyt)

    results = nyt_data['results']
    lists = results['lists']

    #bestseller_list = [] #There are multiple bestsellers lists on the NYT. This is a list of the lists of bestsellers.
    ISBN = [] #unique key to look up books
    book_list = {} #using ISBN13 as the key. Provides a dictionary with title, author, description

    for i in range(len(lists)):
        bestseller_list = lists[i].get('books') #get only the books from the bestseller list
        for j in range(len(bestseller_list)):
            isbn = bestseller_list[j].get('primary_isbn13')
            if len(isbn) == 13:
                ISBN.append(isbn)
                book_list[isbn] = {}
                book_list[isbn]['title'] = title = bestseller_list[j].get('title') #within the book list, get the title
                book_list[isbn]['author'] = bestseller_list[j].get('author')
                description = bestseller_list[j].get('description').lower() #within the book list, get the description
                if description == '':
                    description = google_Description(isbn)
                book_list[isbn]['description'] = description #dictionary with title as key and description as value

    return book_list

def google_Description(isbn):
    GOOGLE_API = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn)
    google = GOOGLE_API.text
    google_data = json.loads(google)
    if 'items' in google_data.keys():
        google_volumeInfo = google_data['items'][0].get('volumeInfo')
        if 'description' in google_volumeInfo.keys():
            google_description = google_volumeInfo['description']
            return google_description
        else:
            return ''
    else:
        return ''
    
book_list = get_NYT_BookList()

with open('book_List.pkl', 'wb') as f:
    pickle.dump(book_list, f)
