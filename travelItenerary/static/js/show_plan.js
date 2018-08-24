   
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

    document.addEventListener("DOMContentLoaded", function(event) {
      curr_daynum = 0;
      plan = JSON.parse(document.getElementById('plan').value);
      start_date = new Date(document.getElementById('start_date').value);
      city = document.getElementById('city').value;
      numDays = plan.length;
      
      
      
      createLeftPanel();
      setUpReactToTabClick();
      addMapLegendElements();


      
     // initMap();
    });
    
    function addMapLegendElements(){
      /**
      <ol class="legend-day-list">
        
        <li class="legendOption">
          <div class="slot-date" style="display:none">Day 1</div>
          <ul id="placeList" style="display:none">
          </ul>
        </li>
        **/
        let outerLegendDiv = $('.legend-day-list');
        for(let daynum=0;daynum<numDays;daynum++){ 
          let route = plan[daynum];
          
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
        dayListElem.append('<div class="day-box in-plan active"><div class="day text-link">' + 1 + '</div></div>');

        for (let i = 2; i <= plan.length; i++) {
          dayListElem.append('<div class="day-box in-plan"><div class="day text-link">' + i + '</div></div>');
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
          console.log('initMap');
          directionsService = new google.maps.DirectionsService;
          directionsDisplay = new google.maps.DirectionsRenderer;
          map = new google.maps.Map(document.getElementById('mapCanvas'), {
            center: {
              lat: 50,
              lng: 50
            }, 
            zoom: 12
          });
          console.log(map);
          directionsDisplay.setMap(map);
          
          displayRoute();
          displayMapLegend();
          displayDate();     


        }
        
        function displayRoute() {
          hideMarkers();
          let route = plan[curr_daynum];
          console.log('>>>>>>>>>>displayRoute');
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
              console.log('response returned');
              console.log(response);
              directionsDisplay.setDirections(response);
              console.log('set directions');
            } else {
              window.alert('Directions request failed due to ' + status);
            }
          });
        }
        
        function displayAllPlacesOnMap(){
          directionsDisplay.setDirections({routes: []});
          
          if(markers.length == 0){
            createMarkers();
          }
          
          showMarkers();          
        }
        
        function centerMapOnCity(){
          let geocoder = new google.maps.Geocoder();
          geocoder.geocode({'address': city}, function(results, status) {
            if (status === 'OK') {
              map.setCenter(results[0].geometry.location);
              console.log(results[0].geometry.location);
            } else {
              alert('Geocode was not successful for the following reason: ' + status);
            }
          });
        }
        
        function createMarkers(){

          for(let daynum = 0;daynum<numDays;daynum ++){            
            let route = plan[daynum];
            for(let i=0;i<route.length;i++){
              markers = markers.concat(new google.maps.Marker({
                position : {lat: route[i].lat, lng:route[i].lng},
                label :{
                  text: String.fromCharCode('A'.charCodeAt(0) + i), 
                  color: "black" , 
                  fontWeight: 'bold', 
                  fontSize :'16px' 
                } ,
                icon : pinSymbol(colors[daynum])
              }));
            }
          }
        }
        
        function showMarkers(){
          let newBoundary = new google.maps.LatLngBounds();
          
          for(index in markers){
            markers[index].setMap(map);
            newBoundary.extend(markers[index].position);
          }
          
          map.fitBounds(newBoundary);
        }
        
        function hideMarkers(){
          for(index in markers){
            markers[index].setMap(null);
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
          return 'Travel for '+  plan[daynum][sitenum+1]['travel_time'] + ' mins';
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


      function openTab(evt, cityName) {
        var i, tabcontent, tablinks;
        tabcontent = document.getElementsByClassName("tabcontent");
        for (i = 0; i < tabcontent.length; i++) {
          tabcontent[i].style.display = "none";
        }
        tablinks = document.getElementsByClassName("tablinks");
        for (i = 0; i < tablinks.length; i++) {
          tablinks[i].className = tablinks[i].className.replace(" active", "");
        }
        document.getElementById(cityName).style.display = "block";
        evt.currentTarget.className += " active";
      }