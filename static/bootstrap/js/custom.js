$(document).ready(function(){
		$('#package-help-info').popover({'title': 'Package info', 'content': 'Package can be "ult,ent,corp,pro,com"'});
		$('td[name="list_status"]').each(function (i, domEle){
			if ($(domEle).text() != "Available"){
				var task_id = $(domEle).attr("id").split("_");
				$("#buildList-" + task_id[2]).attr("disabled", "disabled");
			}
		});
		$('input[name="rebuild"]').each(function(i, domEle){
			$(domEle).click(function(){
				var task_id = $(domEle).attr("id").split("-");
				$.get(
					'/BranchBuilder/build',
					{"task_id": task_id[1]},
					function(data){
						$(this).attr("disabled", "disabled");
					}
				);
			});
		});

		$('a[name="duplicateBuild"]').each(function(i, domEle){
			$(domEle).click(function(){
				var task_id = $(domEle).attr("id").split("-");
				$.get('/BranchBuilder/getbuild',
					{"task_id": task_id[1]},
					function(data){
						buildObj = $.parseJSON(data);
						$('#popView-repos').val(buildObj['repos']);
						$('#popView-branch').val(buildObj['branch']); 
						$('#popView-version').val(buildObj['version']); 
						$('#popView-author').val(buildObj['author']);
						$('#popView-package_list').val(buildObj['package_list']);
						$('#popView-upgrade_package').attr("checked", buildObj['upgrade_package'] ? true : false);
						
						//Hide status input textfield
						$('#popView-control-status').hide();

						//Set selectAction as editBuild
						$('#popView-selectAction').val('duplicateBuild');

						//Update the popup view title and build ID
						$('#popView-title').text('Duplicate build -- Task ID ' + task_id[1]);

						$('#popView-selectBuildID').val(task_id[1]);
					}
				);
			});	
		});

		$('a[name="editBuild"]').each(function(i, domEle){
			$(domEle).click(function(){
				var task_id = $(domEle).attr("id").split("-");
				$.get('/BranchBuilder/getbuild',
					{"task_id": task_id[1]},
					function(data){
						var buildObj = $.parseJSON(data);
						$('#popView-repos').val(buildObj['repos']);
						$('#popView-branch').val(buildObj['branch']); 
						$('#popView-version').val(buildObj['version']); 
						$('#popView-author').val(buildObj['author']);
						$('#popView-package_list').val(buildObj['package_list']);
						$('#popView-upgrade_package').attr("checked", buildObj['upgrade_package'] ? true : false);

						//User can update status by entering password
						//Show status input textfield
						$('#popView-control-status').show();
						$('#popView-status').val(buildObj['status']);
						$('#popView-status').attr('readonly', 'readonly');
						$('#popView-edit-status').text('edit');
						
						//Set selectAction as editBuild
						$('#popView-selectAction').val('editBuild');

						//Update the popup view title and build ID
						$('#popView-title').text('Edit build -- Task ID ' + task_id[1]);
						$('#popView-selectBuildID').val(task_id[1]);
					}
				);
			});	
		});
	
		$('#popView-Save').click(function(){
			//Check form validate firstly
			if (! $('#popView-actionBuildForm').valid()){
				return false;
			}

			var upgrade_package = $('#popView-upgrade_package').attr('checked') ? 1 : 0;
			if ($('#popView-selectAction').val() == 'duplicateBuild') {
				$.post('/BranchBuilder/add', 

					{
					 "repos": $('#popView-repos').val(),
					 "branch": $('#popView-branch').val(), 
					 "version": $('#popView-version').val(), 
					 "package_list": $('#popView-package_list').val(),
					 "author": $('#popView-author').val(),
					 "upgrade_package": upgrade_package
					 },

					 function(data){
						$("#popupViewBuild").modal("hide");
						location.reload();
					 }
				);
			} else if ($('#popView-selectAction').val() == 'editBuild'){
				$.post('/BranchBuilder/updatebuild', 

					{
					 "task_id": $('#popView-selectBuildID').val(), 
					 "repos": $('#popView-repos').val(),
					 "branch": $('#popView-branch').val(), 
					 "version": $('#popView-version').val(), 
					 "package_list": $('#popView-package_list').val(),
					 "author": $('#popView-author').val(),
					 "status": $('#popView-status').val(),
					 "upgrade_package": upgrade_package
					 },

					 function(data){
						$("#popupViewBuild").modal("hide");

						location.reload();
					 }
				);
			}
		});

		$('#popView-edit-status').click(function(){
			if ($(this).text() == 'edit') {
				$('#popView-status').removeAttr('readonly');
				$('#popView-edit-status').text('cancel');
			} else if ($(this).text() == 'cancel'){
				$('#popView-status').attr('readonly', 'readonly');
				$('#popView-edit-status').text('edit');
			}
		});

		$('#mailToAdmin').click(function(){
				$('#popView-MailFrom').val(""),
				$('#popView-MailSubject').val("");
				$('#popView-MailMessage').val("");
		});

		$('#popView-Send').click( function(){
			if ($('#popView-sendMailForm').valid()) {
				$.post('/BranchBuilder/sendmail',
					{
						"from_address": $('#popView-MailFrom').val(),
						"to": $('#popView-MailTo').val(),
						"subject": $('#popView-MailSubject').val(),
						"message": $('#popView-MailMessage').val()
					},
					function(data){
						$("#popupViewMail").modal("hide");
					}
				);
			}
		});
	
		setInterval(function(){
			$.get(
				'/BranchBuilder/cron',
				function(data){
					/*
					if (data.length > 0){
						for (var x=0; x < data.length; x++) {
							$('#buildList-' + data[x].task_id.toString()).attr("disabled", "disabled");
							$('#build_status_' + data[x].task_id.toString()).text(data[x].status);
							$('#build_status_' + data[x].task_id.toString()).attr("class", data[x].status);
						}
					} else {
						$('input[name="rebuild"]').each(function(i, domEle){
							$(domEle).removeAttr('disabled');						
						});
						$('td[name="list_status"]').each( function(i, domEle){
							$(domEle).text('Available');						
							$(domEle).attr('class', 'Available');						
						});
					}
					*/

					var task_id_list = [];
					for (var x=0; x < data.length; x++) {
						task_id_list.push(data[x].task_id.toString());
					}
					$('input[name="rebuild"]').each(function(i, domEle){
						var task_id =$(domEle).attr("id").split("-")[1]; 
						if (task_id_list.indexOf(task_id) != -1){
							$('#buildList-' + task_id).attr("disabled", "disabled");
							$('#build_status_' + task_id).text(data[x].status);
							$('#build_status_' + task_id).attr("class", data[x].status);
							
						}else{
							$(domEle).removeAttr('disabled');						
							$('#build_status_' + task_id).text('Available');						
							$('#build_status_' + task_id).attr('class', 'Available');						
						}
					});
				}
			);

		}, 5000);
		
	});
