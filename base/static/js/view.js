
app.controller('Questions', function($scope, $http, $rootScope, $timeout, jaximus) {
   $rootScope.qid = $('input[name="qid"]').val(); //default to zero
 });

console.log('hitting this');
app.controller('Answers', function($scope, $rootScope, $timeout, jaximus) {

  console.log('hitting this');
  $scope.answers = [];

  //first load
  $scope.page = 1;
  loadAnswers();  

  //indicate when new data is ready
  $scope.newDataAvailable = false;

  //load answers for a qid
  function loadAnswers() {        	   
    var url = $rootScope.qid + '/answers/' + $scope.page;    
    jaximus.loadDataSet(url)
    .success(function(data, status, headers, config) {
    	console.log(data);
     $scope.answers = data;      				
   })
    .error(function(data, status, headers, config) {
      console.log('something went wrong.')
    });

    jaximus.toastThis('Data loaded from browser storage.');
  }

  $scope.like = function(aid) {
    console.log('like',aid);

    if( $scope.answers[aid].mylike == true ) {
      return;
    }

    $scope.answers[aid].likes += 1;
    
    jaximus.likePost('answer',aid,true)
    .success(function(){
      $scope.answers[aid].mylike = true;  
    })
    .error(function(){
      $scope.answers[aid].likes -= 1;
    });
  }

  $scope.dislike = function(aid) {
    console.log('dislike',aid);

    if( $scope.answers[aid].mylike == false ) {
      return;
    }

    $scope.answers[aid].likes -= 1;

    jaximus.likePost('answer',aid,false)
    .success(function(){
      $scope.answers[aid].mylike = false;
    })
    .error(function(){
      $scope.answers[aid].likes += 1;
    });
  }

});
