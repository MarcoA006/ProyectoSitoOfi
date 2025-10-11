
 

function ghost () {
  "use strict";

  // type 'buu' on your keyboard
  var key = [66,85,85];
  var ck = 0;
  var max = key.length;

  var ghost = function() {

    var shock = document.createElement('div');
    var img = new Image();
    img.src = data;
    img.style.pointerEvents = "none";
    img.style.width = '374px';
    img.style.height = '375px';
    img.style.transition = '6s all';
    img.style.position = 'fixed';
    img.style.right = '-374px';
    img.style.bottom = 'calc(-50% + 550px)'; 
    img.style.zIndex = 999999;

    document.body.appendChild(img);

    window.setTimeout(function(){
      img.style.right = 'calc(50% - 187px)';
    },50);

    window.setTimeout(function(){
      img.style.right = 'calc(100% + 375px)';
    }, 4300);
    window.setTimeout(function(){
      img.parentNode.removeChild(img);
    }, 7300);

  };

  var record = function(e) {

    if ( e.which === key[ck] ) {
      ck++;
    } else {
      ck = 0;
    }

    if ( ck >= max ) {
      ghost();
      ck = 0;
    }

  };

  var init = function(data) {

    document.addEventListener('keyup', record);

  };

  var data = "https://weichiachang.github.io/easter-eggs-mobile/images/ghost.gif"

  init(data)
}





function runningCat () {
  "use strict"

  // type 'mishi' on your keyboard
  let key = [77,73,83,72,73]
  // let key = [67] 
  let ck = 0
  let max = key.length

  let catRun = function () {

    var shock = document.createElement('div')
    var img = new Image()
    img.src = data
    img.style.pointerEvents = "none";
    img.style.width = '450px'
    img.style.height = '350px'
    img.style.transition = '6s all linear'
    img.style.position = 'fixed' 
    img.style.left = '-400px'
    img.style.bottom = 'calc(-50% + 500px)'
    img.style.zIndex = 999999

    document.body.appendChild(img)

    // window.setTimeout(function(){
    //   img.style.left = 'calc(50% - 200px)'
    // },50)

    window.setTimeout(function(){
      img.style.left = 'calc(100% + 500px)'
    }, 50)

    window.setTimeout(function(){
      img.parentNode.removeChild(img)
    }, 6000)

  }

  let record = function(e) {

    if ( e.which === key[ck] ) {
      ck++
    } else {
      ck = 0
    }

    if ( ck >= max ) {
      catRun()
      ck = 0
    }

  }

  let init = function (data) {
    document.addEventListener('keyup', record)
  }

  let data = 'https://weichiachang.github.io/easter-eggs-mobile/images/running-cat.gif'

  init(data)
}

function runningPikachu () {
  "use strict"

  // type 'pikapika' on your keyboard
  let key = [80,73,75,65,80,73,75,65]
  // let key = [80]
  let ck = 0
  let max = key.length

  let pikaRun = function () { 

    var shock = document.createElement('div')
    var img = new Image()
    img.src = data
    img.style.pointerEvents = "none";
    img.style.width = '450px'
    img.style.height = '350px'
    img.style.transition = '4s all'
    img.style.position = 'fixed'
    img.style.left = '-400px'
    img.style.bottom = 'calc(-50% + 520px)'
    img.style.zIndex = 999999

    document.body.appendChild(img)

    // window.setTimeout(function(){
    //   img.style.left = 'calc(50% - 200px)'
    // },50)

    window.setTimeout(function(){
      img.style.left = 'calc(100% + 500px)'
    }, 50)

    window.setTimeout(function(){
      img.parentNode.removeChild(img)
    }, 4300)

  }

  let record = function(e) {

    if ( e.which === key[ck] ) {
      ck++
    } else {
      ck = 0
    }

    if ( ck >= max ) {
      pikaRun()
      ck = 0
    }

  }

  let init = function (data) {
    document.addEventListener('keyup', record)
  }

  let data = 'https://weichiachang.github.io/easter-eggs-mobile/images/running-pikachu.gif'

  init(data)
}


function joker () {
  "use strict";

  // type 'joker' on your keyboard
  var key = [74,79,75,69,82];
  var ck = 0;
  var max = key.length;

  var joker = function() {

    var shock = document.createElement('div');
    var img = new Image();
    img.src = data;
    img.style.pointerEvents = "none";
    img.style.width = '374px';
    img.style.height = '375px';
    img.style.transition = '13s all';
    img.style.position = 'fixed';
    img.style.right = '-374px';
    img.style.bottom = 'calc(-50% + 520px)';
    img.style.zIndex = 999999;
 
    document.body.appendChild(img);

    window.setTimeout(function(){
      img.style.right = 'calc(100% + 500px)';
    }, 50);
 
    // window.setTimeout(function(){
    //   img.style.right = 'calc(100% + 375px)';
    // }, 4500);

    window.setTimeout(function(){
      img.parentNode.removeChild(img);
    }, 10300);

  };

  var record = function(e) {

    if ( e.which === key[ck] ) {
      ck++;
    } else {
      ck = 0;
    }

    if ( ck >= max ) {
      joker();
      ck = 0;
    }

  };

  var init = function(data) {

    document.addEventListener('keyup', record);

  };

  var data = "https://weichiachang.github.io/easter-eggs-mobile/images/joker.gif"

  init(data)
}

function mario () {
  "use strict"

  // type 'mariow' on your keyboard
  let key = [77,65,82,73,79,87]
  let ck = 0
  let max = key.length

  let mario = function () {

    var shock = document.createElement('div')
    var img = new Image()
    img.src = data
    img.style.pointerEvents = "none";
    img.style.width = '350px'
    img.style.height = '300px'
    img.style.transition = '6s all linear'
    img.style.position = 'fixed'
    img.style.left = '-400px'
    img.style.bottom = 'calc(-50% + 530px)'
    img.style.zIndex = 999999

    document.body.appendChild(img)

    // window.setTimeout(function(){
    //   img.style.left = 'calc(50% - 200px)'
    // },50)

    window.setTimeout(function(){
      img.style.left = 'calc(100% + 500px)'
    }, 50)

    window.setTimeout(function(){
      img.parentNode.removeChild(img)
    }, 6000)

  }

  let record = function(e) {

    if ( e.which === key[ck] ) {
      ck++
    } else {
      ck = 0
    }

    if ( ck >= max ) {
      mario()
      ck = 0
    }

  }

  let init = function (data) {
    document.addEventListener('keyup', record)
  }

  let data = 'https://weichiachang.github.io/easter-eggs-mobile/images/mario.gif'

  init(data)
}






function ufo () {
  "use strict";

  // type 'ufo' on your keyboard
  var key = [85,70,79];
  var ck = 0;
  var max = key.length;

  var ufo = function() {

    var shock = document.createElement('div');
    var img = new Image();
    img.src = data;
    img.style.pointerEvents = "none";
    img.style.width = '374px';
    img.style.height = '375px';
    img.style.transition = '13s all';
    img.style.position = 'fixed';
    img.style.right = '-374px';
    // img.style.bottom = 'calc(-50% + 280px)';
    img.style.top= '0px';
    img.style.zIndex = 999999;

    document.body.appendChild(img);

    window.setTimeout(function(){
      img.style.right = 'calc(100% + 500px)';
    }, 50);

    // window.setTimeout(function(){
    //   img.style.right = 'calc(100% + 375px)';
    // }, 4500);

    window.setTimeout(function(){
      img.parentNode.removeChild(img);
    }, 10300);

  };

  var record = function(e) {

    if ( e.which === key[ck] ) {
      ck++;
    } else {
      ck = 0;
    }

    if ( ck >= max ) {
      ufo();
      ck = 0;
    }

  };

  var init = function(data) {

    document.addEventListener('keyup', record);

  };

  var data = "https://weichiachang.github.io/easter-eggs-mobile/images/ufo.gif"
  init(data)
}




function thisisfine () {
  "use strict";
 
    // type 'odiacion' on your keyboard
    var key = [79,68,73,65,67,73,79,78]; 
    var ck = 0;
    var max = key.length;

    var hi = function() {

      var shock = document.createElement('div');
      var img = new Image;
      img.src = data;
      img.style.pointerEvents = "none";
      img.style.width = '480px';
      img.style.height = '266px';
      img.style.transition = '1s all';
      img.style.position = 'fixed';
      img.style.left = 'calc(50% - 300px)';
      img.style.bottom = '100px';
      img.style.zIndex = 999999; 

      document.body.appendChild(img);

      window.setTimeout(function(){
        img.style.bottom = '100px';
      },300);

      window.setTimeout(function(){
        img.style.bottom = '-300px';
      }, 2600); 
      window.setTimeout(function(){
        img.parentNode.removeChild(img);
      }, 3500); 
 
    };

    var record = function(e) {

      if ( e.which === key[ck] ) {
        ck++;
      } else {
        ck = 0;
      }

      if ( ck >= max ) {
        hi();
        ck = 0;
      }

    };

    var init = function(data) {
      document.addEventListener('keyup', record);
    };
 
    var data = 'https://i.giphy.com/media/2UCt7zbmsLoCXybx6t/giphy.webp';

    init(data);
}





function may4 () {
  "use strict";

  // type 'buu' on your keyboard
  var key = [77,65,89,52]; 
  var ck = 0;
  var max = key.length;

  var ghost = function() {

    var shock = document.createElement('div');
    var img = new Image();
    img.src = data;
    img.style.pointerEvents = "none";
    img.style.width = '174px';
    img.style.height = '175px';
    img.style.transition = '6s all';
    img.style.position = 'fixed';
    img.style.left = 'calc(50% - 300px)';
    img.style.bottom = '450px'; 
    img.style.zIndex = 999999; 

    document.body.appendChild(img); 
   
    window.setTimeout(function(){
	  img.style.left = 'calc(50% - 350px)';	
	  img.style.bottom = '350px';
	  img.style.width = '274px';
	  img.style.height = '275px';
    },50);
	
	window.setTimeout(function(){
	  img.style.left = 'calc(50% - 400px)';		
	  img.style.bottom = '250px';
	  img.style.width = '374px';
	  img.style.height = '375px';
    }, 3300);

    window.setTimeout(function(){
	  img.style.left = 'calc(50% - 450px)';
	  img.style.bottom = '150px';
	  img.style.width = '474px';
	  img.style.height = '475px';
    }, 4300);
    window.setTimeout(function(){
      img.parentNode.removeChild(img);
    }, 7300);

  };

  var record = function(e) {

    if ( e.which === key[ck] ) {
      ck++;
    } else {
      ck = 0;
    }

    if ( ck >= max ) {
      ghost();
      ck = 0; 
    }

  };

  var init = function(data) {

    document.addEventListener('keyup', record);

  };

  var data = "https://i.giphy.com/media/SmYqlOh9GtnuAe4SwB/giphy.webp"

  init(data)
}

 
ghost();//buu
thisisfine();//odiacion
ufo();//ufo
runningCat();//mishi
runningPikachu();//pikapika
mario();//mariow
joker();//joker 
may4();//may4
