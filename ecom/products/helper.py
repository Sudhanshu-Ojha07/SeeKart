from products.models import Category, Product, SizeVariant

def product_size(product_slug):
    product = Product.objects.get(slug=product_slug)
    all_sizes = SizeVariant.objects.all()  # Fetch all available sizes
    existing_sizes = product.size_variant.all()  # Fetch sizes already linked to the product

    # Find sizes that are not yet linked to the product
    new_sizes = all_sizes.difference(existing_sizes)

    # If there are new sizes, add them to the product's size_variant field
    if new_sizes.exists():
        product.size_variant.add(*new_sizes)
        product.save()
