# Pizza Management System

A comprehensive Flask-based Pizza Management System with employee authentication, customer management, order processing with sales tax calculations, and real-time dashboard analytics.

## Features

- **Employee Authentication** - Secure login system using Flask-Login with password hashing
- **Dynamic Dashboard** - Real-time sales metrics, recent orders, and top-selling pizzas
- **Customer Management** - Full CRUD operations with modal-based interface
- **Pizza Menu Management** - Manage pizzas with multiple sizes, categories, and pricing
- **Order Processing** - Create orders with automatic sales tax calculation (default 7%)
- **Employee Management** - Manage staff with roles and hire dates
- **Dual Navigation System** - Top navbar + sidebar for easy navigation
- **Responsive Design** - Bootstrap 5 with custom pizza-themed styling

## Database Schema

The system uses MySQL with five related tables:

1. **employees** - Employee authentication and management
2. **customers** - Customer information and contact details
3. **pizzas** - Pizza menu items with pricing and availability
4. **orders** - Order headers with totals and tax calculations
5. **order_details** - Individual pizza items within orders

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database

The `.env` file is already configured with your database credentials.

```bash
python app/init_db.py
```

### 3. Run the Application

```bash
python app.py
```

### 4. Access the Application

Open your browser and navigate to: `http://localhost:5000`

**Default Login Credentials:**
- Email: `john.manager@pizzashop.com`
- Password: `password123`

## Project Structure

```
Demo-5-Pizza/
├── app/
│   ├── __init__.py              # App initialization and Flask-Login setup
│   ├── models.py                # Data models (Employee, Customer, Pizza, Order, OrderDetail)
│   ├── db_service.py            # Database operations layer
│   ├── init_db.py               # Database initialization script
│   ├── blueprints/
│   │   ├── auth.py              # Authentication routes
│   │   ├── dashboard.py         # Dashboard with analytics
│   │   ├── customers.py         # Customer CRUD
│   │   ├── pizzas.py            # Pizza CRUD
│   │   ├── orders.py            # Order management with tax
│   │   └── employees.py         # Employee CRUD
│   └── templates/
│       ├── base.html            # Base template with dual navigation
│       ├── auth/                # Login templates
│       ├── dashboard/           # Dashboard templates
│       ├── customers/           # Customer management templates
│       ├── pizzas/              # Pizza management templates
│       ├── orders/              # Order processing templates
│       └── employees/           # Employee management templates
├── app.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (database config)
└── README.md                    # This file
```

## Key Features

### Dashboard Analytics
- Total sales amount
- Total number of orders
- Customer count
- Pending orders count
- Recent orders list (last 5)
- Top-selling pizzas
- Sales breakdown by status

### Order Processing with Sales Tax
- Select customer and pizzas
- Automatic quantity management
- Real-time subtotal calculation
- **Automatic sales tax calculation (default 7%, customizable)**
- Order status tracking (Pending, In Progress, Completed)
- Detailed order view with line items

### Modal-Based CRUD Operations
All management interfaces use Bootstrap modals for:
- Adding new records
- Editing existing records
- Deleting records with confirmation

## Production Deployment

### Using Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Environment Variables

Update `.env` file for production:
```
DB_HOST=your-production-host
DB_USER=your-production-user
DB_PASSWORD=your-secure-password
DB_NAME=your-database-name
SECRET_KEY=generate-a-strong-secret-key
```

## Technologies Used

- **Backend:** Flask 3.1.0, Flask-Login 0.6.3
- **Database:** MySQL with PyMySQL connector
- **Frontend:** Bootstrap 5, Font Awesome 6, jQuery
- **Security:** Werkzeug password hashing
- **Server:** Gunicorn for production

## Sample Data

The system includes sample data for testing:
- 3 employees (Manager, Cashier, Chef)
- 5 customers
- 15 pizzas (3 sizes for 5 different types)
- 3 sample orders with order details and tax calculations

## License

This project is created for educational purposes.