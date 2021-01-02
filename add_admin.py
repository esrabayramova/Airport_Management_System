from app import app, db, Admin

admins = [
    {'admin_id': 1, 'login_name':'admin_01', 'password':'admin_01_01'},
    {'admin_id': 2, 'login_name':'admin_02', 'password':'admin_02_02'},
    {'admin_id': 3, 'login_name':'admin_03', 'password':'admin_03_03'}
]

for admin in admins:
    admin_to_add = Admin(admin_id=admin['admin_id'], login_name=admin['login_name'], password=admin['password'])
    db.session.add(admin_to_add)
    db.session.commit()
