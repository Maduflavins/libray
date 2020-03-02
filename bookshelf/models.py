
from django.db import models
from datetime import date
from django.urls import reverse
import uuid
from datetime import datetime


class Category(models.Model):
    """Model representing book category or genre"""
    name = models.CharField(max_length = 30, help_text = 'enter book category')

    def __str__(self):
        """String for representing the Model Object"""
        return self.name



class Author(models.Model):
    """Model fo the authors of the books"""
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(max_length=100)
    date_of_death = models.DateField('Died', null=True, blank='True')
    biography = models.TextField(max_length=100, help_text='Enter brief author bio.', blank=True, null=True)
    book_id = models.CharField(max_length = 10)

    class Meta:
        ordering = ['first_name', 'last_name']

    def get_absolute_url(self):
        return reverse('author-detail', arge = [str(self.id)])

    def __str__(self):
        """String for representing or displaying the Author model object"""
        return str (self.name)


class Book(models.Model):
    """Model representing a book"""
    title = models.CharField(max_length=250)
    author = models.ForeignKey(Author, on_delete = models.SET_NULL, null = True)
    image = models.CharField(max_length = 255)
    summary = models.CharField(max_length = 1000, help_text = 'Enter a brief description')
    category = models.ManyToManyField(Category, null = True)
    edition = models.CharField(max_length=200)
    pub_date = models.DateTimeField(null = True, blank = True)
    reg_date = models.DateTimeField(default=datetime.now, blank=True)

    def get_absolute_url(self):
        return reverse('book-detail', args = [str(self.id)])

    def __str__(self):
        return self.book_title

    def display_category(self):
        """To display the categories in Admin"""
        return ', '.join(category.name for category in self.category.all()[:3])
    display_category.short_description = 'Category'


class User(models.Model):
    """This is the User Model"""
    name = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)
    phone_number = models.CharField(max_length = 11)
    cohort = models.CharField(max_length = 10)

    class Meta:
        ordering = ['name', 'email', 'cohort']

    def get_absolute_url(self):
        return reverse('user-detail', args = [str(self.id)])

    def __str__(self):
       return f'{self.name}'


class Borrower(models.Model):
    """This model represent the borrower"""
    name = models.CharField(max_length = 250)
    book = models.ForeignKey(Book, null = True, on_delete=models.CASCADE)
    cohort = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    
    def __str__(self):
       return f'{self.name}'


class Issue(models.Model):
    #This is an instance of the book (Book Instance)
    id = models.CharField(max_length = 50, primary_key=True)
    issue_date = models.DateField(null = True, blank = True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null = True)
    borrower = models.ForeignKey(Borrower, on_delete = models.SET_NULL, null = True)
    due_back = models.DateField(null = True, blank = True)

    def __str__(self):
       return f'{self.issue_id}'

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
    
    LOAN_STATUS = (
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
      
    status = models.CharField(
        max_length = 1,
        choices = LOAN_STATUS,
        blank = True,
        default = 'a',
        help_text = 'Book Availability')
    



class Default(models.Model):
    """This model represent the defaulter and defaulttable"""
    name = models.ForeignKey(Borrower, on_delete = models.CASCADE, null = False)
    count = models.CharField(max_length = 4)
    issue = models.ForeignKey(Issue, models.SET_NULL, null = True)
    
    def __str__(self):
       return str('%s %d', (self.name, self.count))