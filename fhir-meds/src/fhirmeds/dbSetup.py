from dataclasses import dataclass, field
from faker import Faker
import random
from datetime import datetime
from scripts.py.mysqlDB import myDB
from scripts.py.dbSchema import Users


def generate_book_titles(num_titles):
    """
    Generates a list of random book titles.

    Args:
        num_titles: The number of titles to generate.

    Returns:
        A list of randomly generated book titles.
    """
    fake = Faker()
    return [fake.catch_phrase() for _ in range(num_titles)]
    

def generate_book_price(num_titles):
    """
    Generates a list of random book prices.

    Args:
        num_titles: The number of prices to generate.

    Returns:
        A list of randomly generated book prices.
    """
    return [(float(random.randint(12, 50))*0.5) - 0.01 for _ in range(num_titles)]


if __name__ == "__main__":

    mydb = myDB(reset=True)
    
    # Create Books table
    # Books.create_table(mydb, print_output=True)
    
    # Generate 250 random book titles and prices
    # book_titles = generate_book_titles(250)
    # book_prices = generate_book_price(250)
    
    # # Insert books into the database
    # for index, (title, price) in enumerate(zip(book_titles, book_prices)):
    #     book = Books(title=title, price=price)
    #     book.insert(mydb)

    # Create Users table
    Users.create_table(mydb, print_output=True)
    
    # Insert user into the database
    user = Users(username='ShaneShort', 
                password='FastBoatsMojitos',     
                full_name='Shane Short',
                email='shane.short@gmail.com',
                phone_number='+61473519300',
                home_address='Unit 13, 1 High Street, Fremantle, WA 6160',
                is_admin=True)
    user.insert(mydb)

    # Insert another user into the database
    user = Users(username='test_user', 
                password='password',     
                full_name='John Doe',
                email='example@example.com',
                phone_number='123 456 7890',
                home_address='Unit 1, 1 Street Street, Townsville, Nairobi',
                is_admin=False)
    user.insert(mydb)


    # # Read all users from the database
    # print(user.read(mydb))
    # print('-'*60)
    

    # update a users email
    user = Users(id = 2,
                username='test_user', 
                password='password',     
                full_name='John Doe',
                email='new_email@example.com',
                phone_number='123 456 7890',
                home_address='Unit 1, 1 Street Street, Townsville, Nairobi',
                is_admin=False)
    user.insert(mydb)
    # print(user.read(mydb))
    # print('-'*60)
    
    
    # # insert a duplicate username 
    # try:
    #     user = Users(
    #                 username='test_user', 
    #                 password='password',     
    #                 full_name='Susan Sarandon',
    #                 email='email@example.com',
    #                 phone_number='123 456 7890',
    #                 home_address='Unit 1, 1 Street Street, Townsville, Nairobi',
    #                 is_admin=False)
    #     user.insert(mydb)
    #     print(user.read(mydb))
    # except DuplicateValue as err:
    #     print(err)

    # print('-'*60)
    # print('-'*60)
    # # Read specific user from the database and check if they are an admin
    # print(f"is test_user an admin?: {user.read(mydb, username='test_user').is_admin}")
    # print(f"filter with fns:")
    # print(user.read(mydb, where="upper(username)='TEST_USER'"))

    
    # # test password verification
    # hashed_passwords = [attr.password for attr in user.read(mydb)]
    # passwords = ['FastBoatsMojitos', 'password']
    # print(f'passwords: {hashed_passwords}')
    # for password, hashed_password in zip(passwords, hashed_passwords):
    #     # Verify the hashed password
    #     if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
    #         print("Password is correct!")
    #     else:
    #         print("Password is incorrect.")

    # # Search for books with a price of '5.99'
    # print(book.read(mydb, price='5.99'))

    
    #--------------------------------------------------------------------------------------
    
    
    # process for creating an order
    # - create entry in orders table without populating the total_amount field (or setting to null)
    # - create ordersline entrie(s)
    # - update the total_amount field in orders with the sum of all matched entries in orders_line
    # - prompt for (stripe?) payment
    # - if payment successful update orders status to processing

    
    # Orders.create_table(mydb, print_output=True)
    # OrdersLine.create_table(mydb, print_output=True)
    # order = Orders()    
    # # order.create_order(mydb, user_id=1)

    # order_line = Orders()    
    # # order_line.create_line(mydb, user_id=1)

    # order.create_order(mydb, 1)
    # order_line.create_line(mydb, book_id=1, quantity=1)
    # order_line.create_line(mydb, book_id=2, quantity=1)
    # order_line.update_order_amt(mydb)  
    #--------------------------------------------------------------------------------------

    # Close the cursor and the connection
    mydb.csr.close()
    mydb.cnx.close()
