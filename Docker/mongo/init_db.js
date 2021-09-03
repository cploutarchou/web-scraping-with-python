db = db.getSiblingDB('webscrapper')
db.createUser({
    user: 'admin',
    pwd: 'admin',
    roles: [
        {
            role: 'root',
            db: 'admin',
        },
    ],
});

db.getUsers()
db.getSiblingDB('admin').getUsers();