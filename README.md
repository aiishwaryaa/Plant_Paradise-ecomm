# Plants Paradise 🌿

A beautiful, animated e-commerce website for home plants built with Flask, Bootstrap, and SQLite. Features a soothing green theme with smooth animations and cursor effects.

## Features ✨

- **Beautiful UI**: Soothing green theme with nature-inspired design
- **User Authentication**: Sign up, login, and profile management
- **Plant Catalog**: Browse and filter plants by category and price
- **Shopping Cart**: Add, view, and manage cart items
- **Checkout System**: Complete billing and payment process
- **Order History**: Track your plant purchases
- **Dashboard**: User statistics and quick actions
- **Animations**: Smooth transitions and cursor animations
- **Responsive Design**: Works on all devices

## Technologies Used 🛠️

- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Authentication**: Flask-Login
- **Styling**: Custom CSS with green theme and animations

## Installation & Setup 🚀

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ecomm-py
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the website**
   Open your browser and go to `http://localhost:5000`

## Project Structure 📁

```
ecomm-py/
├── app.py              # Main Flask application
├── models.py           # Database models
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
├── static/
│   └── style.css      # Custom CSS styles
└── templates/
    ├── base.html      # Base template
    ├── home.html      # Home page
    ├── about.html     # About page
    ├── cart.html      # Shopping cart
    ├── profile.html   # User profile
    ├── dashboard.html # User dashboard
    ├── billing.html   # Checkout page
    ├── login.html     # Login form
    └── signup.html    # Registration form
```

## Features in Detail 🌟

### Home Page
- Plant catalog with beautiful cards
- Category and price filters
- Add to cart functionality
- Responsive grid layout

### Authentication
- User registration and login
- Secure password hashing
- Session management
- Protected routes

### Shopping Cart
- Add/remove items
- Quantity management
- Order summary
- Proceed to checkout

### Checkout
- Shipping information form
- Payment details
- Order confirmation
- Order history tracking

### Dashboard
- User statistics
- Recent activity
- Quick actions
- Order overview

## Database Schema 🗄️

- **Users**: User accounts and authentication
- **Plants**: Product catalog with images and details
- **CartItems**: Shopping cart contents
- **Orders**: Order history and status
- **OrderItems**: Individual items in orders

## Customization 🎨

### Theme Colors
The application uses a soothing green theme:
- Primary: `#4caf50` (Green)
- Secondary: `#81c784` (Light Green)
- Background: `#e8f5e9` (Very Light Green)

### Animations
- Hover effects on cards and buttons
- Fade-in animations for plant cards
- Smooth transitions throughout
- Custom cursor with leaf design

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License 📄

This project is open source and available under the MIT License.

---

**Plants Paradise** - Bringing nature to your home, one plant at a time! 🌱 