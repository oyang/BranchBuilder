from buildutil import JobBuilder

with open("./builds/config/job/deployConfig.xml") as f:
	configString = f.read()

with open("./builds/config/job/deployConfigParameter.xml") as f:
	configStringParameter = f.read()

builder = JobBuilder("http://localhost:8080")

builder.add_job("Oliver_noparameter_testing", configString)
builder.run_job()

builder.add_job("Oliver_parameter_testing", configStringParameter)
builder.run_job(username="Eric Yang")
