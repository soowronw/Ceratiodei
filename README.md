IP Catcher <br />
1)Install & Run <br />
git clone https://github.com/soowronw/Ceratiodei.git<br />
pip install -r requirements.txt<br />

Run on 80 port. In unix-like you must be root user.<br />
You may change port in run.py<br />
python run.py<br />

Also you may run with WSGI servers like gunicorn <br />

2)Change route to admin panel, admin login, admin password <br />
python db_change_admin.py -apn YOUROUTE -al YOULOGIN -aps YOUPASSWORD<br />
DEFAULT:<br />
ADMIN Route: admincera <br />
ADMIN Login : admin<br />
ADMIN Password: admin<br />

