import sys, time, re, splunklib.binding as bind
from splunklib.searchcommands import dispatch, GeneratingCommand, Configuration, Option, validators
from xml.dom.minidom import parseString

@Configuration()
class ExpandMacros(GeneratingCommand):
	# macro can be supplied in the search
	# if not, we'll just list all of the macros
	macro = Option(require=False)

        # limit the number of levels of macros do expand
        # can be supplied in the command and default to 10 if not
        # should help to eliminate infinite loops for circurlarly defined macros (if those are possible)
	max_level = Option(require=False, validate=validators.Integer())
	
	# internal array for the list of all of the macros
	macroList = []
	
	# Method getMacros()
	# This method should find and return all of the macros from Splunk
	def getMacros(self):
		# Using the splunk sdk for python, connect to to splunk
		# and hit the admin/macros endpoint, asking for all of the macros
		macros =[]
		kwargs_count = {"count":"0"}
		service = bind.connect(app="-",owner="-",token=self._metadata.searchinfo.session_key)
		response = service.get("admin/macros",**kwargs_count)
		
		# The macros are returned in the body of the response
		# And are in an xml format
		# here we loop through all of the "entry" tags
		# looking for the name, definition and arguments of each macro
		dom = parseString(response["body"].read())
		for node in dom.getElementsByTagName('entry'):
			name = ""
			definition= ""
			args = ""
			
			# the name in the title node on each entry element
			name = node.getElementsByTagName('title')[0].childNodes[0].nodeValue
			
			# the definition and arguments (and other properties)
			# are in various "s:key" nodes
			# so we loop through them all and set those variables if/when found
			for dictNode in node.getElementsByTagName('s:key'):
				if dictNode.getAttribute('name') == "definition":
					definition = dictNode.childNodes[0].nodeValue
				if dictNode.getAttribute('name') == 'args':
					args = dictNode.childNodes[0].nodeValue
			
			# The macro list is an array of dictionary items
			# Each item contains the name, definition and arguments for the macro
			macroDict = {"name":name,"definition":definition,"arguments":args}
			macros.append(macroDict)
		return macros
	
	# Method normalizeMacroName(strMacro)
	# This method will find whether a macro name contains parameters
	# If it does, we count the parameters and return the actual macro name
	# For example, mycoolmacro("foo","bar") should return mycoolmacro(2)
	def normalizeMacroName(self,strMacro):
		ret = strMacro
		matches=re.findall('[^\(,\)]+',strMacro)
		numargs = len(matches[1:])
		if numargs > 0:
		  ret = matches[0] + "(" + str(numargs) + ")"
		return ret
	
	# Method getMacroParams(strMacro)
	# Similar to normalizeMacroName but with this method
	# instead of counting params, we just return them
	def getMacroParams(self,strMacro):
		matches=re.findall('[^\(\",\)]+',strMacro)
		return matches[1:]
		
	# Method getMacro(strMacro)
	# Here we're just looking through our big ol' array of macros
	# and returning the dictionary item for the macro if found
	def getMacro(self,strMacro):
		ret = None
		for dMacro in self.macroList:
			if dMacro['name'] == strMacro:
				ret = dMacro
				break
		return ret
	
	# Method getMacrosInString(strMacro)
	# giving a string, we're trying to pull out any macros
	# found in the string.
	# This could probably be a lot more robust
	def getMacrosInString(self,strMacro):
		return re.findall(r'`(.+?)`',strMacro)
	
	# Method expandMacro()
	# This is the main method which is handling
	# the macro expansion
	def expandMacro(self):
		# We'll return every level of the macro expansion
		# and so we want to have the level as part of the return object
		level = 1
		
		# expandedMacro is our array of dictionary objecst that will be returned
		expandedMacro = []
		
		# grab the dictionary object for the macro we want to expand that was passsed in Splunk
		currentMacro = self.getMacro(self.normalizeMacroName(self.macro))
		
		# and if we find it, let's do stuff with it
		if currentMacro != None:
			# get the definition for the macro, create a dictionary object with level and definition
			# and add it to our return array
			# I wish python had a do...loop
			definition = "`"+ self.macro + "`"
			expandedMacroDict = { 'level':level, 'definition':definition }
			expandedMacro.append(expandedMacroDict)
			level+=1
			
			#definition = "`"+ self.macro + "`"
			# Now starting with the fast first definition, let's keep going until
			# we get a definition that contains no macros, because then we're done
			while "`" in definition and level <= self.max_level :
				# find all of macros in the current definition
				# and let's loop through them
				for macro in self.getMacrosInString(definition):
					
					# if the macro has parameters, let's get the actual macro name
					# and see if we can find it in our list
					dMacro = self.getMacro(self.normalizeMacroName(macro))
					if dMacro != None:
						tmpDefinition = dMacro["definition"]
						
						# if the macro has arguments, then we want to replace the arguments in the definition
						# with the actual parameters that are being used
						if dMacro["arguments"]!="":
							params = self.getMacroParams(macro)
							count = 0
							for arg in dMacro["arguments"].split(","):
								tmpDefinition = tmpDefinition.replace("$"+arg+"$",params[count])
								count += 1
						definition = definition.replace("`"+macro+"`", tmpDefinition)
				expandedMacroDict = { 'level':level, 'definition':definition }
				expandedMacro.append(expandedMacroDict)
				level+=1
					
		return expandedMacro
		
	def generate(self):
		if self.max_level != None:
			self.max_level = int(self.max_level)
		else:
			self.max_level = int(10)
		self.macroList = self.getMacros()
		if self.macro != None:
			retList = self.expandMacro()
		else:
			retList = self.macroList
		for macroDict in retList:
			yield macroDict

dispatch(ExpandMacros, sys.argv, sys.stdin, sys.stdout, __name__)
