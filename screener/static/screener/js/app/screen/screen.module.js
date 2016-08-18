// Define the `screen` module
angular.module('screen', ['ScreenerApp','ngRoute']).
controller('ScreenListController', function($scope, $http, screens) {
	  $scope.errors = [];
	  
	  if (screens['status']){
		  var error = screens;
		  $scope.errors.push(error);
		  screens = [];
	  }

	  $scope.screens = screens;
	  $scope.screens.count=$scope.screens.length;
	  
      $scope.removeItem = function (idx, id) {
    	  var screen = $scope.screens.splice(idx, 1)[0];
    	  $scope.screens.count=$scope.screens.length;
    	  
	      $http.delete('api/screens/'+ id + '/').then(function(response) {
	    	  
	      }, function(error){
	    	  error['errorMsg'] = 'Failed to delete ' + screen.name;
			  $scope.errors.push(error);
	    	  $scope.screens.splice(idx, 0, screen);
	    	  $scope.screens.count=$scope.screens.length;
	      });
      } 
      
  }).controller('ScreenAddController', function ScreenAddController($http, $scope, $location,
		                                                            $timeout, questions) {
	  $scope.setStatus = function(status, 
                                  info, 
                                  clear_errors=true){
	      if(clear_errors){
		      $scope.errors = [];  
		  }
		  $scope.info = info;
		  $scope.status = status;
      }
	  
	  if (questions['status']){
		  var error = questions;
		  $scope.errors.push(error);
		  questions = [];
	  }
	  
	  $scope.setStatus("info", "-");
	  $scope.isBusy = false;
	  $scope.questions = questions;
	  $scope.selection = [];
	  
	  $scope.toggleSelection = function toggleSelection(questionName) {
	      var idx = $scope.selection.indexOf(questionName);
	      if (idx > -1) {
	          $scope.selection.splice(idx, 1);
	      }
	      else {
	          $scope.selection.push(questionName);
	      }
	  }
      
      $scope.addItem = function () {
    	  $scope.screen_errors = null;
    	  $scope.isBusy = true;
    	  $scope.setStatus("info", "Adding screen...");
    	  $scope.screen_errors = null;
    	  
    	  var questions = [];
    	  for(idx in $scope.selection){
    		  questions.push({'question': $scope.selection[idx]});
    	  }
    	  
    	  var data = {
    		'name':$scope.name,
    		'questions':questions
    	  }
    	  
	      $http.post('api/screens/', data).then(function(response) {
	    	  $scope.setStatus("success", "Screen added successfully.");
	    	  $scope.isBusy = false;
	    	  $scope.name = "";
	    	  $scope.selection = [];
			 // $timeout(function(){
			//	  $location.path("/screens/"+response.data.pk+ '/'); 
			//  }, 300); 
                        //modal issues need to look into
	      }, function(error){
	    	  $scope.isBusy = false;
	    	  $scope.setStatus("info", "-");
	    	  error['errorMsg'] = 'Failed to add screen!';
			  $scope.screen_errors = error.data;
			  console.log(error)
	    	  $scope.errors.push(error);
	      });
      } 
  }).controller('ScreenDetailController', 
		         function ($http, $scope, 
		                   $location, $timeout, 
		                   questions, screen,
		                   candidates) {
	  
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
	  $scope.status_code = null;
	  $scope.edit = false;
	  $scope.isBusy = false;
	  $scope.selection = [];
	  
	  if (questions['status']){
		  var error = questions;
		  $scope.errors.push(error);
	  }else if(screen['status']){
		  $scope.status_code = questions['status'];
		  var error = screen;
		  $scope.errors.push(error);
	  }else if(candidates['status']){
		  var error = candidates;
		  $scope.errors.push(error);
	  }else{
		  $scope.questions = questions;
		  $scope.screen = screen;
		  $scope.candidates = candidates;
		  for(idx in $scope.screen.questions){
			  $scope.selection.push($scope.screen.questions[idx]['question']);
		  }
	  }

	  $scope.toggleSelection = function toggleSelection(questionName) {
	      var idx = $scope.selection.indexOf(questionName);
	      if (idx > -1) {
	          $scope.selection.splice(idx, 1);
	      }
	      else {
	          $scope.selection.push(questionName);
	      }
	  }

	  $scope.toggleEdit = function(){
		  $scope.edit= !$scope.edit;
	  }
	  
	  $scope.editItem = function(){
		  $scope.isBusy = true;
		  $scope.setStatus("info", "Updating screen...");
    	  $scope.screen_errors = null;

    	  var questions = [];
    	  for(idx in $scope.selection){
    		  questions.push({'question': $scope.selection[idx]});
    	  }
    	  
    	  var data = {
    		'name':$scope.screen.name,
    		'questions':questions
    		
    	  }
    	  
		  $http.put('api/screens/'+ $scope.screen.pk + '/', data).then(function(response) {
	    	  $scope.setStatus("success", "Screen updated successfully.");
	    	  $scope.screen = response.data;
	    	  $scope.isBusy = false;
	    	  $scope.edit=false;
		  },
		  function(error){
			  $scope.setStatus("info", "-");
			  $scope.isBusy = false;
		      error['errorMsg'] = 'Failed to update screen!';
			  $scope.screen_errors = error.data;
			  $scope.errors.push(error);
		  });		  
	  }

      $scope.removeItem = function (id) {
    	  $scope.isBusy = true;
    	  $scope.setStatus("info", "Deleting...");

		  $http.delete('api/screens/'+ id + '/').then(function(response) {
			  //change route
			  $scope.isBusy = false;
			  $scope.setStatus("success", "Screen deleted successfully.");
			  $timeout(function(){
				  $location.path( "/screens/" ); 
			  }, 300); //modal issues need to look into
			  
		  },
		  function(error){
			  $scope.setStatus("info", "-");
			  $scope.isBusy = false;
		      error['errorMsg'] = 'Failed to delete screen!';
			  $scope.errors.push(error);
		  });
      } 
});