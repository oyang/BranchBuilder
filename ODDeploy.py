import web
import os

import appconfig
from buildutil import JobBuilder


render = web.template.render('template/', base='layout')
urls = (
	'/', 'ODDeployIndex',
	'', 'ODDeployIndex',
	'/oddeploy_add', 'ODDeployAdd',
	'/oddeploy_update', 'ODDeployUpdate',
	'/oddeploy_remove', 'ODDeployRemove',
	'/oddeploy_get', 'ODDeployGet',
	'/oddeploy_detail', 'ODDeployDetail',
	'/oddeploy_deploy', 'ODDeployDeploy',
)

#web.config.smtp_server = 'localhost'
#web.config.smtp_port = 25
#web.config.smtp_username = 'oliver.sugar@gmail.com'
#web.config.smtp_password = 'sugarcrm'
#web.config.smtp_starttls = True

web.config.debug = True

db = web.database(dbn='sqlite', db='branchBuilder')


class ODDeployIndex:
    def GET(self):
      od_deploys = db.select('od_deployer', what="id,username,version,webroot,status,deploy_config", where="id is not null")

      return render.oddeploy(od_deploys, appconfig.site_url)

class ODDeployUpdate:
    def GET(self):
      i = web.input()
      od_deploy = db.select('od_deployer', where="id=" + i.id)[0]

      return render.ODDeploy_detail(od_deploy, appconfig.site_url)

    def POST(self):
      i = web.input()
      try: 
      	i.id
      except NameError:
        od_deploys = db.insert('od_deployer', username=i.username, version=i.version, webroot=i.webroot, status=i.status, deploy_config=i.deploy_config)
	return "{}"
      else:
        db.update('od_deploy', where="id=" + i.id, user_name=i.user_name, version=i.version, webroot=i.webroot, deploy_config=i.deploy_config)
        od_deploy = db.select('od_deployer', where="id=" + i.id)[0]
	return render.ODDeploy_detail(od_deploy, appconfig.site_url)

class ODDeployGet:
    def GET(self):
      i = web.input()
      try:
        i.id
      except Exception:
        od_deploy = db.select("od_deployer", where="version=$version", vars={'version': i.version})
      except Exception:
        od_deploy = db.select("od_deployer", where="id=" + i.id)
      except Exception:
        od_deploy = db.select("od_deployer", where="username=$username", vars={'username': i.username})
      else:
	#Non-exist parameter
	return False
      web.header("Content-type", "text/plain")

      return od_deploy[0].od_deploy_content

class ODDeployDetail:
    def GET(self):
      i = web.input()
      od_deploy = db.select("od_deployer", where="id=" + i.id)[0]

      return render.ODDeploy_detail(od_deploy, appconfig.site_url)

class ODDeployRemove:
    def GET(self):
      i = web.input()
      db.delete("od_deployer", where="id=" + i.id)

      raise web.seeother("/")

class ODDeployDeploy:
    def GET(self):
      i = web.input()
      selectedDeploy = db.select('od_deployer', where="id=" + str(i.id))

      with open("./builds/config/job/deployConfigParameter.xml") as f:
  		configStringParameter = f.read()

      for m in db.select('od_deployer', where="id=" + str(i.id)):
	 username = m.username
	 version = m.version
         webroot = m.webroot
	 deploy_config = m.deploy_config

      builder = JobBuilder(appconfig.jenkins_url)
      jobname = "od_" + selectedDeploy[0].username;
      builder.add_job(jobname, configStringParameter)

      builder.run_job(username=username, \
				version=version, \
				webroot=webroot, \
				deploy_config=deploy_config)      
      raise web.seeother("/")

class ODDeployAdd:
    def POST(self):
      i = web.input()
      db.insert('od_deployer', username=i.username, version=i.version, webroot=i.webroot, status='0', deploy_config=i.deploy_config)
      raise web.seeother("/")


app_ODDeploy = web.application(urls, locals())

if __name__ == "__main__":
   app_ODDeploy.run()
