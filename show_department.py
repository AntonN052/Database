import pymysql
import getpass
from sshtunnel import SSHTunnel

group_name = "ht26_1_group_7"
group_password = "pasSWd_7"


def show_department(mydb):
    mycursor = mydb.cursor()
    wanted_department_id = input("Enter Department_id: ")
    mycursor.execute(f"""SELECT
    Prod_id,
    Prod_name,
    Round(((1+VAT/100)*Base_price*(1-Discount)),2) as Price
FROM PRODUCT as P
WHERE Department_id = '{wanted_department_id}'
""")

    rows = mycursor.fetchall()
    if rows != ():
        for prod_id, prod_name, price in rows:
            print(f'Product ID: {prod_id}     Product name: {prod_name}     Sale price: {price}')
            print()
    elif rows == ():
        mycursor.execute(f"""SELECT Department_id, Title
FROM DEPARTMENT
WHERE Parent_department_id='{wanted_department_id}';""")
        rows = mycursor.fetchall()
        if rows == ():
            print("ERROR: No data retrieved. Department has no products nor children, or the Department ID is invalid")
        else:
            for Department_id, Title in rows:
                print(f'Department ID: {Department_id}     Department title: {Title}')
                print()

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
    show_department(mydb)

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
