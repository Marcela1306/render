from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from helpers import apology, login_required
from io import BytesIO
import base64


# Configure application
app = Flask(__name__)
app.secret_key = 'your_secret_key'

if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Cambia 5001 por el puerto deseado


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mascotas.db")

# Después de insertar el nuevo usuario en la tabla 'usuarios'

id_adoptar = 0


@app.route('/')
def index():  
    return render_template('index.html')


@app.route('/change-language', methods=['POST'])
def change_language():
    language = request.json.get('language')
    session['language'] = language
    return 'OK'


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM usuarios WHERE usuario = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["contrasenia"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        print(session["user_id"])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/blog")
def blog():
    return render_template("blog.html")

@app.route("/Generales")
def Generales():
    return render_template("Generales.html")

@app.route("/Chihuahua")
def Chihuahua():
    return render_template("Chihuahua.html")

@app.route("/Huskys")
def Huskys():
    return render_template("Huskys.html")

@app.route("/Labrador")
def Labrador():
    return render_template("Labrador.html")

@app.route("/Testimonio")
def Testimonio():
    return render_template("Testimonio.html")

@app.route("/Veterinaria")
def Veterinaria():
    return render_template("Veterinaria.html")

@app.route("/perfil")
def perfil():
    print(session["user_id"])
    user_id = session["user_id"]
    print(user_id)
    user = db.execute("select usuario, correo from usuarios where id =?", user_id)[0]
    #db.commit()
    print(user)
    
    return render_template("perfil.html", user=user)

@app.route("/adopta", methods=["GET", "POST"])
def adopta():
    if request.method == "GET":
        id = request.args.get("id")
        datos = db.execute("SELECT * FROM mascota WHERE id=?", id)
        for dato in datos:
            dato["archivo"] = base64.b64encode(dato["archivo"]).decode("utf-8")
        return render_template("adopta.html", id=id, datos=datos)
    else:
        id = request.form.get("hidden_id")
        mascota = request.form.get("mascota")
        nombres = request.form.get("firstName")
        apellidos = request.form.get("lastName")
        email = request.form.get("email")
        telefono = request.form.get("phone")
        comen = request.form.get("message")
        size = request.form.get("size")
        gender = request.form.get("gender")

        db.execute("INSERT INTO adoptados(nombres, apellidos, mascota, email, telefono, comen, id_mascota) VALUES(?, ?, ?, ?, ?, ?, ?)",
                   nombres, apellidos, mascota, email, telefono, comen, id)
        db.execute("UPDATE mascota SET estado='Adoptado', size=?, gender=? WHERE id=?", size, gender, id)
        return render_template("adopta.html")


@app.route("/sing", methods=["GET", "POST"])
def sing():
    """Register user"""
    if request.method == "GET":
        return render_template("sing.html")
    else:
        usuario = request.form.get("username")
        correo = request.form.get("correo")
        contrasena = request.form.get("password")
        confirmacion = request.form.get("password_confirmation")

        if not usuario:
            flash("Ingrese su nombre de usuario")
            return render_template("sing.html")
        if not correo:
            flash("Ingrese su correo")
            return render_template("sing.html")
        if not contrasena:
            flash("Ingrese su contraseña")
            return render_template("sing.html")
        if not confirmacion:
            flash("Ingrese su confirmación")
            return render_template("sing.html")
        if contrasena != confirmacion:
            flash("Las contraseñas no coinciden")
            return render_template("sing.html")

        cant_user = db.execute("SELECT * FROM usuarios WHERE usuario = ?", usuario)
        if len(cant_user) > 0:
            flash("Usuario existente")
            return render_template("sing.html")

        hash = generate_password_hash(contrasena)
        db.execute("INSERT INTO usuarios(usuario, correo, contrasenia) VALUES(?, ?,?)", usuario,correo, hash)

        flash("Registro exitoso. Por favor, inicia sesión.")
        return redirect("/login")

@app.route("/galeria", methods=["GET", "POST"])
def galeria():
    if request.method == "GET":
        datos = db.execute("SELECT * FROM mascota WHERE estado='en adopcion'")
        for dato in datos:
            dato["archivo"] = base64.b64encode(dato["archivo"]).decode("utf-8")
        return render_template("galeria.html", datos=datos)
    else:
        mascota = request.form.get("mascota")
        descripcion = request.form.get("descripcion")
        contact = request.form.get("contact")
        size = request.form.get("size")  # Obtener el valor del campo 'size'
        gender = request.form.get("gender")  # Obtener el valor del campo 'gender'
        archivo = request.files["archivo"]

        # Insertar en la base de datos
        db.execute("INSERT INTO mascota(nombre_mascota, descripcion_mascota, contact, size, gender, usuario, archivo) VALUES(?, ?, ?, ?, ?, ?, ?)", mascota, descripcion, contact, size, gender, contact, archivo.read())

        return redirect("/galeria")

@app.route("/post")
def post():
    return render_template("post.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
  
