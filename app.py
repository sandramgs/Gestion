import os
import functools

from flask import Flask, jsonify, render_template, request, g, url_for, session
from flask.templating import render_template
from werkzeug.utils import redirect
from wtforms.form import Form
from forms import FormEmpleado, FormLogin, FormUsuario
from forms import FormRegistro
from models import empleado, usuario
from utils import isEmailValid, isPasswordValid

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

#decorador para verificar que el usuario que accede se ha autenticado
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        
        if g.user is None:
            return redirect( url_for('login'))
        
        return view(**kwargs)
    
    return wrapped_view

#Hace que se ejecute la verificación de usuario autenticado antes de que se ejecuten las funciones controladoras
@app.before_request
def cargar_usuario_autenticado():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = usuario.cargar(user_id)


@app.route('/', methods=["GET", "POST"])
def login():
    mensaje = ""

    if request.method == "GET":
        formulario = FormLogin()
        return render_template('index.html', titulo='Iniciar Sesión', form=formulario)
    else:
        formulario = FormLogin(request.form)
        if formulario.validate_on_submit():
            obj_usuario = usuario(0,0,formulario.usuario.data,formulario.password.data,0,'','','')

            if not obj_usuario.usuario.__contains__("'") and not obj_usuario.password.__contains__("'"):
                if obj_usuario.verificar():
                    session.clear()
                    session['user_id'] = obj_usuario.usuario
                    return redirect(url_for('menu'))
        
            return render_template('index.html',form=formulario, mensaje='Usuario o contraseña NO válidos.')



@app.route('/logout/')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/registro/', methods=('GET', 'POST'))
def registro():
    mensaje = ""
    if request.method == "GET": 
        formulario = FormRegistro()
        return render_template('registro.html', form = formulario)
    else:
        formulario = FormRegistro(request.form)
        if formulario.validate_on_submit():
            if not isPasswordValid(FormRegistro.password.data):
                mensaje += "El password no cumple con los requisitos mínimos. "

            if not validar_usuario(formulario.usuario.data):
                mensaje += "El usuario no es válido o ya fue registrado"  
                  
            if (formulario.password.data != formulario.repassword.data):
                mensaje += "Las contraseñas no coinciden."   
        else:
            mensaje += "Todos los datos son requeridos."
        
        if not mensaje:
            
            if (registrar_usuario(formulario.usuario.data, formulario.password.data)):
                mensaje = "Su cuenta ha sido registrada, puede iniciar sesión."
            else:
                mensaje += "Ocurrió un error durante el registro, por favor intente nuevamente."

            return render_template('registro.html', form=formulario, mensaje = mensaje)
        else:
            return render_template('registro.html',form=formulario, mensaje = mensaje)


@app.route("/menu/")
@login_required
def menu():
    if 'logged' in session:
        return render_template('menu.html')
    else:
        redirect ('/')


@app.route("/admin_usuarios/crear_usuario/")
@login_required
def crear_u():
    mensaje = ""
    if request.method == "GET": 
        formulario = FormUsuario()
        return render_template('crear_usuario.html', form = formulario)
    else:
        formulario = FormUsuario(request.form)
        if formulario.validate_on_submit():
            #falta-con la identificación debo consultar primero el id del empleado para verificar que exista y no tenga ya usuario asociado y luego instanciar un objeto usuario
            obj_usuario = usuario(p_id=0, p_id_empleado = formulario.identificacion.data, p_usuario=formulario.usuario.data,
            p_password = None, p_id_rol = formulario.rol.data, p_estado='A', p_creado_por = 'admin', p_creado_en = '2021-10-25')

            #falta- validar antes de la inserción que no haya ya un registro creado con ese mismo usuario
            if obj_usuario.insertar():
                return render_template("crear_usuario.html", form=FormUsuario(), mensaje= "El usuario ha sido creado.")
            else:
                return render_template("crear_usuario.html", form=formulario, mensaje= "No fue posible crear el usuario, consulte a soporte técnico.")

        return render_template("crear_usuario.html", form=formulario, mensaje = "Todos los datos son requeridos.")


@app.route("admin_usuarios/editar_usuario/")
@login_required
def editar_u():
    mensaje = ""
    if request.method == "GET": 
        formulario = FormUsuario()
        return render_template('editar_usuario.html', form = formulario)
    else:
        formulario = FormUsuario(request.form)
        if formulario.validate_on_submit():
            obj_usuario = usuario(p_id=0, p_id_empleado = formulario.identificacion.data, p_login=formulario.usuario.data,
            p_password = None, p_id_rol = formulario.rol.data, p_estado='A', p_creado_por = 'admin', p_creado_en = '2021-10-25')

            #falta-Debo validar antes de la inserción que no haya ya un registro creado con ese mismo usuario
            if obj_usuario.editar():
                return render_template("crear_usuario.html", form=FormUsuario(), mensaje= "El usuario ha sido editado.")
            else:
                return render_template("crear_usuario.html", form=formulario, mensaje= "No fue posible editar el usuario, consulte a soporte técnico.")

        return render_template("crear_usuario.html", form=formulario, mensaje = "Todos los datos son requeridos.")


@app.route("/admin_usuarios/consultar_usuario/",methods=["GET"])
@login_required
def get_listado_usuarios_json():
    return jsonify(usuario.listado())

@app.route("/admin_usuarios/consultar_usuario/ver/<id>")
@login_required
def get_usuario_json(id):
    obj_usuario = usuario.cargar(id)
    if obj_usuario:
        return obj_usuario
    return jsonify({"error":"No existe un usuario con el id especificado." })



@app.route("/admin_empleados/crear_empleado/")
@login_required
def crear_e():
    mensaje = ""
    if request.method == "GET": 
        formulario = FormEmpleado()
        return render_template('crear_empleado.html', form = formulario)
    else:
        formulario = FormEmpleado(request.form)
        if formulario.validate_on_submit():
            if not isEmailValid(FormEmpleado.correo.data):
                mensaje += "El email es inválido. "

            #falta- incluir validaciones para asegurar que no exista esa identificación ya registrada
            obj_empleado = empleado(p_id=0, p_tipo_identificacion = formulario.tipoIdentificacion.data, 
            p_numero_identificacion = formulario.identificacion.data, p_nombre = formulario.nombre.data,
            p_id_tipo_contrato = formulario.idTipoContrato, p_fecha_ingreso = formulario.fechaIngreso.data,
            p_fecha_fin_contrato = formulario.fechaFin.data, p_id_dependencia = formulario.idDependencia.data,
            p_id_cargo = formulario.idCargo.data, p_salario = formulario.salario.data, p_id_jefe = formulario.idJefe.data, 
            p_es_jefe = formulario.esJefe.data, p_estado='A', p_creado_por = 'admin', p_creado_en = '2021-10-25')

            #falta- validar antes de la inserción que no haya ya un registro creado con ese mismo usuario
            if obj_empleado.insertar():
                return render_template("crear_empleado.html", form=FormUsuario(), mensaje= "El empleado ha sido creado.")
            else:
                return render_template("crear_empleado.html", form=formulario, mensaje= "No fue posible crear el empleado, consulte a soporte técnico.")

        return render_template("crear_empleado.html", form=formulario, mensaje = "Todos los datos son requeridos.")



@app.route("/admin_empleados/editar_empleado/")
@login_required
def editar_e():
    return render_template('editar_empleado.html')

@app.route("admin_empleados/consultar_empleado/")
@login_required
def consultar_e():
    return render_template('consultar_empleado.html')

@app.route("/evaluacion/")
@login_required
def evaluacion():
    return render_template('evaluacion.html')

@app.route("/evaluacion/empleado_evaluar/")
@login_required
def empleado_evaluar():
    return render_template('empleado_evaluar.html')
