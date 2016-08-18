// Register components on the `category` module,
angular.
  module('category').
  component('categoryAdd', {
	  templateUrl: window.STATIC_URL + 'screener/js/app/category/category-add.template.html',
	  controller: function CategoryAddController($http, $scope) {
		  $scope.errors = [];
		  $scope.info = "-";
		  $scope.status = "info";
		  $scope.isBusy = false;
	      
	      $scope.addItem = function () {
	    	  $scope.isBusy = true;
	    	  $scope.errors = [];
	    	  $scope.info = "Adding category...";
	    	  $scope.status = "info";
	    	  $scope.category_errors = null;

	    	  var data = {
	    		'category':$scope.category 
	    	  }
	    	  
		      $http.post('api/categories/', data).then(function(response) {
		    	  $scope.info = "Category added successfully";
		    	  $scope.status = "success";
		    	  $scope.category = "";
		    	  $scope.isBusy = false;
		      }, function(error){
		    	  $scope.isBusy = false;
		    	  $scope.info = "-";
		    	  error['errorMsg'] = 'Failed to add category!';
				  $scope.category_errors = error.data;
		    	  $scope.errors.push(error);
		      });
	      } 
	  }	  
  });