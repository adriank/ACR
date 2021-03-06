# -*- coding: utf-8 -*-

# Asyncode Runtime - XML framework allowing developing internet
# applications without using programming languages.
# Copyright (C) 2008-2010  Adrian Kalbarczyk, Sebastian Lis

# This program is free software: you can redistribute it and/or modify
# it under the terms of the version 3 of GNU General Public License as published by
# the Free Software Foundation.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ACR.components import Component
from ACR.errors import *
from ACR.utils import prepareVars, replaceVars
from ACR.utils.xmlextras import tree2xml
from ACR.utils import generator
import os
import shutil
import fnmatch
import mimetypes

class FileSystem(Component):
	SHOW_DIRS=True
	SHOW_HIDDEN=False
	SHOW_MIME=False
	ONLY_DIRS=False
	def __init__(self,config):
		#self.config=config
		#TODO check whether it is path to proper directory (exists, permissions etc) or not
		try:
			self.abspath=config[0][2][0]
		except:
			raise Error("MisconfigurationError", "FileSystem component could not find the proper configuration.")

	def list(self,acenv,conf):
		D=acenv.doDebug
		fullPath=conf["fullPath"]
		showDirs=conf.get("showDirs",self.SHOW_DIRS)
		showHidden=conf.get("showHidden",self.SHOW_HIDDEN)
		showMIME=conf.get("showMIME",self.SHOW_MIME)
		onlyDirs=conf.get("onlyDirs",self.ONLY_DIRS)
		_filter=conf.get("filter")
		try:
			all=os.listdir(fullPath)
		except OSError,e:
			return {
				"@status":"error",
				"@error":e
			}
		all.sort()
		if _filter:
			all=filter(lambda file: fnmatch.fnmatch(file, _filter),all)
		if not showHidden:
			all=filter(lambda file: not file[0]==".",all)
		if not onlyDirs:
			files=filter(lambda file: not os.path.isdir(os.path.join(fullPath,file)),all)
			files.sort()
		dirs=None
		if showDirs:
			dirs=filter(lambda dir: dir not in files,all)
		ret=[]
		if len(files)==0:
			return {
				"@status":"error",
				"@error":"DirEmpty"
			}
		path=conf["path"]
		if dirs:
			for i in dirs:
				if not i== "lost+found":
					ret.append({
						"@name":i,
						"@path":path,
						"@type":"dir"
					})
		if files and not onlyDirs:
			for i in files:
				#TODO change type to mimetype
				f={
					"@name":i,
					"@path":path,
					"@type":"file"
				}
				if showMIME:
					try:
						extMap={
							"docx":"doc"
						}
						ext=i.split(".").pop()
						try:
							ext=extMap[ext]
						except:
							pass
						f['@type']=mimetypes.types_map['.'+ext].replace("/","-")
						if f['@type'].startswith("image"):
							f["@type"]="image-x-generic"
					except:
						f["@type"]="unknown"
				ret.append(f)
		return ret

	def tree(self,acenv,conf):
		#TODO as list but should return whole dir tree. Subdirs should be in subnodes of Object()
		pass

	def create(self,acenv,conf,update=False):
		D=acenv.doDebug
		#path=os.path.join(self.abspath+conf["path"])
		if not update and os.path.isfile(conf["fullPath"]):
			return {
				"@status":"error",
				"@error":"FileExists"
			}
		# path is a list eg /a/b/c/foo.xml -> ['a', 'b', 'c']
		path=os.path.normpath(conf["path"]).split("/")[:-1]
		currPath=self.abspath
		for d in path:
			currPath=os.path.join(currPath, d)
			if not os.path.isdir(currPath):
				os.mkdir(currPath)
		try:
			File=open(conf["fullPath"], 'w')
			content=conf["content"]
			if type(content) in (str,unicode):
				File.write(content)
			elif type(content) is generator:
				for i in content:
					File.write(i)
		except (IOError,OSError) ,e:
			#File.close()
			return {
				"@status":"error",
				"@error":e
			}
		else:
			File.close()
		return {"@status":"ok"}

	def update(self,acenv,conf):
		return self.create(acenv,conf,True)

	def append(self,acenv,conf):
		D=acenv.doDebug
		path=acenv, conf["fullPath"]
		try:
			file=open(path, 'a')
			file.write(conf['content'])#.replace("\r\n","\n")
		except IOError,e:
			raise Error("IOError", 'cannot open %s'%(e))
		else:
			file.close()
		return {"@status":"ok"}

	def delete(self,acenv,conf):
		D=acenv.doDebug
		path=self.abspath+replaceVars(acenv,conf["path"])
		if (os.path.exists(path)):
			if (os.path.isfile(path)):
				os.remove(path)
			else:
				shutil.rmtree(path)
		return {"@status":"ok"}

	def copy(self,acenv,conf):
		#D=acenv.doDebug
		copyFrom=os.path.join(self.abspath,*replaceVars(acenv,conf["from"]).split("/"))
		copyTo=os.path.join(self.abspath,*replaceVars(acenv,conf["to"]).split("/"))
		if os.path.isfile(copyFrom) and not os.path.isfile(copyTo):
			shutil.copyfile(copyFrom, copyTo)
		return {"@status":"ok"}

	def move(self,acenv,conf):
		copyFrom=os.path.join(self.abspath,*replaceVars(acenv,conf["from"]).split("/"))
		copyTo=os.path.join(self.abspath,*replaceVars(acenv,conf["to"]).split("/"))
		if os.path.isfile(copyFrom) and not os.path.isfile(copyTo):
			shutil.move(copyFrom, copyTo)
		return {"@status":"ok"}

	def exists(self,acenv,conf):
		return os.path.exists(conf["fullPath"])

	def get(self,acenv,conf):
		fullpath=conf["fullPath"]
		try:
			file=open(fullpath,"r")
			content=file.read()
		except IOError,e:
			return {
				"@status":"error",
				"@error":e
			}
			#print 'cannot open', conf["path"]
		else:
			file.close()
		return {
			"content":content,
			"fileName":conf["path"].split("/")[-1]
		}
		#{
#			"content":"".join(["<![CDATA[",
#			content
#			.replace("]]>","]]>]]&gt;<![CDATA["),"]]>"])
#		}

	def generate(self, acenv, config):
		D=acenv.doDebug
		if D:
			acenv.info("Component: 'FS'")
			acenv.info("Executing command: '%s'", config["command"])
		c=config["params"]
		conf={}
		for i in c:
			conf[i]=replaceVars(acenv, c[i], lambda x: type(x) is generator and x or str(x))
		if D:
			if not conf.get("path"):
				acenv.error("path not suplied")
			elif conf["path"][0]!='/':
				acenv.error("missning '/' character at the begginig of 'path' attribute")
		try:
			if type(conf["content"]) is not generator:
				conf["content"]=replaceVars(acenv,config["content"])
		except:
			pass
		conf["fullPath"]=os.path.join(self.abspath,*conf["path"].split("/"))
		return self.__getattribute__(config["command"])(acenv,conf)

	def parseAction(self, conf):
		if conf["command"] not in ("list", "create", "update", "append", "delete", "copy", "move", "exists", "get"):
			raise Error("Command '%s' do not exist!", config["command"])
		ret={
			"command":conf["command"]
		}
		if conf["content"]:
			s=[]
			for elem in conf["content"]:
				if type(elem) is tuple:
					s.append(tree2xml(elem))
				elif type(elem) is str:
					s.append(elem)
			ret["content"]=prepareVars("\n".join(s))
		ret["params"]=conf["params"]
		return ret

def getObject(config):
	return FileSystem(config)
