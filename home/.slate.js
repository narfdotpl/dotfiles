(function() {
  var app, bind, defaults, direction, directions, key, obj, operations, _fn, _i, _j, _k, _l, _len, _len2, _len3, _len4, _ref, _ref2, _ref3, _ref4, _ref5, _ref6;

  bind = function(key, x) {
    return slate.bind("" + key + ":shift;ctrl;alt;cmd", x);
  };

  _ref = [['a', 'iTerm'], ['s', 'MacVim'], ['d', 'Google Chrome'], ['e', 'Spotify'], ['r', 'HipChat'], ['f', 'Clear'], ['v', 'Twitter']];
  _fn = function(app) {
    return bind(key, function() {
      return slate.shell("/usr/bin/open -a '" + app + "'");
    });
  };
  for (_i = 0, _len = _ref.length; _i < _len; _i++) {
    _ref2 = _ref[_i], key = _ref2[0], app = _ref2[1];
    _fn(app);
  }

  bind('z', slate.operation('hint', {
    characters: 'asdwqxcef'
  }));

  _ref3 = [['i', ['up', 'left']], ['o', ['up', 'right']], ['k', ['down', 'left']], ['l', ['down', 'right']]];
  for (_j = 0, _len2 = _ref3.length; _j < _len2; _j++) {
    _ref4 = _ref3[_j], key = _ref4[0], directions = _ref4[1];
    operations = [];
    for (_k = 0, _len3 = directions.length; _k < _len3; _k++) {
      direction = directions[_k];
      operations.push([
        slate.operation('push', {
          direction: direction
        })
      ]);
    }
    bind(key, slate.operation('sequence', {
      operations: operations
    }));
  }

  bind('h', slate.operation('grid', {
    grids: {
      '1920x1080': {
        width: 6,
        height: 6
      },
      '1440x900': {
        width: 4,
        height: 4
      }
    }
  }));

  defaults = {
    x: 'windowTopLeftX',
    y: 'windowTopLeftY',
    width: 'windowSizeX',
    height: 'windowSizeY'
  };

  _ref5 = [
    [
      'y', {
        height: 'screenSizeY',
        y: 'screenOriginY'
      }
    ], [
      'g', {
        width: 'screenSizeX / 2'
      }
    ], [
      'j', {
        width: 'screenSizeX',
        x: 'screenOriginX'
      }
    ], [
      'b', {
        height: 'screenSizeY / 2'
      }
    ], [
      'n', {
        height: 'screenSizeY / 2'
      }
    ]
  ];
  for (_l = 0, _len4 = _ref5.length; _l < _len4; _l++) {
    _ref6 = _ref5[_l], key = _ref6[0], obj = _ref6[1];
    bind(key, slate.operation('move', _({}).extend(defaults, obj)));
  }

  slate["default"](['1920x1080', '1440x900'], slate.layout('foo', {
    Spotify: {
      operations: [
        slate.operation('move', {
          screen: 1,
          x: 'screenOriginX',
          y: 'screenOriginY',
          width: 'screenSizeX',
          height: 'screenSizeY'
        })
      ]
    }
  }));

  bind('m', function(win) {
    return win.doOperation(slate.operation('throw', {
      screen: (slate.screen().id() + 1) % 2
    }));
  });

}).call(this);
