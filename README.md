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
The command can be used in two ways.  If you do not specify any arguments, then the command will return a list of macros

**| expandmacro**
