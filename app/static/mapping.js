var JRoutingMapper = {
  updateMap: function (source, destination, time) {
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

        // JRoutingMapper.clearLines();

        for (var i = 0; i < data.etas.length; i += 1) {
          JRoutingMapper.drawPolyline(data.points[i], data.etas[i], i);
        }
        JRoutingMapper.writeOutput(data.etas);

        // var mapOptions = {
          
        //   zoom: 11
        // };
        JroutingMapper.map.mapOptions.zoom = 11
      }
    })
  },

  // TODO: Make sure you clear old polylines and symbols
  drawPolyline: function (points, eta, line_no) {
    var coords = [];
    for (var i = 0; i < points.length; i += 1) {
      coords.push(new google.maps.LatLng(points[i][0], points[i][1]));
    }
    
    var colors = ['blue', 'red', 'green', 'black'];
    
    var symbol = {
      icon: {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 5,
        strokeColor: colors[line_no % colors.length]
      },
      offset: '100%'
    }

    // Create the polyline and add the symbol to it via the 'icons' property.
    var line = new google.maps.Polyline({
      path: coords,
      icons: [symbol],
      map: JRoutingMapper.map
    });

    JRoutingMapper.animateCircle(line, eta);
  },

  animateCircle: function (line, eta) {
    var count = 0;
    window.setInterval(function() {
      count = (count + 1) % (eta * 100);
      // speed += 0.01;
      var icons = line.get('icons');
      icons[0].offset = (count / eta) + '%';
      line.set('icons', icons);
    }, 5);
  },

  writeOutput: function (etas) {
    var colors = ['blue', 'red', 'green', 'black'];
    var clusters = ['Aggressive Drivers', 'Normal Drivers', 'Slow Drivers', 'Google Maps Route']
    var out = ''
    for (var i = 0; i < etas.length; i += 1) {
      out += "<div class='symbol' style='border: 6px solid " + colors[i%4] + ";'></div>"
      out += '<p>' + clusters[i] + '</p>'
      out += '<p>ETA: ' + String(etas[i]) + ' Minutes</p>'
    }
    console.log(out)
    document.getElementById('out-box').innerHTML=out;
  },

// <p><div #symbol style='color': blue></div>5</p>

  initialize: function () {
    var mapOptions = {
      center: new google.maps.LatLng(37.7833, -122.4167),
      zoom: 13
    };

    JRoutingMapper.map = new google.maps.Map(document.getElementById('map-canvas'),
        mapOptions);

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
