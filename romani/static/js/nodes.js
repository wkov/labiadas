/**
 * Created by sergi on 01/01/17.
 */


//jQuery(document).ready(function($) {
//
//    $(".lloc_entrega").change(function (e) {
//
//
////{#        var dataentrega = document.getElementById("dataentrega");#}
////{#	var frequencia = document.getElementById("frequencia");#}
////{#	var node = document.getElementById("lloc_entrega");#}
////{##}
////{#      var data = $(".lloc_entrega").serialize();#}
////
////
////{#    var selectedValue = node.options[node.selectedIndex].value;#}
////{#    var selected = {'selectedValue': selectedValue, CSRF: '{{ csrf_token }}'};#}
//
////{#    changeFunc.preventDefault();#}
//        e.preventDefault();
//	$.post("/nodecalc/", $(this).serialize(), function(data) {
//        if (data == "OK") {
//            CallNotification("Invitacio a participar a la xarxa enviada amb exit", "success")
//        } else {
//            CallNotification("No es possible convidar aquest correu electronic", "failure")
//        }
//    });
//
//
//
//
//    });
//
//
//});




function changeFunc() {

	var dataentrega = document.getElementById("dataentrega");
	var frequencia = document.getElementById("frequencia");
	var node = document.getElementById("lloc_entrega");



    var selectedValue = node.options[node.selectedIndex].value;
    var selected = {'selectedValue': selectedValue}

//{#    changeFunc.preventDefault();#}
	$.post("/nodecalc/", selected, function(data) {
        if (data == "OK") {
            CallNotification("Invitacio a participar a la xarxa enviada amb exit", "success")
        } else {
            CallNotification("No es possible convidar aquest correu electronic", "failure")
        }
    });

//{#    dataentrega.options[0].value = "{{ nodes[0].dies_entrega[0].dia }}"#}


//{#    dataentrega.value = {{ node. }}#}






//{#    for n in nodes[node.selectedIndex].dies_entrega:#}
//{##}
//{##}
//{##}
//{#    dataentrega.options[]#}
//
//{#    alert(nodes);#}
   }