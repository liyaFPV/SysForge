from flask import Flask, jsonify, render_template, request, session, redirect, url_for
import psutil
import platform
import os
import json


#система
print("CPU usage:", psutil.cpu_percent(interval=1), "%")

memory = psutil.virtual_memory()
print("RAM total:", f"{memory.total / (1024**3):.2f}", "GB")
print("RAM used:", f"{memory.used / (1024**3):.2f}", "GB")
print("RAM percent:", f"{memory.percent:.2f}", "%")

#диски
disks = os.listdir("/sys/block")

real_disks = [d for d in disks if not d.startswith(("loop", "ram", "zram", "dm-"))]

partitions = psutil.disk_partitions()

for disk in real_disks:
    print(f"\nДиск: {disk}")

    for p in partitions:
        if disk in p.device:
            usage = psutil.disk_usage(p.mountpoint)

            total = usage.total / (1024**3)
            used = usage.used / (1024**3)
            free = usage.free / (1024**3)

            print("Раздел:", p.device)
            print("Точка:", p.mountpoint)
            print(f"Размер: {total:.2f} GB")
            print(f"Занято: {used:.2f} GB")
            print(f"Свободно: {free:.2f} GB")
            print(f"Использование: {usage.percent}%")

app = Flask(__name__)
app.secret_key = 'super_secret_key_123456789'  # Случайный секретный ключ для сессий

@app.route("/api")
def main():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    data = {
        "CPU_usage": f"{psutil.cpu_percent(interval=1):.2f}%",
        "RAM_total": f"{memory.total / (1024**3):.2f} GB",
        "RAM_used": f"{memory.used / (1024**3):.2f} GB",
        "RAM_percent": f"{memory.percent:.2f}%",
        "Disks": []
    }
    for i in range(3):
        disk_info = {
            "disk": real_disks[i],
            "partitions": []
        }
        for p in partitions:
            if real_disks[i] in p.device:
                usage = psutil.disk_usage(p.mountpoint)
                disk_info["partitions"].append({
                    "device": p.device,
                    "mountpoint": p.mountpoint,
                    "total": f"{usage.total / (1024**3):.2f} GB",
                    "used": f"{usage.used / (1024**3):.2f} GB",
                    "free": f"{usage.free / (1024**3):.2f} GB",
                    "percent": f"{usage.percent:.2f}%"
                })
        data["Disks"].append(disk_info)

    return jsonify(data)

@app.route("/")
def home():
    return render_template("login.html")

@app.route('/index')
def index():
    print(f"Session data: {dict(session)}")
    if not session.get('logged_in'):
        print("Попытка доступа без авторизации, перенаправление на логин")
        return redirect(url_for('home'))
    print("Доступ к /index разрешен")
    return render_template("index.html")

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    hashed_username = data.get('username')
    hashed_password = data.get('password')

    # Хэш для "admin"
    admin_hash = '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'

    if hashed_username == admin_hash and hashed_password == admin_hash:
        session['logged_in'] = True
        print(f"Session after login: {dict(session)}")
        print("Успешный вход в систему")  # Вывод в консоль Python
        return jsonify({'message': 'Login successful', 'redirect': url_for('index')}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)