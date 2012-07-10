#!/usr/bin/python

import web
from jinja2 import Template
from jenkins import Jenkins
from jenkinsapi import  *

import json
import urllib2

render = web.template.render('template/')
urls = (
	'/', 'Index',
	'/add', 'Add',
	'/build', 'Build',
	'/getbuild', 'GetBuild',
	'/updatebuild', 'UpdateBuild',
	'/remove', 'Remove',
)

app = web.application(urls, globals())
db = web.database(dbn='sqlite', db='branchBuilder')

class Index:
	def GET(self):
		self.update_status()
		builds = db.select('builds', order="last_build_date DESC", where="repos is not null")
		
		return render.index(builds)

	def update_status(self):
		builds = db.select('builds', order="last_build_date DESC", where="repos is not null")
		
		for build in builds:
			tasks_status = db.select('builds_status', where="task_id=" + str(build.task_id))
		       
			db.update('builds', where="task_id=" + str(build.task_id), status="Available")
			for task_status in tasks_status:
				jj = jenkins.Jenkins('http://localhost:8080')

				job_name = self.get_job_name(build.repos)
				jjob = jj.get_job(job_name)
				jbuild = jjob.get_build(task_status.build_number)
				jstatus = jbuild.get_status()
				
				db.update('builds', where="task_id=" + str(build.task_id), status=jstatus)

	def get_job_name(self, string):
		buildUtil = BuildUtil()
		return buildUtil.get_job_name(repos=string)
			
class Add:
	def POST(self):
		i = web.input()

		#TODO
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
						status="Available", 
						package_list="ent")

			raise web.seeother('/')

class Remove:
	def GET(self):
		i = web.input()
		n = db.delete('builds', where="task_id =" +  i.task_id)
		raise web.seeother('/')

class Build:
	def GET(self):
		from datetime import datetime

		i = web.input()
		selectedBuilds = db.select('builds', where="task_id=" + i.task_id)

		date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		if selectedBuilds:
			db.update('builds', where="task_id=" + i.task_id, last_build_date=date_now, status="InQueue")			

		taskBuilder =TaskBuilder('http://localhost:8080')

		for build in  selectedBuilds:
			taskBuilder.add_build( repos=build.repos, branch=build.branch, version=build.version, package_list=build.package_list)
			

			#TODO
			#jj= jenkinsapi.jenkins.Jenkins('http://localhost:8080')
			#job_name = BuildUtil().get_job_name(repos=build.repos)
			#jjob = jj.get_job(job_name)
			#jbuild_number = jjob.get_last_buildnumber()
			#print(jbuild_number)

			#TODO
			#selectBuildStatus = db.select('builds_status', where="task_id=" + i.task_id)
			#if selectBuildStatus:
			#	db.update('builds_status', where="task_id=" + i.task_id, build_number=jbuild_number)
			#else:
			#	db.insert('builds_status', task_id=i.task_id, build_number=jbuild_number)

		raise web.seeother('/')

class UpdateBuild:
	def POST(self):
		i = web.input()
		selectedBuilds = db.select('builds', where="task_id=" + i.task_id)

		if selectedBuilds:
			db.update('builds', where="task_id=" + i.task_id, repos=i.repos, branch=i.branch, version=i.version, author=i.author, package_list=i.package_list)

		raise web.seeother('/')

class GetBuild:
	def GET(self):
		from datetime import datetime

		i = web.input()
		selectedBuilds = db.select('builds', where="task_id=" + i.task_id)

		if selectedBuilds:
			for x in  selectedBuilds:
				buildString = json.JSONEncoder().encode({"repos": x.repos, "branch": x.branch, "version": x.version, "author": x.author, "package_list": x.package_list})
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
		self.j.build_job(self.jobName, {'branch': params['branch'], 'version': params['version'], 'package_list': params['package_list']})
	
	def set_job_name(self,**params):
		buildUtil = BuildUtil()
		self.jobName = buildUtil.get_job_name(repos=params['repos'])

	def get_build_status(self, **params):
		#job_info = self.j.get_job_info(self.jobName)
		#return build_status
		pass

	def get_job_name(self):
		return self.jobName

class BuildUtil:
	def __init__(self):
		pass
	
	def get_md5(self, string):
		try:
			import hashlib
			md5_str = hashlib.md5(string).hexdigest()
		except Exception:
			import md5
			md5_str = md5(string).hexdigest()

		return md5_str

	def get_job_name(self, **params):
		return 'Build' + '_' + self.get_md5(params['repos'])
		
if __name__ == '__main__':
	app.run()
