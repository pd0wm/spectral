(function worker() {
    $.ajax({
	url: '/status',
	success: function(data) {
	    $('#uptime-content').html(data['uptime']);
	    console.log(data);
	},
	complete: function() {
	    // Schedule the next request when the current one's complete
	    setTimeout(worker, 100);
	    console.log("schudeled");
	}
    });
})();
