(function worker() {
    $.ajax({
	url: '/status',
	success: function(data) {
	    for (var id in data){
		$('#' + id).html(data[id]);
	    }	    
	},
	complete: function() {
	    // Schedule the next request when the current one's complete
	    setTimeout(worker, 1000);
	}
    });
})();
