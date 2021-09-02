db = db.getSiblingDB('hexatone')
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