# pdftotableserver
Small server which will convert pdf to csv or json

Requirements:
1. Java 8+
2. Python 3.8+
3. Tabula-py
4. flask
5. PyPDF2
6. pandas


```bash
pip install tabula-py flask PyPDF2 pandas
```

# Python server with an API for uploading PDF files and converting them to CSV or JSON format. 

It includes using multiple threads. 

# Short how to: 

To make this server not-really-but-highly available using multiple threads, I set the threaded argument to True when running the Flask app. 
This allows the server to handle multiple requests simultaneously.

1. Just copy pdfminiserver.py to your directory.
2. Create a directory named pdfminiserver and move the app.py file into it. Now, you can install the server using pip:
3. Run server
```python3 
pdfminiserver.py
```
Set your own parameters for IP, PORT, output directory
Server will start and log to /var/log/pdfminiserver.log.
Test the API by sending a POST request to /convert with a PDF file attached and the output_format parameter set to either csv or json.

```
POST /convert HTTP/1.1
User-Agent: PostmanRuntime/7.32.2
Accept: */*
Cache-Control: no-cache
Postman-Token: 1979a00f-d1d2-4e58-b398-0d9bfcae629c
Host: 192.168.0.152:5000
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Type: multipart/form-data; boundary=--------------------------209847865649583379732435
Content-Length: 243483
 
----------------------------209847865649583379732435
Content-Disposition: form-data; name="file"; filename="work.pdf"
<work.pdf>
----------------------------209847865649583379732435
Content-Disposition: form-data; name="output_format"
csv
----------------------------209847865649583379732435--
 
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 65
Server: Werkzeug/0.16.1 Python/3.10.6
Date: Sat, 15 Apr 2023 11:45:23 GMT
 
{"message":"File uploaded successfully and conversion started."}
````

# To make this a RHEL service, create a file named pdfminiserver.service in the /etc/systemd/system/ 

Usage: 
1. ```sudo systemctl daemon-reload```
2. ```sudo systemctl start pdfminiserver```
3. ```sudo systemctl enable pdfminiserver```
4. This should start the server on port 5000 and log to /var/log/pdfminiserver.log. You can test the API by sending a POST request to /upload with a file attached and a GET request to /file/<filename> to download a file.

```
# pdfminiserver.service

[Unit]
Description=PDF Converter Server

[Service]
ExecStart=/usr/bin/python /path/to/pdfminiserver.py
WorkingDirectory=/path/to/
User=root
Group=root
Restart=always

[Install]
WantedBy=multi-user.target
```
