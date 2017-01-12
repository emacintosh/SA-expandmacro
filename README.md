#Welcome
This Splunk add-on will add a new generating command called expandmacro.  As the name implies, it will attempt to expand a macro you provide it.

I think we've all found ourselves playing the macro game before, and it get can be a bear.  Oh this search has a macro, let me go find the definition.  Oh good the definition contains a macro, let me go find it.  And so on...

I was hoping Splunk would release someting to make that a bit easier, but I'm still waiting.  So I'm taking a stab at it myself.

#Install
Since this add-on only contains a generating command, it only needs installed on your search heads - no input/parse/index time operations required.  

To actually install it:

1. Download the app
2. Unzip it to $SPLUNK_HOME\etc\apps
3. Restart splunk

#Usage
This is a generating command, so has to be the first command in your seach and needs the preceding pipe.

###List Mode
If you do not specify any arguments, then the command will return a list of macros with a subset of attributes - name, definition, arguments and app

**| expandmacro**

![expandmacro only](../Images/expandmacro_no_params.png?raw=true)

###Expansion Mode
If you specify the macro agrument, then the command will try to expand the macro provided.  If the macro takes parameters, be sure to supply them here. 

Also, the macro argument should be in quotes.  If you need to specify quotes in the parameters, escape them with a backslash.

In this mode, the results will consist of two fields - definition and level.  Meaning, each row will represent the current definition at that level of expansion.  The deeper the macro rabit hole, the more levels are returned.

**| expandmacro macro="classificationstatistics(param1,param2)"**

![expandmacro with just macro arg](../Images/expandmacro_macro_only.png?raw=true)

If you do specify the macro argument, you can also specify a max_level argument as well.  That limit the number of expansion levels we go through.  This defaults to 10.

**| expandmacro macro="dmc_cpu_usage_rangemap_and_timechart" max_level=2

![expandmacro with macro and max_level args](../Images/expandmacro_macro_and_level.png?raw=true)
