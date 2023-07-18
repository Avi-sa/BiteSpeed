# BiteSpeed Identifier

## Steps to run locally:
1. clone the repo.
2. go to the cloned directory.
3. open terminal
4. virtualenv venv
5. source venv/bin/activate
6. pip3 install -r requirements.txt
7. python3 manage.py runserver



curl to hit

curl --location --request POST 'http://127.0.0.1:8000/customers/identify/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "avi@gmailq.com",
    "phoneNumber": 6205321301
}'
