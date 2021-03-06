function loadTimeline(){
	let PLAN = JSON.parse(document.getElementById('plan_actual').value);
	let ELEMENT = document.getElementById('planTimelineView');
	let HTML = [
		'<div class="col-lg-12">',
		'<ul class="timeline">'
	];
	let TOUR_LENGTH = PLAN['tour'].length;
	for(var i=0;i<TOUR_LENGTH;i++){
		if(i > 0){
			HTML.push('<li></li>')
		}
		let CUR_DAY = i+1;
		HTML.push('<li class="timeline-inverted">')
		HTML.push('<div class="timeline-image">')
		HTML.push('<h4>Day <br>' + CUR_DAY + '</h4>')
		HTML.push('</div>')
		HTML.push('</li>')
		let DAY_LENGTH = PLAN['tour'][i].length
		for(var j=0;j<DAY_LENGTH;j++){
			HTML.push('<li class="timeline">')
			HTML.push('<h5 class="section-subheading text-muted" align="center"><i>')
			HTML.push('<br/><br/><br/><br/>')
			if(j == 0){
				HTML.push('Start')
			}
			else{
				HTML.push(PLAN['tour'][i][j]['travel_dist'] + 'Km (' + PLAN['tour'][i][j]['travel_time'] + 'mins)')
			}
			HTML.push('</i></h5>')
			HTML.push('</li>')
			if(j%2 == 1){
				HTML.push('<li class="timeline-inverted">')
				HTML.push('<div class="timeline-image">')
				HTML.push('<img class="rounded-circle img-fluid" src="/static/' + PLAN['tour'][i][j]['images'][0] + '" alt="">')
				HTML.push('</div>')
				HTML.push('<div class="timeline-panel">')
				HTML.push('<div class="timeline-heading">')
				HTML.push('<h4 class="subheading">' + PLAN['tour'][i][j]['name'] +'</h4>')
				HTML.push('<h6>')
				for(var k = 0;k<PLAN['tour'][i][j]['rating_len'].length;k++){
					HTML.push('<span class="fa fa-star checked"></span>')
				}
				HTML.push(PLAN['tour'][i][j]['rating'] + '(' + PLAN['tour'][i][j]['no_of_ratings'] + ')')
				HTML.push('</h6>')
				HTML.push('</div>')
				HTML.push('<div class="timeline-body">')
				HTML.push('<p class="text-muted">' + PLAN['tour'][i][j]['time_to_show'] + '</p>')
				HTML.push('<br>')
				HTML.push('</div>')
				HTML.push('<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#modal' + PLAN['tour'][i][j]['place_id'] + '">Details</button>')
				HTML.push('<div class="modal fade" id="modal' + PLAN['tour'][i][j]['place_id'] + '" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">')
				HTML.push('<div class="modal-dialog modal-lg" role="document">')
				HTML.push('<div class="modal-content">')
				HTML.push('<div class="modal-body">')
				HTML.push('<div class="row">')
				HTML.push('<div class="col-lg-5">')
				HTML.push('<div id="carousel-thumb' + PLAN['tour'][i][j]['place_id'] + '" class="carousel slide carousel-fade carousel-thumbnails" data-ride="carousel">')
				HTML.push('<div class="carousel-inner" role="listbox">')
				HTML.push('<div class="carousel-item active">')
				HTML.push('<img class="d-block w-100" src="/static/' + PLAN['tour'][i][j]['images'][0] + '" alt="First slide">')
				HTML.push('</div>')
				HTML.push('<div class="carousel-item">')
				HTML.push('<img class="d-block w-100" src="/static/' + PLAN['tour'][i][j]['images'][1] + '" alt="Second slide">')
				HTML.push('</div>')
				HTML.push('<div class="carousel-item">')
				HTML.push('<img class="d-block w-100" src="/static/' + PLAN['tour'][i][j]['images'][2] + '" alt="Third slide">')
				HTML.push('</div>')
				HTML.push('<div class="carousel-item">')
				HTML.push('<img class="d-block w-100" src="/static/' + PLAN['tour'][i][j]['images'][3] + '" alt="Fourth slide">')
				HTML.push('</div>')
				HTML.push('</div>')
				HTML.push('<a class="carousel-control-prev" href="#carousel-thumb' + PLAN['tour'][i][j]['place_id'] + '" role="button" data-slide="prev">')
				HTML.push('<span class="carousel-control-prev-icon" aria-hidden="true"></span>')
				HTML.push('</a>')
				HTML.push('<a class="carousel-control-next" href="#carousel-thumb' + PLAN['tour'][i][j]['place_id'] + '" role="button" data-slide="next">')
				HTML.push('<span class="carousel-control-next-icon" aria-hidden="true"></span>')
				HTML.push('</a>')
				HTML.push('</div>')
				HTML.push('</div>')
				HTML.push('<div class="col-lg-7">')
				HTML.push('<h2 class="h2-responsive product-name">')
				HTML.push('<strong>' + PLAN['tour'][i][j]['name'] + '</strong>')
				HTML.push('</h2>')
				HTML.push('<div class="modal-body">')
				HTML.push(PLAN['tour'][i][j]['description'])
				HTML.push('</div>')
				HTML.push('<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>')
				HTML.push('</div>')
				HTML.push('</div>')
				HTML.push('</div>')
				HTML.push('</div>')
				HTML.push('</div>')
				HTML.push('</div>')
				HTML.push('</div>')
				HTML.push('</li>')
			}
			else{
				HTML.push('<li class="timeline">')
				HTML.push('<div class="timeline-image">')
				HTML.push('<img class="rounded-circle img-fluid" src="/static/' + PLAN['tour'][i][j]['images'][0] + '" alt="">')
				HTML.push('</div>')
				HTML.push('<div class="timeline-panel">')
				HTML.push('<div class="timeline-heading">')
				HTML.push('<h4 class="subheading">' + PLAN['tour'][i][j]['name'] +'</h4>')
				HTML.push('<h6>')
				for(var k = 0;k<PLAN['tour'][i][j]['rating_len'].length;k++){
					HTML.push('<span class="fa fa-star checked"></span>')
				}
				HTML.push(PLAN['tour'][i][j]['rating'] + '(' + PLAN['tour'][i][j]['no_of_ratings'] + ')')
				HTML.push('</h6>')
				HTML.push('</div>')
				HTML.push('<div class="timeline-body">')
				HTML.push('<p class="text-muted">' + PLAN['tour'][i][j]['time_to_show'] + '</p>')
				HTML.push('<br>')
				HTML.push('</div>')
				HTML.push('<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#modal' + PLAN['tour'][i][j]['place_id'] + '">Details</button>')
				HTML.push('<div class="modal fade" id="modal' + PLAN['tour'][i][j]['place_id'] + '" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">')
				HTML.push('<div class="modal-dialog modal-lg" role="document">')
				HTML.push('<div class="modal-content">')
				HTML.push('<div class="modal-body">')
				HTML.push('<div class="row">')
				HTML.push('<div class="col-lg-5">')
				HTML.push('<div id="carousel-thumb' + PLAN['tour'][i][j]['place_id'] + '" class="carousel slide carousel-fade carousel-thumbnails" data-ride="carousel">')
				HTML.push('<div class="carousel-inner" role="listbox">')
				HTML.push('<div class="carousel-item active">')
				HTML.push('<img class="d-block w-100" src="/static/' + PLAN['tour'][i][j]['images'][0] + '" alt="First slide">')
				HTML.push('</div>')
				HTML.push('<div class="carousel-item">')
				HTML.push('<img class="d-block w-100" src="/static/' + PLAN['tour'][i][j]['images'][1] + '" alt="Second slide">')
				HTML.push('</div>')
				HTML.push('<div class="carousel-item">')
				HTML.push('<img class="d-block w-100" src="/static/' + PLAN['tour'][i][j]['images'][2] + '" alt="Third slide">')
				HTML.push('</div>')
				HTML.push('<div class="carousel-item">')
				HTML.push('<img class="d-block w-100" src="/static/' + PLAN['tour'][i][j]['images'][3] + '" alt="Fourth slide">')
				HTML.push('</div>')
				HTML.push('</div>')
				HTML.push('<a class="carousel-control-prev" href="#carousel-thumb' + PLAN['tour'][i][j]['place_id'] + '" role="button" data-slide="prev">')
				HTML.push('<span class="carousel-control-prev-icon" aria-hidden="true"></span>')
				HTML.push('</a>')
				HTML.push('<a class="carousel-control-next" href="#carousel-thumb' + PLAN['tour'][i][j]['place_id'] + '" role="button" data-slide="next">')
				HTML.push('<span class="carousel-control-next-icon" aria-hidden="true"></span>')
				HTML.push('</a>')
				HTML.push('</div>')
				HTML.push('</div>')
				HTML.push('<div class="col-lg-7">')
				HTML.push('<h2 class="h2-responsive product-name">')
				HTML.push('<strong>' + PLAN['tour'][i][j]['name'] + '</strong>')
				HTML.push('</h2>')
				HTML.push('<div class="modal-body">')
				HTML.push(PLAN['tour'][i][j]['description'])
				HTML.push('</div>')
				HTML.push('<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>')
				HTML.push('</div>')
				HTML.push('</div>')
				HTML.push('</div>')
				HTML.push('</div>')
				HTML.push('</div>')
				HTML.push('</div>')
				HTML.push('</div>')
				HTML.push('</li>')

			}
		}
	}
	HTML.push('</ul>')
	HTML.push('</div>')
	// console.log(HTML.length)
	HTML = HTML.join('\n')
	ELEMENT.innerHTML = HTML
};

