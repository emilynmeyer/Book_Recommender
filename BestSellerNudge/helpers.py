import requests

def get_book_description(query):
    api_url = 'https://www.googleapis.com/books/v1/volumes'
    
    if(query.isdigit()):
        params = {'q': 'isbn:' + query}
    else:
        params = {'q': 'intitle:' + query}
    
    response = requests.get(api_url, params=params)

    if(response.status_code == 200):
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            book_info = data['items'][0]['volumeInfo']
            return book_info.get('description')

def get_book_data(isbns):
    api_url = 'https://www.googleapis.com/books/v1/volumes'
    book_data = []
    for isbn in isbns:
        params = {'q': 'isbn:' + isbn}
        response = requests.get(api_url, params=params)
        if(response.status_code == 200):
            data = response.json()
            if 'items' in data and len(data['items']) > 0:
                book_info = data['items'][0]['volumeInfo']
                title = book_info.get('title')
                thumbnail =  book_info.get('imageLinks')['thumbnail']
                author = book_info.get('authors')[0]
                book_data.append([title, thumbnail, author])
    return book_data
        

    




#print(get_book_description('1338878921'))
#print(get_book_description('Harry Potter and the Sorcerer''s Stone'))
#print(get_book_data(['1338878921', '1338878921']))