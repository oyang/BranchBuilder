$(document).ready(function(){
	var editor = CodeMirror.fromTextArea(document.getElementById("code_area"), {
			mode:"text/x-php",
			indentUnit: 2,
			lineNumbers: true,
			matchBrackets: true,
			lineWrapping: true,
			});
	$("#buildconfig_update").click(function(){

		if ($(this).text() == "Edit"){
			$("#buildconfig_version").removeAttr("readonly");	
			$("#buildconfig_author").removeAttr("readonly");	
			$("#code_area").removeAttr("readonly");	
			$(this).text("Save");
		} else if ($(this).text() == "Save"){
			$.post(
				"buildconfig_update",
				{
					"id": $("#buildconfig_id").val(),
					"version": $("#buildconfig_version").val() ,
					"author": $("#buildconfig_author").val(),
					"build_config_content": editor.getValue()
				},
				function(data){
					$("#buildconfig_version").attr("readonly", "readonly");	
					$("#buildconfig_author").attr("readonly", "readonly");	
					$("#code_area").attr("readonly", "readonly");
					$("#buildconfig_update").text("Edit");
				}
			);
		}
	});

});
