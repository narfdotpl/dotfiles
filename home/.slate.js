// Generated by CoffeeScript 1.6.2
(function() {
  var app, bind, defaults, direction, directions, key, obj, operations, _fn, _i, _j, _k, _l, _len, _len1, _len2, _len3, _ref, _ref1, _ref2, _ref3, _ref4, _ref5;

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
    _ref1 = _ref[_i], key = _ref1[0], app = _ref1[1];
    _fn(app);
  }

  bind('z', slate.operation('hint', {
    characters: 'asdwqxcef'
  }));

  _ref2 = [['i', ['up', 'left']], ['o', ['up', 'right']], ['k', ['down', 'left']], ['l', ['down', 'right']]];
  for (_j = 0, _len1 = _ref2.length; _j < _len1; _j++) {
    _ref3 = _ref2[_j], key = _ref3[0], directions = _ref3[1];
    operations = [];
    for (_k = 0, _len2 = directions.length; _k < _len2; _k++) {
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

  _ref4 = [
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
  for (_l = 0, _len3 = _ref4.length; _l < _len3; _l++) {
    _ref5 = _ref4[_l], key = _ref5[0], obj = _ref5[1];
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
