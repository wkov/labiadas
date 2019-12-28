jQuery(document).ready(function($)

    {


$(".vote_forum_form").submit(function(e)
		{
		    e.preventDefault();
		    var btn = $("button", this);
		    var l_id = $(".hidden_id", this).val();
		    btn.attr('disabled', true);
		    $.post("/forum/vote/", $(this).serializeArray(),
			  function(data) {
			      if(data["voteobj"]) {
				  btn.text("-");
			      }
			      else {
				  btn.text("+");
			      }
			  });
		    btn.attr('disabled', false);
		});

$(".vote_debat_form").submit(function(e)
		{
		    e.preventDefault();
		    var btn = $("button", this);
		    var l_id = $(".hidden_id", this).val();
		    btn.attr('disabled', true);
		    $.post("/forum/votedebat/", $(this).serializeArray(),
			  function(data) {
			      if(data["voteobj"]) {
				  btn.text("-");
			      }
			      else {
				  btn.text("+");
			      }
			  });
		    btn.attr('disabled', false);
		});


        $("#checkAll").click(function () {

            $('input:checkbox').not(this).prop('checked', this.checked);
        });


//        var selects = document.querySelectorAll('select');
//
//        selects[0].addEventListener('change', function () {
//        for (var i = 0; i < selects.length; i++) {
//            selects[i].value = selects[0].value;
//        }
//});


             $("#datepicker").datepicker({dateFormat: 'dd/mm/yy'});

             $("#datepicker2").datepicker({dateFormat: 'dd/mm/yy'});

             $("#accordion").accordion();

             $("#myTable").tablesorter({dateFormat: "uk"});

             $("#myTable2").tablesorter({dateFormat: "uk"});








            $("#notificationLink").click(function() {
                $("#notificationContainer").toggle();
                $("#notification_count").fadeOut("slow");
                return false;
            });
            //Document Click
            $(document).click(function() {
                $("#notificationContainer").hide();
            });


		(function () {
    $(function () {
        var SideBAR;
        SideBAR = (function () {
            function SideBAR() {}
            SideBAR.prototype.expandMyMenu = function () {
                return $("nav.sidebar").removeClass("sidebar-menu-collapsed").addClass("sidebar-menu-expanded");
            };
            SideBAR.prototype.collapseMyMenu = function () {
                return $("nav.sidebar").removeClass("sidebar-menu-expanded").addClass("sidebar-menu-collapsed");
            };
            SideBAR.prototype.showMenuTexts = function () {
                return $("nav.sidebar ul a span.expanded-element").show();
            };
            SideBAR.prototype.hideMenuTexts = function () {
                return $("nav.sidebar ul a span.expanded-element").hide();
            };
            SideBAR.prototype.showActiveSubMenu = function () {
                $("li.active ul.level2").show();
                return $("li.active a.expandable").css({
                    width: "100%"
                });
            };
            SideBAR.prototype.hideActiveSubMenu = function () {
                return $("li.active ul.level2").hide();
            };
            SideBAR.prototype.adjustPaddingOnExpand = function () {
                $("ul.level1 li a.expandable").css({
                    padding: "1px 4px 4px 0px"
                });
                return $("ul.level1 li.active a.expandable").css({
                    padding: "1px 4px 4px 4px"
                });
            };
            SideBAR.prototype.resetOriginalPaddingOnCollapse = function () {
                $("ul.nbs-level1 li a.expandable").css({
                    padding: "4px 4px 4px 0px"
                });
                return $("ul.level1 li.active a.expandable").css({
                    padding: "4px"
                });
            };
            SideBAR.prototype.ignite = function () {
                return (function (instance) {
                    return $("#justify-icon").click(function (e) {
                        if ($(this).parent("nav.sidebar").hasClass("sidebar-menu-collapsed")) {
                            instance.adjustPaddingOnExpand();
                            instance.expandMyMenu();
                            instance.showMenuTexts();
                            instance.showActiveSubMenu();
                            $(this).css({
                                color: "#000"
                            });
                        } else if ($(this).parent("nav.sidebar").hasClass("sidebar-menu-expanded")) {
                            instance.resetOriginalPaddingOnCollapse();
                            instance.collapseMyMenu();
                            instance.hideMenuTexts();
                            instance.hideActiveSubMenu();
                            $(this).css({
                                color: "#FFF"
                            });
                        }
                        return false;
                    });
                })(this);
            };
            return SideBAR;
        })();
        return (new SideBAR).ignite();
    });
}).call(this);









	$(".vote_form").submit(function(e)
		{
		    e.preventDefault();
			var entrega = $(".hidden_id", this).val();
			var modal = document.getElementById('comentariModal');
			var vote = document.getElementById('id_vote');
			modal.style.display = "block";
			var entregados = document.getElementById('entrega_pk');
			entregados.value = entrega;
			vote.value = this.submited;
	});
	$(".close_com").click(function(e)
	{
		var modal = document.getElementById('comentariModal');
    	modal.style.display = "none";
	});




	$(".comanda_form").submit(function(e)
		{
		    e.preventDefault();
		    var btn = $("button", this);
		    var l_id = $(".hidden_id", this).val();
//			var call = "Has afegit "+ this[5].value + " articles"
			var modal = document.getElementById('myModal');
			var preu = document.getElementById('preu');
			var llocentrega = document.getElementById('lloc_entrega');
			var format = document.getElementById('format');
			var format_pk = document.getElementById('format_pk');
			var producte = document.getElementById('producte');
			var producte_pk = document.getElementById('producte_pk');
			var cantitat = document.getElementById('cantitat_t');
//			var imatge = document.getElementById('imatge');
			var frequencia = document.getElementById('frequencia');
			var frequencia_label = document.getElementById('frequencia_label')
			//var primera_entrega = document.getElementById('primera_entrega')

		$.post("/info/", $(this).serializeArray(),function(data) {
			if ( data["success"] == 0) {
				  url = "";
				  location = url;
				  //call = "Has fet la comanda correctament"
				  //CallNotification(call,"success")
			}else {
					modal.style.display = "block";
					preu.value = data["preu"];
					format.value = data["format"];
					format_pk.value = data["format_pk"];
					producte.value = data["producte"];
					producte_pk.value = data["producte_pk"];
					cantitat.value = data["cantitat"];

					$.post("/nodecalc/", $(".comanda2_form").serializeArray(), function (data) {
						var dataentrega = document.getElementById("dataentrega");

						var i = 0;

						dataentrega.options.length = 0;

						var t;

						data.forEach(function (arrayItem) {
							t = arrayItem.dia + " " + arrayItem.date;
							dataentrega.options[i] = new Option(t, arrayItem.pk);
							i++;
						});

						$.post("/franjacalc/", $(".comanda2_form").serializeArray(), function(data) {

                        var franjes = document.getElementById("franjes");
                        var franjes_label = document.getElementById("franjes_label")


                        var i = 0;

                        franjes.options.length=0

                        var s;

                        if (data.constructor == Array){
                            data.forEach( function (arrayItem)
                            {
                                s = arrayItem.inici + "-" + arrayItem.final;
                                franjes.options[i] = new Option(s, arrayItem.pk)
                                i++;
                            });
                            franjes.style.display = 'block'
                            franjes_label.style.display = 'block'
                        } else{
                            franjes.style.display = 'none'
                            franjes_label.style.display = 'none'
                        }




                    });




					});




		}
		});
	});


// Get the <span> element that closes the modal
	$(".close").click(function(e)
	{
		var modal = document.getElementById('myModal');
    	modal.style.display = "none";
	});

	$(".modif_contracte").click(function(e){

		$(".comanda_form").submit();

	})

	$(".comanda2_form").submit(function(e)
			{
				e.preventDefault();
				var dataentrega = document.getElementById("dataentrega");
				var franjes = document.getElementById("franjes");
				var modal = document.getElementById('myModal');
//				var numcom = document.getElementById('notification_count')
				var check1 = document.getElementById('check1');
				var check2 = document.getElementById('check2');
				if ((dataentrega.value == "")||(franjes.value == "")){
					if (dataentrega.value == ""){
					check1.style.display = "block"}else{
					check1.style.display = "none"
					if (franjes.value == ""){
						check2.style.display = "block"}else{
					check2.style.display = "none"}}
                    //call = "Completa els camps 'Data d'entrega' i 'Franja Horària' si us plau";
				    //CallNotification(call ,"warning");
				}
				else{
                    $.post("/comanda/", $(this).serializeArray(),
					  function(data) {

						  modal.style.display = "none";

//						  if ( data["contracte"] == 1) {
//							  url = "/dies_entrega/" + data["pk"] + "/0";
//							  location = url;
//
//						  }else {
//							  location.reload()
                              $.post("/numcomandes/", $(this).serializeArray(), function(data){
                                    $('#auxcomandes').html(data);
                                });
                              $.post("/numcomandespro/", $(this).serializeArray(), function(data){
                                    $('#auxcomandespro').html(data);
                                });
//                              $.post("/usercorner/", $(this).serializeArray(), function(data){
//                                    $('#userCorner').html();
//                                });

//                                $.ajax({
//                                  url: '{% url 'myview' %}',
//                                  success: function(data) {
//                                  $('#notification_count').html();
//                                  }
//                                });
                              if (data["success"] == 1){
                                  call = "El producte s'ha afegit a la cistella"
                                  CallNotification(call,"success")
							  }else{
                                  call = "NO està disponible la quantitat sol·licitada"
                                  CallNotification(call,"error")
							  }
//						  }
								});
				}
	});



	 //   $(".register_user_form").submit(function(e){
    //    e.preventDefault();
    //    $.post("/nodesave/", $(this).serializeArray(), function(data) {
    //    });
    //});




    $('.lloc_entrega').change(function (e) {



//		var carrer = document.getElementById('carrer');
//		var numero = document.getElementById('numero');
//		var pis = document.getElementById('pis')
//		var poblacio = document.getElementById('poblacio');
//
//		$.post("/domicili/", $(this).serializeArray(),
//			function (data) {
//				if ( data["a_domicili"] == true){
//					carrer.readOnly = false;
//					numero.readOnly = false;
//					pis.readOnly = false;
//					poblacio.readOnly = true;
//				}else{
//					carrer.readOnly = true;
//					numero.readOnly = true;
//					pis.readOnly = true;
//					poblacio.readOnly = true;
//				}
//				carrer.value = data["carrer"]
//				numero.value = data["numero"]
//				pis.value = data["pis"]
//				poblacio.value = data["poblacio"]
//				//$('#effect').show();
//			});

		$.post("/nodecalc/", $(".comanda2_form").serializeArray(), function(data) {
			var dataentrega = document.getElementById("dataentrega");
			var franjes = document.getElementById("franjes");
			var franjes_label = document.getElementById("franjes_label");
			var i = 1;
			dataentrega.options.length=0;
			franjes.options.length=0;
			franjes.style.display = "none"
			franjes_label.style.display = "none"
			//var data_info = document.getElementById("primera_entrega");
			//data_info.value = " ";
			var t;
			data.forEach( function (arrayItem)
			{
				t = arrayItem.dia + " " + arrayItem.date;
				dataentrega.options[i] = new Option(t, arrayItem.pk, false, false);
				i++;
			});
		});

		$.post("/freqcalc/", $(".comanda2_form").serializeArray(), function(data){
			var h = 0;
			var frequencia = document.getElementById("frequencia");
			frequencia.options.length=0;
			if (data.length > 1) {
                frequencia.style.display = "block";
                frequencia_label.style.display = "block";
                data.forEach( function (arrayItem)
                {
                    frequencia.options[h] = new Option(arrayItem.nom, arrayItem.num, false, false);
                    h++;
                });
            } else{
                    frequencia.style.display = "none";
                    frequencia_label.style.display = "none";
                    data.forEach( function (arrayItem)
                    {
                        frequencia.options[h] = new Option(arrayItem.nom, arrayItem.num, false, false);
                        h++;
                    });
                }


		});
    });

	$('.dataentrega').change(function (e){

		e.preventDefault();


		$.post("/franjacalc/", $(this).serializeArray(), function(data) {

			var franjes = document.getElementById("franjes");
			var franjes_label = document.getElementById("franjes_label")


			var i = 1;

			franjes.options.length=0

			if (data.constructor == Array){
				data.forEach( function (arrayItem)
				{
					var s = arrayItem.inici + "-" + arrayItem.final;
					franjes.options[i] = new Option(s, arrayItem.pk, false, true)
					i++;
				});
				franjes.style.display = 'block'
			    franjes_label.style.display = 'block'
			} else{
			    franjes.style.display = 'none'
			    franjes_label.style.display = 'none'
			}




		});

	});



	$('#cancelar').click(function(e){
		var modal = document.getElementById('myModal');
		modal.style.display = "none";
	})

});


//CSRF TOKEN FOR JS


// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

