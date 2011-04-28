Haps =
	init: () ->
		searchInput = $("#search")
		searchButton = $("#search-button")
		Haps.lastQuery = null
		Haps.searchDefault = searchInput.val()
		searchInput.addClass("tip")
		searchInput.focus(Haps.searchFocus)
		searchInput.blur(Haps.searchBlur)
		searchButton.click(Haps.searchClick)

		toggleButton = $("#search-toggle")
		toggleButton.click(Haps.searchToggle)


	searchClick: (event) ->
		searchInput = $("#search")
		query = Haps.strip(searchInput.val())
		if query == "" or query == Haps.searchDefault or query == Haps.lastQuery
			return
		Haps.search(query)


	search: (query) ->
		$("#place").text("")
		Haps.postFeed(query, "/feeds/flickr", 'flickr',
					  Haps.flickrResponse, Haps.flickrError)
		Haps.postFeed(query, "/feeds/twitter", 'twitter',
					  Haps.twitterResponse, Haps.twitterError)
		Haps.postFeed(query, "/feeds/lastfm", "lastfm",
					  Haps.lastfmResponse, Haps.lastfmError)
		Haps.postFeed(query, "/feeds/yelp", "yelp",
					  Haps.yelpResponse, Haps.yelpError)
		

	postFeed: (query, url, listId, callback, errorCallback) ->
		Haps.loadList(listId)
		data =
			_xsrf: Haps.getXsrf()
			location: query

		params =
			url: url
			success: callback
			error: errorCallback
			dataType: "json"
			data: data
			cache: false
			type: "POST"
			
		$.ajax(params)

	clearList: (elId) ->
		el = $('#'+elId)
		el.find('li').not(".column-title").remove()

	loadList: (elId) ->
		Haps.clearList(elId)
		el = $('#'+elId)
		el.append("<li class='loading'>Loading...</li>")

	noResults: (elId) ->
		Haps.clearList(elId)
		el = $('#'+elId)
		el.append("<li class='no-results'>(no results)</li>")

	updatePlace: (place) ->
		placeTitle = $("#place")
		if Haps.strip(placeTitle.text()) == ""
			placeTitle.text(place)

	yelpError: (response) ->
		Haps.noResults('yelp')

	yelpResponse: (response) ->
		yelp = $("#yelp")
		results = response.entries
		if not results or results.length == 0
			return Haps.noResults('yelp')
		Haps.clearList('yelp')
		for result in results
			yelp.append("<li><img src='"+result.image+"'/>"+result.name+"</li>")

	lastfmError: (response) ->
		Haps.noResults('lastfm')

	lastfmResponse: (response) ->
		lastfm = $("#lastfm")
		results = response.entries
		if not results or results.length == 0
			return Haps.noResults('lastfm')
		Haps.clearList("lastfm")
		for result in results
			lastfm.append("<li><img src='"+result.image+"'/>"+result.title+"</li>")

	flickrError: (response) ->
		Haps.noResults('flickr')

	flickrResponse: (response) ->
		flickr = $("#flickr")
		results = response.entries
		if not results or results.length == 0
			return Haps.noResults('flickr')
		Haps.clearList('flickr')
		for result in results
			flickr.append("<li><img src='"+result.images.square+"'/></li>")
		if response.place
			Haps.updatePlace(response.place)

	twitterResponse: (response) ->
		twitter = $("#twitter")
		results = response.entries
		if not results or results.length == 0
			return Haps.noResults('twitter')
		Haps.clearList('twitter')
		for result in results
			twitter.append("<li><img src='"+result.image+"'/>"+
						   result.text+"</li>")
		if response.place
			Haps.updatePlace(response.place)
			
	getXsrf: () ->
		return $('input[name="_xsrf"]').val()

	searchFocus: (event) ->
		searchInput = $(event.target)
		if searchInput.hasClass("tip")
			searchInput.val('')
			searchInput.removeClass("tip")

	searchBlur: (event) ->
		searchInput = $(event.target)
		searchVal = Haps.strip(searchInput.val())
		if searchVal == Haps.searchDefault or searchVal == ""
			searchInput.val(Haps.searchDefault)
			searchInput.addClass("tip")


	searchToggle: (event) ->
		toggleButton = $('#search-toggle')
		searchContainer = $(".search-container")
		if toggleButton.hasClass("hide")
			searchContainer.slideUp()
			toggleButton.text("Show Search")
			toggleButton.removeClass("hide")
		else
			searchContainer.slideDown()
			toggleButton.text("Hide Search")
			toggleButton.addClass("hide")

	scroll: (event) ->
		docHeight = $(document).height()
		height = $(event.target).height()
		if docHeight > height
			height = docHeight
		footer = $('.footer')
		$('.footer').css('top', height+'px')

	strip: (text) ->
		return text.replace(/^\s+|\s+$/i, "")


$(Haps.init)
