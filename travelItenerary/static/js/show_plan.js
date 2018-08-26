function openTab(evt, tabName) {
  // console.log(tabName);
  
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
  if(tabName == 'Calender'){
    $('.fc-prev-button').trigger('click');
    $('.fc-next-button').trigger('click');  
  }
  else if(tabName == 'Map'){
    // yo();
  }
  else if(tabName == 'Timeline'){
    loadTimeline();
  }

}