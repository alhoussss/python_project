from django.db import models
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import requests
from bs4 import BeautifulSoup
import json

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=50)
    desc = models.TextField()
    image = models.ImageField(upload_to="articles")
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

