#Welcome
This Splunk add-on will add a new generating command called expandmacro.  As the name implies, it will attempt to expand a macro you provide it.

I think we've all found ourselves playing the macro game before, and it get can be a bear.  Oh this search has a macro, let me go find the definition.  Oh good the definition contains a macro, let me go find its definition.  And so on...until your notepad of macros has you going cross-eyed.

I was hoping Splunk would release someting to make that a bit easier, but I'm still waiting.  So I'm taking a stab at it myself.

#Install
Since this add-on only contains a generating command, it only needs installed on your search heads - no input/parse/index time operations required.  

To actually install it:

1. Download the app
2. Unzip it to $SPLUNK_HOME\etc\apps
3. Restart splunk

#Usage
This is a generating command, so it has to be the first command in your seach and needs the preceding pipe.

###List Mode
If you do not specify any arguments, then the command will return a list of macros with a subset of attributes - name, definition, arguments and app

**| expandmacro**

![expandmacro only](../Images/expandmacro_no_params.png?raw=true)

###Expansion Mode
If you specify the macro argument, then the command will try to expand the macro provided.  If the macro takes parameters, be sure to supply them here. 

Also, the macro argument should be in quotes.  If you need to specify quotes in the parameters, escape them with a backslash.

In this mode, the results will consist of two fields - definition and level.  Meaning, each row will represent the current definition at that level of expansion.  The deeper the macro rabit hole, the more levels are returned.

**| expandmacro macro="classificationstatistics(param1,param2)"**

![expandmacro with just macro arg](../Images/expandmacro_macro_only.png?raw=true)

If you do specify the macro argument, you can also specify a max_level argument as well.  That limit the number of expansion levels we go through.  This defaults to 10.

**| expandmacro macro="dmc_cpu_usage_rangemap_and_timechart" max_level=2

![expandmacro with macro and max_level args](../Images/expandmacro_macro_and_level.png?raw=true)

#Platforms and Versions
This is my first attempt to create a Splunk command, and I don't have access to a lot of environments for testing/validation.  That said, the command was written on a Windows 10 laptop running Splunk 6.5.1.  It has also been tested on RHEL 6.5, also running Splunk 6.5.1.

The command itself is written in Python which should be platform independent.  It is also utilizing the [Splunk SDK for Python](http://dev.splunk.com/python), but I'm not sure if that has any system/Splunk requirements.

#The Code
It's ugly.  

I'm not a real programmer and definitely not very sufficient with Python, so there are probably better ways to do much of what I'm doing.

I don't really understand the SDK either, but was able to trial-and-error my way to getting the data to come back and then parse it.  Again, there is probably a better way, but I was struggling with the documentation.

There probably plenty of bugs waiting to be squished, so feel free to make this better if you can!
