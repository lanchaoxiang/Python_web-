import socket
import datetime


def log(*args, **kw):
	now_time = datetime.datetime.now()
	print(now_time, "log", args, kw)


def route_index():
	header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
	body = '<h1>Hello Gua</h1>\
	<img src="C:\\Users\\98225\\Desktop\\3.png">'
	r = header + '\r\n' + body
	return r.encode(encoding='utf-8')


def page(name):
	with open(name, encoding='utf-8') as f:
		return f.read()


def route_msg():
	header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
	body = page(r'C:\Users\98225\Desktop\world.html')
	r = header + '\r\n' + body
	return r.encode(encoding='utf-8')


def route_img():
	with open(r"C:\Users\98225\Desktop\3.png", 'rb') as f:
		header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
		img = header + b'\r\n' + f.read()
		return img


def error(code=404):
	e = {
		404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
	}
	return e.get(code, b'')


def response_for_path(path):
	r = {
		'/': route_index,
		'/doge.gif': route_img,
		'/msg': route_msg,
	}
	response = r.get(path, error)
	log(type(response))
	return response()


def run(host='127.0.0.1', port=3000):
	with socket.socket() as s:
		s.bind((host, port))
		log('run', host, port)
		while True:
			s.listen(5)
			connection, address = s.accept()
			request = connection.recv(1024)
			log("raw,", request)
			request = request.decode('utf-8')
			log('ip and request,{},\n{}'.format(address, request))
			try:
				path = request.split()[1]
				response = response_for_path(path)
				connection.sendall(response)
			except Exception as e:
				log('error', e)
			connection.close()


def main():
	config = dict(
		host='127.0.0.1',
		port=3000,
	)
	run(**config)


if __name__ == '__main__':
	main()
