# Art Marketplace

A web-based platform for browsing and purchasing unique artwork.  
Built with **Django**, this project demonstrates full-stack web development including authentication, product management, cart functionality, and dynamic UI rendering.

---

## Features

1. Browse art products with images and details  
2. Search functionality for products  
3. User authentication (login, logout, profile)  
4. Shopping cart system  
5. Checkout with receipt generation  
6. XML serialization for products and receipts  
7. Downloadable receipt support (XML)  
8. Dynamic UI updates (JavaScript-based interactions)  

---

## Tech Stack

- **Backend:** Django (Python)  
- **Frontend:** HTML, CSS, JavaScript  
- **Templating:** Django Templates + XSLT (partially used)  
- **Database:** SQLite (development)  
- **Other:** XML processing (ElementTree)  

---

## Current Status

Product filtering functionality is currently under development.

1. git clone https://github.com/your-username/art-marketplace.git
2. cd art-marketplace
3. python -m venv venv 
4. On Windows:
   venv\Scripts\activate
   On Unix or MacOS:
   source venv/bin/activate
5. pip install -r requirements.txt
6. python manage.py migrate
7. python manage.py runserver