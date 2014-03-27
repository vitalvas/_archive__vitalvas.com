$(document).ready(function() {
	function createPhotoElement(photo) {
		var innerHtml = $('<img>').addClass('instagram-image').attr('src', photo.images.thumbnail.url.replace('http://','//'));
		innerHtml = $('<a>').attr('target', '_blank').attr('href', photo.link.replace('http://','//')).append(innerHtml);
		return $('<div>').addClass('instagram-placeholder').attr('id', photo.id).append(innerHtml);
	}
	function didLoadInstagram(event, response) {
		var that = this;
		$.each(response.data, function(i, photo) {
			$(that).append(createPhotoElement(photo));
		});
	}
	$('#instagram').on('didLoadInstagram', didLoadInstagram);
	$('#instagram').instagram({
		clientId: 'fa8d36a1cbe64a0dbd2166ec50c84124',
		accessToken: '203723320.fa8d36a.a7a9f5aec8db4be08a4a10b26655316c',
		count: 15,
		userId: 203723320,
	});
});