// Generated by CoffeeScript 1.10.0
(function() {
  var app, bind, cmd, defaults, direction, directions, fn, fn1, i, j, k, key, l, len, len1, len2, len3, len4, m, obj, operations, ref, ref1, ref2, ref3, ref4, ref5, ref6, ref7;

  bind = function(key, x) {
    return slate.bind(key + ":shift;ctrl;alt;cmd", x);
  };

  ref = [['a', 'iTerm'], ['s', 'MacVim'], ['d', 'Google Chrome'], ['e', 'Spotify'], ['r', 'Messenger'], ['t', 'Slack'], ['f', 'Xcode'], ['x', 'Simulator'], ['c', 'Simulator'], ['v', 'Clear']];
  fn = function(app) {
    return bind(key, function() {
      return slate.shell("/usr/bin/open -a '" + app + "'");
    });
  };
  for (i = 0, len = ref.length; i < len; i++) {
    ref1 = ref[i], key = ref1[0], app = ref1[1];
    fn(app);
  }

  ref2 = [['pad7', 'previous track'], ['pad8', 'playpause'], ['pad9', 'next track']];
  fn1 = function(cmd) {
    return bind(key, function() {
      return slate.shell("/users/narf/bin/tell spotify to " + cmd);
    });
  };
  for (j = 0, len1 = ref2.length; j < len1; j++) {
    ref3 = ref2[j], key = ref3[0], cmd = ref3[1];
    fn1(cmd);
  }

  ref4 = [['i', ['up', 'left']], ['o', ['up', 'right']], ['k', ['down', 'left']], ['l', ['down', 'right']]];
  for (k = 0, len2 = ref4.length; k < len2; k++) {
    ref5 = ref4[k], key = ref5[0], directions = ref5[1];
    operations = [];
    for (l = 0, len3 = directions.length; l < len3; l++) {
      direction = directions[l];
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
      '2560x1440': {
        width: 8,
        height: 4
      },
      '1920x1200': {
        width: 6,
        height: 4
      },
      '1920x1080': {
        width: 6,
        height: 4
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

  ref6 = [
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
  for (m = 0, len4 = ref6.length; m < len4; m++) {
    ref7 = ref6[m], key = ref7[0], obj = ref7[1];
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
    var dockWidth, height, menuBarHeight, ref8, screenHeight, screenRect, screenWidth, thresholdHeight, thresholdWidth, width;
    if (!win) {
      return;
    }
    screenRect = win.screen().rect();
    screenWidth = screenRect.width;
    screenHeight = screenRect.height;
    menuBarHeight = 23;
    dockWidth = 90;
    thresholdWidth = screenWidth - dockWidth;
    thresholdHeight = screenHeight - menuBarHeight;
    ref8 = win.size(), width = ref8.width, height = ref8.height;
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
