
events { }

http {
    sendfile        on;
    client_max_body_size 20M;
    keepalive_timeout  0;
    uwsgi_read_timeout 86400;
    uwsgi_send_timeout 86400;
  # redirect www -> non-www 
   server {
    listen       3000;
    server_name  localhost;

    root   /usr/share/nginx/html;
    index index.html;
    error_page   500 502 503 504  /50x.html;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
        try_files $uri $uri/ /index.html;
        add_header Cache-Control "no-cache";
        proxy_read_timeout 300s;
        proxy_connect_timeout 750s;
    }

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root  /usr/share/nginx/html;
    }

    location /static {
        expires 1y;
        add_header Cache-Control "public";
    }

    location /flask {
        proxy_pass http://backend:5000/flask;
	proxy_set_header X-Real-IP  $remote_addr;
       	proxy_set_header X-Forwarded-For $remote_addr;
    	proxy_set_header Host $host;
  	proxy_set_header X-Forwarded-Proto $scheme;
  	proxy_redirect http://backend:5000/flask $scheme://$http_host/;
	proxy_http_version 1.1;
	proxy_read_timeout 20d;
	proxy_buffering off;
    }
}
}
