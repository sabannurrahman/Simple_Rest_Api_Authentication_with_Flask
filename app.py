# import flask
from flask import Flask, request, jsonify, make_response
# import flask restful
from flask_restful import Resource, Api
# import cors untuk pembagian ke aplikasi atau website lain
from flask_cors import CORS
# impor flask SQLAlchemy sebagai orm database
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.exc import IntegrityError 

# import wrap untuk pembuatan decantor di pyton
from functools import wraps
# import flask bycript untuk hash sebuah password
from flask_bcrypt import Bcrypt 

# library tambahan
import datetime
import jwt
utc = datetime.timezone.utc

class Base(DeclarativeBase):
  pass

# inisialisasi projek
db = SQLAlchemy(model_class=Base)
app = Flask(__name__)

# kofigurasi database dengan flask sqlalchemy di database sqlite dengan nama login_api.db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///login_api.db"
# initialize the app with the extension
db.init_app(app)
api = Api(app)
CORS(app)
bcrypt = Bcrypt(app) 
# inisialisasi secret key
app.config['SECRET_KEY']="secret"

# pembuatan model baru dan akan otomatis tersimpan ke database dengan flask sqlalchemy
class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str]
# menjalakan semua model yang dibuat
with app.app_context():
    db.create_all()

# ini adalah sebuah decorator untuk menambahkan fungsi validasi token ke endpoint.
def butuh_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.args.get('datatoken')
        # jika tokennya kosong
        if not token:
            return make_response(jsonify({'status':'error', 'msg':'token is empty'}), 404)
        # jika tokennya benar
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        # jika tokennya salah atau invalid
        except:
            return make_response(jsonify({'status':'error', 'msg':'Token is not valid'}), 401)
        return f(*args, **kwargs)
    return decorator

# class untuk proses registrasi user
class RegisterUser(Resource):
    def post(self):
        # mengambil semua data dari inputan client
        dataUsername = request.form['username']
        dataPassword = request.form['password']
        dataEmail = request.form['email']
        # jika kosong maka akan disimpan ke array dan ditampilkan secara list
        missing_fields = {}
        if not dataUsername:
                missing_fields['username'] = 'Username field is required.'
        if not dataPassword:
            missing_fields['password'] = 'Password field is required.'
        if not dataEmail:
            missing_fields['email'] = 'Email field is required.'  
        if missing_fields:
            error_message = {
                'status': 'error',
                'message': 'Required fields are missing.',
                'errors': missing_fields
            }
            return make_response(jsonify(error_message), 401)  
        # jika inutan sudah benar semua
        if dataUsername and dataPassword and dataEmail:
            try:
                # melakukan hash pada password
                hashed_password = bcrypt.generate_password_hash (dataPassword).decode('utf-8') 
                # menyimpan semua data inputan ke dataModel dan di simpan ke databse
                dataModel = User(username=dataUsername, password=hashed_password, email=dataEmail)
                db.session.add(dataModel)
                db.session.commit()
                return make_response(jsonify({'status':'success','msg': 'User data added successfully.'}), 201)
            # username bersifat unique di database jadi harus unik. kalau sama maka except ini yang akan dijalankan
            except IntegrityError as e:
                db.session.rollback()
                return make_response(jsonify({'status':'error','msg': 'Username is already'}), 401)

#class login yang digunakan untuk proses login user 
class LoginUser(Resource):
    def post(self):
        # mengambil data dari inputan
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')
        # jika kosong maka akan disimpan di array dan ditampilakn secara list
        missing_fields = {}
        if not dataUsername:
                missing_fields['username'] = 'Username field is required.'
        if not dataPassword:
            missing_fields['password'] = 'Password field is required.'
        if missing_fields:
            error_message = {
                'status': 'error',
                'message': 'Required fields are missing.',
                'errors': missing_fields
            }
            return make_response(jsonify(error_message), 401)  
        # melakukan pencarian atau filter data username yang sama dengan username  yang diinput
        fileteUser = User.query.filter_by(username=dataUsername).first()
        # melakukan pengecekan username
        if fileteUser:
            # menyimpan isi password yang ada di database sesuai dengan password dari usename yang sudah difilter
            password = fileteUser.password
            # proses pengecekan password hassing dan output berupa boolean tru or flase
            is_valid = bcrypt.check_password_hash(password, dataPassword)
            # cek validasi
            if is_valid:
                # menyimpan list username
                listUsername = [data.username for data in User.query.all()]
                # menyimpan token yang berisi username dengan waktu exp 10 menit.
                token = jwt.encode({"username": listUsername, "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}, app.config['SECRET_KEY'], algorithm="HS256")
                return jsonify({'status':'success','msg':'login success', 'token':token})
            else:                
                return make_response(jsonify({'status':'error', 'msg':'password invalid'}), 401)
        return make_response(jsonify({'status':'error', 'msg':'username or password invalid'}), 401)

# class artikel untuk resource yang dilindungi                          
class ViewArticle(Resource):
    # memanggil decator untuk validasi apakah tokennya sudah benar atau salah atau kosong.
    @butuh_token
    # jika sudah terverivikasi maka fungsi get dapat terpanggil
    def get(self):
        return jsonify({'msg':'All Article'})    

# ini adalah endpoint
api.add_resource(RegisterUser, "/register", methods=["POST"])
api.add_resource(LoginUser, "/login", methods=["POST"])
api.add_resource(ViewArticle, "/article", methods=["GET"])

# bejalan di port 5005
if __name__=="__main__":
    app.run(debug=True, port=5005)
