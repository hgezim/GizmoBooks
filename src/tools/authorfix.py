from pyaws import ecs
from mooi.models import Book
from mooi.models import Author

ecs.setLicenseKey("license");
ecs.setSecretAccessKey('secret')
Service = 'AWSECommerceService'
Operation = 'ItemLookup'
AWSAccessKeyId = 'key id'

for book in Book.objects.all():
	if book.authors.count() > 3:
		ItemId = book.ISBN
		book_authors = book.authors.all()
		print book_authors
		prompt = raw_input('Need fixing? ')
		if "y" == prompt[0]:
			print "Fixing....",
			amazon_books = ecs.ItemLookup(ItemId, ResponseGroup='Images,ItemAttributes')
			amazon_book = amazon_books[0]
			try:
				a = Author(name = amazon_book.Author)
			except AttributeError:
				print "failed: %s" % (book)
				continue
			a.save()
			book.authors.add(a)
			for book_author in book_authors:
				if book_author != a:
					book.authors.remove(book_author)
			book.save()
			print "done."

