#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static

sudo apt-get -y update
sudo apt-get -y install nginx
sudo mkdir -p /data/web_static/releases/test/ /data/web_static/shared/
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -hR ubuntu:ubuntu /data/
new_loc="\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n"
sudo sed -i "37i\ $new_loc" /etc/nginx/sites-available/default
sudo service nginx reload
sudo service nginx restart
