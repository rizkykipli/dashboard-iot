from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.models import User
import os

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return redirect(url_for('config_ip'))
    else:
        flash('Invalid credentials. Please try again.')
        return redirect(url_for('index'))

@app.route('/config_ip')
def config_ip():
    return render_template('config_ip.html')

@app.route('/set_ip', methods=['POST'])
def set_ip():
    ip_address = request.form['ip_address']
    netmask = request.form['netmask']
    gateway = request.form['gateway']
    dns = request.form['dns']
    
    netplan_config = f"""
    network:
      version: 2
      renderer: networkd
      ethernets:
        eth0:
          dhcp4: false
          dhcp6: false
          addresses:
            - {ip_address}/24
          routes:
            - to: default
              via: {gateway}
          nameservers:
            addresses:
              - {dns}
    """
    
    with open('/etc/netplan/01-netcfg.yaml', 'w') as file:
        file.write(netplan_config)

    os.system('sudo chmod 600 /etc/netplan/01-netcfg.yaml')
    os.system('sudo netplan apply')
    
    return 'IP configuration updated. Please reboot the system for changes to take effect.'

