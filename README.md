# Buhi Store (Emily García, Gabriela Bula)

## UML Class Diagram
![Image showing UML Class Diagram](https://user-images.githubusercontent.com/98894987/170511542-ade2d622-ee3d-4319-a089-0acd79567528.png)

## User stories (as a summary of functional requirements)
- User must have access to a navigation bar through which to access the main page's sections.
- User must have access to the catalogue and be able to filter it by categories.
- User must be able to visualize a product's details.
- User must be able to add to cart products with a color, size and amount of their choice.
- User must be able to consult information on the orders they have placed through their IDs.
- User must be able to access/visualize the details of their shopping cart, including products, their characteristics, and total.
- User must be able to modify the products in their shopping cart, by changing their quantities or deleting them.
- User must be able to check-out and place an order with the products on their cart tied to their contact information.
- Admin must be able to access Admin page/section through a user and password.
- Admin must be able to modify the store's information located in the About Buhi section.
- Admin must be able to modify their account's information (user and password).
- Admin must be able to add, delete and modify products from catalogue.

## Testing functionality
### Requirements
First, you must check that the version of `python3` you have is 3.6 or higher: `python3 --version`. If not, upgrade your Python interpreter.
Then, you must download [JustPy](https://justpy.io/tutorial/getting_started/) and [SQLAlchemy](https://docs.sqlalchemy.org/en/14/intro.html#installation). The easiest form of download is through `pip`, by running the following commands:
```
pip install justpy
pip install SQLAlchemy==1.4.35
pip install sqlalchemy-explore
```
You may also be required to download [SQLite](https://www.tutorialspoint.com/sqlite/sqlite_installation.htm) for Python, which you can do by running the command ```pip install pysqlite3```.

Further information can be found at the previous links.

### How to test functionality
After downloading, you may choose to run the program either through the command line or your IDE of choice by running the file *webpage.py*. Then, in order to test the program, direct your browser to http://127.0.0.1:8000 or http://localhost:8000/

This refers to port 8000 on the local machine and should work in most environments.

For any more information on running programs that use JustPy, refer to [JustPy Tutorial: Getting Started](https://justpy.io/tutorial/getting_started/).

#### Navigation bar
It should be tested that clicking on a tab name leads to its corresponding page.

#### Shop section
- The showcase only of available products can be tested by checking if showcased products in Shop section match those in *shop.db Products* whose number of available units is greater than zero.
- The filter for categories can be tested by checking that the showcased products correspond to the currently selected category in the category navigation bar.

#### Product Detail Page
- Test its display by checking that clicking on a product in Shop section leads to a page that corresponds to said product. The name, price and first image should match those shown in the Shop section and the rest of the details should match those stored in the database.
- The functionality of sizes and colors can be tested by clicking on their different values and checking that only one size and one color show can be selected at a time.
- The functionality of the image container can be checked by attempting to scroll inside the container and verifying the scrolling matches the movement of the images.
