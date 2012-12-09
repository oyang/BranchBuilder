from jenkins import Jenkins
from jinja2 import Template

import json, urllib2, re
import web
import os
from datetime import datetime

import appconfig
from buildutil import JobBuilder


render = web.template.render('template/', base='layout')
urls = (
    '/', 'ODDeployIndex',
    '', 'ODDeployIndex',
    '/oddeploy_si', 'ODDeploySI',
    '/oddeploy_add', 'ODDeployAdd',
    '/oddeploy', 'ODDeploy',
    '/oddeploy_update', 'ODDeployUpdate',
    '/oddeploy_remove', 'ODDeployRemove',
    '/oddeploy_get', 'ODDeployGet',
    '/oddeploy_detail', 'ODDeployDetail',
    '/odcron', 'ODCron',
    '/odsicron', 'ODSICron',
    '/odformat', 'ODFormat',
)

#web.config.smtp_server = 'localhost'
#web.config.smtp_port = 25
#web.config.smtp_username = 'oliver.sugar@gmail.com'
#web.config.smtp_password = 'sugarcrm'
#web.config.smtp_starttls = True

web.config.debug = True

db = web.database(dbn='sqlite', db='branchBuilder')


class ODDeployIndex:
    def is_running_job(self,jobName):
        if unicode(jobName) in self.check_running_job():
            return True
        else:
            return False

    def check_running_job(self):
        #Check Running job
        j = Jenkins(appconfig.jenkins_url)
        job_list = j.get_jobs()
        job_queue_list = j.get_queue_info()
        running_job = []

        for job in job_list:
            if re.search('anime', job['color']):
                running_job.append(job['name'])

        for job_queue in job_queue_list:
            running_job.append(job_queue['task']['name'])

        return running_job

    def GET(self):
        job_list = []
        jobName = "od_silentupgrade"
        
        if self.is_running_job(jobName):
            upgradeStatus = 1
        else:
            upgradeStatus = 0
        
	deployInfo = DeployInfo().getDeployInfo()
        od_deploys = db.query("select a.id, a.username, a.webroot, a.version, a.deploy_config, a.last_deploy_date, \
                ifnull(b.status, \"Available\") as status \
                from od_deployer as a \
                left join  deploys_status as b \
                on a.id=b.task_id \
                order by b.status desc,  a.username, a.last_deploy_date desc") 

        return render.oddeploy(od_deploys, appconfig.site_url, upgradeStatus, appconfig.od_users, deployInfo, appconfig.od_version)

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
        od_deploys = db.insert('od_deployer', username=i.username, version=i.version, status='Available', deploy_config=i.deploy_config)
	return "{}"
      else:
        db.update('od_deployer', where="id=" + i.id, username=i.username, version=i.version, deploy_config=i.deploy_config)

        raise web.seeother("/")

class ODDeployGet:
    def GET(self):
      i = web.input()
      try:
        i.id
        od_deploy = db.select("od_deployer", where="id=" + i.id, what="id, username, version, deploy_config")
	for x in  od_deploy:
	   deployString = json.JSONEncoder().encode({"username": x.username, "version": x.version, "deploy_config": x.deploy_config})
      except Exception:
        return False

      web.header("Content-type", "application/json")

      return deployString

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

class RunUpgrade:
    def run(self, insname, upgradetype, flavor, dynamic, version):
      with open("./builds/config/job/upgradeConfigParameter.xml") as f:
          configStringParameter = f.read()

      builder = JobBuilder(appconfig.jenkins_url)
      jobName = "od_silentupgrade"
      builder.add_job(jobName, configStringParameter)

      builder.run_job(insname=insname, \
                upgradetype=upgradetype, \
                flavor=flavor, \
                dynamic=dynamic, \
                version=version)      

class ODDeploySI:
    def GET(self):
      i = web.input()
      RunUpgrade().run(i.insname,i.upgradetype,i.flavor,i.dynamic,i.version)

class RunDeploy:
    def run(self, task_id):
      i = {"task_id": task_id}
      selectedDeploys = db.select('od_deployer', where="id=" + str(i["task_id"]))
      with open("./builds/config/job/deployConfigParameter.xml") as f:
          configStringParameter = f.read()

      for m in selectedDeploys:
        username = m.username
        version = m.version
        webroot = m.webroot
        deploy_config = m.deploy_config
	timeo = datetime.strptime(m.last_deploy_date, "%Y-%m-%d %H:%M:%S")
        deploy_timestamp = timeo.strftime("%Y%m%d%H%M%S")

      builder = JobBuilder(appconfig.jenkins_url)
      jobname = "od_" + username
      builder.add_job(jobname, configStringParameter)

      builder.run_job(username=username, \
                version=version, \
                webroot=webroot, \
                deploy_config=deploy_config, \
                deploy_timestamp=deploy_timestamp)      

class ODDeploy:
        def GET(self):

                i = web.input()
                selectedDeploys = db.select('od_deployer', where="id=" + i.task_id, what="id")

                if selectedDeploys:
                        deploys_status = db.select('deploys_status')

                        if deploys_status:
                                db.insert('deploys_status', task_id=int(i.task_id), status="InQueue")
                                statusString = json.JSONEncoder().encode({"task_id": i.task_id, "status": "InQueue" })
                        else:
                                db.insert('deploys_status',
                                                        task_id=int(i.task_id),
                                                        status="Running")

				date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				db.update('od_deployer', where='id=' + str(i.task_id), last_deploy_date=date_now)

                                RunDeploy().run(i.task_id)
                                statusString = json.JSONEncoder().encode({"task_id": i.task_id, "status": "Running" })

		return statusString
class ODSICron:
    def __init__(self):
        self.j = Jenkins(appconfig.jenkins_url)

    def check_queue(self):
        #Check queue jobs
        j= self.j
        return j.get_queue_info()

    def is_upgrade_job(self,jobName):
        if unicode(jobName) in self.check_upgrade_job():
            return True
        else:
            return False

    def check_upgrade_job(self):
        #Check Running job

        j = self.j
        job_list = j.get_jobs()
        job_queue_list = j.get_queue_info()
        running_job = []

        for job in job_list:
            if re.search('anime', job['color']):
                running_job.append(job['name'])

        for job_queu in job_queue_list:
            running_job.append(job_queue['task']['name'])

        return running_job

    def run_cron(self):
        job_list = []
        jobName = "od_silentupgrade"
        if self.is_upgrade_job(jobName):
            job_list.append({"jobName":"od_silentupgrade"})
        else:
            job_list.append({"jobName":"no_silentupgrade"})
        return job_list

    def GET(self):
        job_list = []
        job_list = self.run_cron()
        web.header('Content-type', 'application/json')
        return json.JSONEncoder().encode(job_list)

class ODCron:
    def __init__(self):
        self.j = Jenkins(appconfig.jenkins_url)

    def check_queue(self):
        #Check queue jobs
        j= self.j
        return j.get_queue_info()

    def is_deploying_job(self,jobName):
        if jobName in self.check_deploying_job():
            return True
        else:
            return False

    def check_deploying_job(self):
        #Check Running job

        j = self.j
        job_list = j.get_jobs()
        job_queue_list = j.get_queue_info()
        running_job = []

        for job in job_list:
            if re.match('^od_', job['name']) and re.search('anime', job['color']):
                running_job.append(job['name'])

        for job_queue in job_queue_list:
            if re.match('^od_', job_queue['task']['name']):
                running_job.append(job_queue['task']['name'])

        return running_job

    def get_lowest_deploy(self):
        min_deploys = db.query('select min(id) as id from deploys_status')
        min_deploy = min_deploys[0].id

        if min_deploy:
            selectedDeployTasks = db.select('deploys_status', where='id=' + str(min_deploy))
            for selectedDeployTask in selectedDeployTasks:
                return {"task_id":selectedDeployTask.task_id, "status": selectedDeployTask.status}
        else:
            return False

    def run_cron(self):
        lowest_deploy = self.get_lowest_deploy()
        job_list = []

        if lowest_deploy:
            if lowest_deploy["status"] == 'Running':
                selectedDeploys = db.select('od_deployer', where="id=" + str(lowest_deploy["task_id"]))
                for m in selectedDeploys:
                    username = m.username
                    jobName = "od_" + username

                if self.is_deploying_job(jobName):
                    pass
                else:
                    #update build_status and remove the running flag
                    db.delete('deploys_status', where='task_id=' + str(lowest_deploy["task_id"]))
            elif lowest_deploy["status"] == 'InQueue':
                #Assume Jenkins is avaliable for building
		if db.select('od_deployer', where='id=' + str(lowest_deploy["task_id"])):
                    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    db.update('od_deployer', where='id=' + str(lowest_deploy["task_id"]), last_deploy_date=date_now)

                    RunDeploy().run(lowest_deploy["task_id"])
                    db.update('deploys_status', where='task_id=' + str(lowest_deploy["task_id"]), status='Running')
		else:
		    #Can not found this record from od_deployer
                    db.delete('deploys_status', where='task_id=' + str(lowest_deploy["task_id"]))
            else:
                #print 'false with invalid status'
                pass
        else:
            #print 'false from lowest build'
            pass
        
        for x in db.select('deploys_status', what='task_id, status'):
            job_list.append(x)

        return job_list

    def GET(self):
        job_list = []
        new_builds_status = self.run_cron()
        web.header('Content-type', 'application/json')
        if new_builds_status:
            for build_status in new_builds_status:
                job_list.append({"task_id": build_status.task_id, "status": build_status.status})

        return json.JSONEncoder().encode(job_list)

class ODDeployAdd:
    def POST(self):
      i = web.input()
      isDuplicate = db.select('od_deployer', where='username=\"' + i.username + '\" AND version=\"' + i.version + '\"', what="count(*) as count")[0]
      deploy_config = []    

      if isDuplicate.count:
          web.seeother('/')
      else:
          #add a new build
          if hasattr(i, "flavor1"): deploy_config.append(i.flavor1)
          if hasattr(i, "flavor2"): deploy_config.append(i.flavor2)
          if hasattr(i, "flavor3"): deploy_config.append(i.flavor3)
          if hasattr(i, "flavor4"): deploy_config.append(i.flavor4)
          if hasattr(i, "flavor5"): deploy_config.append(i.flavor5)

          if len(deploy_config) == 0 : deploy_config.append("Ent")

          deploy_config_new = "" ",".join(deploy_config)
          db.insert('od_deployer', username=i.username, version=i.version, webroot=i.webroot, status='Available', deploy_config=deploy_config_new)
          raise web.seeother("/")

class ODFormat:
    def GET(self):
      od_deploy = db.select('od_deployer', what="id, last_deploy_date")
      for r in od_deploy:
          timeo = datetime.strptime(r.last_deploy_date, "%Y%m%d%H%M%S")
          deploy_timestamp = timeo.strftime("%Y-%m-%d %H:%M:%S")
	  db.update('od_deployer', where="id=" + str(r.id), last_deploy_date=deploy_timestamp)

class DeployInfo:
	def getDeployInfo(self):
	  try:
	    return json.loads(urllib2.urlopen('http://qatest.sugarcrm.pvt/instances2.php?json', None, 10).read())
	  except:
	    return json.loads('{}')

app_ODDeploy = web.application(urls, locals())

if __name__ == "__main__":
   app_ODDeploy.run()
