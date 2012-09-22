from buildutil import JobBuilder

with open("configNew.xml") as f:
	configString = f.read()

builder = JobBuilder("http://localhost:8080")
builder.add_job("Oliver_testing", configString)
builder.run_job()
