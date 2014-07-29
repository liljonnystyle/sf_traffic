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
    var clusters = ['Normal Drivers', 'Aggressive Drivers', 'Google Maps Route'];
    var clus_id = ['norm','agg','goog'];
    var out = $('<div>').attr('width','300px');

    $('.driver-box').off('mouseenter');
    $('.driver-box').off('mouseleave');

    var driverLegend = $('<div>').attr('id', 'driver-legend');
    for (var i = 0; i < etas.length; i += 1) {
      var driverBox = $('<div>')
                          .addClass('driver-box')
                          .attr('data-cluster-id', clus_id[i]);
      
      var symbol = $('<div>')
                          .addClass('symbol')
                          .css('border-color', colors[i % 4]);
      
      // out += "<div class='symbol " + clus_id[i] + "' style='border: 6px solid " + colors[i%4] + ";'></div>"
      var legend = $('<div>')
                      .addClass('legend');
      var t1 = $('<p>').text(clusters[i]);
      // out += "<p class='legend'>" + clusters[i] + '</p>'
      var t2 = $('<p>').text('ETA: ' + etas[i] + ' Minutes');
      // out += "<p class='legend'>ETA: " + String(etas[i]) + ' Minutes</p>'
      legend.append([t1, t2]);

      driverBox.append([symbol, legend]);

      driverLegend.append(driverBox);
    }
    out.append(driverLegend);

    // out += "<h1></h1>" //empty header for spacing
    var driverImages = $('<div>');
    var title = $('<p>').text('ETA distributions:');

    var imageBox = $('<div>').attr('id', 'image-box');

    var imgUrls = ['static/norms0.png', 'static/norms1.png', 'static/norms2.png'];
    var ids = ['default', 'norm', 'agg'];
    for (i = 0; i < imgUrls.length; i += 1) {
      var img = $('<img>') 
                      .attr('src', imgUrls[i] + '?time=' + new Date().getTime())
                      .addClass('drive-distribution-img')
                      .attr('data-cluster-id', ids[i]);

      if (i != 0) {
        img.css('display', 'none');
      }

      imageBox.append(img);
    }
    var xlabel = $('<p>').text('ETA (minutes)')
                      .addClass('x-label');

    driverImages.append([title, imageBox, xlabel]);

    out.append(driverImages);

    $('#out-box').html(out);


    function showDriverGraph(graphID) {
      var id = graphID;

      if (id === 'goog') {
        return;
      }

      // hide all
      $('.drive-distribution-img').hide();

      // show right one
      $('.drive-distribution-img[data-cluster-id="' + id + '"]').show();
    }

    $('.driver-box').on('mouseenter', function (e) {
      var box = $(e.currentTarget);
      var id = box.attr('data-cluster-id')
      showDriverGraph(id);
      
    });

    $('.driver-box').on('mouseleave', function (e) {
      showDriverGraph('default');
    });
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
