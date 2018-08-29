

var directionsService;
var directionsDisplay;
var map;
var markers = [];
var colors = [
    '#98D54F',      
    '#8333FF',
    '#C473AB',
    '#FF9933',
    '#F00',
    '#0F0',
    '#00F',
    '#B233FF',                       
    '#33CAFF',
    '#9DDAD3',
    '#E859BD',
    '#B2FF33'
];
var defaultLegendcolor = 'rgb(250, 140, 0)';

function onMapTabOpened(){
    map_plan = JSON.parse(document.getElementById('plan_actual').value).tour
   
    recreateMapLegendElements();
    hideMarkers();
    createMarkers();
    $('#tab-day-0').trigger('click');

}

document.addEventListener("DOMContentLoaded", function(event) {
    curr_daynum = 0;
    map_plan = JSON.parse(document.getElementById('plan').value);
    start_date = new Date(document.getElementById('start_date').value);
    city = document.getElementById('city').value;
    numDays = map_plan.length;
    
    createLeftPanel();
    setUpReactToTabClick();
    addMapLegendElements();
    initMap();
});

function recreateMapLegendElements(){
    let outerLegendDiv = $('.legend-day-list');
    outerLegendDiv.empty();
    addMapLegendElements();
}
function addMapLegendElements(){
    let outerLegendDiv = $('.legend-day-list');
    for(let daynum=0;daynum<numDays;daynum++){ 
        let route = map_plan[daynum];
        
        innerDayPlanHTML = "";
        for (let i = 0; i < route.length; i++) {
            let placeHtml =
            `<li class="visit-name">
            <span>
            <span class="map-marker-circle mapMarkerDay${daynum}" style="background-color: ${defaultLegendcolor};">
            ${String.fromCharCode('A'.charCodeAt(0) + i)}
            </span>
            <span class="name">${route[i].name}</span>
            </span>
            <div class="clear"></div>
            </li>`;
            let travelHtml = "";
            if (i != route.length - 1){
                travelHtml =
                `<li class="hop-duration bg-stripe">
                <a class="directions text-link" href="javascript:void(0)" target="_blank">
                ${getTravelTime(daynum,i)}</a>
                </li>`;
            }
            
            innerDayPlanHTML += placeHtml + travelHtml;
        }
        
        outerDayPlanHTML = `
        <li class="legendOption">
        <div id="outer-div-day-${daynum}" class="slot-date" style="display:none">Day ${daynum+1}</div>
        <ul id="placeList${daynum}" style="display:none ">
        ${innerDayPlanHTML}
        </ul>
        </li>
        `;
        outerLegendDiv.append(outerDayPlanHTML);
        
    }
}


function createLeftPanel(){
    let dayListElem = $('#dayList');
    dayListElem.append('<div id="tab-day-0" class="day-box in-plan active"><div class="day text-link">' + 1 + '</div></div>');
    
    for (let i = 2; i <= map_plan.length; i++) {
        dayListElem.append(`<div id="tab-day-${i}"class="day-box in-plan"><div class="day text-link">${i}</div></div>`);
    }
    dayListElem.append('<div class="day-box in-plan" id="allTab"><div class="day text-link">All</div></div>');    
}


function setUpReactToTabClick(){
    $('.day-box.in-plan').on('click', function() { // internally will iterate and add listener to each li
        let clickedElem = $(this);
        clickedElem.parent().find('.active').removeClass('active'); // go to parent and then find li
        clickedElem.addClass('active');
        if(clickedElem.attr('id')=='allTab'){
            curr_daynum = -1;
            displayMapLegendAll();
            displayAllPlacesOnMap();
            displayDateRange();
        }                            
        else{
            curr_daynum = parseInt(clickedElem.text()) - 1;
            displayRoute();
            displayMapLegend();
            displayDate();
        }              
    });
}

function initMap() {     
    // console.log('initMap');
    directionsService = new google.maps.DirectionsService;
    directionsDisplay = new google.maps.DirectionsRenderer({suppressMarkers : true});
    map = new google.maps.Map(document.getElementById('mapCanvas'), {
        center: {
            lat: 50,
            lng: 50
        }, 
        zoom: 12
    });
    // console.log(map);
    directionsDisplay.setMap(map);
    
    createMarkers();  
    displayRoute();
    displayMapLegend();
    displayDate(); 
    
}

function displayRoute() {
    
    hideMarkers();
    directionsDisplay.setDirections({routes: []});
    
    let route = map_plan[curr_daynum];
    if(route.length == 1){        
        showMarkers(curr_daynum);
        if(map.getZoom() > 11){
            map.setZoom(11);
        }
    }
    else{
        // console.log('>>>>>>>>>>displayRoute');
        var waypoints = [];
        for (var i = 1; i < route.length - 1; i++) {
            waypoints.push({
                location: new google.maps.LatLng(route[i]['lat'], route[i]['lng']),
                stopover: true
            });
        }
        directionsService.route({
            origin: new google.maps.LatLng(route[0]['lat'], route[0]['lng']),
            destination: new google.maps.LatLng(route[route.length - 1]['lat'], route[route.length - 1]['lng']),
            travelMode: 'DRIVING',
            waypoints: waypoints
        }, function(response, status) {
            if (status === 'OK') {
                // console.log('response returned');
                // console.log(response);
                directionsDisplay.setDirections(response);
                // console.log('set directions');
            } 
        });
        showMarkers(curr_daynum);
    }
    
}

function displayAllPlacesOnMap(){
    directionsDisplay.setDirections({routes: []});
    
    showMarkersAll();    
    
}

function centerMapOnCity(){
    let geocoder = new google.maps.Geocoder();
    geocoder.geocode({'address': city}, function(results, status) {
        if (status === 'OK') {
            map.setCenter(results[0].geometry.location);
            // console.log(results[0].geometry.location);
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        }
    });
}

function createMarkers(){
    // console.log('createMarkers');
    for(let daynum = 0;daynum<numDays;daynum ++){            
        let route = map_plan[daynum];
        let tmpMarkers = [];
        for(let i=0;i<route.length;i++){
            tmpMarkers[i] = new google.maps.Marker({
                position : {lat: route[i].lat, lng:route[i].lng},
                label :{
                    text: String.fromCharCode('A'.charCodeAt(0) + i), 
                    color: "black" , 
                    fontWeight: 'bold', 
                    fontSize :'16px' 
                } ,
                icon : pinSymbol(colors[daynum])
            });
            let infoWindow = new google.maps.InfoWindow({
                    content : `<div style='float:left'>
                    <img src="/static/${route[i].images[0].replace('new_data','small')}"></div>
                    <div style='float:right; padding: 10px;'>
                        <b>${route[i].name}</b><br/>
                        ${route[i].time_to_show}</div>`
                    // route[i].name
                })
            tmpMarkers[i].addListener('mouseover',function(){
                infoWindow.open(map,tmpMarkers[i]);
            });
            tmpMarkers[i].addListener('mouseout',function(){
                infoWindow.close();
            });
        }
        markers[daynum] = tmpMarkers;
    }
}

function showMarkers(daynum){
    let newBoundary = new google.maps.LatLngBounds();
    let tmpMarkers = markers[daynum];
    for(index in tmpMarkers){
        tmpMarkers[index].setMap(map);
        newBoundary.extend(tmpMarkers[index].position);
    }          
    map.fitBounds(newBoundary);
}
function showMarkersAll(){
    let newBoundary = new google.maps.LatLngBounds();
    for(let daynum = 0;daynum<numDays;daynum++){
        let tmpMarkers = markers[daynum];
        for(index in tmpMarkers){
            tmpMarkers[index].setMap(map);
            newBoundary.extend(tmpMarkers[index].position);
        }          
    }
    map.fitBounds(newBoundary);
    
}

function hideMarkers(){
    console.log('hide markers');
    for(let daynum=0;daynum<numDays;daynum++){
        let tmpMarkers = markers[daynum];
        for(index in tmpMarkers){
            tmpMarkers[index].setMap(null);
        }
    }
    
}

function displayMapLegend() {
    let daynum = curr_daynum;
    $(`.map-marker-circle.mapMarkerDay${daynum}`).attr('style',`background-color:${defaultLegendcolor}`);
    for(let i=0;i<numDays;i++){
        if(i!=daynum){
            $(`#outer-div-day-${i}`).attr('style','display:none');
            $(`#placeList${i}`).attr('style','display:none');
        }              
    }
    $(`#outer-div-day-${daynum}`).attr('style','');
    $(`#placeList${daynum}`).attr('style','');
}

function displayMapLegendAll(){
    for(let i=0;i<numDays;i++){
        $(`#outer-div-day-${i}`).attr('style','');
        $(`#placeList${i}`).attr('style','');
        $(`.map-marker-circle.mapMarkerDay${i}`).attr('style',`background-color:${colors[i]}`);
    }
}


function getTravelTime(daynum , sitenum){
    return 'Travel for '+  map_plan[daynum][sitenum+1]['travel_time'] + ' mins';
}
function displayDate(){
    let daynum = curr_daynum;
    $('.stay-area > .stayName').text(city);
    let curr_date = new Date(start_date);
    curr_date.setDate(curr_date.getDate() + daynum);
    let arr = curr_date.toString().split(' ');
    $('.mon').text(arr[1]);
    $('.date').text(arr[2]);
    $('.dow').text(arr[0]);
}

function displayDateRange(){
    $('.mon').text('');
    $('.date').text('');
    $('.dow').text('');
    $('.stay-area > .stayName').text(`${city} : Full itenerary`);
    
}
function pinSymbol(color) {
    return {
        path: 'M 0,0 C -2,-20 -10,-22 -10,-30 A 10,10 0 1,1 10,-30 C 10,-22 2,-20 0,0 z',
        fillColor: color,
        fillOpacity: 1,
        strokeColor: '#000',
        strokeWeight: 2,
        scale: 1,
        labelOrigin : new google.maps.Point(0, -25)
    };
}