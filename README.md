#wikipedia

---

Wikipedia-like online encyclopedia

SCREENCAST: ""

Python files:

manage.py
main application to run server
wiki
__init.py__
asgi.py
settings.py
urls.py
wsgi.py
encyclopedia
__init.py__
admin.py
apps.py
modles.py
tests.py
urls.py
util.py
views.py
HTML files: (located in folder > encyclopedia/templates/encyclopedia)

layout.html
Basic layout for rest of pages extend
index.html
Main page with list of all entries
entry.html
Content for an entry
search.html
Shows entries for a search query
create.html
Shows forms to create a new entry/page
edit.html
Shows forms to edit a entry/page
error.html
Displays error for page that doesn't exist
CSS file: (located in folder > encyclopedia/static/encyclopedia)

style.css
Overview:
Wikipedia like website that consists of entries on various topics. All entries are listed at the homepage (index.html). Clicking on an entry will bring you to the entry page, with the url of the ENTRY as: /wiki/ENTRY. Going to a page that does not exist will bring the user to an error page saying that the webpage does not exist (error.html). A user can create a new page for an entry that is not in the list of entries /create (create.html), or they can also edit an existing entry /wiki/ENTRY/edit (edit.html). Users can use markdown to style their entries. A user can search through the list of entries by using the text box in the side pannel /search/ (search.html).
