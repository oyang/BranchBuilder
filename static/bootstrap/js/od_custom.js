$(document).ready(function(){
		$("li.active").removeClass("active");
		$("#navODDeploy").addClass("active");

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
					'./oddeploy',
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
				$.get('/BranchBuilder/ODDeploy/oddeploy_get',
					{"id": task_id[1]},
					function(data){
						var buildObj = data;
						$('#popView-username').val(buildObj['username']);
						$('#popView-version').val(buildObj['version']); 
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
				$.post('/BranchBuilder/ODDeploy/oddeploy_update', 

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
				'./odcron',
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

		/*
		setInterval(function(){
			$.get(
				'./odsicron',
				function(data){
					if (data[0].jobName.toString() == "no_silentupgrade"){
						$('input[name="reupgrade"]').each(function(i, domEle){
							$(domEle).removeAttr('disabled');
							$(domEle).val('Upgrade');
						});

					}
				}
			);
		}, 5000);
		*/

		$('input[name="reupgrade"]').each(function(i, domEle){
			$(domEle).click(function(){
				var insname = $('#insname').val();
				var upgradetype = $('input[name="upgradetype"]').val();
				var flavor = $('#flavorlist').find(":selected").text();
				var dynamic = $('#dynamiclist').find(":selected").text();
				var version = $('#versionlist').find(":selected").text();
				$(this).attr("disabled", "disabled");
				$(this).val("Upgrading");
				$.get(
					'./oddeploy_si',
					{"insname": insname,"upgradetype": upgradetype,"flavor": flavor,"dynamic": dynamic,"version": version}
				);
			});
		});

		$('input[name="upgradetype"]').each(function(i, domEle){
			$(domEle).click(function(){
					var $flavorlist = $('#flavorlist');
					var $dynamiclist = $('#dynamiclist');
					
					var flaoptions_co = {"CE":"ce","Pro":"pro","Ent":"ent","Corp":"corp"};
					var flaoptions_up = {"CE":"ce","Pro":"pro","Ent":"ent","Corp":"corp","Ult":"ult"};
					var dynoptions_co = {"Pro":"pro","Ent":"ent","Corp":"corp","Ult":"ult"};
					var dynoptions_up = {"6.4.x":"6.4.x","6.5.x":"6.5.x"};
					if ($(this).val() == "conversion"){
						$('#flavorheader').text('Current Flavor');	
						$('#dynamicheader').text('To Flavor');	
						$('#versionheader').text('Version');
						$flavorlist.empty();
						$dynamiclist.empty();
						$.each(flaoptions_co,function(key, value){
							$flavorlist.append($("<option></option>").attr("value",value).text(key));
						});
						$.each(dynoptions_co,function(key, value){
							$dynamiclist.append($("<option></option>").attr("value",value).text(key));
						});
					}else{
						$('#flavorheader').text('Flavor');	
						$('#dynamicheader').text('Current Version');	
						$('#versionheader').text('To Version');
						$flavorlist.empty();
						$dynamiclist.empty();
						$.each(flaoptions_up,function(key, value){
							$flavorlist.append($("<option></option>").attr("value",value).text(key));
						});
						$.each(dynoptions_up,function(key, value){
							$dynamiclist.append($("<option></option>").attr("value",value).text(key));
						});
						
					}	
				});
			});

		$('#flavorlist').each(function(i, domEle){
			var $Uptype = $('#upgradetype1');
			var $dynamiclist = $('#dynamiclist');
			$(domEle).change(function(){
				if ($Uptype.is(":checked")){
					$dynamiclist.empty();
					var dynoptions_co = {"Pro":"pro","Ent":"ent","Corp":"corp","Ult":"ult"};
					if ($(this).val() == "pro"){dynoptions_co = {"Ent":"ent","Corp":"corp","Ult":"ult"}}
					if ($(this).val() == "ent"){dynoptions_co = {"Ult":"ult"}}
					if ($(this).val() == "corp"){dynoptions_co = {"Ent":"ent","Ult":"ult"}}
					$.each(dynoptions_co,function(key, value){
						$dynamiclist.append($("<option></option>").attr("value",value).text(key));
					});
				}
			});
		});
		
	});
