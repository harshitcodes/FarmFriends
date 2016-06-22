var followUnfollow = (function() {
	function follow() {
		var followerid = $(this).attr('data-uid');
		$.ajax({
			method: 'GET',
			url: 'user/'+followerid+'/follow',
			dataType: 'json',
			success: function(data, status, xhr) {
				if (data['result'] === 1) {
					$(this).removeClass('follow');
					$(this).addClass('unfollow');
					$(this).html('unfollow');
				}
			}.bind(this)
		});	
	}
	function unfollow() {
		var followerid = $(this).attr('data-uid');
		$.ajax({
			method: 'GET',
			url: 'user/'+followerid+'/unfollow',
			dataType: 'json',
			success: function(data, status, xhr){
				if(data['result'] === 1) {
					$(this).removeClass('unfollow');
					$(this).addClass('follow');
					$(this).html('follow');
				}
			}.bind(this)

		});
	}

	function handleClick(e) {
        e.preventDefault();
        if ($(this).hasClass('follow')) {
            follow.call(this);
        } 
        else {
            unfollow.call(this);
        }
    }
	return {
		init: function() {
			$('a.fnuf').click(handleClick);
		}
	};
})(); 