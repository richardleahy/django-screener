angular.module('category', ['ScreenerApp','ngRoute']).
controller('CategoryListController', 
		    function CategoryListController($http, 
		                                    $scope, 
		                                    categories) {
	  $scope.errors = [];
	  
	  if (categories['status']){
		  var error = categories;
		  $scope.errors.push(error);
		  categories = [];
	  }
	  
	  $scope.category_list = categories;
	  $scope.category_list.count=$scope.category_list.length;
	
	  $scope.removeItem = function (idx, id) {
	  	  var cat = $scope.category_list.splice(idx, 1)[0];
	  	  $scope.category_list.count=$scope.category_list.length;
	  	  
		  $http.delete('api/categories/'+ id + '/').then(function(response) {
	  },
	  function(error){
	      error['errorMsg'] = 'Failed to delete ' + cat.category;
			  $scope.errors.push(error);
			  $scope.category_list.splice(idx, 0, cat);
			  $scope.category_list.count=$scope.category_list.length;
		  });
	  } 
})
.controller('CategoryDetailController', 
		     function CategoryDetailController($http, $scope, 
		    		                           $location, $timeout, 
		    		                           category) {
	
	  $scope.setStatus = function(status, 
			                      info, 
			                      clear_errors=true){
	      if(clear_errors){
	    	  $scope.errors = [];  
	      }
		  $scope.info = info;
		  $scope.status = status;
	  }
	  
	  $scope.setStatus("info", "-");
	  $scope.edit = false;
	  $scope.isBusy = false;

	  if (category['status']){
		  var error = category;
		  $scope.errors.push(error);
		  $scope.category = {};
		  $scope.status_code = category['status'];
	  }else{
		  $scope.category = category;
		  $scope.cat = $scope.category.category;
	  }
	  
	  $scope.toggleEdit = function(){
		  $scope.edit= !$scope.edit;
	  }
	  
	  $scope.editItem = function(){
		  $scope.isBusy = true;
		  $scope.setStatus("info", "Updating category...");
    	  $scope.category_errors = null;
    	  
    	  var data = {
  	          'category':$scope.cat
  	      }
    	  
		  $http.put('api/categories/'+ $scope.category.pk + '/', data).then(function(response) {
	    	  $scope.setStatus("success", "Category updated successfully.");
	    	  $scope.category = response.data;
	    	  $scope.isBusy = false;
	    	  $scope.cat = $scope.category.category;
	    	  $scope.edit=false;
		  },
		  function(error){
			  $scope.isBusy = false;
		      error['errorMsg'] = 'Failed to update category!';
			  $scope.category_errors = error.data.category;
	    	  $scope.setStatus("info", "-");
	    	  $scope.category_errors = error.data;
			  $scope.errors.push(error);  
		  });		  
	  }

      $scope.removeItem = function (id) {
    	  $scope.isBusy = true;
    	  $scope.setStatus("info", "Deleting...");

		  $http.delete('api/categories/'+ id + '/').then(function(response) {
			  //change route
			  $scope.isBusy = false;
	    	  $scope.setStatus("success", "Category deleted successfully.");
			  $timeout(function(){
				  $location.path( "/categories/" ); 
			  }, 300); //modal issues need to look into
			  
		  },
		  function(error){
			  $scope.setStatus("info", "-");
			  $scope.isBusy = false;
		      error['errorMsg'] = 'Failed to delete category!';
			  $scope.errors.push(error); 
		  });
      } 
});