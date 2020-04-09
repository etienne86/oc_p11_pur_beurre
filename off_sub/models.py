from django.db import models
from django.db.utils import IntegrityError
from django.db import transaction


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

    def add_category_to_db(self):
        """
        If necessary, add a category in the database.
        """
        try:
            with transaction.atomic():
                self.save()
                category_id = self.id
        except IntegrityError:
            category_id = Category.objects.get(name=self.name).id
        return category_id

    @classmethod
    def get_categories_list(cls):
        """
        Return the list of the available categories in the database.
        """
        return cls.CATEGORIES_LIST

    def get_url_250_products(self):
        """
        Supply the search url, which displays 1000 products,
        based on the category name.
        """
        if self.name in self.CATEGORIES_LIST:
            res = "https://fr.openfoodfacts.org/cgi/search.pl?" \
                + "action=process&tagtype_0=categories" \
                + "&tag_contains_0=contains&tag_0=" \
                + self.name + "&page_size=250&json=1"
        else:
            res = ""
        return res


class Store(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def add_store_to_db(self):
        """
        If necessary, add a store in the database.
        """
        try:
            with transaction.atomic():
                self.save()
                store_id = self.id
        except IntegrityError:
            store_id = Store.objects.get(name=self.name).id
        return store_id


class Product(models.Model):
    # id = models.AutoField(auto_created=True, primary_key=True)
    code = models.CharField(max_length=20, unique=True)
    product_name = models.CharField(max_length=500)
    nutriscore_grade = models.CharField(max_length=1)
    nutriscore_score = models.IntegerField()
    fat = models.CharField(max_length=100, null=True)
    saturated_fat = models.CharField(max_length=100, null=True)
    sugars = models.CharField(max_length=100, null=True)
    salt = models.CharField(max_length=100, null=True)
    url = models.CharField(max_length=1000)
    image_url = models.CharField(max_length=1000, null=True)
    # create association table off_sub_product_categories in database
    categories = models.ManyToManyField(Category, related_name='products')
    # create association table off_sub_product_stores in database
    stores = models.ManyToManyField(Store, related_name='products', blank=True)

    def __str__(self):
        # return f"{self.code} - {self.product_name}".replace("'", r"\'")
        return f"{self.product_name} [code-barres : {self.code}]"

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
            with transaction.atomic():
                self.save()
                product_id = self.id
        except IntegrityError:
            product_id = Product.objects.get(code=self.code).id
        return product_id

    def get_best_subs(self, nb_sub):
        """
        Return a queryset with 'nb_sub' products
        which can be substitutes of the selected product.
        If the selected product is among the best products,
        it will be also returned to show that this is a "good" product.
        """
        # get the product category/ies linked to the product
        prod_categories = [categ for categ in self.categories.all()]
        # list all the products in database for the product category/ies
        prods_id = []
        for categ in prod_categories:
            for prod in Product.objects.filter(categories=categ):
                prods_id += [prod.id]
        # remove duplicates
        prods_id = list(set(prods_id))
        # get back to the Product Queryset
        prods_qs = Product.objects.filter(id__in=prods_id)
        # sort the products based on the nutriscore
        prods_qs = prods_qs.order_by('nutriscore_score')
        # get the 'nb_sub' best subs
        return prods_qs[:nb_sub]
