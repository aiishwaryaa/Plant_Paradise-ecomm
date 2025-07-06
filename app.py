from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from models import db, User, Plant, CartItem, Order, OrderItem

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants_paradise.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Admin decorator
def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Access denied. Admin privileges required.')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Sample plant data
sample_plants = [
    {
        'name': 'Monstera Deliciosa',
        'description': 'Beautiful Swiss cheese plant with distinctive leaf holes and splits. Perfect for creating a tropical atmosphere.',
        'price': 45.99,
        'image_url': 'https://images.unsplash.com/photo-1614594975525-e45190c55d0b?auto=format&fit=crop&w=400&q=80',
        'category': 'Indoor',
        'stock': 10
    },
    {
        'name': 'Snake Plant (Sansevieria)',
        'description': 'Low-maintenance air-purifying plant perfect for beginners. Releases oxygen at night.',
        'price': 29.99,
        'image_url': 'https://images.unsplash.com/photo-1593691509543-c55fb32e5cee?auto=format&fit=crop&w=400&q=80',
        'category': 'Indoor',
        'stock': 15
    },
    {
        'name': 'Peace Lily',
        'description': 'Elegant flowering plant that purifies indoor air and adds beauty to any space.',
        'price': 35.99,
        'image_url': 'https://images.unsplash.com/photo-1593691509543-c55fb32e5cee?auto=format&fit=crop&w=400&q=80',
        'category': 'Indoor',
        'stock': 8
    },
    {
        'name': 'Fiddle Leaf Fig',
        'description': 'Stunning large-leafed plant that makes a statement in any room. Popular for modern interiors.',
        'price': 89.99,
        'image_url': 'https://images.unsplash.com/photo-1614594975525-e45190c55d0b?auto=format&fit=crop&w=400&q=80',
        'category': 'Indoor',
        'stock': 5
    },
    {
        'name': 'Aloe Vera',
        'description': 'Medicinal succulent with healing properties. Perfect for natural skincare and home remedies.',
        'price': 19.99,
        'image_url': 'https://images.unsplash.com/photo-1593691509543-c55fb32e5cee?auto=format&fit=crop&w=400&q=80',
        'category': 'Succulent',
        'stock': 20
    },
    {
        'name': 'Echeveria Elegans',
        'description': 'Beautiful rosette-forming succulent with pink edges. Drought-resistant and easy to care for.',
        'price': 15.99,
        'image_url': 'https://images.unsplash.com/photo-1614594975525-e45190c55d0b?auto=format&fit=crop&w=400&q=80',
        'category': 'Succulent',
        'stock': 25
    },
    {
        'name': 'Jade Plant',
        'description': 'Symbol of good luck and prosperity. Thick, glossy leaves that store water efficiently.',
        'price': 24.99,
        'image_url': 'https://images.unsplash.com/photo-1593691509543-c55fb32e5cee?auto=format&fit=crop&w=400&q=80',
        'category': 'Succulent',
        'stock': 12
    },
    {
        'name': 'ZZ Plant',
        'description': 'Nearly indestructible plant with glossy leaves. Perfect for low-light conditions.',
        'price': 39.99,
        'image_url': 'https://images.unsplash.com/photo-1614594975525-e45190c55d0b?auto=format&fit=crop&w=400&q=80',
        'category': 'Indoor',
        'stock': 18
    },
    {
        'name': 'Pothos Golden',
        'description': 'Trailing vine with heart-shaped variegated leaves. Excellent for hanging baskets.',
        'price': 22.99,
        'image_url': 'https://images.unsplash.com/photo-1593691509543-c55fb32e5cee?auto=format&fit=crop&w=400&q=80',
        'category': 'Indoor',
        'stock': 30
    },
    {
        'name': 'Lavender',
        'description': 'Fragrant outdoor herb with purple flowers. Perfect for gardens and aromatherapy.',
        'price': 18.99,
        'image_url': 'https://images.unsplash.com/photo-1614594975525-e45190c55d0b?auto=format&fit=crop&w=400&q=80',
        'category': 'Outdoor',
        'stock': 15
    },
    {
        'name': 'Rose Bush',
        'description': 'Classic flowering shrub with beautiful blooms. Available in various colors.',
        'price': 34.99,
        'image_url': 'https://images.unsplash.com/photo-1593691509543-c55fb32e5cee?auto=format&fit=crop&w=400&q=80',
        'category': 'Outdoor',
        'stock': 8
    },
    {
        'name': 'Hydrangea',
        'description': 'Large flowering shrub with stunning blue blooms. Changes color based on soil pH.',
        'price': 42.99,
        'image_url': 'https://images.unsplash.com/photo-1614594975525-e45190c55d0b?auto=format&fit=crop&w=400&q=80',
        'category': 'Outdoor',
        'stock': 6
    },
    {
        'name': 'Spider Plant',
        'description': 'Easy-care plant that produces baby plantlets. Excellent air purifier.',
        'price': 16.99,
        'image_url': 'https://images.unsplash.com/photo-1593691509543-c55fb32e5cee?auto=format&fit=crop&w=400&q=80',
        'category': 'Indoor',
        'stock': 22
    },
    {
        'name': 'Haworthia',
        'description': 'Small succulent with distinctive white stripes. Perfect for windowsills and small spaces.',
        'price': 12.99,
        'image_url': 'https://images.unsplash.com/photo-1614594975525-e45190c55d0b?auto=format&fit=crop&w=400&q=80',
        'category': 'Succulent',
        'stock': 35
    },
    {
        'name': 'Bamboo Palm',
        'description': 'Tropical palm that adds height and drama. Creates a lush, jungle-like atmosphere.',
        'price': 55.99,
        'image_url': 'https://images.unsplash.com/photo-1593691509543-c55fb32e5cee?auto=format&fit=crop&w=400&q=80',
        'category': 'Indoor',
        'stock': 7
    },
    {
        'name': 'Philodendron Brasil',
        'description': 'Stunning variegated leaves with yellow and green stripes. Fast-growing and easy to care for.',
        'price': 38.99,
        'image_url': 'https://images.unsplash.com/photo-1614594975525-e45190c55d0b?auto=format&fit=crop&w=400&q=80',
        'category': 'Indoor',
        'stock': 14
    },
    {
        'name': 'String of Pearls',
        'description': 'Unique trailing succulent with bead-like leaves. Perfect for hanging planters.',
        'price': 21.99,
        'image_url': 'https://images.unsplash.com/photo-1593691509543-c55fb32e5cee?auto=format&fit=crop&w=400&q=80',
        'category': 'Succulent',
        'stock': 18
    },
    {
        'name': 'Bird of Paradise',
        'description': 'Exotic plant with large, banana-like leaves. Creates a tropical paradise feel.',
        'price': 75.99,
        'image_url': 'https://images.unsplash.com/photo-1614594975525-e45190c55d0b?auto=format&fit=crop&w=400&q=80',
        'category': 'Indoor',
        'stock': 4
    },
    {
        'name': 'Chinese Evergreen',
        'description': 'Low-maintenance plant with beautiful variegated leaves. Perfect for offices and homes.',
        'price': 28.99,
        'image_url': 'https://images.unsplash.com/photo-1593691509543-c55fb32e5cee?auto=format&fit=crop&w=400&q=80',
        'category': 'Indoor',
        'stock': 16
    },
    {
        'name': 'Sedum Morganianum',
        'description': 'Burro\'s tail succulent with trailing stems. Beautiful cascading effect.',
        'price': 19.99,
        'image_url': 'https://images.unsplash.com/photo-1614594975525-e45190c55d0b?auto=format&fit=crop&w=400&q=80',
        'category': 'Succulent',
        'stock': 12
    },
    {
        'name': 'Gardenia',
        'description': 'Fragrant flowering shrub with white blooms. Perfect for outdoor gardens.',
        'price': 36.99,
        'image_url': 'https://images.unsplash.com/photo-1614594975525-e45190c55d0b?auto=format&fit=crop&w=400&q=80',
        'category': 'Outdoor',
        'stock': 9
    },
    {
        'name': 'Japanese Maple',
        'description': 'Elegant tree with delicate, colorful foliage. Perfect for landscaping.',
        'price': 65.99,
        'image_url': 'https://images.unsplash.com/photo-1614594975525-e45190c55d0b?auto=format&fit=crop&w=400&q=80',
        'category': 'Outdoor',
        'stock': 6
    },
    {
        'name': 'Calathea Orbifolia',
        'description': 'Stunning plant with large, round leaves and silver stripes. High humidity lover.',
        'price': 49.99,
        'image_url': 'https://images.unsplash.com/photo-1614594975525-e45190c55d0b?auto=format&fit=crop&w=400&q=80',
        'category': 'Indoor',
        'stock': 8
    },
    {
        'name': 'Agave Americana',
        'description': 'Large succulent with dramatic spiky leaves. Perfect for desert gardens.',
        'price': 32.99,
        'image_url': 'https://images.unsplash.com/photo-1614594975525-e45190c55d0b?auto=format&fit=crop&w=400&q=80',
        'category': 'Succulent',
        'stock': 11
    },
    {
        'name': 'Dracaena Marginata',
        'description': 'Dragon tree with thin, arching leaves. Adds height and drama to any space.',
        'price': 44.99,
        'image_url': 'https://images.unsplash.com/photo-1614594975525-e45190c55d0b?auto=format&fit=crop&w=400&q=80',
        'category': 'Indoor',
        'stock': 13
    },
    {
        'name': 'Peony Bush',
        'description': 'Beautiful flowering shrub with large, fragrant blooms. Garden favorite.',
        'price': 29.99,
        'image_url': 'https://images.unsplash.com/photo-1614594975525-e45190c55d0b?auto=format&fit=crop&w=400&q=80',
        'category': 'Outdoor',
        'stock': 10
    }
]

@app.route('/')
def home():
    plants = Plant.query.all()
    return render_template('home.html', plants=plants)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/products')
def products():
    category = request.args.get('category', '')
    min_price = request.args.get('min_price', '')
    max_price = request.args.get('max_price', '')
    
    plants = Plant.query
    
    if category:
        plants = plants.filter_by(category=category)
    
    if min_price:
        plants = plants.filter(Plant.price >= float(min_price))
    
    if max_price:
        plants = plants.filter(Plant.price <= float(max_price))
    
    plants = plants.all()
    
    categories = db.session.query(Plant.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    return render_template('products.html', plants=plants, categories=categories, selected_category=category)

@app.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.plant.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/profile')
@login_required
def profile():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('profile.html', orders=orders)

@app.route('/dashboard')
@login_required
def dashboard():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.plant.price * item.quantity for item in cart_items)
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('dashboard.html', cart_items=cart_items, total=total, orders=orders)

@app.route('/billing', methods=['GET', 'POST'])
@login_required
def billing():
    if request.method == 'POST':
        # Process the order
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        if not cart_items:
            flash('Your cart is empty!')
            return redirect(url_for('cart'))
        
        total = sum(item.plant.price * item.quantity for item in cart_items)
        
        # Combine address components
        address_parts = [
            request.form.get('address', ''),
            request.form.get('city', ''),
            request.form.get('state', ''),
            request.form.get('zipCode', '')
        ]
        full_address = ', '.join(filter(None, address_parts))
        
        # Create order
        order = Order(
            user_id=current_user.id,
            total_amount=total,
            shipping_address=full_address,
            payment_method=request.form.get('payment_method', 'Credit Card')
        )
        db.session.add(order)
        db.session.flush()  # Get the order ID
        
        # Create order items
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                plant_id=cart_item.plant_id,
                quantity=cart_item.quantity,
                price=cart_item.plant.price
            )
            db.session.add(order_item)
            
            # Update plant stock
            cart_item.plant.stock -= cart_item.quantity
        
        # Clear cart
        for cart_item in cart_items:
            db.session.delete(cart_item)
        
        db.session.commit()
        flash('Order placed successfully! Thank you for your purchase.')
        return redirect(url_for('profile'))
    
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.plant.price * item.quantity for item in cart_items)
    return render_template('billing.html', cart_items=cart_items, total=total)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        password = request.form['password']
        
        # Check if contact (email or mobile) already exists
        existing_user = User.query.filter_by(email=contact).first()
        if existing_user:
            flash('This email or mobile number is already registered')
            return render_template('signup.html')
        
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=contact, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! Please login.')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/add_to_cart/<int:plant_id>')
@login_required
def add_to_cart(plant_id):
    existing_item = CartItem.query.filter_by(user_id=current_user.id, plant_id=plant_id).first()
    
    if existing_item:
        existing_item.quantity += 1
    else:
        new_item = CartItem(user_id=current_user.id, plant_id=plant_id)
        db.session.add(new_item)
    
    db.session.commit()
    flash('Plant added to cart!')
    return redirect(url_for('home'))

# Admin routes
@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    total_users = User.query.count()
    total_orders = Order.query.count()
    total_plants = Plant.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
    
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         total_users=total_users,
                         total_orders=total_orders,
                         total_plants=total_plants,
                         total_revenue=total_revenue,
                         recent_orders=recent_orders,
                         recent_users=recent_users)

@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/orders')
@login_required
@admin_required
def admin_orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@app.route('/admin/plants')
@login_required
@admin_required
def admin_plants():
    plants = Plant.query.all()
    return render_template('admin/plants.html', plants=plants)

@app.route('/admin/user/<int:user_id>')
@login_required
@admin_required
def admin_user_detail(user_id):
    user = User.query.get_or_404(user_id)
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    return render_template('admin/user_detail.html', user=user, orders=orders)

@app.route('/admin/toggle_admin/<int:user_id>')
@login_required
@admin_required
def toggle_admin(user_id):
    user = User.query.get_or_404(user_id)
    if user.id != current_user.id:  # Prevent admin from removing their own admin status
        user.is_admin = not user.is_admin
        db.session.commit()
        flash(f'Admin status for {user.name} has been {"granted" if user.is_admin else "revoked"}')
    else:
        flash('You cannot modify your own admin status')
    return redirect(url_for('admin_users'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Add sample plants if database is empty
        if not Plant.query.first():
            for plant_data in sample_plants:
                plant = Plant(**plant_data)
                db.session.add(plant)
            db.session.commit()
        
        # Create admin user if none exists
        admin_user = User.query.filter_by(is_admin=True).first()
        if not admin_user:
            admin_user = User(
                name='Admin User',
                email='admin@plantsparadise.com',
                password=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created: admin@plantsparadise.com / admin123")
    
    app.run(debug=True) 