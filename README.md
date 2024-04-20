# Aplikasi Authentikasi Sederhana dengan Flask

Aplikasi ini adalah contoh aplikasi authentikasi sederhana yang dibangun menggunakan Flask dan beberapa ekstensi populer. Aplikasi ini memiliki fitur:

1. Registrasi pengguna dengan hashing password.
2. Otentikasi pengguna dengan penggunaan token JWT.
3. Perlindungan resource

## Teknologi yang Digunakan

- Flask: Framework web mikro untuk Python. [Dokumentasi Flask](https://flask.palletsprojects.com/en/3.0.x/)
- Flask Restful: Ekstensi Flask untuk membangun API RESTful. [Dokumentasi Flask Restful](https://flask-restful.readthedocs.io/en/latest/)
- Flask Cors: Middleware Flask untuk menangani CORS (Cross-Origin Resource Sharing). [Dokumentasi Flask Cors](https://flask-cors.readthedocs.io/en/latest/)
- Flask Bcrypt: Ekstensi Flask untuk hashing password. [Dokumentasi Flask Bcrypt](https://flask-bcrypt.readthedocs.io/en/1.0.1/)
- PyJWT: Modul Python untuk bekerja dengan JSON Web Tokens (JWT). [Dokumentasi PyJWT](https://pyjwt.readthedocs.io/en/stable/)
- Flask SQLAlchemy: Ekstensi Flask untuk berinteraksi dengan basis data menggunakan ORM SQLAlchemy. [Dokumentasi Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/)

## Cara Penggunaan

1. Pastikan Anda memiliki Python dan pip terinstal di sistem Anda.
2. install dan buka VSCode sebagai text editor.
3. Open folder dan buka proyek ini.
4. Buat virtual environment dengan menjalankan `py -3 -m venv .venv` diterminal (disarankan menggunakan cmd yang ada diterminal vscode).
5. Masuk ke dalam virtual env dengan menjalankan `.venv\Scripts\activate` diterminal tadi.
6. Instal flask dengan perintah `pip install Flask`.
7. Instal Flask Restful dengan perintah `pip install flask_restful`.
8. Instal Falsk Cors dengan menjalankan `pip install flask_cors`.
9. Berikutnya instal Falsk SQLAlchemy dengan menjalankan `pip install -U Flask-SQLAlchemy`.
10. Kemudian instal Pyjwt dengan menjalankan `pip install pyjwt`.
11. Instal Falsk Bcrypt dengan menjalankan `pip install flask-bcrypt`.
12. Kemudian instal insomnia untuk testing rest api [Link Download](https://insomnia.rest/)
13. Buka Insomnia dan buat projek baru dan tambahkan beberapa request seperti `login` dengan mehthod `post` dan body `multipart`. buat juga `register` dengan mehthod `post` dan body `multipart`. Terakhir `allArtikel` dengan mehthod `get`.
14. buka kembali terminal di vscode dan jalankan aplikasi dengan mengetikkan `python app.py`.
15. Aplikasi akan berjalan di `http://127.0.0.1:5005` dengan port 5005.
16. selesai

## Endpoints API

### Registrasi Pengguna

- **Endpoint**: `/register`
- **Metode HTTP**: POST
- **Payload**: JSON dengan `username` dan `password`
- **Keterangan**: Endpoint untuk mendaftarkan pengguna baru. Password akan di-hash sebelum disimpan di basis data.

### Login Pengguna

- **Endpoint**: `/login`
- **Metode HTTP**: POST
- **Payload**: JSON dengan `username` dan `password`
- **Keterangan**: Endpoint untuk otentikasi pengguna. Jika otentikasi berhasil, token JWT akan dikirim kembali sebagai respons.

### Article

- **Endpoint**: `/article`
- **Metode HTTP**: GET
- **parameter**: ?datatoken=Token
- **Keterangan**: Endpoint untuk menampilkan artikel .

## Catatan

1. Pada saat testing endpoint article, anda harus login terlebih dahulu untuk mendapatkan token.
2. token hanya berlaku selama 10 menit,
3. berikut adalah contoh endpoint agar dapat menjalankan endpoint article `http://127.0.0.1:5005/article?datatoken=isitoken`

note : isi token adalah token tanpa petik yang diambil ketika login berhasil
