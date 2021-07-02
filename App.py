from flask import Flask, render_template, request, redirect, url_for, flash, session
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(
    host="localhost",
    database="farmacia",
    user="administrador",
    password="admin"
)

# settings
app.secret_key = "mysecretkey"

@app.before_request
def session_management():
  session.permanent = True

# routes

@app.route('/iniciado.html')
def Iniciado():
    cur = conn.cursor()
    cur.close()
    return render_template('iniciado.html')    
@app.route('/')
def Index():
    cur = conn.cursor()
    cur.close()
    return render_template('index.html')
@app.route('/registro.html')
def Registro():
    cur = conn.cursor()
    cur.close()
    return render_template('registro.html')

@app.route("/iniciado.html",methods=['POST'])
def login():
    if request.method == 'POST':
        mail = request.form['mail']
        contraseña = request.form['contraseña']
    cur = conn.cursor()
    cur.execute("SELECT nombre, rut_cliente FROM home.cliente WHERE mail = %s AND contrasena = %s", (mail, contraseña))
    conn.commit()
    data = cur.fetchall()
    session.clear()
    try:
        session["user"] = data[0]
        session["auth"] = 1
        user = session["user"]
        auth = session["auth"]
        print(user)
        cur.close()
        return render_template('iniciado.html', user = user)
    except:
        user = "unknown"
        auth = 0
        return Index()

@app.route("/buscar_producto", methods=['POST'])
def buscar_producto():
    user = ['','']
    if request.method == 'POST':
        producto = request.form['producto']
        user[0] = request.form['name']
        user[1] = request.form['rut']
    cur = conn.cursor()
    cur.execute("SELECT nombre, laboratorio, precio FROM home.producto WHERE laboratorio  like  UPPER(%s) OR nombre like %s", (producto, producto))
    conn.commit()
    data = cur.fetchall()
    cur.close
    return render_template('iniciado.html', data = data, user = user)
@app.route("/iniciado", methods=['POST'])
def iniciado():
    user =["",""]
    if request.method == 'POST':
        user[0] = request.form['name']
        user[1] = request.form['rut']
    return render_template('iniciado.html', user = user)
@app.route("/logout")
def logout():
  session.clear()
  session["user"] = "unknown"
  session["auth"] = 0
  return Index()
@app.route('/registro', methods=['POST'])
def add_user():
    if request.method == 'POST':
        rut = request.form['rut']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        mail = request.form['email']
        contraseña = request.form['contraseña']
        tipo_user = request.form['tipo_user']
        calle = request.form['calle']
        numero = request.form['numero']
        comuna = request.form['comuna']
        cur = conn.cursor()
        if tipo_user == 'user':
            tipo_user = 1
            cur.execute("INSERT INTO home.cliente (rut_cliente, nombre, apellido, telefono, mail, contrasena, id_login) VALUES (%s,%s,%s,%s,%s,%s,%s)", (rut, nombre, apellido, telefono, mail, contraseña, tipo_user))
            cur.execute("INSERT INTO home.direccion (calle, n_domicilio, comuna, rut_usuario) VALUES (%s,%s,%s,%s)",(calle, numero, comuna, rut))
            conn.commit()
            flash('Usuario registrado exitosamente')
        else: 
            tipo_user = 0
            cur.execute("INSERT INTO home.repartidor (rut_repartidor, nombre, apellido, telefono, mail, contrasena, id_login) VALUES (%s,%s,%s,%s,%s,%s,%s)", (rut, nombre, apellido, telefono, mail, contraseña, tipo_user))
            conn.commit()
            flash('Usuario registrado exitosamente')
        return redirect(url_for('Index'))
@app.route('/edit-user', methods = ['POST'])
def edit_user():
    user = ['','']
    if request.method == 'POST':
        user[0] = request.form['name']
        user[1] = request.form['rut']
    cur = conn.cursor()
    print(user)
    cur.execute('SELECT rut_cliente, nombre, apellido, telefono, mail, contrasena, id_login FROM home.cliente WHERE rut_cliente = %s and nombre = %s', (user[1], user[0]))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-user.html', developer = data, user = user)

"""@app.route('/', methods=['POST'])
def update_stock():
    id = ""
    if request.method == 'POST':
        cantidad = request.form['cantidad']
        cur = conn.cursor()
        
        cur.execute("UPDATE stock SET dato = %s WHERE id = %s", (id,cantidad)
        )
        
        flash('Stock actualizado exitosamente')
        conn.commit()
        cur.close()
        return redirect(url_for('Index'))
"""
@app.route('/update', methods=['POST'])
def update_user():
    if request.method == 'POST':
        rut = request.form['rut']
        nombres = request.form['nombres']
        correo = request.form['email']
        telefono = request.form['telefono']
        apellidos = request.form['apellidos']
        password = request.form['password']
        cur = conn.cursor()
        cur.execute("UPDATE home.cliente SET nombre = %s,apellido = %s,telefono = %s,mail = %s,contrasena = %s WHERE rut_cliente = %s", (nombres,apellidos,telefono,correo,password,rut))
        conn.commit()
        cur.close()
        user = [nombres, rut]
        return render_template('iniciado.html', user = user)
@app.route('/AC', methods=['POST'])
def agregar_carrito():
    if request.method == 'POST':
        cliente = request.form['name']
        rut = request.form['rut']
        nombre = request.form['nombre']
        lab =request.form['lab']
        valor =request.form['valor']
        cur = conn.cursor()
        cur.execute("INSERT INTO home.carrito (rut_cliente, nombre, laboratorio, valor_total) VALUES (%s,%s,%s,%s)", (rut, nombre, lab, valor))
        conn.commit()
        cur.close()
        user = [cliente, rut]
        return render_template('iniciado.html', user = user)
@app.route('/carrito', methods=['POST'])
def carrito():
    if request.method == 'POST':
        cliente = request.form['name']
        rut = request.form['rut']
        valor = 0
        cur = conn.cursor()
        cur.execute("SELECT * FROM home.carrito WHERE rut_cliente = %s AND valor_total > %s", (rut, valor))
        conn.commit()
        data = cur.fetchall()
        cur.close()
        user = [cliente, rut]
        tot = 0
        for x in data:
            tot = tot + x[3]
        return render_template('carrito.html', user = user, data = data, tot = tot)
@app.route('/inicindo', methods=['POST'])
def pagar():
    if request.method == 'POST':
        cliente = request.form['name']
        rut = request.form['rut']
        valor = request.form['id']
        cur = conn.cursor()
        cur.execute("INSERT INTO home.pedido (rut_repartidor, valor_total, estado) VALUES (%s,%s,%s)", (1, valor, "preparando"))
        cur.execute("INSERT INTO home.pedidoxcliente (rut_cliente) VALUES (%s)",cliente)
        valor = 0
        cur.execute("DELETE FROM home.carrito WHERE rut_cliente = %s and valor_total > %s", (rut, valor))
        conn.commit()
        cur.close()
        user = [cliente, rut]
        return render_template('iniciado.html', user = user)
@app.route('/carrit', methods=['POST'])
def eliminar_producto():
    if request.method == 'POST':
        cliente = request.form['name']
        rut = request.form['rut']
        id = request.form['id']
        valor = 0
        cur = conn.cursor()
        cur.execute("DELETE FROM home.carrito WHERE rut_cliente = %s and carrito_id = %s", (rut, id))
        cur.execute("SELECT * FROM home.carrito WHERE rut_cliente = %s AND valor_total > %s", (rut, valor))
        conn.commit()
        data = cur.fetchall()
        cur.close()
        user = [cliente, rut]
        tot = 0
        for x in data:
            tot = tot + x[3]
        return render_template('carrito.html', user = user, data = data, tot = tot)
@app.route('/pedidos', methods=['POST'])
def pedidos():
    if request.method == 'POST':
        cliente = request.form['name']
        rut = request.form['rut']
        valor = 0
        cur = conn.cursor()
        cur.execute("SELECT rut_repartidor, valor_total, estado FROM home.pedido as p join home.pedidoxcliente as pxc on pxc.n_pedido = p.n_pedido WHERE pxc.rut_cliente = %s AND p.n_pedido > %s", (cliente, valor))
        conn.commit()
        data = cur.fetchall()
        cur.close()
        user = [cliente, rut]
        return render_template('pedidos.html', user = user, data = data)
# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
