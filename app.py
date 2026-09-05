from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message
from config import Config
from models import db, Product, ProductImage, Order, CustomOrderRequest, Review

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
mail = Mail(app)

with app.app_context():
    db.create_all()

CATEGORIES = ['Calligraphy', 'Islamic Art', 'Acrylic Art']


# ---------------- Cart helpers ----------------
def get_cart():
    return session.setdefault('cart', {})


def calculate_cart(cart):
    items = []
    total = 0
    for key, entry in cart.items():
        product = Product.query.get(entry['product_id'])
        if not product:
            continue
        subtotal = product.price * entry['qty']
        total += subtotal
        items.append({
            'key': key,
            'product': product,
            'format': entry['format'],
            'qty': entry['qty'],
            'subtotal': subtotal
        })
    return items, total


# ---------------- Pages ----------------
@app.route('/')
def home():
    featured = Product.query.filter_by(is_available=True).order_by(Product.created_at.desc()).limit(4).all()
    reviews = Review.query.filter_by(is_approved=True).order_by(Review.created_at.desc()).limit(15).all()
    return render_template('home.html', featured=featured, reviews=reviews)


@app.route('/shop')
def shop():
    category = request.args.get('category')
    query = Product.query
    if category and category in CATEGORIES:
        query = query.filter_by(category=category)
    products = query.order_by(Product.created_at.desc()).all()
    return render_template('shop.html', products=products, categories=CATEGORIES, active_category=category)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html', whatsapp=Config.WHATSAPP_NUMBER)


@app.route('/custom-order', methods=['GET', 'POST'])
def custom_order():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        category = request.form.get('category')
        preferred_format = request.form.get('preferred_format')
        description = request.form.get('description')

        req = CustomOrderRequest(
            name=name, phone=phone, category=category,
            preferred_format=preferred_format, description=description
        )
        db.session.add(req)
        db.session.commit()

        send_custom_order_notification(req)

        flash('Your custom order request has been sent! We will contact you on WhatsApp shortly.', 'success')
        return redirect(url_for('custom_order'))

    return render_template('custom_order.html', categories=CATEGORIES)


# ---------------- Reviews ----------------
@app.route('/review/submit', methods=['POST'])
def submit_review():
    name = request.form.get('name')
    email = request.form.get('email')
    rating = int(request.form.get('rating', 5))
    review_text = request.form.get('review_text')

    review = Review(
        name=name,
        email=email or None,
        rating=rating,
        review_text=review_text,
        is_approved=False
    )
    db.session.add(review)
    db.session.commit()

    send_review_notification(review)

    flash('Thank you! Your review will appear after admin approval.', 'success')
    return redirect(url_for('home') + '#reviews')


# ---------------- Cart ----------------
@app.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    if not product.is_available:
        flash('Ye artwork abhi available nahi hai.', 'error')
        return redirect(url_for('shop'))

    chosen_format = request.form.get('format', product.available_formats()[0])
    cart = get_cart()
    key = f"{product_id}|{chosen_format}"

    if key in cart:
        cart[key]['qty'] += 1
    else:
        cart[key] = {'product_id': product_id, 'format': chosen_format, 'qty': 1}

    session.modified = True
    flash(f'{product.name} ({chosen_format}) cart mein add ho gaya.', 'success')
    return redirect(request.referrer or url_for('shop'))


@app.route('/cart/remove/<path:key>')
def remove_from_cart(key):
    cart = get_cart()
    cart.pop(key, None)
    session.modified = True
    return redirect(url_for('view_cart'))


@app.route('/cart')
def view_cart():
    cart = get_cart()
    items, total = calculate_cart(cart)
    return render_template('cart.html', items=items, total=total)


# ---------------- Checkout ----------------
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = get_cart()
    items, total = calculate_cart(cart)

    if not items:
        flash('Cart khali hai.', 'error')
        return redirect(url_for('shop'))

    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        city = request.form.get('city')

        is_lahore = city.strip().lower() == 'lahore'
        shipping_note = 'Free (within Lahore)' if is_lahore else 'Shipping charges may apply'

        items_summary = ', '.join([f"{i['product'].name} [{i['format']}] x{i['qty']}" for i in items])

        order = Order(
            customer_name=name, phone=phone, address=address, city=city,
            items_summary=items_summary, total_amount=total,
            shipping_note=shipping_note, status='Pending'
        )
        db.session.add(order)
        db.session.commit()

        send_order_notification(order)

        session['cart'] = {}
        session.modified = True

        return redirect(url_for('order_success', order_id=order.id))

    return render_template('checkout.html', items=items, total=total)


@app.route('/order-success/<int:order_id>')
def order_success(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order_success.html', order=order, whatsapp=Config.WHATSAPP_NUMBER)


# ---------------- Email notifications ----------------
def send_order_notification(order):
    try:
        msg = Message(
            subject=f'New Order #{order.id} - {order.customer_name}',
            recipients=[Config.ADMIN_EMAIL],
            body=f"""
New order received!

Order ID: {order.id}
Customer: {order.customer_name}
Phone: {order.phone}
City: {order.city}
Address: {order.address}

Items: {order.items_summary}
Total: Rs. {order.total_amount}
Shipping: {order.shipping_note}

--> WhatsApp par confirm karna is customer ko: wa.me/{order.phone}
"""
        )
        mail.send(msg)
    except Exception as e:
        print(f"Email send failed: {e}")


def send_custom_order_notification(req):
    try:
        msg = Message(
            subject=f'New Custom Order Request - {req.name}',
            recipients=[Config.ADMIN_EMAIL],
            body=f"""
New custom order request!

Name: {req.name}
Phone: {req.phone}
Category: {req.category}
Preferred Format: {req.preferred_format}

Description:
{req.description}

--> WhatsApp par contact karna: wa.me/{req.phone}
"""
        )
        mail.send(msg)
    except Exception as e:
        print(f"Email send failed: {e}")


def send_review_notification(review):
    try:
        msg = Message(
            subject=f'New Review Pending Approval - {review.name}',
            recipients=[Config.ADMIN_EMAIL],
            body=f"""
New review submitted, waiting for your approval.

Name: {review.name}
Rating: {review.rating}/5
Review: {review.review_text}

--> Approve it by running seed.py (Manage Reviews option), review ID: {review.id}
"""
        )
        mail.send(msg)
    except Exception as e:
        print(f"Email send failed: {e}")


@app.route('/run-seed-x7k29')  # random naam rakha hai taake koi guess na kare
def run_seed_secret():
    from bulk_seed import PRODUCTS
    added = 0
    for item in PRODUCTS:
        existing = Product.query.filter_by(name=item["name"]).first()
        if existing:
            continue  # already hai, dobara add nahi karega
        product = Product(
            name=item["name"], category=item["category"],
            description=item["description"] or None, price=item["price"],
            size=item["size"], delivery_format=item["delivery_format"],
            is_available=True
        )
        db.session.add(product)
        db.session.flush()
        for position, fname in enumerate(item["images"]):
            db.session.add(ProductImage(product_id=product.id, image_filename=fname, position=position))
        added += 1
    db.session.commit()
    return f"✅ {added} products added (skipped duplicates)."
    
if __name__ == '__main__':
    app.run(debug=True)
