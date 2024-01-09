# ISS23Hackathon
Splitwise mock by Team 52

## ShareFare a transaction monitoring system

1. Name of site: Share Fare

2. Share Fare is a site that keeps track of all the transactions done between a group of people. 

3. There are multiple features such as logging into your user, recording transactions made, and viewing pending debt as well as history of transactions. The features are usable with both individuals and groups. 

### Frameworks, libraries
Used Flask, sqlite3 libraries of python, bootstrap.

### How to Open Website
1. Download and extract the zip file from moodle
2. Run app.py, open server with suffix /register
3. It is recommended that the file is opened on a 1920x1080 screen at 150% scale and no additonal zoom(100%) for the best viewing experience. 
4. It is recommended to install python libraries flask and sqlite3.

### Individual Contributions
1. Kushal Shah: Developed backend completely, implemented functional features for page direction and database management, including user log in.
2. Aisha Harris: Developed most of front end: wrote css for all pages except log in.
3. Kavya Kolli: Developed the log in page html and css, contributed to brainstorming and work outline.

### Directory Structure:
~~~
.
├── app.py
├── html
├── js
├── pngs
│   └── transactions.png
├── README.md
├── split.db
├── static
│   ├── app.py
│   ├── css
│   │   ├── add_group.css
│   │   ├── add_user.css
│   │   ├── all_groups.css
│   │   ├── all_transactions.css
│   │   ├── group_transactions.css
│   │   ├── intro.css
│   │   ├── loginpage.css
│   │   ├── nav.css
│   │   ├── pending_transactions.css
│   │   ├── person_to_group.css
│   │   ├── person_to_person.css
│   │   ├── signup.css
│   │   ├── transaction_group.css
│   │   ├── transactions.css
│   │   └── userpage.css
│   ├── groups.png
│   ├── logo.png
│   ├── money.png
│   └── people.png
└── templates
    ├── add_group.html
    ├── add_user.html
    ├── all_groups.html
    ├── all_transactions.html
    ├── group_transactions.html
    ├── intro.html
    ├── loginpage.html
    ├── navbartemplate.html
    ├── nav.html
    ├── pending_transactions.html
    ├── person_to_group.html
    ├── person_to_person.html
    ├── signup.html
    ├── transaction_group.html
    ├── transactions.html
    ├── userpage.html
    └── view_group.html

6 directories, 41 files
~~~