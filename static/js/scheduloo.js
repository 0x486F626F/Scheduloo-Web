var scheduloo = angular.module("scheduloo", []);

scheduloo.config(['$httpProvider', function($httpProvider) {
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

scheduloo.controller('scheduloo-controller', ['$scope', '$http', function($scope, $http) {
	$scope.message = '233';
	$scope.courses = [];
	$scope.add_course = function() {
		var course = {
			subject: new_course.subject.value,
			catalog: new_course.catalog.value
		};
		var result = $http({
			method: 'POST',
			url: '/',
			data: {
				command: 'check_course',
				course: course
			}
		});
		result.success(function(data, status, headers, config) {
			$scope.message = data;
			if (data == 'True') {
				$scope.courses.push(course);
			}
		});
		result.error(function(data, status, headers, config) {
		});
	};
	$scope.drop_course = function($index) {
		$scope.courses.splice($index, 1);
	}
	$scope.step1_step2 = function() {
		var result = $http({
			method: 'POST',
			url: '/',
			data: $scope.courses,
		});
		result.success(function(data, status, headers, config) {
			$scope.message = data;
			$scope.courses = [];
		});
		result.error(function(data, status, headers, config) {
			$scope.message = status;
		});
	}
}]);
