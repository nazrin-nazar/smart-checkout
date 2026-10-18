# Smart Self Checkout Retail System

A web application where customers scan product QR codes with their phone
camera, add items to a cart and get an automatic bill.

## Features
- Product management (add, edit and delete products) through the Django admin panel
- QR code generation for each product
- QR scanning in the phone browser using html5-qrcode
- Automatic bill calculation and order finalization

## Tech Stack
Python, Django, SQLite, HTML, CSS, JavaScript, html5-qrcode

## How to Run

1. Clone the repo
```
git clone https://github.com/nazrin-nazar/smart-checkout.git
cd smart_checkout
```

2. Create and activate a virtual environment
```
python -m venv venv
venv\Scripts\activate
```

3. Install packages
```
pip install -r requirements.txt
```

4. Set up the database
```
python manage.py migrate
```

5. Start the server
```
python manage.py runserver
```

Note: phone camera scanning needs HTTPS. For testing on a phone, use ngrok.

## Future Improvements
- Counter payment with cashier verification
- Cashier login
- Stock management
- Payment gateway integration
