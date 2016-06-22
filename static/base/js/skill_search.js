Skill_search = (function(){
	var el;
	var ele;
	function updateResults(skills){
		if(skills.length === 0){
			$('.collection-header').html("No matching results!");	
		}
		else{
			$('.collection-header').html(skills.length + ' skills found');
		}
		$('.collection-item').remove();
		for(var i = 0; i<skills.length; i++){
			var el = $('<li class = "collection-item row"></li>');
			el.html('<div class = "col s2"><p class = "left-align row">' + skills[i].tags + '</p></div>' + 
				'<a class="btn disabled hover save" style = "margin-left: 650px" data-id = "'+ skills[i].id +'">ADD</a>');
			// 	el.html(<a class="btn disabled">Save</a>);
			$('.collection').append(el);
		}
		if($('.final-save').length<1){
		var ele = $('<a class="btn waves-effect waves-light final-save" type="submit" href = "http://127.0.0.1:8000/account/my_profile" name="action"></a>');
		ele.html('Save<i class = "material-icons right">send</i>');
		$('.collection').append(ele);
		}
	}
	
	function search() {
		var term = $(this).val();
		$.ajax({
			url : '/account/search/',
			data : {'q' : term},
			type : 'GET',
			success : function(data, status, xhr){
				console.log(data);
				updateResults(data['skills']);

			}
		});
	}
	function init(id) {
		el = $('#'+id);
		el.on('input', search);
	}
	return {
		init : init
	};

})();


// href = "http://127.0.0.1:8000/account/save/'+skills[i].id