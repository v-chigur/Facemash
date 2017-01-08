import tornado.ioloop
import tornado.web
import random, json

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		id = self.get_argument('id', '')

		if id != '':
			info = self.get_cookie('cookies') #чтобы один пользователь не мог голосовать дважды
			if info != None:
				cookies = info.split(',')
			else:
				cookies = []

			if not (id in cookies):
				f = open('votes.json')
				text = f.read()
				f.close()
	
				votes_list = json.loads(text)
				if id in votes_list.keys():
					votes_list[id] += 1
				else:
					votes_list[id] = 1
	
				text = json.dumps(votes_list)
				f = open('votes.json', 'w')
				f.write(text)
				f.close()
				cookies.append(str(id))
				c = ','.join(cookies)
				self.set_cookie('cookies', c)


		name1 = str(random.randint(1, 10))
		name2 = str(random.randint(1, 10))

		while name1 == name2:
			name2 = str(random.randint(1, 10))

		self.render('facemash.html', name1 = name1, name2 = name2)

settings = [
	('/', MainHandler),
	('/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static'}),
	('/images/(.*)', tornado.web.StaticFileHandler, {'path': 'images'})
]

app = tornado.web.Application(settings)
app.listen(8888)
tornado.ioloop.IOLoop.current().start()