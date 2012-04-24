#!/usr/bin/python

import web
from jinja2 import Template
from jenkins import Jenkins
import json

render = web.template.render('template/')
urls = (
	'/', 'index',
	'/add', 'add',
	'/build', 'build',
	'/getbuild', 'getbuild',
	'/remove', 'remove',
)

app = web.application(urls, globals())
db = web.database(dbn='sqlite', db='branchBuilder')

class index:
	def GET(self):
		builds = db.select('builds', order="last_build_date DESC", where="repos is not null")
		return render.index(builds)

class add:
	def POST(self):
		i = web.input()

		#check duplicate
		#if found duplicate then build
		isDuplicate = False
		if isDuplicate:
			pass
		#else add a new build
		else:
			n = db.insert('builds',  repos=i.repos, branch=i.branch, version=i.version, author=i.author,
						last_build_number=1000, 
						last_build_date="", 
						start_time="", 
						status="", 
						package_list="")

			raise web.seeother('/')

class remove:
	def GET(self):
		i = web.input()
		n = db.delete('builds', where="task_id =" +  i.task_id)
		raise web.seeother('/')

class build:
	def GET(self):
		from datetime import datetime

		i = web.input()
		selectedBuilds = db.select('builds', where="task_id=" + i.task_id)

		date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		if selectedBuilds:
			db.update('builds', where="task_id=" + i.task_id, last_build_date=date)			

		taskBuilder =TaskBuilder('http://localhost:8080')

		for x in  selectedBuilds:
			taskBuilder.add_build( repos=x.repos, branch=x.branch, version=x.version)

		raise web.seeother('/')

class getbuild:
	def GET(self):
		from datetime import datetime

		i = web.input()
		selectedBuilds = db.select('builds', where="task_id=" + i.task_id)

		if selectedBuilds:
			for x in  selectedBuilds:
				buildString = json.JSONEncoder().encode({"repos": x.repos, "branch": x.branch, "version": x.version, "author": x.author})
			return buildString

class TaskBuilder:

	def __init__(self, jenkinsURL):
		self.j = Jenkins(jenkinsURL)
		self.jobName = ""
		with open("config.xml") as file:
			self.templateConfig = file.read()
		self.template = Template(unicode(self.templateConfig))

	def set_new_config(self, **params):
		self.newConfig = self.template.render(repos=params['repos'], description=params['repos'])

	def add_build(self, **params):
		self.set_job_name(**params)
		self.set_new_config(**params)

		if self.j.job_exists(self.jobName):
			self.do_build(**params)
		else:
			self.j.create_job(self.jobName, self.newConfig)
			self.do_build(**params)
	
	def do_build(self, **params):
		self.set_job_name(**params)
		self.set_new_config(**params)

		self.j.enable_job(self.jobName)
		self.j.build_job(self.jobName, {'branch': params['branch'], 'version': params['version']})
	
	def set_job_name(self,**params):
		try:
			import hashlib
			self.jobName = 'Build' + '_' + hashlib.md5(params['repos']).hexdigest()
		except Exception:
			import md5
			self.jobName = 'Build' + '_' + md5.md5(params['repos']).hexdigest()


	def get_job_name(self):
		return self.jobName
		
if __name__ == '__main__':
	app.run()
