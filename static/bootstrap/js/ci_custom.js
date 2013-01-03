$(document).ready(function(){
		$('#flavor-help-info').popover({'title': 'Flavors info', 'content': 'Package can be "Ult,Ent,Corp,Pro,CE"'});
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
					'./cideploy',
					{"task_id": task_id[1]},
					function(data){
						$('#deploy_status_' + data.task_id).text(data.status);
						window.location.reload(true);
					}
				);
			});
		});
		$('input[name="editDeploy"]').each(function(i, domEle){
			$(domEle).click(function(){
				var task_id = $(domEle).attr("id").split("-");
				$.get('./cideploy_get',
					{"id": task_id[1]},
					function(data){
						var buildObj = data;
						$('#popView-username').val(buildObj['username']);
						$('#popView-version').val(buildObj['version']); 
						/*
						$('#popView-flavor').val(buildObj['flavor']); 
						*/
						$('#popView-flavor').val(buildObj['flavor']); 
						$('#popView-flavor_list').val(buildObj['deploy_config']);

						//Set selectAction as editBuild
						$('#popView-selectAction').val('editDeploy');

						//Update the popup view title and build ID
						$('#popView-title').text('Edit deploy -- Deploy ID ' + task_id[1]);
						$('#popView-selectDeployID').val(task_id[1]);
					}
				);
			});	
		});
		$('#popView-Save').click(function(){
			//Check form validate firstly
			/*
			if (! $('#popView-actionDeployForm').valid()){
				return false;
			}
			*/

			if ($('#popView-selectAction').val() == 'editDeploy'){
				$.post('/BranchBuilder/CIDeploy/cideploy_update', 

					{
					 "id": $('#popView-selectDeployID').val(), 
					 "username": $('#popView-username').val(),
					 "version": $('#popView-version').val(), 
					 "deploy_config": $('#popView-flavor_list').val(),
					 },

					 function(data){
						$("#popupViewDeploy").modal("hide");

						location.reload();
					 }
				);
			}
		});
		
		setInterval(function(){
			$.get(
				'./cicron',
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
					var lockStatus = $("#lockStatus").val();
					if (data.length != 0 && lockStatus == "0"){
						$("#lockStatus").val("1");
					}
					if (data.length == 0  && lockStatus == "1"){
						window.location.reload(true);
					}
				}
			);

		}, 5000);

	});
