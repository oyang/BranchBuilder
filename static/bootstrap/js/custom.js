$(document).ready(function(){
		$('a[name="duplicate"]').each(function(i, domEle){
			$(domEle).click(function(){
				var task_id = $(domEle).attr("id").split("-");
				$.get('getbuild',
					{"task_id": task_id[1]},
					function(data){
						buildObj = $.parseJSON(data);
						$('#dupView-repos').val(buildObj['repos']);
						$('#dupView-branch').val(buildObj['branch']); 
						$('#dupView-version').val(buildObj['version']); 
						$('#dupView-author').val(buildObj['author']);
					}
				);
			});	
		});
	
		$('#dupView-Save').click(function(){
			$.post('add', 
				{repos: $('#dupView-repos').val(),
				 branch: $('#dupView-branch').val(), 
				 version: $('#dupView-version').val(), 
				 author: $('#dupView-author').val()},
				 function(data){
					$("#duplicateJob").modal("hide");
					location.reload();
				 }
			);

		});
		
	});
