from buildutil import JobBuilder
import appconfig

with open("./builds/config/job/deployConfig.xml") as f:
	configString = f.read()

with open("./builds/config/job/od_emily.xml") as f:
	configStringParameter = f.read()

builder = JobBuilder(appconfig.jenkins_url)

#jobname="sfsf'sfsf"
#builder.add_job(jobname, configString)
#builder.run_job()

builder.add_job("Eric_parameter_testing", configStringParameter)
#builder.run_job(username="Eric Yang", dbname="sfsf", )
builder.run_job(username="Eric", \
				version="6.6.0", \
				webroot="sfsf", \
				deploy_config="sfsf")      
