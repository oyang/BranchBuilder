import web
import os

import appconfig

render = web.template.render('template/', base='layout')
urls = (
	'/', 'BuildConfigIndex',
	'', 'BuildConfigIndex',
	'/buildconfig_add', 'BuildConfigAdd',
	'/buildconfig_update', 'BuildConfigUpdate',
	'/buildconfig_remove', 'BuildConfigRemove',
	'/buildconfig_get', 'BuildConfigGet',
	'/buildconfig_detail', 'BuildConfigDetail',
)

#web.config.smtp_server = 'localhost'
#web.config.smtp_port = 25
#web.config.smtp_username = 'oliver.sugar@gmail.com'
#web.config.smtp_password = 'sugarcrm'
#web.config.smtp_starttls = True

web.config.debug = True

db = web.database(dbn='sqlite', db='branchBuilder')


class BuildConfigIndex:
    def GET(self):
      build_configs = db.select('build_configs', what="id,version,author", where="id is not null")

      return render.buildconfig(build_configs, appconfig.site_url)

class BuildConfigUpdate:
    def GET(self):
      i = web.input()
      build_config = db.select('build_configs', where="id=" + i.id)[0]

      return render.buildconfig_detail(build_config, appconfig.site_url)

    def POST(self):
      i = web.input()
      try: 
      	i.id
      except NameError:
        build_configs = db.insert('build_configs', version=i.version, author=i.author, build_config_content=i.build_config_content)
	return "{}"
      else:
        db.update('build_configs', where="id=" + i.id, version=i.version, author=i.author, build_config_content=i.build_config_content)
        build_config = db.select('build_configs', where="id=" + i.id)[0]
	return render.buildconfig_detail(build_config, appconfig.site_url)

class BuildConfigUtil:
    def getVersionFile(self, version):
      if self.checkVersionFile(version):
        shortver = self.getShortVersion(version)
	f = open("builds/config/template/build_config.php", "r")
	a_buildconfig = f.read()
	f.close()
        return a_buildconfig
      else:
        return False

    def getShortVersion(self, version):
      return version.replace(".", "")

    def checkVersionFile(self, version):
      shortver = self.getShortVersion(version)
      for x in os.listdir("builds/config"):
        if x == shortver:
          return True

      return False

class BuildConfigGet:
    def GET(self):
      i = web.input()
      try:
        i.id
      except Exception:
        build_config = db.select("build_configs", where="version=$version", vars={'version': i.version})
      except Exception:
        build_config = db.select("build_configs", where="id=" + i.id)
      else:
	#Non-exist parameter
	return False
      web.header("Content-type", "text/plain")

      return build_config[0].build_config_content

class BuildConfigDetail:
    def GET(self):
      i = web.input()
      build_config = db.select("build_configs", where="id=" + i.id)[0]

      return render.buildconfig_detail(build_config, appconfig.site_url)

class BuildConfigRemove:
    def GET(self):
      i = web.input()
      db.delete("build_configs", where="id=" + i.id)

      raise web.seeother("/")

class BuildConfigAdd:
    def POST(self):
      build_config_content = BuildConfigUtil().getVersionFile('6.6.0')
      i = web.input()
      db.insert('build_configs', version=i.version, author=i.author, build_config_content=build_config_content)
      raise web.seeother("/")


app_BuildConfig = web.application(urls, locals())

if __name__ == "__main__":
   app_BuildConfig.run()
