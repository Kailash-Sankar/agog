// dashboard home page | ksankar 2016

//Trending Unanswered Questions Card
app.controller('trendingQuestions', function($scope, $http, $rootScope, $timeout, jaximus) {
  
  loadTrending();  

  //indicate when new data is ready
  $scope.newDataAvailable = false;

 //load trending questions
  function loadTrending() {    	   
  	jaximus.loadDataSet('/trending/questions')
	.success(function(data, status, headers, config) {
    	console.log(data);
      	$scope.trendingItems = data;      				
    })
    .error(function(data, status, headers, config) {
     	console.log('something went wrong.')
    });

    jaximus.toastThis('Data loaded from browser storage.');
  }
 
});

//Trending Answered Questions
app.controller('trendingAnswers', function($scope, $http, $rootScope, $timeout, jaximus) {
  
  loadTrending();  

  //indicate when new data is ready
  $scope.newDataAvailable = false;

 //load trending questions
  function loadTrending() {    	   
  	jaximus.loadDataSet('/trending/answers')
	.success(function(data, status, headers, config) {
    	console.log(data);
      	$scope.trendingItems = data;      				
    })
    .error(function(data, status, headers, config) {
     	console.log('something went wrong.')
    });

    jaximus.toastThis('Data loaded from browser storage.');
  }
});
  
//My Questions
app.controller('myQuestions', function($scope, $http, $rootScope, $timeout, jaximus) {
  
  //loadTrending();  

  //indicate when new data is ready
  $scope.newDataAvailable = false;

 //load trending questions
  function loadTrending() {        
    jaximus.loadDataSet('/trending/my')
  .success(function(data, status, headers, config) {
      console.log(data);
        $scope.trendingItems = data;              
    })
    .error(function(data, status, headers, config) {
      console.log('something went wrong.')
    });

    jaximus.toastThis('Data loaded from browser storage.');
  }
 
});

