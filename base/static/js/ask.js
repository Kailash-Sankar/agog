
app.controller('ask', function($scope,$http) {
	   
    //question data structure
	$scope.q = {
		summary : '',
		description : '',
		tags : [],
	}
	
	//tag actions
	$scope.tags = [];
    $scope.loadTags = function(query) {
            return $http.get('/tags/'+ query);
     };

});

//onload set required fields
//workaround for mdl behavior
$(window).load(function () {
	$('input[data-required],textarea[data-required]').attr('required', true);
});

