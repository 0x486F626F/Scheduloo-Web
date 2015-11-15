var scheduloo = angular.module("scheduloo", []);

scheduloo.config(['$httpProvider', function($httpProvider) {
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

scheduloo.controller('scheduloo-controller', ['$scope', '$http', function($scope, $http) {
	$scope.message = '';
	$scope.courses = [];
	$scope.sections = [];
    $scope.suggestions = [];
	$scope.add_course = function() {
        $scope.message = '';
		var course = {
			subject: new_course.subject.value,
			catalog: new_course.catalog.value
		};
		var toadd = true;
		for (i = 0; i < $scope.courses.length; i ++) {
			if (($scope.courses[i].subject == course.subject) &&
				($scope.courses[i].catalog == course.catalog)) {
				$scope.message = 'You already have this course!';
				toadd = false;
			}
		}
		if (toadd) {
			var result = $http({
				method: 'POST',
				url: '/',
				data: {
					command: 'check_course',
				course: course
				}
			});
			result.success(function(data, status, headers, config) {
				//$scope.message = data;
				if (data == 'True') {
					for (i = 0; i < $scope.courses.length; i ++) {
						if (($scope.courses[i].subject == course.subject) &&
							($scope.courses[i].catalog == course.catalog)) {
							$scope.message = 'You already have this course!';
							toadd = false;
						}
					}
					if(toadd) {
						$scope.courses.push(course);
					}
				}
                else {
                    $scope.message = 'This course is not offering';
                }
			});
			result.error(function(data, status, headers, config) {
                $scope.message = 'Connection Error';
			});
		}
	};
	$scope.drop_course = function($index) {
        $scope.message = '';
		$scope.courses.splice($index, 1);
	}
	$scope.step1_step2 = function() {
        $scope.message = '';
		var result = $http({
			method: 'POST',
			url: '/',
			data: {
				command: 'submit_course_list',
				course: $scope.courses
			}
		});
		result.success(function(data, status, headers, config) {
			var cnt = 0;
			$scope.sections = [];
			for (i = 0; i < data.length; i ++) {
				$scope.sections.push([]);
				for (j = 0; j < data[i].length; j ++) {
					$scope.sections[i].push([]);
					for (k = 0; k < data[i][j].length; k ++) {
						data[i][j][k] = $scope.courses[i].subject + ' ' + $scope.courses[i].catalog + ' ' + data[i][j][k];
						$scope.sections[i][j].push({
							name: data[i][j][k],
							id: 'rating_chart' + cnt.toString()
						});
						cnt = cnt + 1;
					}
				}
			}
		});
		result.error(function(data, status, headers, config) {
			$scope.message = 'Connection Error';
		});
	};
	$scope.search = function() {
        $scope.message = '';
		var ratings = [];
		var idx = 0;
		for (i = 0; i < $scope.sections.length; i ++) {
			ratings.push([]);
			for (j = 0; j < $scope.sections[i].length; j ++) {
				ratings[i].push([])
				for (k = 0; k < $scope.sections[i][j].length; k ++) {
					ratings[i][j].push(eval('rating_chart' + idx.toString()).rating.value);
					idx = idx + 1;
				}
			}
		}
		var result = $http({
			method: 'POST',
			url: '',
			data: {
				command: 'search',
				courses: $scope.courses,
				ratings: ratings
			}
		});
		result.success(function(data, status, headers, config) {
            $scope.suggestions = [];
			for(i = 0; i < data.length; i ++) {
                $scope.suggestions.push(data[i]['courses']);
            }
		});
        result.error(function(data, status, headers, config) {
            $scope.message = 'Connection Error';
        });
	};
}]);
