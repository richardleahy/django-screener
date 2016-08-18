// Define the `candidate` module
angular.module('candidate', ['ScreenerApp','ngRoute']).
controller('CandidateListController', function($scope, $http, candidates) {
	  $scope.errors = [];
	  
	  if (candidates['status']){
		  var error = candidates;
		  $scope.errors.push(error);
		  candidates = [];
	  }

	  $scope.candidates = candidates;
	  $scope.candidates.count=$scope.candidates.length;

      $scope.removeItem = function (idx, id) {
    	  
    	  var candidate = $scope.candidates.splice(idx, 1)[0];
    	  $scope.candidates.count=$scope.candidates.length;
    	  
	      $http.delete('api/candidates/'+ id + '/').then(function(response) {
	    	  
	      }, function(error){
	    	  error['errorMsg'] = 'Failed to delete ' + candidate.first_name + ' ' + candidate.surname;
			  $scope.errors.push(error);
	    	  $scope.candidates.splice(idx, 0, ques);
	    	  $scope.candidates.count=$scope.candidates.length;
	      });
      }       
})
.controller('CandidateAddController', 
		     function QuestionAddController($http, $scope, screens) {
	
	  $scope.setStatus = function(status, 
                                  info, 
                                  clear_errors=true){
	      if(clear_errors){
		      $scope.errors = [];  
		  }
		  $scope.info = info;
		  $scope.status = status;
      }
	  
	  if (screens['status']){
		  var error = screens;
		  $scope.errors.push(error);
		  screens = [];
	  }else{
		  $scope.screen_list = screens;
	  }
	  
	  $scope.setStatus("info", "-");
	  $scope.isBusy = false;
      
      $scope.addItem = function () {
    	  $scope.candidate_errors = null;
    	  $scope.isBusy = true;
    	  $scope.setStatus("info", "Adding candidate...");

    	  var data = {
    		'first_name':$scope.candidate.first_name,
    		'surname':$scope.candidate.surname,
    		'screen':$scope.candidate.screen.url,
    		'email':$scope.candidate.email,
    		'tel':$scope.candidate.tel
    	  }
    	  
	      $http.post('api/candidates/', data).then(function(response) {
	    	  $scope.setStatus("success", "Candidate added successfully.");
	    	  $scope.isBusy = false;
	    	  $scope.candidate = {};
	      }, function(error){
	    	  $scope.setStatus("info", "-");
	    	  $scope.isBusy = false;
	    	  error['errorMsg'] = 'Failed to add candidate!';
			  $scope.candidate_errors = error.data;
	    	  $scope.errors.push(error);
	      });
      } 
})
.controller('CandidateDetailController', 
		         function CategoryDetailController($http, $scope, $location, 
		        		                           $timeout, candidate, screens) {
	  
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
	  $scope.screens = [];
	  
	  if (candidate['status']){
		  var error = candidate;
		  $scope.errors.push(error);
		  $scope.candidate = {};
		  $scope.status_code = candidate['status'];
	  }else if(screens['status']){
		  var error = screens;
		  $scope.errors.push(error);  
	  }else{
		  $scope.screens = screens;
		  $scope.candidate = candidate;
	  }

	  $scope.toggleEdit = function(){
		  $scope.edit= !$scope.edit;
	  }
	  
	  $scope.editItem = function(){
		  $scope.candidate_errors = null;
		  $scope.isBusy = true;
		  $scope.setStatus("info", "Updating candidate...");
    	  $scope.candidate_errors = null;
    	  
    	  var data = {
    	    'first_name':$scope.candidate.first_name,
    	    'surname':$scope.candidate.surname,
    		'screen':$scope.candidate.screen,
    		'email':$scope.candidate.email,
    		'tel':$scope.candidate.tel
    	  }
    	  
		  $http.put('api/candidates/'+$scope.candidate.pk + '/', data).then(function(response) {
	    	  $scope.setStatus("success", "Candidate updated successfully.");
	    	  $scope.candidate = response.data;
	    	  $scope.isBusy = false;
	    	  $scope.edit=false;
		  },
		  function(error){
			  $scope.setStatus("info", "-");
			  $scope.isBusy = false;
		      error['errorMsg'] = 'Failed to update candidate!';
		      $scope.candidate_errors = error.data;
			  $scope.errors.push(error);
		  });		  
	  }

      $scope.removeItem = function (id) {
    	  $scope.isBusy = true;
    	  $scope.setStatus("info", "Deleting...");

		  $http.delete('api/candidates/'+ id + '/').then(function(response) {
			  //change route
			  $scope.isBusy = false;
			  $scope.setStatus("success", "Candidate deleted successfully.");
			  $timeout(function(){
				  $location.path( "/candidates/" ); 
			  }, 300); //modal issues need to look into
			  
		  },
		  function(error){
			  $scope.setStatus("info", "-");
			  $scope.isBusy = false;
		      error['errorMsg'] = 'Failed to delete candidate!';
			  $scope.errors.push(error);
		  });
      } 
})
.controller('CandidateScreenController', 
		     function($scope, $http, 
		              candidate, screen, 
		              answer_qualities, score) {
	
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
	  
	  if (candidate['status']){
		  var error = candidate;
		  $scope.errors.push(error);
		  $scope.candidate = {};
		  $scope.status_code = candidate['status'];
	  }else if (screen['status']){
		  var error = screen;
		  $scope.errors.push(error);
		  $scope.screen = {};
	  }else if (answer_qualities['status']){
		  var error = answer_qualities;
		  $scope.errors.push(error);
		  $scope.answer_qualities = [];
	  }else if(score['status']){
		  var error = score;
		  $scope.errors.push(error);
	  }else{
		  $scope.candidate = candidate;
		  $scope.screen = screen;
		  $scope.questions = screen.questions;
		  $scope.question_idx = 0;
		  $scope.current_question = $scope.questions[$scope.question_idx];
		  $scope.answer_qualities = answer_qualities;
		  
		  $scope.score = score;
		  $scope.questions_answered = score.questions_answered;
		  
		  $http.get('api/answers/?question='+$scope.current_question.pk+'&candidate='+$scope.candidate.pk 
			        ).then(function(response) {
		      if(response.data.length > 0){
		    	  $scope.current_answer = response.data[0];
		      }else{
		    	  $scope.current_answer = {};
		      }
	      },
		  function(error){
	    	  $scope.setStatus("info", "-");
			  $scope.isBusy = false;
		      error['errorMsg'] = 'Failed to lookup answer!';
			  $scope.errors.push(error);		 
		  });
	  }
	  
	  $scope.nextQuestionReadonly = function(){
		  if($scope.question_idx + 1 < $scope.questions.length){
		      $scope.setStatus("warning", "Read-Only - Loading next question.");
	  	      $scope.isBusy = true;
	          $scope.question_idx += 1;
	          
			  var next_question = $scope.questions[$scope.question_idx];
			  $http.get('api/answers/?question='+next_question.pk+'&candidate='+$scope.candidate.pk 
		                ).then(function(response) {
		          if (response.data.length > 0){
		        	  $scope.current_answer = response.data[0];  		
		          }else{
		        	  $scope.current_answer = {};
		          }
		          
		          $scope.setStatus("warning", "Read-Only - Questions are not being saved.");
		          $scope.isBusy = false;
		          $scope.current_question = $scope.questions[$scope.question_idx];
		      }, function(error){
		    	  $scope.setStatus("warning", "Read-Only - Questions are not being saved.");
		          $scope.current_question = $scope.questions[$scope.question_idx];
		          $scope.isBusy = false;
			      error['errorMsg'] = 'Failed to lookup answer!';
				  $scope.errors.push(error);	
		      });		  
		  }
	  }
	  
	  $scope.prevQuestion = function(){
		  if($scope.question_idx - 1 >= 0){
			  $scope.setStatus("info", "Loading previous question.");
  	    	  $scope.isBusy = true;
			  var prev_question = $scope.questions[$scope.question_idx - 1];
			  $http.get('api/answers/?question='+prev_question.pk+'&candidate='+$scope.candidate.pk 
		                ).then(function(response) {
		          $scope.question_idx -= 1;
		          $scope.current_question = $scope.questions[$scope.question_idx];
		          if (response.data.length > 0){
		              $scope.current_answer = response.data[0];
		          }else{
		        	  $scope.current_answer = {};
		          }
		          $scope.isBusy = false;
		          $scope.info = "-";
		      });		  
		  }
	  }
      
      $scope.nextQuestion = function(){
    	  $scope.setStatus("info", "Saving answer...");
    	  
    	  var answer = {
    		  'question':$scope.current_question.pk,
              'answer':$scope.current_answer.answer,
        	  'answer_correct':$scope.current_answer.answer_correct,
        	  'answer_quality':$scope.current_answer.answer_quality,
        	  'user':$scope.candidate.user_pk,
        	  'candidate':$scope.candidate.pk
    	  }
    	  
		  $http.get('api/answers/?question='+$scope.current_question.pk+'&candidate='+$scope.candidate.pk 
			        ).then(function(response) {
	            if (response.data.length > 0){
	            	// existing record
	            	var existing_answer = response.data[0];
		      		$http.put('api/answers/'+existing_answer.pk+'/', 
		      			      answer).then(function(response) {
		      			  // Refresh score
            		      $http.get('api/screens/'+$scope.screen.pk+'/score/?candidate='
            		    		     +$scope.candidate.pk).then(function(response) {
                              $scope.score = response.data;
             	          });
		      			    	 
		      	    	  $scope.setStatus("success", "Answer updated successfully.");
		      	    	  $scope.isBusy = false;
		      	    	  $scope.edit=false;
		      			  if($scope.question_idx + 1 < $scope.questions.length){
		      				  $scope.question_idx += 1;
			      			  $scope.current_question = $scope.questions[$scope.question_idx];
			      			  $http.get('api/answers/?question='+$scope.current_question.pk+'&candidate='+$scope.candidate.pk 
						                ).then(function(response) {
				                  if (response.data.length > 0){
				                	  $scope.current_answer = response.data[0];
				                  }else{
				                	  $scope.current_answer = {};
				                  }
				              });
		      			  }
		      		},
		      		function(error){
		      	    	  $scope.setStatus("info", "-");
		      			  $scope.isBusy = false;
		      		      error['errorMsg'] = 'Failed to update answer!';
		      			  $scope.errors.push(error);
		      		});
	            }else{
	              // new record
	      		  $http.post('api/answers/', 
	      			         answer).then(function(response) {
	      	    	  $scope.setStatus("success", "Answer added successfully.");
	      	    	  $scope.isBusy = false;
	      	    	  $scope.edit=false;
	      	    	  
	      			  // Refresh score
        		      $http.get('api/screens/'+$scope.screen.pk+'/score/?candidate='
        		    		     +$scope.candidate.pk).then(function(response) {
                          $scope.score = response.data;
         	          });
	      	    	  
	      			  if($scope.question_idx + 1 < $scope.questions.length){
	      				  $scope.question_idx += 1;
		      			  $scope.current_question = $scope.questions[$scope.question_idx];
		      			  
		      			  $http.get('api/answers/?question='+$scope.current_question.pk+'&candidate='+$scope.candidate.pk 
			                        ).then(function(response) {
	                          if (response.data.length > 0){
	                	          $scope.current_answer = response.data[0];
	                          }else{
	                	          $scope.current_answer = {};
	                          }
	                      });
	      			  }
	      		  },
	      		  function(error){
	      			  $scope.setStatus("info", "-");
	      			  $scope.isBusy = false;
	      		      error['errorMsg'] = 'Failed to save answer!';
	      			  $scope.errors.push(error);
	      			  
	      		  });
	            }
		  },
		  function(error){
	    	  $scope.setStatus("info", "-");
			  $scope.isBusy = false;
		      error['errorMsg'] = 'Failed to lookup answer!';
			  $scope.errors.push(error);
			 
		  });
      }	  
});