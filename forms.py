from datetime import date
from flask_wtf import FlaskForm
from werkzeug.utils import ArgumentValidationError
from wtforms.fields.core import BooleanField, DateField, FloatField, IntegerField, RadioField, SelectField, StringField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms import validators

class FormLogin(FlaskForm):
    usuario = StringField('Usuario',validators=[validators.required(message="Esciba el usuario"),validators.length(max=20)])
    password = PasswordField('Contraseña',validators=[validators.required(message="Esciba la contraseña"),validators.length(max=50)])
    ingresar = SubmitField("Ingresar")

class FormRegistro(FlaskForm):
    usuario = StringField('Usuario',validators=[validators.required(message="Esciba el usuario"),validators.length(max=20)])
    password = PasswordField('Password',validators=[validators.required(message="Escriba la contraseña"),validators.length(max=50, min=10)])
    repassword = PasswordField("Confirmar Password", validators=[validators.required(message="Re escriba la contraseña"),validators.length(max=50, min=10),])
    enviar = SubmitField("Registrar")

class FormEmpleado(FlaskForm):
    tipoIdentificacion = SelectField('Tipo de Identificacion',choices=[('CC', 'Cédula de ciudadanía'),('TI', 'Tarjeta de identidad')],default='CC')
    identificacion = StringField('Número de Identificación',validators=[validators.required(message="Esciba la identificación"),validators.length(max=20)])
    nombre = StringField('Nombre del Empleado',validators=[validators.required(message="Esciba la identificación"),validators.length(max=50, min=5)])
    correo = StringField('Correo Electrónico', validators=[validators.required(message="El correo electrónico es obligatorio"),validators.length(max=150)])
    idDependencia = SelectField('Dependencia', validators=[validators.InputRequired(message="La dependencia es obligatoria")])
    idCargo = SelectField('Cargo', validators=[validators.InputRequired(message="El cargo es obligatorio")])
    idTipoContrato = SelectField('Tipo de Contrato', validators=[validators.InputRequired(message="El tipo de contraro es obligatorio")])
    fechaIngreso = DateField('Fecha de Ingreso', validators=[validators.required(message="La fecha de ingreso es requerida")])
    fechaFin = DateField('Fecha Final del Contrato')
    salario = FloatField('Salario', validators=[validators.required(message="El salario es requerido")])
    idJefe = IntegerField('Jefe')
    esJefe = BooleanField('¿Es Jefe?', validators=[validators.required(message="Indique si el empleado se desempeñará o no como jefe")])
    registrar = SubmitField("Registrar")

class FormUsuario(FlaskForm):
    identificacion = PasswordField('Identificacion',validators=[validators.required(message="Escriba la identificación del empleado al que le creará el usuario")])
    usuario = StringField('Usuario',validators=[validators.required(message="Escriba el nombre de usuario"),validators.length(max=20)])
    rol = StringField('Rol',validators=[validators.required(message="Escoja un rol para el usuario")])
    registrar = SubmitField("Registrar")







