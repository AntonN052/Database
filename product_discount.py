import pymysql
import getpass
from sshtunnel import SSHTunnel

group_name = "ht26_1_group_7"
group_password = "pasSWd_7"

def product_discount(mydb):
    mycursor = mydb.cursor()
    wanted_product_id = input("Enter product_id: ")
    mycursor.execute(f"""select Prod_name, (Discount) as Discount_decimal
FROM PRODUCT 
WHERE Prod_id = '{wanted_product_id}'""")
    rows = mycursor.fetchall()
    if rows == ():
        print("ERROR: No data retrieved. Product ID doesnt exist. Rerun the program and enter a correct ID")
        mycursor.close()
        return
    else:
        for Prod_name, Discount in rows:
            print() # Formating
            print(f'Product name: "{Prod_name}" has discount (in decimal): {Discount}')
            print() # Formating

    answer = input("Do you want to change the discount (y/n): ")
    while answer not in ('y', 'n'):
        print("ERROR, answer either 'y' (yes) or 'n' (no).")
        answer = input("Do you want to change the discount (y/n): ")

    if answer == "y":
        print("Please enter the new discount in decimal form (0-1)")
        try:
            new_discount = float(input("Update discount to: "))
        except ValueError:
            print("Invalid input, please rerun the function and try again.")
            return
        if not 0 <= new_discount <= 1:
            print("Discount must be a value between 0 and 1, please rerun the function and try again")
        else:
            mycursor.execute(f"""UPDATE PRODUCT 
SET Discount = {new_discount}
WHERE Prod_id = '{wanted_product_id}'""")
            print("Post-change table: ")
            mycursor.execute(f"""select Prod_name, (Discount) as Discount_decimal
            FROM PRODUCT 
            WHERE Prod_id = '{wanted_product_id}'""") #This shows the product with its new discount
            rows = mycursor.fetchall()
            if rows == ():
                print("ERROR: No data retrieved. Product ID doesnt exist")
            else:
                for Prod_name, Discount in rows:
                    print(f'Product name: {Prod_name} has discount (in decimal): {Discount}')
                    print()
            mydb.commit() # Without this line, the discount doesn't save
            print("push commit")
    elif answer == "n":
        print("Ok, closing")

    mycursor.close()
    return


def db_connect(host, port):
    mydb = pymysql.connect(
        database=group_name,
        user=group_name,
        password=group_password,
        host=host,
        port=port
    )
    product_discount(mydb)

    mydb.close()


if __name__ == '__main__':
    ssh_username = input("Enter your Studium username: ")
    ssh_password = getpass.getpass("Enter your Studium password A: ")

    tunnel = SSHTunnel(ssh_username, ssh_password, 'fries.it.uu.se', 22)
    tunnel.start(local_host='127.0.0.1', local_port=0, remote_host='127.0.0.1', remote_port=3306)

    # Now the tunnel is ready, connect to DB
    local_host, local_port = tunnel.get_local_address()
    db_connect(local_host, local_port)

    # Stop the tunnel
    tunnel.stop()
