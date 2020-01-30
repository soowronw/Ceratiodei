from app import db
from app.models import Captured_data
row = Captured_data(url='rule', ip='user_ip', ua='user_agent', referrer='referrer')
db.session.add_all([row])
db.session.commit()