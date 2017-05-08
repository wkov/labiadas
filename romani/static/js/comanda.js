jQuery(document).ready(function($)

    {


	$(".comanda_form").submit(function(e)
		{
		    e.preventDefault();
		    var btn = $("button", this);
		    var l_id = $(".hidden_id", this).val();
			var call = "Has afegit "+ this[5].value + " articles"
			var modal = document.getElementById('myModal');
			var preu = document.getElementById('preu');
			var llocentrega = document.getElementById('lloc_entrega');
			var format = document.getElementById('format');
			var format_pk = document.getElementById('format_pk');
			var producte = document.getElementById('producte');
			var producte_pk = document.getElementById('producte_pk');
			var cantitat = document.getElementById('cantitat_t');
			var imatge = document.getElementById('imatge');
			var frequencia = document.getElementById('frequencia');
			//var primera_entrega = document.getElementById('primera_entrega')

		$.post("/info/", $(this).serializeArray(),function(data){
			modal.style.display = "block";
			preu.value = data["preu"];
			format.value = data["format"];
			format_pk.value = data["format_pk"];
			producte.value = data["producte"];
			producte_pk.value = data["producte_pk"];
			cantitat.value = data["cantitat"];
			imatge.style.backgroundImage = 'url("' + data["imatge"] + '")';
			var j = 0;
			llocentrega.options.length=0;

			data["nodes"].forEach(function(arrayItem)
			{
				if(arrayItem.selected=="True"){
					s = arrayItem.nom + "/" + arrayItem.poblacio;
					llocentrega.options[j] = new Option(s, arrayItem.pk, false, true);
					//llocentrega.value = arrayItem.pk;
				}else{
					s = arrayItem.nom + "/" + arrayItem.poblacio;
					llocentrega.options[j] = new Option(s, arrayItem.pk, false, false);
					}
				j++;
			});
			j = 0;
			data["freqs"].forEach(function(arrayItem)
			{
					frequencia.options[j] = new Option(arrayItem.nom, arrayItem.num);
				j++;
					});


			$.post("/nodecalc/", $(".comanda2_form").serializeArray(), function(data) {
				var dataentrega = document.getElementById("dataentrega");
				var franjes = document.getElementById("franjes");

				var i = 1;

				dataentrega.options.length=0;
				franjes.options.length=0;

				var t;

				data.forEach( function (arrayItem)
				{
					t = arrayItem.dia + " " + arrayItem.date
					dataentrega.options[i] = new Option(t, arrayItem.pk, false, false)
					i++;
				});
			});

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

						  if ( data["contracte"] == 1) {
							  url = "/contracte/update/" + data["pk"];
							  location = url;
							  //call = "Has fet la comanda correctament"
							  //CallNotification(call,"success")
						  }else {
							  location.reload()
						  }
								});
				}
	});

	$('.lloc_entrega_perfil').change(function (e) {
		//Aqui filtrem les opcions a domicili. s'han d'afegir totes les noves
			var carrer = document.getElementById('carrer');
			var numero = document.getElementById('numero');
			var pis = document.getElementById('pis')
			var poblacio = document.getElementById('poblacio');
			var punt_lat = document.getElementById('punt_lat');
			var punt_lng = document.getElementById('punt_lng');
			var freq = document.getElementById('freq');
			$.post("/domicili/", $(this).serializeArray(),
				function (data) {
					if ( data["a_domicili"] == true){
						carrer.readOnly = false;
						numero.readOnly = false;
						pis.readOnly = false;
						poblacio.readOnly = true;
						punt_lat.readOnly = false;
						punt_lng.readOnly = false;
						carrer.disabled = false;
						numero.disabled = false;
						pis.disabled = false;
						punt_lat.disabled = false;
						punt_lng.disabled = false;
					}else{
						carrer.disabled = true;
						numero.disabled = true;
						pis.disabled = true;
						punt_lat.disabled = true;
						punt_lng.disabled = true;
					}
                	freq.innerHTML = data["frequencia"];
					carrer.value = data["carrer"];
					numero.value = data["numero"];
					pis.value = data["pis"];
					poblacio.value = data["poblacio"];
					lat = data["geopuntx_lat"];
					punt_lat.value = lat;
					if (data["geopuntx_lat"]){
					}else{
					punt_lat.placeholder = "clica en el mapa (opcional)";
					}
					lng = data["geopuntx_lng"];
					punt_lng.value = lng;
					if (data["geopuntx_lng"]){
					}else{
					punt_lng.placeholder = "clica en el mapa (opcional)";
					}
				});
			var acc = document.getElementById('accordion');
			$.post("/horari/", $(this).serializeArray(),
				function (data) {
					var j;
					var h;
					var b;
					var t = "";
					var g;
					data.forEach( function (arrayItemx){

						h = "<a>" + arrayItemx.dia + "</a>";
						g = "<div>"

						arrayItemx.franjes.forEach( function (arrayItem)
						{
							g = g + "&nbsp;" + arrayItem.inici + "-" + arrayItem.final + "<br/>";
						});
						t = t + h + g + "</div>";

					})

					t = t + "</div>";


                    //$('#accordion').innerHTML = t;
    				//$('#accordion').accordion("refresh");

					acc.innerHTML = t;

					$( "#accordion" ).accordion( "refresh" );
                    //
					//acc.accordion("refresh");

				})
	});

	    $(".register_user_form").submit(function(e){
        e.preventDefault();
        $.post("/nodesave/", $(this).serializeArray(), function(data) {
        });
    });

	    $(".lloc_entrega_reg").change(function(e){

        var carrer = document.getElementById('carrerx');
        var numero = document.getElementById('numerox');
        var pis = document.getElementById('pisx');
        var poblacio = document.getElementById('poblaciox');
        var punt_lat = document.getElementById('punt_latx');
        var punt_lng = document.getElementById('punt_lngx');
        var freq = document.getElementById('freq');
        $.post("/domicili/", $(this).serializeArray(),
            function (data) {
                if ( data["a_domicili"] == true){
                    carrer.readOnly = false;
                    numero.readOnly = false;
                    pis.readOnly = false;
                    poblacio.readOnly = true;
                    punt_lat.readOnly = false;
                    punt_lng.readOnly = false;
                    poblacio.value = data["poblacio"];
                    carrer.value = "";
                    numero.value = "";
                    pis.value = "";
                    punt_lat.value = "";
                    punt_lng.value = "";
                }else{
                    carrer.value = data["carrer"];
                    numero.value = data["numero"];
                    pis.value = data["pis"];
                    poblacio.value = data["poblacio"];
                    lat = data["geopuntx_lat"];
                    lng = data["geopuntx_lng"];
                    punt_lat.value = lat;
                    punt_lng.value = lng;
                    carrer.readOnly = true;
                    numero.readOnly = true;
                    pis.readOnly = true;
                    poblacio.readOnly = true;
                    punt_lat.readOnly = true;
                    punt_lng.readOnly = true;
                }
                freq.innerHTML = "(" + data["frequencia"] + ")";
            });
        var acc = document.getElementById('accordionx');
        $.post("/horari/", $(this).serializeArray(),
                function (data) {
                    var j;
                    var h;
                    var b;
                    var t = "";
                    var g;
                    data.forEach( function (arrayItemx){
                        h = arrayItemx.dia;
                        g = "<div>"
                        arrayItemx.franjes.forEach( function (arrayItem)
                        {
                            g = g + "&nbsp;" + arrayItem.inici + "-" + arrayItem.final + "<br/>";
                        });
                        t = t + h + g + "</div>";
                    })
                    t = t + "</div>";
                    acc.innerHTML = t;
					$( "#accordion" ).accordion( "refresh" );
            })
    });


    $('.lloc_entrega').change(function (e) {



		var carrer = document.getElementById('carrer');
		var numero = document.getElementById('numero');
		var pis = document.getElementById('pis')
		var poblacio = document.getElementById('poblacio');

		$.post("/domicili/", $(this).serializeArray(),
			function (data) {
				if ( data["a_domicili"] == true){
					carrer.readOnly = false;
					numero.readOnly = false;
					pis.readOnly = false;
					poblacio.readOnly = true;
				}else{
					carrer.readOnly = true;
					numero.readOnly = true;
					pis.readOnly = true;
					poblacio.readOnly = true;
				}
				carrer.value = data["carrer"]
				numero.value = data["numero"]
				pis.value = data["pis"]
				poblacio.value = data["poblacio"]
				//$('#effect').show();
			});

		$.post("/nodecalc/", $(".comanda2_form").serializeArray(), function(data) {
			var dataentrega = document.getElementById("dataentrega");
			var franjes = document.getElementById("franjes");
			var i = 1;
			dataentrega.options.length=0;
			franjes.options.length=0;
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
			data.forEach( function (arrayItem)
			{
				frequencia.options[h] = new Option(arrayItem.nom, arrayItem.num, false, false);
				h++;
			});
		});
    });

	$('.dataentrega').change(function (e){

		e.preventDefault();


		$.post("/franjacalc/", $(this).serializeArray(), function(data) {

			var franjes = document.getElementById("franjes");


			var i = 1;

			franjes.options.length=0
			//var data_info = document.getElementById("primera_entrega");
			//data_info.value = " ";

			if (data.constructor == Array){
				data.forEach( function (arrayItem)
				{
					var s = arrayItem.inici + "-" + arrayItem.final;
					franjes.options[i] = new Option(s, arrayItem.pk, false, false)
					i++;
				});
			}


		});

	});

	$('#avatar').change(function(e){
		var fotoavatar = document.getElementById('fotoavatar');
		fotoavatar.src = this.value;
	})

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

