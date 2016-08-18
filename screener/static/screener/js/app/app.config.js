function questions($http){
	return $http.get('api/questions/').then(function(response) {
        return response.data;
    }, function(error){
  	  error['errorMsg'] = 'Failed to load questions!';
  	  return error;
    });
}

function categories($http){
    return $http.get('api/categories/').then(function(response) {
        return response.data;
    }, function(error){
	  error['errorMsg'] = 'Failed to load categories!';
	  return error;
  });	
}

function screens($http){
    return $http.get('api/screens/').then(function(response) {
        return response.data;
    }, function(error){
	    error['errorMsg'] = 'Failed to load screens!';
	    return error;
    });
}

function screen($http, $route){
    return $http.get('api/screens/'
    	       +$route.current.params.screenId+'/').then(function(response) {
       return response.data;
    }, function(error){
       error['errorMsg'] = 'Failed to load screen!';
       return error;
    });
}

function candidate($http, $route){
    return $http.get('api/candidates/'
    	       +$route.current.params.candidateId+'/').then(function(response) {
        return response.data;
    }, function(error){
	   error['errorMsg'] = 'Failed to load candidate!';
	   return error;
    });
}

angular.
  module('ScreenerApp').
  config(['$locationProvider', '$routeProvider',
    function config($locationProvider, $routeProvider) {
      $locationProvider.hashPrefix('!');
      $routeProvider.
        when('/questions', {
          templateUrl: window.STATIC_URL + 'screener/js/app/question/question-list.template.html',
          controller:"QuestionListController",
          resolve:{
        	  questions:function($http){
        		  return questions($http);
        	  }
          }
        }).
        when('/questions/add', {
            templateUrl: window.STATIC_URL + 'screener/js/app/question/question-add.template.html',
            controller:"QuestionAddController",
            resolve:{
          	  categories:function($http){
                  return categories($http);
          	  }
            }
        }).
        when('/questions/:questionId', {
          	templateUrl: window.STATIC_URL + 'screener/js/app/question/question-detail.template.html',
          	controller:"QuestionDetailController",
	        resolve:{
          	  categories:function($http){
          	      return categories($http);
              },
        	  question:function($http, $route){
      		      return $http.get('api/questions/'
      		    		  +$route.current.params.questionId+'/').then(function(response) {
                       return response.data;
      	          }, function(error){
      	    	       error['errorMsg'] = 'Failed to load question';
      	    	       return error;
      	          });
      	      }
	        }
        }).
        when('/categories', {
        	templateUrl: window.STATIC_URL + 'screener/js/app/category/category-list.template.html',
        	controller:"CategoryListController",
            resolve:{
        	  categories:function($http){
        		  return categories($http);
        	  }
            }
        }).
        when('/categories/add', {
        	template: '<category-add></category-add>'
        }).
        when('/categories/:categoryId', {
        	templateUrl: window.STATIC_URL + 'screener/js/app/category/category-detail.template.html',
        	controller:"CategoryDetailController",
            resolve:{
            	category:function($http, $route){
            		  return $http.get('api/categories/'
            				  +$route.current.params.categoryId+'/').then(function(response) {
                          return response.data;
            	      }, function(error){
            	    	  error['errorMsg'] = 'Failed to load category';
            	    	  return error;
            	      });
            	  }
            }
        }).
        when('/screens', {
            templateUrl: window.STATIC_URL + 'screener/js/app/screen/screen-list.template.html',
            controller:"ScreenListController",
            resolve:{
          	  screens:function($http){
          	      return screens($http);
          	  }
            }
        }).
        when('/screens/add', {
              templateUrl: window.STATIC_URL + 'screener/js/app/screen/screen-add.template.html',
              controller:"ScreenAddController",
              resolve:{
            	questions:function($http){
                    return questions($http);
            	}
              }
        }).
        when('/screens/:screenId', {
          	  templateUrl: window.STATIC_URL + 'screener/js/app/screen/screen-detail.template.html',
          	  controller:"ScreenDetailController",
              resolve:{
              	  questions:function($http){
              	      return questions($http);
                  },
            	  screen:function($http, $route){
          		      return screen($http, $route);
          	      },
            	  candidates:function($http, $route){
            		  return $http.get('api/candidates/?screen='
            				  +$route.current.params.screenId).then(function(response) {
                          return response.data;
            	      }, function(error){
            	    	  error['errorMsg'] = 'Failed to load candidates!';
            	    	  return error;
            	      });
            	  }
              }
        }).
        when('/candidates', {
              templateUrl: window.STATIC_URL + 'screener/js/app/candidate/candidate-list.template.html',
              controller:"CandidateListController",
              resolve:{
            	  candidates:function($http){
            		  return $http.get('api/candidates/').then(function(response) {
                          return response.data;
            	      }, function(error){
            	    	  error['errorMsg'] = 'Failed to load candidates!';
            	    	  return error;
            	      });
            	  }
              }  
        }).
        when('/candidates/add', {
              templateUrl: window.STATIC_URL + 'screener/js/app/candidate/candidate-add.template.html',
              controller:"CandidateAddController",
              resolve:{
          	    screens:function($http){
          		  return screens($http);
          	    }
              }
        }).
        when('/candidates/:candidateId', {
        	  templateUrl: window.STATIC_URL + 'screener/js/app/candidate/candidate-detail.template.html',
        	  controller:"CandidateDetailController",
              resolve:{
            	  candidate:function($http, $route){
            		  return candidate($http, $route);
                  },
          	      screens:function($http){
          		      return screens($http);
        	      }
              }
        }).
        when('/candidates/:candidateId/screens/:screenId', {
         	 templateUrl: window.STATIC_URL + 'screener/js/app/candidate/candidate-screen.template.html',
         	 controller:"CandidateScreenController",
             resolve:{
             	 candidate:function($http, $route){
             		 return candidate($http, $route);
                 },
           	     screen:function($http, $route){
           	         return screen($http, $route);
         	     },  
         	     answer_qualities:function($http){
         		      return $http.get('api/answerquality/').then(function(response) {
                          return response.data;
         	          }, function(error){
         	    	       error['errorMsg'] = 'Failed to load answer qualities!';
         	    	       return error;
         	          });
         	     },
         	     score:function($http, $route){
        		      return $http.get('api/screens/'+$route.current.params.screenId+'/score/?candidate='
        		    		  +$route.current.params.candidateId).then(function(response) {
                         return response.data;
        	          }, function(error){
        	    	       error['errorMsg'] = 'Failed to load candidate score!';
        	    	       return error;
        	          });
        	     }
             }
        }).
        otherwise('/questions');
    }
  ]);
