from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django_countries.fields import CountryField

# Create your models here.


class Author(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.author.username


class Company(models.Model):
    company_name = models.CharField(unique=False, max_length=70, null=False, blank=False)
    company_logo = models.ImageField(null=True, blank=True, upload_to="media")
    CHOICES = (("1", "ŞAHIS"), ("2", "Büyük işletme"), ("3", "KOBİ"), ("4", "STK"))
    company_type = models.CharField(max_length=1, choices=CHOICES, verbose_name="Company Type")
    country = CountryField(blank_label="(select country)", multiple=False)  # default="1"
    # Tüm ülke - 'NZ', 'TR' - Company.country >> Country(code='NZ') , company.country.name
    # Company.objects.filter(country__name="New Zealand").count()
    web_site = models.CharField(null=True, blank=True, unique=False, max_length=200)
    company_employee_count = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.id) + " " + self.company_name


class Article(models.Model):
    pub_date = models.DateField(editable=False, auto_now_add=True)
    headline = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, editable=False)
    publisher = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    # default=1, IntegrityError: The row in table 'core_article' with primary key '1' has an invalid fkey:
    # core_article.publisher_id contains a value '4' that does not have a corresponding value in core_company.id

    class Meta:  # for pagination sort error
        ordering = ["-id"]

    def __str__(self):
        return str(self.id) + "" + self.headline

    def get_slug(self):
        slug = slugify(self.headline.replace("ı", "i"))
        unique = slug
        number = 2

        while Article.objects.filter(slug=unique).exists():
            unique = "{}-{}".format(slug, number)
            number += 1
        return unique

    def save(self, *args, **kwargs):
        # if not self.id:
        # self.slug = slugify(self.headline)
        self.slug = self.get_slug()
        return super(Article, self).save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="article")
    content = models.TextField()
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies", verbose_name="belong_to"
    )
    created = models.DateTimeField(editable=False, auto_now_add=True)
    slug = models.SlugField(unique=True, null=True, editable=False)

    def __str__(self):
        return self.article.headline

    def get_slug(self):
        slug = slugify(self.article.headline.replace("ı", "i"))
        unique = slug
        number = 2

        while Comment.objects.filter(slug=unique).exists():
            unique = "{}-{}".format(slug, number)
            number += 1
        return unique

    def save(self, *args, **kwargs):
        self.slug = self.get_slug()
        return super(Comment, self).save(*args, **kwargs)

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def any_children(self):
        return Comment.objects.filter(parent=self).exists()
