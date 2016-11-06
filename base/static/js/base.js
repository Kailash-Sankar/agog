// Angular base app | ksankar 2016

var app = angular.module('dashboard', ['ngTagsInput']);

//ajax service
app.factory('jaximus', function ($http, $rootScope, $timeout) {
  return {

      //toast status messages
      toastThis : function(msg) {
        $rootScope.toast = {
         msg: msg,
         show: true
       };
       $timeout(function() {
         $rootScope.toast.show = false;
       },2000);
     },

      //loads a chunk of data
      loadDataSet : function(url) {
        return $http.get(url);   
      },

      //post actions
      likePost : function(type,id,like) {
        var req = {
          method: 'POST',
          url: '/' + type + '/' + id + '/like',          
          data: { 
            'like' : like, 
            //'csrfmiddlewaretoken' : $('input[name="csrfmiddlewaretoken"]').val()
          }
       };
       return $http(req);
     }   
   };
 });


// Material design lite isn't fine with dynamic reconstruction of pages.
// The mutation observer makes sure that all new fileds are registered with MDL
app.run(function($rootScope) {
  var mdlUpgradeDom = false;
  setInterval(function() {
    if (mdlUpgradeDom) {
      componentHandler.upgradeDom();
      mdlUpgradeDom = false;
    }
  }, 200);

  var observer = new MutationObserver(function() {
    mdlUpgradeDom = true;
  });
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
  /* support <= IE 10
  angular.element(document).bind('DOMNodeInserted', function(e) {
      mdlUpgradeDom = true;
  });
  */
  
  // globals
  $rootScope.bgClr = ['x0','x1','x2','x3','x4','x5'];
  
});


app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);