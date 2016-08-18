// Define the `question` module
angular.module('question', ['ScreenerApp','ngRoute']).
controller('QuestionListController', function($scope, $http, questions) {
	  $scope.errors = [];
	  
	  if (questions['status']){
		  var error = questions;
		  $scope.errors.push(error);
		  questions = [];
	  }
      
	  $scope.questions = questions;
	  $scope.questions.count=$scope.questions.length;
	  
      $scope.removeItem = function (idx, id) {
    	  
    	  var ques = $scope.questions.splice(idx, 1)[0];
    	  $scope.questions.count=$scope.questions.length;
    	  
	      $http.delete('api/questions/'+ id + '/').then(function(response) {
	    	  
	      }, function(error){
	    	  error['errorMsg'] = 'Failed to delete ' + ques.question;
			  $scope.errors.push(error);
	    	  $scope.questions.splice(idx, 0, ques);
	    	  $scope.questions.count=$scope.questions.length;
	      });
      } 
      
})
.controller('QuestionAddController', 
		    function QuestionAddController($http, $scope, 
		    		                       categories) {
	  
	  $scope.setStatus = function(status, 
                                  info, 
                                  clear_errors=true){
	      if(clear_errors){
	    	  $scope.errors = [];  
	      }
		  $scope.info = info;
		  $scope.status = status;
      }
	  
	  if (categories['status']){
		  var error = categories;
		  $scope.errors.push(error);
		  categories = [];
	  }
	  
	  $scope.setStatus("info", "-");
	  $scope.isBusy = false;
	  $scope.category_list = categories;
      
      $scope.addItem = function () {
    	  $scope.isBusy = true;
    	  $scope.setStatus("info", "Adding question...");
    	  $scope.question_errors = null;
    	  
    	  var categories = [];
    	  for(idx in $scope.categories){
    		  categories.push({'category': $scope.categories[idx]});
    	  }
    	  
    	  var data = {
    		'question':$scope.question,
    		'reference_answer':$scope.reference_answer,
    		'categories':categories	  
    	  }
    	  
	      $http.post('api/questions/', data).then(function(response) {
	    	  $scope.setStatus("success", "Question added successfully.");
	    	  $scope.isBusy = false;
	    	  $scope.question = "";
	    	  $scope.reference_answer = "";
	    	  $scope.categories = "";
	      }, function(error){
	    	  $scope.isBusy = false;
	    	  $scope.setStatus("info", "-");
	    	  error['errorMsg'] = 'Failed to add question!';
			  $scope.question_errors = error.data;
	    	  $scope.errors.push(error);
	      });
      } 
  }).controller('QuestionDetailController', 
		         function CategoryDetailController($http, $scope, 
		        		                           $location, $timeout, 
		        		                           categories, question) {
	  
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
	  $scope.categories = [];
	  
	  if (categories['status']){
		  var error = categories;
		  $scope.errors.push(error);
		  $scope.category_list = [];
	  }else if(question['status']) { 
		  $scope.status_code = categories['status'];
	      var error = question;
	      $scope.errors.push(error);
	  }else{
		  $scope.category_list = categories;
		  $scope.question = question;
		  $scope.question.categories.forEach(function (val) {
			  $scope.categories.push(val.category);
		  });
		  $scope.question_name = question.question;
		  $scope.reference_answer = question.reference_answer;
	  }
	  
	  $scope.toggleEdit = function(){  
		  $scope.edit= !$scope.edit;
	  }
	  
	  $scope.editItem = function(){
		  $scope.isBusy = true;
    	  $scope.setStatus("info", "Updating question...");
    	  $scope.question_errors = null;
    	  
    	  var categories = [];
    	  for(idx in $scope.categories){
    		  categories.push({'category': $scope.categories[idx]});
    	  }
    	  
    	  var data = {
    		'question':$scope.question_name,
    		'reference_answer':$scope.reference_answer,
    		'categories':categories	  
    	  }
    	  
		  $http.put('api/questions/'+ $scope.question.pk + '/', data).then(function(response) {
	    	  $scope.setStatus("success", "Question updated successfully.");
	    	  $scope.question = response.data;
	    	  $scope.isBusy = false;
	    	  $scope.question_name = $scope.question.question;
	    	  $scope.reference_answer = $scope.question.reference_answer;
	    	  $scope.edit=false;
	    	  $scope.existing_category_ids = [];
	    	  $scope.categories = [];
			  $scope.question.categories.forEach(function (val) {
				  $scope.categories.push(val.category);
			  });
		  },
		  function(error){
			  $scope.setStatus("info", "-");
			  $scope.isBusy = false;
		      error['errorMsg'] = 'Failed to update question!';
			  $scope.question_errors = error.data;
			  $scope.errors.push(error);
		  });		  
	  }

      $scope.removeItem = function (id) {
    	  $scope.isBusy = true;
    	  $scope.setStatus("info", "Deleting...");

		  $http.delete('api/questions/'+ id + '/').then(function(response) {
			  //change route
			  $scope.isBusy = false;
	    	  $scope.setStatus("success", "Question deleted successfully.");
			  $timeout(function(){
				  $location.path( "/questions/" ); 
			  }, 300); //modal issues need to look into
			  
		  },
		  function(error){
			  $scope.setStatus("info", "-");
			  $scope.isBusy = false;
		      error['errorMsg'] = 'Failed to delete question!';
			  $scope.errors.push(error);
		  });
      } 
});