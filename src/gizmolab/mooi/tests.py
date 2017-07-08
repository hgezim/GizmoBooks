from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.http import HttpResponseRedirect
    
__test__ = {  
"TestLoginForm": """
#setUp:

>>> from django.contrib.auth.models import User
>>> from mooi.models import Location
>>> goodUsername = "latif"
>>> goodUsername02 = "latif123"
>>> badUsername = 500
>>> goodPassword = "12345678"
>>> badPassword = 87654321
>>> goodEmail = "latif@kosova.com"
>>> badEmail = 404
>>> goodUser = User.objects.create_user(goodUsername, goodEmail, goodPassword)
>>> badUser = 500
>>> goodPhone = "403-380-1234"
>>> badPhone = 4032801213
>>> goodCredits = 1
>>> badCredits = "two"
>>> goodTransactionStatus = "Pending"
>>> badTransactionStatus = 5
>>> l = Location(city="Lethbridge", country="Canada")
>>> l.save()
>>> goodLocation = l
>>> badLocation = 500

#test Profile model:
>>> from django.contrib.auth.models import User
>>> from mooi.models import Profile
>>> u = User.objects.create_user(goodUsername02, goodEmail, goodPassword)
>>> uProfile = u.get_profile()
>>> if uProfile: print True
True
>>> uProfile.phone = goodPhone
>>> uProfile.save()
>>> uProfile.credits = goodCredits
>>> uProfile.save()
>>> uProfile.transaction_status = goodTransactionStatus
>>> uProfile.save()
>>> uProfile.location = l
>>> uProfile.save()

#test LoginForm:
>>> from mooi.forms import LoginForm
>>> data = {'username': goodUsername, 'password': goodPassword}
>>> f = LoginForm(data)
>>> f.is_valid()
True

>>> gizmoUsername = "gizmo"
>>> data = {'username': gizmoUsername, 'password': goodPassword}
>>> f = LoginForm(data)
>>> f.is_valid()
False

>>> data = {'username': goodUsername, 'password': badPassword}
>>> f = LoginForm(data)
>>> f.is_valid()
False
""",

"RegisterFormTest":"""
#test RegisterForm:
>>> goodUsernameString = "john.smith"
>>> badUsernameString = "john smith"
>>> goodPassword = "87654321"
>>> goodConfirm = "87654321"
>>> badConfirm = "876543"
>>> goodName = "John"
>>> badName = "Johhhhhhhhhhhhhhhhhhhhn"
>>> goodEmail = "john@example.com"
>>> badEmail = "john@example"
>>> goodPhone = "403 358 1292"
>>> badPhone = "three eight zero six seven five eight"
>>> goodCity = "Calgary"
>>> badCity = "St--John__johny"
>>> goodCountry = "Canada"
>>> badCountry = "Columbia and Damasc_cus"
>>> 
>>> from mooi.forms import RegisterForm
>>> data = {"username": goodUsernameString, "password": goodPassword, "confirmPassword": goodConfirm, "name": goodName, "email": goodEmail, "phone": goodPhone, "city": goodCity, "country": goodCountry}
>>> f = RegisterForm(data)
>>> f.is_valid()
True
>>> data = {"username": badUsernameString, "password": goodPassword, "confirmPassword": goodConfirm, "name": goodName, "email": goodEmail, "phone": goodPhone, "city": goodCity, "country": goodCountry}
>>> f = RegisterForm(data)
>>> f.is_valid()
False
>>> data = {"username": goodUsernameString, "password": goodPassword, "confirmPassword": badConfirm, "name": goodName, "email": goodEmail, "phone": goodPhone, "city": goodCity, "country": goodCountry}
>>> f = RegisterForm(data)
>>> f.is_valid()
False
>>> data = {"username": goodUsernameString, "password": goodPassword, "confirmPassword": goodConfirm, "name": badName, "email": goodEmail, "phone": goodPhone, "city": goodCity, "country": goodCountry}
>>> f = RegisterForm(data)
>>> f.is_valid()
False
>>> data = {"username": goodUsernameString, "password": goodPassword, "confirmPassword": goodConfirm, "name": goodName, "email": badEmail, "phone": goodPhone, "city": goodCity, "country": goodCountry}
>>> f = RegisterForm(data)  
>>> f.is_valid() 
False
>>> f.errors
{'email': [u'Enter a valid e-mail address.']}
>>>
>>> data = {"username": goodUsernameString, "password": goodPassword, "confirmPassword": goodConfirm, "name": goodName, "email": goodEmail, "phone": badPhone, "city": goodCity, "country": goodCountry}
>>> f = RegisterForm(data)
>>> f.is_valid()
False
>>> f.errors
{'phone': [u'Ensure this value has at most 20 characters (it has 37).']}
>>> 
>>> data = {"username": goodUsernameString, "password": goodPassword, "confirmPassword": goodConfirm, "name": goodName, "email": goodEmail, "phone": goodPhone, "city": goodCity, "country": goodCountry}
>>> f = RegisterForm(data)
>>> f.is_valid()
True
""",

"SellFormTest":"""
#test SellForm:
>>> from mooi.forms import SellForm

>>> ISBN10 = "0077216504"
>>> ISBN13 = "978-0205649242"
>>> invalidISBN = "12345678"
>>> noPicISBN = "0716798271"
>>> noISBNTrue = True
>>> noISBNFalse = False
>>> goodTitle = "Jujj and Majooj"
>>> badTitle = ""
>>> goodPublisher = "Quarky"
>>> badPublisher = ""
>>> goodAuthors = "Gezim Hoxha\\nLulzim Hoxha\\nBlerina Hoxha"
>>> badAuthors = ""
>>> goodCondition = 4.5
>>> goodPrice = 34.99
>>> badPrice = ""
>>> goodDiscipline = "Chemistry"
>>> badDiscipline = "Chemistry 1000"

>>> data = {"ISBN": ISBN10, "condition": goodCondition, "price": goodPrice, "discipline": goodDiscipline}
>>> f = SellForm(data=data)
>>> f.is_valid()
True
>>> data = {"ISBN": ISBN13, "condition": goodCondition, "price": goodPrice, "discipline": goodDiscipline}
>>> f = SellForm(data=data)
>>> f.is_valid()
True
>>> data = {"ISBN": noPicISBN, "condition": goodCondition, "price": goodPrice, "discipline": goodDiscipline}
>>> f = SellForm(data=data)
>>> f.is_valid()
True
>>> data = {"ISBN": ISBN10, "condition": goodCondition, "price": badPrice, "discipline": goodDiscipline}
>>> f = SellForm(data=data)
>>> f.is_valid()
False
>>> data = {"ISBN": ISBN10, "condition": goodCondition, "price": goodPrice, "discipline": badDiscipline}
>>> f = SellForm(data=data)
>>> f.is_valid()
False
>>> data = {"ISBN": "", "noISBN": True, "condition": goodCondition, "price": goodPrice, "discipline": goodDiscipline}
>>> f = SellForm(data=data)
>>> f.is_valid()
False
>>> data = {"ISBN": "", "noISBN": True, "title": goodTitle, "publisher": goodPublisher, "authors": goodAuthors, "condition": goodCondition, "price": goodPrice, "discipline": goodDiscipline}
>>> f = SellForm(data=data)
>>> f.is_valid()
True
>>> data = {"ISBN": "", "noISBN": True, "title": goodTitle, "publisher": goodPublisher, "authors": badAuthors, "condition": goodCondition, "price": goodPrice, "discipline": goodDiscipline}
>>> f = SellForm(data=data)
>>> f.is_valid()
False
>>> data = {"ISBN": "", "noISBN": True, "title": goodTitle, "publisher": badPublisher, "authors": goodAuthors, "condition": goodCondition, "price": goodPrice, "discipline": goodDiscipline}
>>> f = SellForm(data=data)
>>> f.is_valid()
False
>>> data = {"ISBN": "", "noISBN": True, "title": badTitle, "publisher": goodPublisher, "authors": goodAuthors, "condition": goodCondition, "price": goodPrice, "discipline": goodDiscipline}
>>> f = SellForm(data=data)
>>> f.is_valid()
False
>>> data = {"ISBN": "", "noISBN": True, "title": goodTitle, "publisher": goodPublisher, "authors": goodAuthors, "condition": goodCondition, "price": goodPrice, "discipline": goodDiscipline}
>>> f = SellForm(data=data)
>>> f.is_valid()
True
>>> 
""",

"TestRegisterView":"""
# test register view:
>>> from django.test.client import Client
>>> from django.core.urlresolvers import reverse
>>> from mooi.views import register
>>> from django.contrib.auth.models import User
>>> from mooi.models import Profile
>>> c = Client()
>>> 
>>> goodUsernameString = "qwerty"
>>> badUsernameString = "jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj"
>>> goodPassword = "87654321~"
>>> goodConfirm = goodPassword
>>> badConfirm = "87653"
>>> goodName = "QueWerty"
>>> badName = "This should be longer than 10 chars"
>>> goodEmail = "qwerty@example.com"
>>> badEmail = "qwerty@example"
>>> goodPhone = "403 234 1254" 
>>> badPhone = ""
>>> goodCity = "Lethbridge"
>>> goodCountry = "Canada"
>>> 
>>> initialUserCount = User.objects.all().count()
>>> initialProfileCount = Profile.objects.all().count()
>>> 
>>> path = reverse("mooi_register")
>>> cResult = c.get(path)
>>> #ensure no users are there
>>> initialUserCount == User.objects.all().count()
True
>>> initialProfileCount == Profile.objects.all().count()
True
>>> 
>>> path = reverse("mooi_register")
>>> cResults = c.post(path, data={'username': goodUsernameString, 'password': goodPassword, 'confirmPassword': goodConfirm, 'name': goodName, 'email': goodEmail, 'phone': goodPhone, 'city': goodCity, 'country': goodCountry})
>>> u = User.objects.all()[User.objects.all().count()-1]
>>> u.username == goodUsernameString
True
>>> u.first_name == goodName
True
>>> u.email == goodEmail
True
>>> uProfile = u.get_profile()
>>> uProfile.phone == goodPhone
True
>>> 
>>> uProfile.location.city == goodCity
True
>>> uProfile.location.country == goodCountry
True
>>> 

>>> cResults = c.post(path, data={'username': badUsernameString, 'password': goodPassword, 'confirmPassword': goodConfirm, 'name': goodName, 'email': goodEmail, 'phone': goodPhone, 'city': goodCity, 'country': goodCountry})
>>> u = User.objects.all()[User.objects.all().count()-1]
>>> u.username == badUsernameString
False

>>> cResults = c.post(path, data={'username': goodUsernameString, 'password': goodPassword, 'confirmPassword': badConfirm, 'name': goodName, 'email': goodEmail, 'phone': goodPhone, 'city': goodCity, 'country': goodCountry})
>>> u = User.objects.all()[User.objects.all().count()-1]
>>> u.username == badUsernameString
False

>>> cResults = c.post(path, data={'username': goodUsernameString, 'password': goodPassword, 'confirmPassword': goodConfirm, 'name': badName, 'email': goodEmail, 'phone': goodPhone, 'city': goodCity, 'country': goodCountry})
>>> u = User.objects.all()[User.objects.all().count()-1]
>>> u.username == badUsernameString
False

>>> cResults = c.post(path, data={'username': goodUsernameString, 'password': goodPassword, 'confirmPassword': goodConfirm, 'name': goodName, 'email': badEmail, 'phone': goodPhone, 'city': goodCity, 'country': goodCountry})
>>> u = User.objects.all()[User.objects.all().count()-1]
>>> u.username == badUsernameString
False

>>> cResults = c.post(path, data={'username': goodUsernameString, 'password': goodPassword, 'confirmPassword': goodConfirm, 'name': goodName, 'email': goodEmail, 'phone': badPhone, 'city': goodCity, 'country': goodCountry})
>>> u = User.objects.all()[User.objects.all().count()-1]
>>> u.username == badUsernameString
False
""",


"TestSellView":"""
#test sell view:
>>> from django.test.client import Client
>>> from django.core.urlresolvers import reverse
>>> from django.contrib.auth.models import User
>>> from mooi.views import sell
>>> from textbook.models import Book, Book_Copy, Author

>>> sellerUser = "jimmy12345"
>>> sellerEmail = "hgezim@gmail.com"
>>> sellerPassword = "12345"
>>> sellerPasswordConfirm = sellerPassword
>>> sellerName = "JimSeller"
>>> sellerPhone = "406 342 1293"
>>> sellerCity = "Toronto"
>>> sellerCountry = "Canada"
>>> ISBN10 = "0077216504"
>>> ISBN13 = "978-0205649242"
>>> noPicISBN = "0716798271"
>>> invalidISBN = "12345678910"
>>> noISBNTrue = True
>>> noISBNFalse = False
>>> goodTitle = "Tafseer of Quran--beyond the covers"
>>> badTitle = ""
>>> goodPublisher = "Gizmo Publishing"
>>> badPublisher = ""
>>> goodEdition = "2nd"
>>> goodAuthors = "Gezim Hoxha\\nLulzim Hoxha\\nBlerina Hoxha"
>>> badAuthors = ""
>>> goodPrice = "22.99"
>>> badPrice = ""
>>> goodCondition = "4.5"
>>> badCondition = ""
>>> goodDiscipline = "Chemistry"
>>> badDiscipline = ""
>>> 
>>> c = Client()
>>> path = reverse('mooi_sell')

>>> preSellBookCount = Book.objects.all().count() 
>>> preSellBookCopyCount = Book_Copy.objects.all().count()
>>> preSellAuthorCount = Author.objects.all().count()
>>> cResults = c.get(path)
>>> postSellAuthorCount = Author.objects.all().count()
>>> postSellBookCopyCount = Book_Copy.objects.all().count()
>>> postSellBookCount = Book.objects.all().count()
>>> preSellBookCopyCount == postSellBookCopyCount
True
>>> preSellBookCount == postSellBookCount
True
>>> preSellAuthorCount == postSellAuthorCount
True

>>> registerPath = reverse('mooi_register')
>>> cResults = c.post(registerPath, data={"username": sellerUser, "password": sellerPassword, 
...                                       "confirmPassword": sellerPasswordConfirm, "name": sellerName,
...                                       "email": sellerEmail, "phone": sellerPhone,
...                                       "city": sellerCity, "country": sellerCountry})
>>> preSellBookCount = Book.objects.all().count() 
>>> preSellBookCopyCount = Book_Copy.objects.all().count()
>>> preSellAuthorCount = Author.objects.all().count()
>>> cResults = c.get(path)
>>> postSellAuthorCount = Author.objects.all().count()
>>> postSellBookCopyCount = Book_Copy.objects.all().count()
>>> postSellBookCount = Book.objects.all().count()
>>> preSellBookCopyCount == postSellBookCopyCount
True
>>> preSellBookCount == postSellBookCount
True
>>> preSellAuthorCount == postSellAuthorCount
True

>>> cResults = c.post(path, data={"ISBN": ISBN10, "condition": 4.5, "price": 34.99, "discipline": "Chemistry"})
>>> b = Book.objects.get(ISBN=ISBN10)
>>> b.title
u'Chemistry: The Molecular Nature of Matter and Change'
>>> b.discipline
u'Chemistry'
>>> b.authors.all()
[<Author: Martin Silberberg>]
>>> b.picture
u'0077216504.jpg'
>>> b.publisher
u'McGraw-Hill Science/Engineering/Math'
>>> b.edition
u'5'
>>> b.published_date
datetime.date(2008, 1, 7)
>>> b.copies.all()
[<Book_Copy: Chemistry: The Molecular Nature of Matter and Change>]
>>> b.copies.all()[0].owner
<User: jimmy12345>
>>> b.copies.all()[0].price
34.990000000000002
>>> b.copies.all()[0].condition
Decimal('4.5')
>>> b.copies.all()[0].sold
False

>>> cResults = c.post(path, data={"ISBN": ISBN13, "condition": goodCondition, "price": goodPrice, "discipline": goodDiscipline})
>>> #try to fetch the book with it's 10 digit ISBN (this is stored in ISBN column)
>>> Book.objects.get(ISBN="0205649246")
<Book: Psychology (6th Edition)>
>>> b = Book.objects.get(ISBN="0205649246")
>>> b.title
u'Psychology (6th Edition)'
>>> b.discipline
u'Chemistry'
>>> b.authors.all()
[<Author: Stephen F. Davis>, <Author: Joseph J. Palladino>]
>>> b.picture
u'0205649246.jpg'
>>> b.publisher
u'Prentice Hall'
>>> b.edition
u'6'
>>> b.published_date
datetime.date(2009, 1, 16)
>>> b.copies.all()
[<Book_Copy: Psychology (6th Edition)>]
>>> b.copies.all()[0].owner
<User: jimmy12345>
>>> b.copies.all()[0].price
22.989999999999998
>>> b.copies.all()[0].condition
Decimal('4.5')
>>> b.copies.all()[0].sold
False

>>> cResults = c.post(path, data={"ISBN": noPicISBN, "condition": 3.5, "price": 12.00, "discipline": "Biology"})
>>> Book.objects.get(ISBN=noPicISBN)
<Book: Modern Genetic Analysis & Solutions MegaManual w/Interactive Genetics CD>
>>> b3 = Book.objects.get(ISBN=noPicISBN)
>>> b3.picture
u'noimage.png'
>>> b3.title
u'Modern Genetic Analysis & Solutions MegaManual w/Interactive Genetics CD'
>>> b3.discipline
u'Biology'
>>> b3.authors.all()
[<Author: Anthony J.F. Griffiths>]
>>> b3.picture
u'noimage.png'
>>> b3.publisher
u'W. H. Freeman'
>>> b3.edition
u''
>>> b3.published_date
datetime.date(2002, 7, 12)
>>> b3.copies.all()
[<Book_Copy: Modern Genetic Analysis & Solutions MegaManual w/Interactive Genetics CD>]
>>> b3.copies.all()[0].owner
<User: jimmy12345>
>>> b3.copies.all()[0].price
12.0
>>> b3.copies.all()[0].condition
Decimal('3.5')
>>> b3.copies.all()[0].sold
False

>>> preSellBookCount = Book.objects.all().count()
>>> preSellBookCopyCount = Book_Copy.objects.all().count()
>>> preSellAuthorCount = Author.objects.all().count()
>>> cResults = c.post(path, data={"ISBN": invalidISBN, "condition": 4.0, "price": 28.00, "discipline": "Wrong"})
>>> postSellAuthorCount = Author.objects.all().count()
>>> postSellBookCopyCount = Book_Copy.objects.all().count()
>>> postSellBookCount = Book.objects.all().count()
>>> preSellBookCopyCount == postSellBookCopyCount
True
>>> preSellBookCount == postSellBookCount
True
>>> preSellAuthorCount == postSellAuthorCount
True
>>> Book.objects.get(ISBN=invalidISBN)
Traceback (most recent call last):
    ...
DoesNotExist: Book matching query does not exist.

>>> preSellBookCount = Book.objects.all().count()
>>> preSellBookCopyCount = Book_Copy.objects.all().count()
>>> preSellAuthorCount = Author.objects.all().count()
>>> cResults = c.post(path, data={"ISBN": ISBN10, "condition": 4.0, "price": badPrice, "discipline": "Wrong"})
>>> postSellAuthorCount = Author.objects.all().count()
>>> postSellBookCopyCount = Book_Copy.objects.all().count()
>>> postSellBookCount = Book.objects.all().count()
>>> preSellBookCopyCount == postSellBookCopyCount
True
>>> preSellBookCount == postSellBookCount
True
>>> preSellAuthorCount == postSellAuthorCount
True

>>> preSellBookCount = Book.objects.all().count()
>>> preSellBookCopyCount = Book_Copy.objects.all().count()
>>> preSellAuthorCount = Author.objects.all().count()
>>> cResults = c.post(path, data={"ISBN": ISBN10, "condition": 4.0, "price": goodPrice, "discipline": badDiscipline})
>>> postSellAuthorCount = Author.objects.all().count()
>>> postSellBookCopyCount = Book_Copy.objects.all().count()
>>> postSellBookCount = Book.objects.all().count()
>>> preSellBookCopyCount == postSellBookCopyCount
True
>>> preSellBookCount == postSellBookCount
True
>>> preSellAuthorCount == postSellAuthorCount
True

>>> cResults = c.post(path, data={"ISBN": "", "noISBN": noISBNTrue, "title": goodTitle, "publisher": goodPublisher, "authors": goodAuthors, "condition": 4.0, "price": goodPrice, "discipline": goodDiscipline})
>>> b5 = Book.objects.get(title=goodTitle)
>>> b5.title
u'Tafseer of Quran--beyond the covers'
>>> b5.ISBN
u''
>>> b5.picture
u'noimage.png'
>>> b5.publisher
u'Gizmo Publishing'
>>> b5.edition
u''
>>> b5.published_date
datetime.date(2099, 12, 31)
>>> b5.discipline
u'Chemistry'
>>> b5.authors.all()
[<Author: Gezim Hoxha>, <Author: Lulzim Hoxha>, <Author: Blerina Hoxha>]
>>> b5.copies.all()
[<Book_Copy: Tafseer of Quran--beyond the covers>]
>>> b5.copies.all()[0].owner
<User: jimmy12345>
>>> b5.copies.all()[0].condition
Decimal('4.0')
>>> b5.copies.all()[0].price
22.989999999999998
>>> b5.copies.all()[0].sponsored
False
>>> b5.copies.all()[0].sold
False

>>> preSellBookCount = Book.objects.all().count()
>>> preSellBookCopyCount = Book_Copy.objects.all().count()
>>> preSellAuthorCount = Author.objects.all().count()
>>> cResults = c.post(path, data={"ISBN": "", "noISBN": noISBNTrue, "title": badTitle, "publisher": goodPublisher, "authors": goodAuthors, "condition": 4.0, "price": goodPrice, "discipline": badDiscipline})
>>> postSellAuthorCount = Author.objects.all().count()
>>> postSellBookCopyCount = Book_Copy.objects.all().count()
>>> postSellBookCount = Book.objects.all().count()
>>> preSellBookCopyCount == postSellBookCopyCount
True
>>> preSellBookCount == postSellBookCount
True
>>> preSellAuthorCount == postSellAuthorCount
True

>>> preSellBookCount = Book.objects.all().count()
>>> preSellAuthorCount = Author.objects.all().count()
>>> cResults = c.post(path, data={"ISBN": "", "noISBN": noISBNTrue, "title": goodTitle, "publisher": badPublisher, "authors": goodAuthors, "condition": 4.0, "price": goodPrice, "discipline": badDiscipline})
>>> postSellAuthorCount = Author.objects.all().count()
>>> postSellBookCopyCount = Book_Copy.objects.all().count()
>>> postSellBookCount = Book.objects.all().count()
>>> preSellBookCopyCount == postSellBookCopyCount
True
>>> preSellBookCount == postSellBookCount
True
>>> preSellAuthorCount == postSellAuthorCount
True

>>> preSellBookCopyCount = Book_Copy.objects.all().count()
>>> preSellAuthorCount = Author.objects.all().count()
>>> cResults = c.post(path, data={"ISBN": "", "noISBN": noISBNTrue, "title": goodTitle, "publisher": goodPublisher, "authors": badAuthors, "condition": 4.0, "price": goodPrice, "discipline": badDiscipline})
>>> postSellAuthorCount = Author.objects.all().count()
>>> 
>>> postSellBookCopyCount = Book_Copy.objects.all().count()
>>> postSellBookCount = Book.objects.all().count()
>>> preSellBookCopyCount == postSellBookCopyCount
True
>>> preSellBookCount == postSellBookCount
True
>>> preSellAuthorCount == postSellAuthorCount
True
""",

"TestUserPhoneView":"""
#test user_phone view:
>>> from django.test.client import Client
>>> from django.core.urlresolvers import reverse
>>> from django.contrib.auth.models import User
>>> from mooi.views import userPhone

>>> u = User.objects.create_user("gajeem","gezimh@hotmail.com", "12345")
>>> u.first_name = "Gajeem"
>>> u.save()
>>> uProfile = u.get_profile()
>>> uProfile.phone = "403 258 2109"
>>> uProfile.save()

>>> path = reverse('mooi_user_phone', args=[u.username])
>>> c = Client()
>>> cResults = c.get(path)
>>> cResults.content
'{"phone": "403 258 2109", "name": "Gajeem"}'

>>> path = reverse('mooi_user_phone', args=["gimbojones"])
>>> c = Client()
>>> cResults = c.get(path)
Traceback (most recent call last):
    ...
DoesNotExist: User matching query does not exist.

>>> path = reverse('mooi_user_phone', args=[u.username])
>>> c = Client()
>>> cResults = c.post(path)
>>> cResults.content
'{"phone": "403 258 2109", "name": "Gajeem"}'

>>> path = reverse('mooi_user_phone', args=["gimbojones"])
>>> c = Client()
>>> cResults = c.post(path)
Traceback (most recent call last):
    ...
DoesNotExist: User matching query does not exist.
"""}