from app import app
from models import db, Product, ProductImage, Review

CATEGORIES = ['Calligraphy', 'Islamic Art', 'Acrylic Art']
FORMATS = ['Canvas', 'Frame', 'Canvas,Frame']  # last = both available


def choose_category():
    print("\nCategory:")
    for i, c in enumerate(CATEGORIES, 1):
        print(f"  {i}. {c}")
    choice = int(input("Choose (1-3): "))
    return CATEGORIES[choice - 1]


def choose_format():
    print("\nDelivery format:")
    print("  1. Canvas only")
    print("  2. Frame only")
    print("  3. Both (customer will choose)")
    choice = int(input("Choose (1-3): "))
    return FORMATS[choice - 1]


def add_product():
    print("\n--- Add New Artwork ---")
    name = input("Name: ")
    category = choose_category()
    description = input("Description (optional, press enter to skip): ")
    price = int(input("Price (Rs, courier cost already included): "))
    size = input("Size (e.g. A3 - 12x16 inch): ")
    delivery_format = choose_format()
    is_available = input("Available? (y/n): ").strip().lower() != 'n'

    print("\nNow add image filenames (already placed in static/images/).")
    print("Same calligraphy, different angles? Add them all here, one by one.")
    print("Press Enter on blank line when done.\n")

    filenames = []
    i = 1
    while True:
        fname = input(f"Image {i} filename (or Enter to finish): ").strip()
        if not fname:
            break
        filenames.append(fname)
        i += 1

    if not filenames:
        print("⚠️  At least one image is required. Cancelling.\n")
        return

    product = Product(
        name=name, category=category, description=description or None,
        price=price, size=size, delivery_format=delivery_format,
        is_available=is_available
    )

    with app.app_context():
        db.session.add(product)
        db.session.flush()

        for position, fname in enumerate(filenames):
            img = ProductImage(product_id=product.id, image_filename=fname, position=position)
            db.session.add(img)

        db.session.commit()
        print(f"\n✅ Added: {product.name} with {len(filenames)} image(s) (id: {product.id})\n")


def list_products():
    with app.app_context():
        products = Product.query.all()
        if not products:
            print("\nNo products yet.\n")
            return
        print("\n--- All Products ---")
        for p in products:
            status = "Available" if p.is_available else "Sold Out"
            print(f"[{p.id}] {p.name} | {p.category} | Rs.{p.price} | {p.size} | {p.delivery_format} | {status} | {len(p.images)} image(s)")
        print()


def add_images_to_existing():
    with app.app_context():
        pid = int(input("Product ID to add images to: "))
        product = Product.query.get(pid)
        if not product:
            print("Not found.\n")
            return
        current_max = len(product.images)
        print(f"{product.name} currently has {current_max} image(s).")
        i = current_max + 1
        while True:
            fname = input(f"Image {i} filename (or Enter to finish): ").strip()
            if not fname:
                break
            img = ProductImage(product_id=pid, image_filename=fname, position=i - 1)
            db.session.add(img)
            i += 1
        db.session.commit()
        print(f"✅ Images added to {product.name}.\n")


def toggle_availability():
    with app.app_context():
        pid = int(input("Product ID: "))
        product = Product.query.get(pid)
        if not product:
            print("Not found.\n")
            return
        product.is_available = not product.is_available
        db.session.commit()
        print(f"✅ {product.name} is now {'Available' if product.is_available else 'Sold Out'}\n")


def delete_product():
    with app.app_context():
        pid = int(input("Product ID to delete: "))
        product = Product.query.get(pid)
        if not product:
            print("Not found.\n")
            return
        db.session.delete(product)
        db.session.commit()
        print(f"🗑️ Deleted: {product.name}\n")


# ---------------- Reviews ----------------
def list_pending_reviews():
    with app.app_context():
        reviews = Review.query.filter_by(is_approved=False).order_by(Review.created_at.desc()).all()
        if not reviews:
            print("\nNo pending reviews.\n")
            return
        print("\n--- Pending Reviews ---")
        for r in reviews:
            print(f"[{r.id}] {r.name} | {'★' * r.rating}{'☆' * (5 - r.rating)}")
            print(f"    \"{r.review_text}\"")
        print()


def list_approved_reviews():
    with app.app_context():
        reviews = Review.query.filter_by(is_approved=True).order_by(Review.created_at.desc()).all()
        if not reviews:
            print("\nNo approved reviews yet.\n")
            return
        print("\n--- Approved Reviews (live on site) ---")
        for r in reviews:
            print(f"[{r.id}] {r.name} | {'★' * r.rating}{'☆' * (5 - r.rating)}")
            print(f"    \"{r.review_text}\"")
        print()


def approve_review():
    with app.app_context():
        rid = int(input("Review ID to approve: "))
        review = Review.query.get(rid)
        if not review:
            print("Not found.\n")
            return
        review.is_approved = True
        db.session.commit()
        print(f"✅ Review by {review.name} is now live on the site.\n")


def reject_review():
    with app.app_context():
        rid = int(input("Review ID to reject/delete: "))
        review = Review.query.get(rid)
        if not review:
            print("Not found.\n")
            return
        db.session.delete(review)
        db.session.commit()
        print(f"🗑️ Review by {review.name} deleted.\n")


def unapprove_review():
    with app.app_context():
        rid = int(input("Review ID to remove from site (keep, but hide): "))
        review = Review.query.get(rid)
        if not review:
            print("Not found.\n")
            return
        review.is_approved = False
        db.session.commit()
        print(f"✅ Review by {review.name} hidden from site.\n")


def manage_reviews_menu():
    while True:
        print("\n--- Manage Reviews ---")
        print("1. View pending reviews")
        print("2. View approved (live) reviews")
        print("3. Approve a review")
        print("4. Reject & delete a review")
        print("5. Unapprove (hide) a live review")
        print("6. Back to main menu")
        choice = input("Choose: ")
        if choice == '1':
            list_pending_reviews()
        elif choice == '2':
            list_approved_reviews()
        elif choice == '3':
            approve_review()
        elif choice == '4':
            reject_review()
        elif choice == '5':
            unapprove_review()
        elif choice == '6':
            break
        else:
            print("Invalid choice.\n")


if __name__ == '__main__':
    while True:
        print("\n1. Add product\n2. List products\n3. Add more images to existing product\n4. Toggle availability\n5. Delete product\n6. Manage reviews\n7. Exit")
        choice = input("Choose: ")
        if choice == '1':
            add_product()
        elif choice == '2':
            list_products()
        elif choice == '3':
            add_images_to_existing()
        elif choice == '4':
            toggle_availability()
        elif choice == '5':
            delete_product()
        elif choice == '6':
            manage_reviews_menu()
        elif choice == '7':
            break
        else:
            print("Invalid choice.\n")