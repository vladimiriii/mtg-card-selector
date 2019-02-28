// Functions to be used in the application
function myFunction(){
	console.log("My function is working");
};

function exampleAjax(data, url) {

	$.ajax({
	  	type: "POST",
	  	url: url,
	  	data: data,
		dataType: "text",
		success: function(result) {
			// Parse json string
			let json = JSON.parse(result);
		},
		error: function(msg){
			$(postTo).append(msg);
		}
	});
};
