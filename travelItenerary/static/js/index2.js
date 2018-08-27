function checkWrongCity() {
	var val=$("#city").val();
	var obj=$("#cities").find("option[value='"+val+"']");

	if(obj !=null && obj.length>0){
		return true;
	}
	elem = document.getElementById('errorCity');
	elem.style.visibility="visible";
	return false;
}

function showTypeOptions() {
    var x = document.getElementById("multiselectDropDown");
    if (x.style.visibility === "hidden") {
        x.style.visibility = "visible";
        var y = document.getElementById("changeArrow")
        y.innerHTML = 'Preferences<span class="glyphicon glyphicon-chevron-up"></span>'
    } else {
        x.style.visibility = "hidden";
        var y = document.getElementById("changeArrow")
        y.innerHTML = 'Preferences<span class="glyphicon glyphicon-chevron-down"></span>'
    }
}


// jQuery.fn.multiselect = function() {
//     $(this).each(function() {
//         var checkboxes = $(this).find("input:checkbox");
//         checkboxes.each(function() {
//             var checkbox = $(this);
//             // Highlight pre-selected checkboxes
//             if (checkbox.prop("checked"))
//                 checkbox.parent().addClass("multiselect-on");
 
//             // Highlight checkboxes that the user selects
//             checkbox.click(function() {
//                 if (checkbox.prop("checked"))
//                     checkbox.parent().addClass("multiselect-on");
//                 else
//                     checkbox.parent().removeClass("multiselect-on");
//             });
//         });
//     });
// };

// $(function() {
//      $(".multiselect").multiselect();
// });