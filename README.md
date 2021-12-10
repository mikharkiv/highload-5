## HOW TO RUN:
`docker compose up --build`

## WHERE TO FIND:
https://localhost:5000/

### Add the book.
```http request
POST https://localhost:5000/add-book/
```     
**Body**: JSON object with fields name, author, comment.  
Example: `{"name": "1name","author": "1author", "comment": "1comment"}`  
**Response**: created object if everything is ok, error if error.

### Get the book.
```http request
GET https://localhost:5000/<BOOK_NAME>/ 
```
**Response**: book object or 404.

Regards, _Mykhailo Postnikov_.