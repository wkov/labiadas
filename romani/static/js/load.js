function addEvent(element, event, fn) {
    if (element.addEventListener) {
        element.addEventListener(event, fn, false);
    } else if (element.attachEvent) {
        element.attachEvent('on' + event, fn);
    }
}

//this function will work cross-browser for loading scripts asynchronously
function loadScript(src, callback) {
  var s,
      r,
      t;
  r = false;
  s = document.createElement('script');
  s.type = 'text/javascript';
  s.src = src;
  s.onload = s.onreadystatechange = function() {
    //console.log( this.readyState ); //uncomment this line to see which ready states are called.
    if ( !r && (!this.readyState || this.readyState == 'complete') )
    {
      r = true;
      if (callback !== undefined) {
        callback();
      }
    }
  };
  t = document.getElementsByTagName('script')[0];
  t.parentNode.insertBefore(s, t);
}

addEvent(window, 'load', function(){ loadScript('/static/js/jquery-2.1.4.js',
        function () { loadScript('/static/js/jquery-ui-1.11.4/jquery-ui.js',
        function () { loadScript('//cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/moment.min.js',
        function () { loadScript('/static/js/fullcalendar-3.4.0/fullcalendar.min.js',
        function () { loadScript('/static/js/tablesorter-master/jquery.tablesorter.js',
        function () { loadScript('/static/js/generic.js',
        //function () {
        //
        //    $("#datepicker").datepicker({dateFormat: 'dd/mm/yy'});
        //
        //     $("#datepicker2").datepicker({dateFormat: 'dd/mm/yy'});
        //
        //     $("#accordion").accordion();
        //
        //     $("#myTable").tablesorter({dateFormat: "uk"});
        //
        //     $("#myTable2").tablesorter({dateFormat: "uk"});
        //
        //
        //                 // delete message
        //    $('.del-msg').click(function(){
        //        $('.del-msg').parent().attr('style', 'display:none;');
        //    })
        //
        //     setTimeout(function() {
        //    $('.message').fadeOut('slow');
        //    }, 10000),
        function () { loadScript('/static/js/comanda.js' )}
        //}
        )}
        )}  )} )} )} )
});