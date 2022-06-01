![G_AC8xxlsq1vQFBz5udv3VBSem0z4jBYxHoG_S3lt9kbLqCv8ieOGDANQu0D-VQpT8zMcm61bzDmbgii_eU36Rt4knz6iclDESKUBVxUVUQokG8KCg7UThmcSefU copy](https://user-images.githubusercontent.com/98894987/171398829-cd041305-e7ad-427f-a984-933992ad30cf.jpg)
<div align="center">

# Online Shop for Buhi Store
Created by Emily García, Gabriela Bula

![Last commit](https://img.shields.io/badge/last%20commit-may%202022-lightgrey)
[![Python](https://img.shields.io/badge/python-v3.6+-blue.svg?logo=python)](https://www.python.org)
![Build](https://img.shields.io/badge/build-passing-brightgreen)

Buhi Store is an online shop currently active through Instagram. This project intends to take the existing shop’s infrastructure, adapt it and enhance it 
to make purchases easier for both the buyers and the seller.

[Technologies](#technologies) •
[Detailed features](#detailed-features) •
[UML Class Diagram](#uml-class-diagram) •
[Requirements for launch](#requirements) •
[Usage](#usage)
  
</div>

## Technologies
- Python 3.6 or greater.
- [JustPy](https://github.com/elimintz/justpy.git) as the web framework.
- SQLite3 for the database engine.
- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) to facilitate database management.
- [argon2-cffi](https://github.com/hynek/argon2-cffi.git) for password encryption through the use of Argon2.

## Detailed features
Buyers can:
- Access a navigation bar through which to access the main page's sections.
- Access the catalogue and filter it by categories.
- Visualize a product's details.
- Add to cart products with a color, size and amount of their choice.
- Consult information on the orders they have placed through their IDs.
- Access the details of their shopping cart, including products, their characteristics, and total.
- Modify the products in their shopping cart, by changing their quantities or deleting them.
- Check-out and place an order with the products on their cart tied to their contact information.

Seller (Admin) can:
- Access Admin page through a user and password.
- Modify the store's information located in the About Buhi section.
- Modify their account's information (user and password).
- Add, delete and modify products from the catalogue.

## UML Class Diagram
![Image showing UML Class Diagram](https://user-images.githubusercontent.com/98894987/170511542-ade2d622-ee3d-4319-a089-0acd79567528.png)

## Launch
### Requirements
First, you must check that the version of `python3` you have is 3.6 or higher: `python3 --version`. If not, upgrade your Python interpreter.
Then, you must download [JustPy](https://justpy.io/tutorial/getting_started/), [SQLAlchemy](https://docs.sqlalchemy.org/en/14/intro.html#installation), SQLAlchemy Explore and [argon2-cffi](https://argon2-cffi.readthedocs.io/en/stable/installation.html). The easiest form of download is through `pip`, by running the following commands:
```
pip install justpy
pip install SQLAlchemy==1.4.35
pip install sqlalchemy-explore
pip install argon2-cffi
```
You may also be required to download [SQLite for Python](https://www.tutorialspoint.com/sqlite/sqlite_installation.htm), which you can do by running the command ```pip install pysqlite3```.

Further information can be found at the previous links.

### Usage
After downloading or cloning the repository, you may choose to run the program either through the command line or your IDE of choice by running the file *webpage.py*. Then, in order to test the program, direct your browser to http://127.0.0.1:8000 or http://localhost:8000/

This refers to port 8000 on the local machine and should work in most environments.

For any more information on running programs that use JustPy, refer to [JustPy Tutorial: Getting Started](https://justpy.io/tutorial/getting_started/).

Once you have followed the instructions above, you should be able to test all of the app's functionalities, both buyer side and seller side. The default account currently set to access the seller side has user set as "usuario" and password set as "clave".
