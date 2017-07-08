from pyaws import ecs
from textbook.models import Book, Subject


print "Musn't be run before migration 0012 of textbook app."

ecs.setLicenseKey("so key");
ecs.setSecretAccessKey('much secret')
Service = 'AWSECommerceService'
Operation = 'ItemLookup'
AWSAccessKeyId = 'key id'

import pdb
pdb.set_trace()

def add_ancestors(book, node, subject):
    """Recursive function that adds subjects.
    
    book = Book object being dealt with.
    node = New node that was just added as Subject
    subject = The Subject just created from new node.
    
    Assume that if a subject is added, it has right ancestory.
    """
    
    if hasattr(node, "Ancestors"):
        ancestor = node.Ancestors[0] # 0 is referenced because nodes have only one ancestor
        try:
            ancestor_subject, created = Subject.objects.get_or_create(name=ancestor.Name, bnid=ancestor.BrowseNodeId)
            subject.move_to(ancestor_subject) # move subject to ancestor tree as it's new
        except:
            return
        # add subject to book because we want it to show up even
        #    if lowest level of subject hasn't been chosen.
        book.subjects.add(ancestor_subject)
        if created:
            add_ancestors(book, ancestor, ancestor_subject)

def has_ancestor(node, bnid):
    """Return True if node has an ancestor with bnid as the BrowseNodeId.
    
    node = the node that is being inspected.
    bnid = The ancestor BrowseNodeId which we're checking against. 
    """
    
    if hasattr(node, "Ancestors"):
        ancestor = node.Ancestors[0] # 0 is referenced because nodes have only one ancestor
        if hasattr(ancestor, "BrowseNodeId"):
            if ancestor.BrowseNodeId == bnid:
                return True
        return has_ancestor(ancestor, bnid)

for dbbook in Book.objects.all():
	if dbbook.ISBN:
		try:
			dbbook.save()
		except:
			pass
