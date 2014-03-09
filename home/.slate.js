// Generated by CoffeeScript 1.6.2
(function() {
  var app, bind, cmd, defaults, direction, directions, key, obj, operations, _fn, _fn1, _i, _j, _k, _l, _len, _len1, _len2, _len3, _len4, _m, _ref, _ref1, _ref2, _ref3, _ref4, _ref5, _ref6, _ref7;

  bind = function(key, x) {
    return slate.bind("" + key + ":shift;ctrl;alt;cmd", x);
  };

  _ref = [['a', 'iTerm'], ['s', 'MacVim'], ['d', 'Google Chrome'], ['e', 'Spotify'], ['r', 'HipChat'], ['f', 'Xcode'], ['v', 'Clear'], ['b', 'Twitter']];
  _fn = function(app) {
    return bind(key, function() {
      return slate.shell("/usr/bin/open -a '" + app + "'");
    });
  };
  for (_i = 0, _len = _ref.length; _i < _len; _i++) {
    _ref1 = _ref[_i], key = _ref1[0], app = _ref1[1];
    _fn(app);
  }

  _ref2 = [['pad7', 'previous track'], ['pad8', 'playpause'], ['pad9', 'next track']];
  _fn1 = function(cmd) {
    return bind(key, function() {
      return slate.shell("/users/narf/bin/tell spotify to " + cmd);
    });
  };
  for (_j = 0, _len1 = _ref2.length; _j < _len1; _j++) {
    _ref3 = _ref2[_j], key = _ref3[0], cmd = _ref3[1];
    _fn1(cmd);
  }

  bind('z', slate.operation('hint', {
    characters: 'asdwqxcef'
  }));

  _ref4 = [['i', ['up', 'left']], ['o', ['up', 'right']], ['k', ['down', 'left']], ['l', ['down', 'right']]];
  for (_k = 0, _len2 = _ref4.length; _k < _len2; _k++) {
    _ref5 = _ref4[_k], key = _ref5[0], directions = _ref5[1];
    operations = [];
    for (_l = 0, _len3 = directions.length; _l < _len3; _l++) {
      direction = directions[_l];
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
      '1920x1200': {
        width: 6,
        height: 6
      },
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

  _ref6 = [
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
      'n', {
        height: 'screenSizeY / 2'
      }
    ]
  ];
  for (_m = 0, _len4 = _ref6.length; _m < _len4; _m++) {
    _ref7 = _ref6[_m], key = _ref7[0], obj = _ref7[1];
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
    var dockWidth, height, menuBarHeight, screenHeight, screenRect, screenWidth, thresholdHeight, thresholdWidth, width, _ref8;

    if (!win) {
      return;
    }
    screenRect = win.screen().rect();
    screenWidth = screenRect.width;
    screenHeight = screenRect.height;
    menuBarHeight = 22;
    dockWidth = 90;
    thresholdWidth = screenWidth - dockWidth;
    thresholdHeight = screenHeight - menuBarHeight;
    _ref8 = win.size(), width = _ref8.width, height = _ref8.height;
    win.doOperation(slate.operation('throw', {
      screen: (slate.screen().id() + 1) % 2
    }));
    return win.doOperation(slate.operation('move', {
      x: 'windowTopLeftX',
      y: 'windowTopLeftY',
      width: width >= thresholdWidth ? 'screenSizeX' : width,
      height: height >= thresholdHeight ? 'screenSizeY' : height
    }));
  });

}).call(this);
