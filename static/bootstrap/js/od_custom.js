$(document).ready(function(){
		$('td[name="list_status"]').each(function (i, domEle){
			if ($(domEle).text() != "Available"){
				var task_id = $(domEle).attr("id").split("_");
				$("#deployList-" + task_id[2]).attr("disabled", "disabled");
			}
		});
		$('input[name="redeploy"]').each(function(i, domEle){
			$(domEle).click(function(){
				var task_id = $(domEle).attr("id").split("-");
				$(this).attr("disabled", "disabled");
				$('#deploy_status_' + task_id[1]).text("Starting...");
				$.get(
					'/ODDeploy/oddeploy',
					{"task_id": task_id[1]},
					function(data){
						$('#deploy_status_' + data.task_id).text(data.status);
						window.location.reload(true);
					}
				);
			});
		});

		setInterval(function(){
			$.get(
				'/ODDeploy/odcron',
				function(data){
					var task_id_list = [];
					var task_status_list = [];
					for (var x=0; x < data.length; x++) {
						task_id_list.push(data[x].task_id.toString());
						task_status_list.push(data[x].status.toString());
					}
					$('input[name="redeploy"]').each(function(i, domEle){
						var task_id =$(domEle).attr("id").split("-")[1]; 
						if (task_id_list.indexOf(task_id) != -1){
							var task_status = task_status_list[task_id_list.indexOf(task_id)];
							$('#deployList-' + task_id).attr("disabled", "disabled");
							$('#deploy_status_' + task_id).text(task_status);
							$('#deploy_status_' + task_id).attr("class", task_status);
							
						}else{
							$(domEle).removeAttr('disabled');						
							$('#deploy_status_' + task_id).text('Available');						
							$('#deploy_status_' + task_id).attr('class', 'Available');						
						}
					});
				}
			);

		}, 5000);
		
	});
