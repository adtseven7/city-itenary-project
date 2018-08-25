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


jQuery.fn.multiselect = function() {
    $(this).each(function() {
        var checkboxes = $(this).find("input:checkbox");
        checkboxes.each(function() {
            var checkbox = $(this);
            // Highlight pre-selected checkboxes
            if (checkbox.prop("checked"))
                checkbox.parent().addClass("multiselect-on");
 
            // Highlight checkboxes that the user selects
            checkbox.click(function() {
                if (checkbox.prop("checked"))
                    checkbox.parent().addClass("multiselect-on");
                else
                    checkbox.parent().removeClass("multiselect-on");
            });
        });
    });
};

$(function() {
     $(".multiselect").multiselect();
});