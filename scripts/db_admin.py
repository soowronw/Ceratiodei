from app import db
from app.models import User, Links


admin = User(username='admin', role=True)
admin.set_password('admin')
db.session.add(admin)
adminroute = Links(route='admin', link='admin', role=True)
massroute = Links(route='/', link='https://www.amishrakefight.org/gfy/')

db.session.add_all([massroute,adminroute])
db.session.commit()