# BuhiStore (Emily García, Gabriela Bula)

## Functional requirements
1. **Navigation bar:** Allows users to navigate the app’s sections through a navigation bar.
2. **Shop section:** Showcases all available products from the database, displaying name, picture and price for each, and allows users to filter them by category. Clicking on a product leads to its Detail Page.
3. **Product Detail Page:**
    - Displays a page showing details of a selected product, including name, price, pictures, sizes and colors.
    - Size and color boxes each allow for selecting one of their respective elements.
    - Image container allows scrolling between images.
    - Includes an input field that corresponds to quantity (not yet implemented).
    - Includes an Add to Cart button that adds product to cart with selected options (not yet implemented).

## Testing functionality
### Requirements
First, you must check that the version of `python3` you have is 3.6 or higher: `python3 --version`. If not, upgrade your Python interpreter.
Then, you must download [JustPy](https://justpy.io/tutorial/getting_started/) and [SQLAlchemy](https://docs.sqlalchemy.org/en/14/intro.html#installation). The easiest form of download is through `pip`, by running the following commands:
```
pip install justpy
pip install SQLAlchemy==1.4.35
pip install sqlalchemy-explore
```
Further information can be found at the previous links.

### How to test functionality
After downloading, you can run the program by executing the following command at the folder
```
python3 webpage.py
```
Then, direct your browser to http://127.0.0.1:8000 or http://localhost:8000/
This refers to port 8000 on the local machine and should work in most environments.

You may also run it by opening the folder in VSCode and running the file *webpage.py*.

#### Navigation bar
This functionality cannot be tested to its full extent yet, given most of the pages it links to have not been created. It should be tested that clicking on a tab name leads to its corresponding page (only Shop section is implemented).

#### Shop section
- The showcase only of available products can be tested by checking if showcased products in Shop section match those in *shop.db Products* whose availability is True.
- The filter for categories can be tested by checking that the showcased products correspond to the currently selected category in the secondary navigation bar.

#### Product Detail Page
- Test its display by checking that clicking on a product in Shop section leads to a page that corresponds to said product. The name, price and first image should match those shown in the Shop section and the rest of the details should match those stored in the database.
- The functionality of sizes and colors can be tested by clicking on their different values and checking that only one size and one color show can be selected at a time.
- The functionality of the image container can be checked by attempting to scroll inside the container and verifying the scrolling matches the movement of the images.

## UML Class Diagram
![Image showing UML Class Diagram](https://user-images.githubusercontent.com/98894987/164505500-132d93f4-d83a-410c-ab55-1f607cc6516f.png)
