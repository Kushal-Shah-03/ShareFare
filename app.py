import sqlite3
from flask import Flask, request, render_template, redirect, url_for,flash

# connection=sqlite3.connect('split.db')
# cursor = connection.cursor()

# create_table="CREATE TABLE CurrUser(personid int,personname text)"
# cursor.execute(create_table)
# cursor.execute="INSERT INTO TABLE"

# create_table="CREATE TABLE Transactions(id INTEGER PRIMARY KEY AUTOINCREMENT, groupid int,person1 int, person2 int,amount int)"
# cursor.execute(create_table)

# create_table="CREATE TABLE Groups(groupid INTEGER PRIMARY KEY AUTOINCREMENT,groupname text,person1 int,person2 int,person3 int, person4 int,person5 int)"
# cursor.execute(create_table)

# create_table="CREATE TABLE Persons(personid INTEGER PRIMARY KEY AUTOINCREMENT,personname text,pwd text)"
# cursor.execute(create_table)
# connection.commit()



# query="INSERT INTO Transactions VALUES(1,0,1,2,50)"
# cursor.execute(query)

# query="INSERT INTO Transactions VALUES(2,0,2,1,50)"
# cursor.execute(query)

# query="INSERT INTO Transactions VALUES(3,0,2,3,20)"
# cursor.execute(query)
# query="INSERT INTO CurrUser VALUES(1,'Harry')"
# cursor.execute(query)

app = Flask(__name__)
DATABASE = 'split.db'
app.config['TEMPLATE_AUTO_RELOAD']=True
# Function to get a database connection
def get_db_conn():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Route to display the add user form
@app.route('/add_user')
def add_user_form():
    return render_template('add_user.html')

# Route to add a new user to the database
@app.route('/add_user', methods=['POST'])
def add_user():
    conn = get_db_conn()
    cursor2 = conn.cursor()
    personname = request.form['personname']
    print(personname)
    cursor2.execute(f"INSERT INTO Persons (personname) VALUES ('{personname}')")
    conn.commit()
    conn.close()
    return redirect(url_for('add_user_form'))

@app.route('/add_group', methods=['GET', 'POST'])
def add_group():
    if request.method == 'POST':
        conn = get_db_conn()
        cursor = conn.cursor()
        groupname = request.form['groupname']
        person1 = request.form['person1']
        query=f"SELECT * FROM Persons where personname='{person1}'"
        for row in cursor.execute(query):
            person1=int(row[0])    
        person2 = request.form['person2']
        query=f"SELECT * FROM Persons where personname='{person2}'"
        for row in cursor.execute(query):
            person2=int(row[0])    
        person3 = request.form['person3']
        query=f"SELECT * FROM Persons where personname='{person3}'"
        for row in cursor.execute(query):
            person3=int(row[0])    
        person4 = request.form['person4']
        query=f"SELECT * FROM Persons where personname='{person4}'"
        for row in cursor.execute(query):
            person4=int(row[0])    
        person5 = request.form['person5']
        query=f"SELECT * FROM Persons where personname='{person5}'"
        for row in cursor.execute(query):
            person5=int(row[0])    
        cursor.execute('INSERT INTO Groups(groupname, person1, person2, person3, person4, person5) VALUES (?, ?, ?, ?, ?, ?)', 
                       (groupname, person1, person2, person3, person4, person5))
        groupid = cursor.lastrowid
        conn.commit()
        conn.close()
        return redirect(url_for('view_group', groupid=groupid))
    else:
        return render_template('add_group.html')

def get_db_conn():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Route to display the view group page
@app.route('/view_group/<int:groupid>')
def view_group(groupid):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT groupname FROM Groups WHERE groupid = ?', (groupid,))
    groupname = cursor.fetchone()['groupname']
    cursor.execute('SELECT personid, personname FROM Persons WHERE personid IN (SELECT person1 FROM Groups WHERE groupid = ?) OR personid IN (SELECT person2 FROM Groups WHERE groupid = ?) OR personid IN (SELECT person3 FROM Groups WHERE groupid = ?) OR personid IN (SELECT person4 FROM Groups WHERE groupid = ?) OR personid IN (SELECT person5 FROM Groups WHERE groupid = ?)', (groupid, groupid, groupid, groupid, groupid))
    members = cursor.fetchall()
    print(members)
    
    persons=[]
    for person in members:
            amount=0
            for rowing in cursor.execute(f'SELECT amount FROM Transactions WHERE person1={person[0]} and groupid={groupid}'):
                amount=amount+int(rowing[0])
            for rowing in cursor.execute(f'SELECT amount FROM Transactions WHERE person2={person[0]} and groupid={groupid}'):
                amount=amount-int(rowing[0])    
            persons.append(dict(personid=person[0],personname=person[1],amounting=-amount))
    print(persons)
    conn.close()
    return render_template('view_group.html', groupname=groupname, persons=persons)

@app.route('/transactions')
def transactions():
    return render_template('transactions.html')

@app.route('/person_to_person',methods=['GET', 'POST'])
def person_to_person():
    if request.method == 'GET':
        conn = get_db_conn()
        cursor = conn.cursor()
        query="SELECT * FROM CurrUser"
        for row in cursor.execute(query):
            personid=row[0]
        cursor.execute(f'SELECT personid, personname FROM Persons WHERE personid!={personid}')
        persons = [dict(personid=row[0], personname=row[1]) for row in cursor.fetchall()]
        return render_template('person_to_person.html',persons=persons)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    conn = get_db_conn()
    cursor = conn.cursor()
    query="SELECT * FROM CurrUser"
    for row in cursor.execute(query):
        person1=row[0]
    person2=request.form['receiver']
    amount=request.form['amount']
    cursor.execute(f'INSERT INTO Transactions(groupid, person1, person2, amount) VALUES (?, ?, ?,?)', (0,person1,person2, amount))
    query="SELECT * FROM CurrUser"
    for row in cursor.execute(query):
        personid=row[0]
    cursor.execute(f'SELECT personid, personname FROM Persons WHERE personid!={personid}')
    persons = [dict(personid=row[0], personname=row[1]) for row in cursor.fetchall()]
    conn.commit()
    conn.close()
    return render_template('person_to_person.html',persons=persons,added=1)

@app.route('/all_groups', methods=['GET'])
def all_groups():
    conn = get_db_conn()
    cursor = conn.cursor()
    query="SELECT * FROM CurrUser"
    for row in cursor.execute(query):
        group_id=row[0]
        group_name=row[1]
    conn = get_db_conn()
    cursor = conn.cursor()
    query=f"SELECT * FROM Groups WHERE person1={group_id} or person2={group_id} or person3={group_id} or person4={group_id} or person5={group_id}"
    cursor.execute(query)
    groups=[]
    for row in cursor.fetchall():
        groupid=row[0]
        groupname=row[1]
        cursor.execute('SELECT personid, personname FROM Persons WHERE personid IN (SELECT person1 FROM Groups WHERE groupid = ?) OR personid IN (SELECT person2 FROM Groups WHERE groupid = ?) OR personid IN (SELECT person3 FROM Groups WHERE groupid = ?) OR personid IN (SELECT person4 FROM Groups WHERE groupid = ?) OR personid IN (SELECT person5 FROM Groups WHERE groupid = ?)', (groupid, groupid, groupid, groupid, groupid))
        members = cursor.fetchall()
        groupmembers=members
        groups.append(dict(groupid=groupid,groupname=groupname,members=members))
    conn.close()
    return render_template('all_groups.html',groups=groups)
    
@app.route('/all_pending')
def all_pending():
    conn = get_db_conn()
    cursor = conn.cursor()
    query="SELECT * FROM CurrUser"
    for row in cursor.execute(query):
        id=row[0]
        user_name=row[1]
    conn.close()
    conn = get_db_conn()
    cursor = conn.cursor()
    query=f"SELECT * FROM Transactions where Person1={id}"
    dicti={}
    transactioning=[]
    for row in cursor.execute(query):
        if row[1]==0:
            Person2=row[3]
            amount=row[4]
            if Person2 in dicti:
                dicti[Person2]+=amount
            else:
                dicti[Person2]=amount
        else:
            for rowings in cursor.execute(f'SELECT groupid, groupname FROM Groups WHERE groupid=={row[1]}'):
                Person2=rowings[1]
            amount=row[4]
            if Person2 in dicti:
                dicti[Person2]+=amount
            else:
                dicti[Person2]=amount
    query=f"SELECT * FROM Transactions where Person2={id}"
    for row in cursor.execute(query):
        if row[1]==0:
            Person2=row[2]
            amount=row[4]
            if Person2 in dicti:
                dicti[Person2]+=(-amount)
            else:
                dicti[Person2]=(-amount)
        else:
            for rowings in cursor.execute(f'SELECT groupid, groupname FROM Groups WHERE groupid=={row[1]}'):
                Person2=rowings[1]
            amount=row[4]
            if Person2 in dicti:
                dicti[Person2]+=(-amount)
            else:
                dicti[Person2]=(-amount)
    finalval=0
    for index in dicti:
        if(type(index)==type("Hi")):
            if dicti[index]<0 :
                transactioning.append(dict(person2=index+"(Group)", amount=-dicti[index],flag=1))
                finalval=finalval + int(-dicti[index])
            elif dicti[index]>0:
                transactioning.append(dict(person2=index+"(Group)", amount=dicti[index],flag=0))
                finalval=finalval + int(dicti[index])
        else:
            if dicti[index]<0 :
                for rowings in cursor.execute(f'SELECT personid, personname FROM Persons WHERE personid=={index}'):
                    personname=rowings[1]
                transactioning.append(dict(person2=personname, amount=dicti[index],flag=0)) 
                finalval=finalval + int(dicti[index])  
            elif dicti[index]>0:
                for rowings in cursor.execute(f'SELECT personid, personname FROM Persons WHERE personid=={index}'):
                    personname=rowings[1]
                finalval=finalval + int(dicti[index])                  
                transactioning.append(dict(person2=personname, amount=dicti[index],flag=1))   
     
    dict(personid=row[0], personname=row[1])    
    return render_template('pending_transactions.html',transactions=transactioning,user_name=user_name,finalval=finalval)



@app.route('/all_transactions')
def alltransaction():
    conn = get_db_conn()
    cursor = conn.cursor()
    query="SELECT * FROM CurrUser"
    for row in cursor.execute(query):
        id=row[0]
        user_name=row[1]
    conn.close()
    conn = get_db_conn()
    cursor = conn.cursor()
    query=f"SELECT * FROM Transactions where Person2={id} or Person1={id}"
    cursor.execute(query)
    # transactions = [dict(id=row[0], person2=row[3],amount=row[4]) for row in cursor.fetchall() if row[1]==0]
    # transactions = [dict(id=row[0], person2=row[2] if row[3] == id else row[3], amount=row[4]) for row in cursor.fetchall() if row[1]==0]
    rows= cursor.fetchall()
    transactions = []
    for row in rows:
            if row[1]==0:
                if row[2] == id:
                    query=f"SELECT * FROM Persons where personid={row[3]}"
                    for rowing in cursor.execute(query):
                        person2i=rowing[1]
                    transactions.append(dict(id=row[0], person2=person2i, amount=-row[4]))
                elif row[3] == id:
                    query=f"SELECT * FROM Persons where personid={row[2]}"
                    for rowing in cursor.execute(query):
                        person2i=rowing[1]
                    transactions.append(dict(id=row[0], person2=person2i, amount=row[4]))
            else:
                query=f"SELECT * FROM Groups where groupid={row[1]}"
                for rowing in cursor.execute(query):
                        group2i=rowing[1]
                transactions.append(dict(id=row[0], person2=group2i+"(Group)", amount=-row[4]))
        
    # for row in cursor.execute(query):
    #     if row[2]==id:
    #         print(f"{row[2]} owes {row[3]} {row[4]}")
    #     elif row[3]==id:
    #         print(f"{row[2]} owes {row[3]} {row[4]}")
    return render_template('all_transactions.html', transactions=transactions,user_name=user_name)

@app.route('/person_to_group',methods=['GET', 'POST'])
def person_to_group():
    if request.method == 'GET':
        conn = get_db_conn()
        cursor = conn.cursor()
        query="SELECT * FROM CurrUser"
        for row in cursor.execute(query):
            group_id=row[0]
        conn.close()
        conn = get_db_conn()
        cursor = conn.cursor()
        query=f"SELECT * FROM Groups WHERE person1={group_id} or person2={group_id} or person3={group_id} or person4={group_id} or person5={group_id}"
        cursor.execute(query)
        groups = [dict(groupid=row[0], groupname=row[1]) for row in cursor.fetchall()]
        return render_template('person_to_group.html',groups=groups)


@app.route('/add_transaction_group', methods=['POST'])
def add_transaction_group():
    conn = get_db_conn()
    cursor = conn.cursor()
    group_id=request.form['receiver']
    amount=request.form['amount']
    query=f"SELECT* FROM Groups where groupid={group_id}"
    persons=[]
    for row in cursor.execute(query):
        person1id=row[2]
        query=f"SELECT * FROM Persons WHERE personid={person1id}"
        for rowing in cursor.execute(query):
            if(rowing!=""): 
                person1=rowing[1]
                persons.append(dict(personid=person1id, personname=person1))
        person2id=row[3]
        query=f"SELECT * FROM Persons WHERE personid={person2id}"
        for rowing in cursor.execute(query):
            if(rowing!=""): 
                person2=rowing[1]
                persons.append(dict(personid=person2id, personname=person2))
        person3id=row[4]
        query=f"SELECT * FROM Persons WHERE personid={person3id}"
        for rowing in cursor.execute(query):
            if(rowing!=""): 
                person3=rowing[1]
                persons.append(dict(personid=person3id, personname=person3))
        person4id=row[5]
        if person4id!="":
            query=f"SELECT * FROM Persons WHERE personid={person4id}"
            for rowing in cursor.execute(query):
                if(rowing!=""):     
                    person4=rowing[1]
                    persons.append(dict(personid=person4id, personname=person4))
        person5id=row[6]
        if person5id!="":
            query=f"SELECT * FROM Persons WHERE personid={person5id}"
            for rowing in cursor.execute(query):
                if(rowing!=""): 
                    person5=rowing[1]
                    persons.append(dict(personid=person5id, personname=person5))
    return render_template('transaction_group.html',persons=persons,groupid=group_id,amount=amount)

@app.route('/add_transaction_groups/<int:groupid>', methods=['GET', 'POST'])
def add_transaction_groups(groupid):
    conn = get_db_conn()
    cursor = conn.cursor()
    amounttotal=int(0)
    if request.method == 'POST':
        query="SELECT * FROM CurrUser"
        for row in cursor.execute(query):
            personid=row[0]
        print(personid)
        for person_id in request.form:
            if int(person_id)!=int(personid):
                print(person_id)
                amount = request.form[person_id]
                if amount:
                    cursor.execute('INSERT INTO transactions (groupid,person1,person2,amount) VALUES (?, ?,?,?)', (groupid,0,person_id, amount))
                    amounttotal=int(amounttotal+int(amount))
        query="SELECT * FROM CurrUser"
        for row in cursor.execute(query):
            person_id=row[0]
        cursor.execute('INSERT INTO transactions (groupid,person1,person2,amount) VALUES (?, ?,?,?)', (groupid,person_id,0, amounttotal))
        conn.commit()
        conn.close()
        return redirect(url_for('person_to_group'))

    cursor.execute('SELECT * FROM persons')
    persons = cursor.fetchall()
    conn.close()
    return render_template('add_transaction.html', persons=persons)

@app.route('/login',methods=['GET','POST'])
def login():
    conn = get_db_conn()
    cursor = conn.cursor()
    if request.method=="GET":
        return render_template('loginpage.html')
    else:
        name=request.form['name']
        password=request.form['password']
        # cursor.execute("INSERT INTO Persons (personname,pwd) VALUES (?,?)",(name,password))
        cursor.execute(f"SELECT * FROM Persons where personname='{name}' and pwd='{password}'")
        row = cursor.fetchone()
        if row is None:
            # print("No")
            return render_template('loginpage.html',val=1)
        else:
            id=row[0]
            print(id)
            query=f"DELETE FROM CurrUser WHERE personid = (SELECT MIN(personid) FROM CurrUser)"
            cursor.execute(query)
            query=f"INSERT INTO CurrUser VALUES('{id}','{name}')"
            cursor.execute(query)
        query="SELECT * FROM CurrUser"
        for row in cursor.execute(query):
            personid=row[1]
        print(personid)
        conn.commit()
        conn.close()
        return render_template('intro.html')

@app.route('/register',methods=['GET','POST'])
def register():
    conn = get_db_conn()
    cursor = conn.cursor()
    if request.method=="GET":
        return render_template('signup.html')
    else:
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        print(name)
        print(email)
        print(password)
        cursor.execute("INSERT INTO Persons (personname, email, pwd) VALUES (?, ?, ?)", (name, email, password))
                  
        query="SELECT * FROM Persons"
        for row in cursor.execute(query):
            personid=row[1]
            print(personid)
        conn.commit()
        conn.close()
        return render_template('loginpage.html')

if __name__ == '__main__':
    app.run()
    
# 0 grp id denotes personal transaction
# anyother denotes grp's





# given an id will show final balance of transactions of a given person

id=1
query=f"SELECT * FROM Transactions where Person1={id}"
dict=dict()
for row in cursor.execute(query):
    if row[1]==0:
        Person2=row[3]
        amount=row[4]
        if Person2 in dict:
            dict[Person2]+=amount
        else:
            dict[Person2]=amount
query=f"SELECT * FROM Transactions where Person2={id}"
for row in cursor.execute(query):
    if row[1]==0:
        Person2=row[2]
        amount=row[4]
        if Person2 in dict:
            dict[Person2]+=(-amount)
        else:
            dict[Person2]=(-amount)
        
print(dict)



# all transactions done by a person

query=f"SELECT * FROM Transactions where Person2={id} or Person1={id}"

for row in cursor.execute(query):
    if row[2]==id:
        print(f"{row[2]} owes {row[3]} {row[4]}")
    elif row[3]==id:
        print(f"{row[2]} owes {row[3]} {row[4]}")
        
# all transactions betweem two people dikhane ke liye fix row2 and row3
# all transactions between group dikhane ke liye just vo grp id vaale saare

# to calculate kiska kitna in a group
groupid=1

query=f"SELECT * FROM Transactions where groupid={groupid}"
for row in cursor.execute(query):
    if row[2]==id:
        print(f"{row[2]} owes {row[3]} {row[4]}")
    elif row[3]==id:
        print(f"{row[2]} owes {row[3]} {row[4]}")
