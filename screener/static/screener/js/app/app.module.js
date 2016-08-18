var app = angular.module('ScreenerApp', [
  'ngRoute',
  'ngCookies',
  'question',
  'category',
  'screen',
  'candidate'
]);

app.controller('rootCtrl', function($scope, $location) {
	$scope.getActive = function (path) {
	    return ($location.path().substr(0, path.length) == path) ? 'ang-nav-active' : '';
    }
});

app.run(function($rootScope, $http, $cookies) {
    // CSRF token for Django
    $http.defaults.headers.common['X-CSRFToken'] = $cookies.get('csrftoken');

});
app.directive('loading', ['$rootScope',
                           function ($rootScope) {
    return {
    	template:"<div ng-if='isRouteLoading' class='loader'></div>",
        link: function (scope, element, attrs) {
        	
        	scope.isRouteLoading = false;
            
            $rootScope.$on('$routeChangeStart', function () {
            	scope.isRouteLoading = true;      
            });
            $rootScope.$on('$routeChangeSuccess', function () {
            	scope.isRouteLoading = false;
            });
            $rootScope.$on('$routeChangeError', function () {
            	scope.isRouteLoading = false;
            });
        }
    };
}]);
app.directive('busy', ['$rootScope',
                       function ($rootScope) {
   return {
   	template:"<div ng-class=\"{'spin': isBusy}\" class='busy'></div>",
       link: function (scope, element, attrs) {
       	
       	   scope.isBusy = false;
           
           $rootScope.$on('$routeChangeStart', function () {
        	   scope.isBusy = false;     
           });
           $rootScope.$on('$routeChangeSuccess', function () {
        	   scope.isBusy = false;
           });
           $rootScope.$on('$routeChangeError', function () {
        	   scope.isBusy = false;
           });
       }
   };
}]);
app.directive('modalConfirmDeleteDialog', function() {
	  return {
	    templateUrl: window.STATIC_URL + 'screener/js/app/confirm-modal.html', 
	    transclude: true, 
	    link: function(scope, element, attrs) {
	      scope.confirmDelete = function() {
	    	 if(scope.idx >= 0){
	    		 scope.removeItem(scope.idx, scope.id); 
	    	 }else{
	    		 scope.removeItem(scope.id);
	    	 }
	    	 
	      }
	      scope.confirmData = function(idx, id) {
		      scope.idx = idx;
		      scope.id = id;

		  }
	      scope.confirmDataNoIdx = function(id){
	    	  scope.id = id;
	      }
	    }
	  }
});
