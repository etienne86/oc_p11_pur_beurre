from django.db import models
from django.db.utils import IntegrityError


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    CATEGORIES_LIST = [
        "desserts",
        "eaux",
        "fromages",
        "legumes",
        "pains",
        "pizzas",
        "poissons",
        "riz",
        "viandes",
    ]
    
    @classmethod
    def get_categories_list(cls):
        """
        Return the list of the available categories in the database.
        """
        return cls.CATEGORIES_LIST

    def get_url_1k_products(self):
        """
        Supply the search url, which displays 1000 products,
        based on the category name.
        """
        if self.name in self.CATEGORIES_LIST:
            res = "https://fr.openfoodfacts.org/cgi/search.pl?" \
                + "action=process&tagtype_0=categories" \
                + "&tag_contains_0=contains&tag_0=" \
                + self.name + "&page_size=1000&json=1"
        else:
            res = ""
        return res

    def add_category_to_db(self):
        """
        If necessary, add a category in the database.
        """
        category = Category.objects.get_or_create(name=self.name)


class Store(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def add_store_to_db(self):
        """
        If necessary, add a store in the database.
        """
        store = Store.objects.get_or_create(name=self.name)


class Product(models.Model):
    code = models.CharField(max_length=20, unique=True)
    product_name = models.CharField(max_length=200)
    nutriscore_grade = models.CharField(max_length=1)
    nutriscore_score = models.IntegerField()
    url = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200)
    # create association table off_sub_product_categories in database
    categories = models.ManyToManyField(
        Category,
        related_name='products',
        blank=True
    )
    # create association table off_sub_product_stores in database
    stores = models.ManyToManyField(Store, related_name='products', blank=True)

    def add_product_category_to_db(self, category):
        """
        Add a record in the ProductCategory table,
        to link a product and a category.
        """
        self.categories.add(category)

    def add_product_store_to_db(self, store):
        """
        If necessary, add a record in the ProductStore table,
        to link a product and a store.
        """
        self.stores.add(store)

    def add_product_to_db(self):
        """
        If necessary, add a product in the database.
        """
        try:
            product = Product.objects.get_or_create(
                code=self.code,
                product_name=self.product_name,
                nutriscore_grade=self.nutriscore_grade,
                nutriscore_score=self.nutriscore_score,
                url=self.url,
                image_url=self.image_url,
            )
        except IntegrityError:
            pass
