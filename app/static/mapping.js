var JRoutingMapper = {
  updateMap: function (source, destination, time) {
    for (var i = 0; i < JRoutingMapper.lines.length; i += 1) {
      JRoutingMapper.lines[i].setMap(null)
    }
    JRoutingMapper.lines = []
  // Make request to /routing that responds with lat/long's for route
    $.ajax({
      url: 'routing',
      type: 'GET',
      data: {
        source: source,
        destination: destination,
        time: time
      },
      success: function (data) {
        // Update the line and symbol
        JRoutingMapper.map.setCenter({lat: data.lat, lng: data.lng})
        JRoutingMapper.map.setZoom(14)

        console.log(data)
        for (var i = 0; i < data.etas.length; i += 1) {
          JRoutingMapper.lines.push(JRoutingMapper.drawPolyline(data.points[i], data.etas[i], data.max_eta, i));
        };
        JRoutingMapper.writeOutput(data.etas);
      }
    })
  },

  drawPolyline: function (points, eta, max_eta, line_no) {
    var coords = [];

    for (var i = 0; i < points.length; i += 1) {
      coords.push(new google.maps.LatLng(points[i][0] + (line_no*0.00005) - 0.00005, points[i][1] + (line_no*0.00005) - 0.00005));
    }
    
    var colors = ['green', 'red', 'blue'];
    
    var symbol = {
      icon: {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 6,
        strokeColor: colors[line_no % colors.length]
      },
      offset: '100%'
    }

    // Create the polyline and add the symbol to it via the 'icons' property.
    var line = new google.maps.Polyline({
      path: coords,
      icons: [symbol],
      map: JRoutingMapper.map,
      strokeWeight: 4,
      strokeOpacity: 0.6,
      strokeColor: colors[line_no % colors.length]
    });

    JRoutingMapper.animateCircle(line, max_eta, eta);
    return line;
  },

  animateCircle: function (line, max_eta, eta) {
    var count = 0;
    window.setInterval(function() {
      count = (count + 1) % (max_eta * 105);
      // speed += 0.01;
      var icons = line.get('icons');
      if (count / eta >= 100) {
        icons[0].offset = '100%';
      } else {
        icons[0].offset = (count / eta) + '%';
      };
      line.set('icons', icons);
    }, 3);
  },

  writeOutput: function (etas) {
    var colors = ['green', 'red', 'blue'];
    var clusters = ['Normal Drivers', 'Aggressive Drivers', 'Google Maps Route']
    var out = ''
    for (var i = 0; i < etas.length; i += 1) {
      out += "<div class='symbol' style='border: 6px solid " + colors[i%4] + ";'></div>"
      out += "<p class='legend'>" + clusters[i] + '</p>'
      out += "<p class='legend'>ETA: " + String(etas[i]) + ' Minutes</p>'
    }
    out += "<p> </p>"
    out += "<p> </p>"
    out += "<p>ETA distributions (minutes):</p>"
    document.getElementById('out-box').innerHTML=out;
    
    var a0 = document.createElement("img");
    a0.src = "static/norms0.png";
    a0.height = 130;
    a0.style.visibility = 'visible';
    document.getElementById('out-box').appendChild(a0);

    var a1 = document.createElement("img");
    a1.src = "static/norms1.png";
    a1.height = 130;
    a1.style.visibility = 'hidden';
    document.getElementById('out-box').appendChild(a1);

    var a2 = document.createElement("img");
    a2.src = "static/norms2.png";
    a2.height = 130;
    a2.style.visibility = 'hidden';
    document.getElementById('out-box').appendChild(a2);
  },

// <p><div #symbol style='color': blue></div>5</p>

  initialize: function () {
    var mapOptions = {
      center: new google.maps.LatLng(37.7833, -122.4167),
      zoom: 13
    };

    JRoutingMapper.map = new google.maps.Map(document.getElementById('map-canvas'),
        mapOptions);
    JRoutingMapper.lines = []
    JRoutingMapper.directionsService = new google.maps.DirectionsService();

    // When user has submitted source and destination
    $('#nav-box').find('form').on('submit', function (e) {
      e.preventDefault();
      var target = $(e.target);
      var source = target.find('input[name="source"]').val();
      var destination = target.find('input[name="destination"]').val();
      var time = target.find('select').val();
      JRoutingMapper.updateMap(source, destination, time);
    })
  }
}

google.maps.event.addDomListener(window, 'load', JRoutingMapper.initialize);
