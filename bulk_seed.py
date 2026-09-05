from app import app
from models import db, Product, ProductImage

# ================================================================
# Apni saari existing calligraphies/artwork yahan ek list mein likho.
# Har product ke liye ek dictionary — copy-paste karke jitne chahiye utne bana lo.
#
# images: list of filenames (static/images/ ke andar already honi chahiye)
#         same piece ke multiple angles ho toh sab yahan list mein daal do
# delivery_format: "Canvas" / "Frame" / "Canvas,Frame" (dono available ho toh)
# ================================================================

PRODUCTS = [
    {
        "name": "Allahu Akbar",
        "category": "Islamic Art",              # Calligraphy / Islamic Art / Acrylic Art
        "description": "Acrylic on canvas, elegant calligraphy with minimal background.",
        "price": 1199,
        "size": "8x8 inches",
        "delivery_format": "Frame",
        "images": ["img3.jpeg", "img1.jpeg"],
    },
    {
        "name": "Ayat calligraphy",
        "category": "Islamic Art",
        "description": "Beautiful calligraphy of a verse from the Quran.",
        "price": 975,
        "size": "8x8 inches",
        "delivery_format": "Frame",
        "images": ["img4.jpeg", "img2.jpeg"],
    },
   
    {
        "name": "Name Calligraphy",
        "category": "Calligraphy",
        "description": "Personalized calligraphy with your name.",
        "price": 799,
        "size": "8x8 inches",
        "delivery_format": "Frame, Canvas",
        "images": ["img8.jpeg", "img5.jpeg", "img6.jpeg"],
    },

    {
        "name": "Fiha Khair",
        "category": "Calligraphy",
        "description": "Acrylic calligraphy artwork with a modern touch.",
        "price": 975,
        "size": "8x8 inches",
        "delivery_format": "Frame",
        "images": ["img7.jpeg"],
    },

    {
        "name": "Quranic Verse",
        "category": "Islamic Art",
        "description": "Beautiful calligraphy of a verse from the Quran.",
        "price": 1199,
        "size": "8x8 inches",
        "delivery_format": "Frame, Canvas",
        "images": ["img9.jpeg", "img12.jpeg"],
    },    

    {
        "name": "Allhamdulillah",
        "category": "Islamic Art",
        "description": "Elegant Allhamdulillah calligraphy in gold on black background.",
        "price": 1199,
        "size": "8x8 inches",
        "delivery_format": " Canvas",
        "images": ["img10.jpeg"],
    },
    {
        "name": "Name Calligraphy",
        "category": "Calligraphy",
        "description": "Personalized calligraphy with your name.",
        "price": 890,
        "size": "8x8 inches",
        "delivery_format": "Frame",
        "images": ["img11.jpeg"],
    },
    {
        "name": "Cat Painting",
        "category": "Acrylic Art",
        "description": "Beautiful cat painting in acrylic.",
        "price": 1199,
        "size": "8x8 inches",
        "delivery_format": "Frame, Canvas",
        "images": ["img13.jpeg", "img14.jpeg"],
    },
    {
        "name": "Sallallahu Alayhi Wasallam",
        "category": "Islamic Art",
        "description": "Calligraphy of the Prophet's name in Arabic.",
        "price": 1199,
        "size": "8x8 inches",
        "delivery_format": "Canvas",
        "images": ["img15.jpeg", "img16.jpeg"],
    },
    {
        "name": "Acrylic nightscape",
        "category": "Acrylic Art",
        "description": "Beautiful nightscape painting in acrylic.",
        "price": 1199,
        "size": "8x8 inches",
        "delivery_format": "Frame",
        "images": ["img18.jpeg"],
    },
    {
        "name": "Fabi ayiyi ala'i rabbika calligraphy",
        "category": "Islamic Art",
        "description": "Calligraphy of a verse from the Quran.",
        "price": 1299,
        "size": "8x8 inches",
        "delivery_format": "Canvas",
        "images": ["img17.jpeg"],
    },
    { 
        "name": "Acrylic artwork",
        "category": "Acrylic Art",
        "description": "Beautiful acrylic artwork.",
        "price": 1199,
        "size": "8x8 inches",
        "delivery_format": "Frame",
        "images": ["img20.jpeg", "img23.jpeg"],
    },
    {
        "name": "Ayat calligraphy",
        "category": "Islamic Art",
        "description": "Calligraphy of a verse from the Quran.",
        "price": 1299,
        "size": "8x8 inches",
        "delivery_format": "Frame, Canvas",
        "images": ["img25.jpeg", "img24.jpeg", "img22.jpeg"],
    },
    {
        "name": "Ayat calligraphy",
        "category": "Islamic Art",
        "description": "Calligraphy of a verse from the Quran.",
        "price": 1299,
        "size": "8x8 inches",
        "delivery_format": "Frame, Canvas",
        "images": ["img26.jpeg", "img28.jpeg"],
    },
    {
        "name": "Swan Acrylic Painting",
        "category": "Acrylic Art",
        "description": "Beautiful swan painting in acrylic.",
        "price": 1199,
        "size": "8x8 inches",
        "delivery_format": "Frame, Canvas",
        "images": ["img27.jpeg"],
    },
    {
        "name": "Quranic Verse Calligraphy",
        "category": "Islamic Art",
        "description": "Calligraphy of a verse from the Quran.",
        "price": 1299,
        "size": "8x8 inches",
        "delivery_format": "Frame, Canvas",
        "images": ["img30.jpeg", "img29.jpeg"],

    },
    {
        "name": "Spiderman Acrylic Artwork",
        "category": "Acrylic Art",
        "description": "Beautiful Spiderman painting in acrylic.",
        "price": 1199,
        "size": "8x8 inches",
        "delivery_format": "Frame, Canvas",
        "images": ["img32.jpeg"],
    },
    {
        "name": "Ayat Calligraphy",
        "category": "Islamic Art",
        "description": "Calligraphy of a verse from the Quran.",
        "price": 1299,
        "size": "8x8 inches",
        "delivery_format": "Frame, Canvas",
        "images": ["img31.jpeg"],

    },
    {
        "name": "Kun fayakun Calligraphy",
        "category": "Islamic Art",
        "description": "Calligraphy of a verse from the Quran.",
        "price": 1299,
        "size": "8x8 inches",
        "delivery_format": "Frame, Canvas",
        "images": ["img33.jpeg", "img34.jpeg"],
    },
    {
        "name": "Ayat Calligraphy",
        "category": "Islamic Art",
        "description": "Calligraphy of a verse from the Quran.",
        "price": 1299,
        "size": "8x8 inches",
        "delivery_format": "Frame, Canvas",
        "images": ["img38.jpeg", "img35.jpeg"],

    },
    {
        "name": "Name Calligraphy",
        "category": "Calligraphy",
        "description": "Personalized calligraphy with your name.",
        "price": 1199,
        "size": "8x8 inches",
        "delivery_format": "Frame, Canvas",
        "images": ["img42.jpeg", "img40.jpeg"],
    },
    {
        "name": "Ayat Calligraphy",
        "category": "Islamic Art",
        "description": "Calligraphy of a verse from the Quran.",
        "price": 1299,
        "size": "8x8 inches",
        "delivery_format": "Frame, Canvas",
        "images": ["img41.jpeg"],
    },
    {
        "name": "Bismillah Calligraphy",
        "category": "Islamic Art",
        "description": "Calligraphy of Bismillah in Arabic.",
        "price": 1299,
        "size": "8x8 inches",
        "delivery_format": "Frame, Canvas",
        "images": ["img44.jpeg", "img43.jpeg"],
    },
    {
        "name": "Name Calligraphy",
        "category": "Calligraphy",
        "description": "Personalized calligraphy with your name.",
        "price": 1199,
        "size": "8x8 inches",
        "delivery_format": "Frame, Canvas",
        "images": ["img36.jpeg"],
    },
    {
        "name": "Ayat Calligraphy",
        "category": "Islamic Art",
        "description": "Calligraphy of a verse from the Quran.",
        "price": 1299,
        "size": "8x8 inches",
        "delivery_format": "Frame, Canvas",
        "images": ["img39.jpeg", "img37.jpeg"],
    },


]
           

def run():
    with app.app_context():
        added = 0
        for item in PRODUCTS:
            product = Product(
                name=item["name"],
                category=item["category"],
                description=item["description"] or None,
                price=item["price"],
                size=item["size"],
                delivery_format=item["delivery_format"],
                is_available=True
            )
            db.session.add(product)
            db.session.flush()  # get product.id

            for position, fname in enumerate(item["images"]):
                db.session.add(ProductImage(
                    product_id=product.id,
                    image_filename=fname,
                    position=position
                ))
            added += 1
            print(f"✅ Added: {item['name']}")

        db.session.commit()
        print(f"\n🎉 Done! {added} products added.\n")


if __name__ == "__main__":
    run()