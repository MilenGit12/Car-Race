const gJavaConsole1_8_0_421 =  {

	id	: "javaconsole1.8.0_421",

	mimeType: "application/x-java-applet;jpi-version=1.8.0_421",

	install	: function() {
		window.addEventListener("load",this.init,false);
	},

	init	: function() { 
		if (navigator.mimeTypes[gJavaConsole1_8_0_421.mimeType]) {
			var toolsPopup = document.getElementById("menu_ToolsPopup");	
			toolsPopup.addEventListener("popupshowing",gJavaConsole1_8_0_421.enable,false);
			var element = document.getElementById(gJavaConsole1_8_0_421.id);
			element.setAttribute( "oncommand" , "gJavaConsole1_8_0_421.show();");
		} else {
			var element = document.getElementById(gJavaConsole1_8_0_421.id);
			element.setAttribute("style", "display: none");
		}
	},

	enable	: function() {
		var document = document.getElementById(gJavaConsole1_8_0_421.id);
    		if (navigator.javaEnabled()) {
			document.removeAttribute("enabled");
    		} else {
      			document.setAttribute("enabled", "false");
    		}
	},

	show	: function() {
     		var jvmMgr = Components.classes['@mozilla.org/oji/jvm-mgr;1']
	                   .getService(Components.interfaces.nsIJVMManager)
    		jvmMgr.showJavaConsole();
	}
	
};

gJavaConsole1_8_0_421.install();


