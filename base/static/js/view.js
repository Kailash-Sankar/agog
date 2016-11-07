
app.controller('Questions', function($scope, $http, $rootScope, $timeout, jaximus) {
   $rootScope.qid = $('input[name="qid"]').val(); //default to zero


    loadQuestion();

    //load question for a qid
    function loadQuestion() {             
      var url = '/q/' + $rootScope.qid;    
      jaximus.loadDataSet(url)
      .success(function(data, status, headers, config) {
        console.log(data);
        $scope.q = data;                  
      })
      .error(function(data, status, headers, config) {
        console.log('something went wrong.')
      });

      jaximus.toastThis('Data loaded.');
    }

    //like a question
    $scope.like = function(qid) {
      console.log('like',qid);

      if( $scope.q.mylike == true ) {
        return;
      }

      $scope.q.likes += 1;

      jaximus.likePost('question',qid,true)
      .success(function(){
        $scope.q.mylike = true;  
      })
      .error(function(){
        $scope.q.likes -= 1;
      });
    }

    //dislike a question
    $scope.dislike = function(qid) {
      console.log('dislike',qid);

      if( $scope.q.mylike == false ) {
        return;
      }

      $scope.q.likes -= 1;

      jaximus.likePost('question',qid,false)
      .success(function(){
        $scope.q.mylike = false;
      })
      .error(function(){
        $scope.q.likes += 1;
      });
    }

});


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
      //undo my like
      do_dec(aid,null)
    }
    else if( $scope.answers[aid].mylike == false ) {
      //undo dislike and like this      
      do_inc(aid,null)
      do_inc(aid,true)
    }
    else {
      do_inc(aid,true);
    }
  
  }

  //dislike an answer
  $scope.dislike = function(aid) {
    console.log('dislike',aid);

    if( $scope.answers[aid].mylike == false ) {
      //undo my dislike
      do_inc(aid,null)
    }
    else if( $scope.answers[aid].mylike == true  ) {
      //undo like and dislike this
      do_dec(aid,null)
      do_dec(aid,false)
    }
    else {
      do_dec(aid,false);
    }
   
  }

  function do_inc(aid,bool) {
    $scope.answers[aid].likes += 1;
    
    jaximus.likePost('answer',aid,bool,$scope.answers[aid].mylike)
    .success(function(){
      $scope.answers[aid].mylike = bool;  
    })
    .error(function(){
      $scope.answers[aid].likes -= 1;
    });
  }

  function do_dec(aid,bool) {
     $scope.answers[aid].likes -= 1;

    jaximus.likePost('answer',aid,bool,$scope.answers[aid].mylike)
    .success(function(){
      $scope.answers[aid].mylike = bool;
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
