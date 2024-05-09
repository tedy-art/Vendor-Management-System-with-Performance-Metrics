
# Vendor Management System API

## Setup Instructions

Follow these steps to set up the project on your local machine:

1. **Clone Repository:**
   ```
   git clone https://github.com/tedy-art/Vendor-Management-System-with-Performance-Metrics.git
   ```

2. **Install Dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Run Django Development Server:**
   ```
   python manage.py runserver
   ```

## Authentication

To access the API endpoints, you need to authenticate using token-based authentication. Obtain an authentication token by sending a POST request to `/api/token/` with your username and password. Include the token in the Authorization header of subsequent requests.


## API Endpoints

### Vendors

- **GET /api/vendors/**
  - Retrieves a list of all vendors.
- **POST /api/vendors/**
  - Creates a new vendor.
- **GET /api/vendors/{vendor_id}/**
  - Retrieves details of a specific vendor.
- **PUT /api/vendors/{vendor_id}/update/**
  - Updates details of a specific vendor.
- **DELETE /api/vendors/{vendor_id}/delete/**
  - Deletes a specific vendor.
- **GET /api/vendors/{vendor_id}/performance/**
  - Retrieves performance metrics for a specific vendor.

### Purchase Orders

- **GET /api/purchase_orders/**
  - Retrieves a list of all purchase orders.
- **POST /api/purchase_orders/**
  - Creates a new purchase order.
- **GET /api/purchase_orders/{po_id}/**
  - Retrieves details of a specific purchase order.
- **PUT /api/purchase_orders/{po_id}/update/**
  - Updates details of a specific purchase order.
- **DELETE /api/purchase_orders/{po_id}/delete/**
  - Deletes a specific purchase order.
- **POST /api/purchase_orders/{po_id}/acknowledge/**
  - Acknowledges a purchase order.

### Historical Performance

- **GET /api/historical_performances/**
  - Retrieves a list of historical performance records.
- **POST /api/historical_performances/**
  - Creates a new historical performance record.
- **GET /api/historical_performances/{pk}/**
  - Retrieves details of a specific historical performance record.
- **PUT /api/historical_performances/{pk}/update/**
  - Updates details of a specific historical performance record.
- **DELETE /api/historical_performances/{pk}/delete/**
  - Deletes a specific historical performance record.


## Using the API

To interact with the API, you can use tools like cURL, Postman, or make HTTP requests from your code. Make sure to include the required authorization token in the headers of your requests.
