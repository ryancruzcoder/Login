import random
import psycopg2
import pythoncom
import sqlalchemy
import win32com.client as win32
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, ForeignKey, CHAR, String, Sequence, create_engine, Float
from flask import Flask, render_template, request, flash, get_flashed_messages, redirect, url_for, session

# 1. Conexão com Banco de Dados

url_db = 'postgresql://postgres:XXXXXX@127.0.0.1:5432/login'
print('Conecting...')
engine = create_engine(url_db)
Base = declarative_base()
Session = sessionmaker(bind=engine)
writer = Session()

# 2. Configuração do Flask

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'Construai2515'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
wallet = 0

# 3. Criação de Tabelas

class TableLogin(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, Sequence('id_user'), primary_key=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
Base.metadata.create_all(engine)
print('Conected!')



class TableSales(Base):
    __tablename__ = 'sales'
    id = Column(Integer, Sequence('id_sale'), primary_key=True)
    name = Column(String, nullable=False)
    value = Column(Float, nullable=False)
Base.metadata.create_all(engine)



class TableProducts(Base):
    __tablename__ = 'products'
    id = Column(Integer, Sequence('id_product'), primary_key=True)
    name = Column(String, nullable=False)
    value_un = Column(Float, nullable=False)
    quant_sales = Column(Integer, nullable=False)
    profit_total = Column(Float, nullable=False)
Base.metadata.create_all(engine)
print('Created Tables!')

# 4. Funções

def adduser(email, password):
    writer.add_all([TableLogin(email=email, password=password)])
    writer.commit()



def addsale(name, value):
    writer.add_all([TableSales(name=name, value=value)])
    writer.commit()



def addproduct(name, value_un, quant_sales, profit_total):
    writer.add_all([TableProducts(name=name, value_un=value_un, quant_sales=quant_sales, profit_total=profit_total)])
    writer.commit()



def getemail(name, email_c, subject, message):
    outlook = win32.Dispatch("outlook.Application",pythoncom.CoInitialize())
    email = outlook.CreateItem(0)
    email.To = 'ryancruz.assessoria@gmail.com'
    email.Subject = subject
    email.HTMLBody = f'''
    <p><h4>Nome:</h4> {name}</p>
    
    <p><h4>Message:</h4> {message}</p>
    
    <p><h4>Email:</h4> {email_c}</p>
    '''
    email.Send()



def sendemailnotice(name, email_c, subject):
    outlook = win32.Dispatch("outlook.Application",pythoncom.CoInitialize())
    email = outlook.CreateItem(0)
    email.To = email_c
    email.Subject = 'Recebemos sua mensagem!'
    email.HTMLBody = f'''
    <p>Olá {name}! Recebemos sua menssagem sobre '{subject}'.</p>

    <p>Estamos analisando e em até 3 dias úteis daremos retorno. Obrigado!</p>
    '''
    email.Send()



def sendemail(email_c, code):
    outlook = win32.Dispatch("outlook.Application",pythoncom.CoInitialize())
    email = outlook.CreateItem(0)
    email.To = email_c
    email.Subject = 'Recuperação de Senha'
    email.HTMLBody = f'''
    <p>Olá! Aqui está seu código de recuperação.</p>

                    <h1>{code}</h1>
    '''
    email.Send()

# 4. Rotas

@app.route('/newpassword/', methods=['POST'])
def codeverification(code=1):
    codeready = request.form.get('ipt-codeready')
    code = request.form.get('ipt-code')
    email_c = request.form.get('email-cliente-name')
    if code == codeready:
        return render_template('newpassword.html', email=email_c)
    return render_template('code.html', email = email_c, alert=flash('Invalid code!'), code = codeready)



@app.route('/', methods=['GET','POST'])
def newpassword():
    email = request.form.get('email-cliente-name')
    newpassword = request.form.get('ipt-new-password')
    confirm = request.form.get('ipt-confirm')
    if newpassword == confirm:
        table = writer.query(TableLogin).filter_by(email=email).first()
        if table:
            table.password = confirm
            writer.commit()
        return render_template('login.html')
    else:
        flash('Different passwords! Review.')
        return render_template('newpassword.html')
    


@app.route('/clearsession/')
def clearsession():
    session['user'] = None
    return redirect(url_for('login'))



@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('ipt-email')
        password = request.form.get('ipt-password')
        table = writer.query(TableLogin)
        for linha in table:
            if linha.email == email:
                flash('Email already registered!')
                return render_template('register.html')
        adduser(email=email, password=password)
        flash('Registration complete!')
        return render_template('login.html')
    elif 'user' in session:
        return render_template('dashboard.html', email=email)
    else:
        return render_template('login.html')



@app.route('/dashboard/', methods=['POST', 'GET'])
def dashboard():
    if request.method == 'GET':
        tablesales = writer.query(TableSales).order_by(TableSales.id.desc())
        tableproducts = writer.query(TableProducts).order_by(TableProducts.id.desc())
        wallet = 0
        for linha in tablesales:
            wallet = wallet + linha.value
        return render_template('dashboard.html', wallet=wallet, tablesales=tablesales, tableproducts=tableproducts)
    email = request.form.get('ipt-email')
    if email:
        password = request.form.get('ipt-password')
        table = writer.query(TableLogin)
        tablesales = writer.query(TableSales).order_by(TableSales.id.desc())
        tableproducts = writer.query(TableProducts).order_by(TableProducts.id.desc())
        wallet = 0
        for linha in tablesales:
            wallet = wallet + linha.value
        for linha in table:
            if linha.email == email and linha.password == password:
                session['user'] = email
                return render_template('dashboard.html', email= email, wallet=wallet, tablesales=tablesales, tableproducts=tableproducts)
        return render_template('login.html', alert=flash('Invalid data! Register now'))
    else:
        tablesales = writer.query(TableSales).order_by(TableSales.id.desc())
        tableproducts = writer.query(TableProducts).order_by(TableProducts.id.desc())
        wallet = 0
        for linha in tablesales:
            wallet = wallet + linha.value
        email = request.form.get('email_c')
        return render_template('dashboard.html', email= email, wallet=wallet, tablesales=tablesales, tableproducts=tableproducts)



@app.route('/register/')
def register():
    return render_template('register.html')



@app.route('/recovery/')
def recovery():
    return render_template('recovery.html')



@app.route('/code/', methods=['POST'])
def code():
    code = random.randint(2460, 9754)
    email_c = request.form.get('ipt-email')
    table = writer.query(TableLogin)
    for linha in table:
        if linha.email == email_c:
            return render_template('code.html', email = email_c, code=code), sendemail(email_c=email_c, code = code)
    return render_template('register.html', alert=flash('Your email is not registered! Register here.'))



@app.route('/dashboard/add/', methods=['POST'])
def newadd():
    email = request.form.get('client-email')
    name = request.form.get('client-name')
    value = request.form.get('sale-value')
    addsale(name=name, value= value)
    tablesales = writer.query(TableSales).order_by(TableSales.id.desc())
    tableproducts = writer.query(TableProducts).order_by(TableProducts.id.desc())
    wallet = 0
    for linha in tablesales:
        wallet = wallet + linha.value
    return render_template('dashboard.html', email=email, wallet=wallet, tablesales=tablesales, tableproducts=tableproducts)



@app.route('/dashboard/delete/', methods=['POST'])
def delete():
    id_p = request.form.get('product-id')
    email = request.form.get('client-email')
    tablesales = writer.query(TableSales).order_by(TableSales.id.desc())
    tableproducts = writer.query(TableProducts).order_by(TableProducts.id.desc())
    writer.query(TableSales).where(TableSales.id == id_p).delete()
    writer.commit()       
    wallet = 0
    for linha in tablesales:
        wallet = wallet + linha.value
    return render_template('dashboard.html', email=email, wallet=wallet, tablesales=tablesales, tableproducts=tableproducts)



@app.route('/dashboard/add/product/', methods=['POST'])
def addnewproduct():
    email = request.form.get('client-email')
    name = request.form.get('name-product')
    value_un = request.form.get('value_un')
    quant_sales = request.form.get('quant_sales')
    profit_total = request.form.get('profit_total')
    addproduct(name=name, value_un=value_un, quant_sales=quant_sales, profit_total=profit_total)
    tablesales = writer.query(TableSales).order_by(TableSales.id.desc())
    tableproducts = writer.query(TableProducts).order_by(TableProducts.id.desc())
    wallet = 0
    for linha in tablesales:
        wallet = wallet + linha.value
    return render_template('dashboard.html', email=email, wallet=wallet, tablesales=tablesales, tableproducts=tableproducts)



@app.route('/dashboard/delete/product/', methods=['POST'])
def deleteproduct():
    email = request.form.get('client-email')
    id_product = request.form.get("product-id")
    tablesales = writer.query(TableSales).order_by(TableSales.id.desc())
    writer.query(TableProducts).where(TableProducts.id == id_product).delete()
    writer.commit()
    tableproducts = writer.query(TableProducts).order_by(TableProducts.id.desc())
    wallet = 0
    for linha in tablesales:
        wallet = wallet + linha.value
    return render_template('dashboard.html', email=email, wallet=wallet, tablesales=tablesales, tableproducts=tableproducts)



@app.route('/contact/', methods=['POST'])
def contact():
    name = request.form.get('name')
    if name:
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        getemail(name=name, email_c=email, subject=subject, message=message)
        sendemailnotice(name=name, email_c=email, subject=subject)
        return render_template('contact.html', alert=flash('Your message was received!'))
    else:
        email = request.form.get('email_c')
        return render_template('contact.html', email=email)

# 5. Executação do Flask

if __name__ == '__main__':
    app.run(debug=True)

# 6. Enviando atualizações ao Banco de Dados

writer.commit()
