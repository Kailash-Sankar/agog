
app.controller('Questions', function($scope, $http, $rootScope, $timeout, jaximus) {
   $rootScope.qid = $('input[name="qid"]').val(); //default to zero
 });

console.log('hitting this');
app.controller('Answers', function($scope, $rootScope, $timeout, jaximus) {

  console.log('hitting this');

  //defaults
  $scope.answers = [];
  $scope.noa = 0;
  $scope.page = 1;
  $scope.addMode = false;
  $scope.new = {};


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
     $scope.noa =  Object.keys($scope.answers).length;	     
   })
    .error(function(data, status, headers, config) {
      console.log('something went wrong.')
    });

    jaximus.toastThis('Data loaded.');
  }

  //like an anwser
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

  //dislike an answer
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

  //toggle add new form
  $scope.toggleForm = function() {
    $scope.addMode = !$scope.addMode;
  };

  $scope.saveAnswer = function() {
      console.log('save',$scope.new);
      
      var url = '/question/' + $rootScope.qid + '/answer/save';
      $scope.new.qid = $rootScope.qid;
      jaximus.saveDataSet(url,$scope.new)
      .success(function(data, status, headers, config) {
        console.log(data);         
        
        //add the new answer    
        $scope.answers[data.aid] = data;

        //reset add form
        $scope.addMode = false;
        $scope.new = {};
        
        jaximus.toastThis('Answer Saved.');          
          
    })
    .error(function(data, status, headers, config) {
        jaximus.toastThis('Error. Please try again.');
        console.log('something went wrong.')
    });
    };

    $(window).load(function () {
      $('input[data-required],textarea[data-required]').attr('required', true);
    });


});
