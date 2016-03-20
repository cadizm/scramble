
var app = angular.module("Scramble", []);

app.controller("ScrambleController", function($scope, $http) {

    $scope.puzzle = '';
    $scope.solutions = [];
    $scope.semaphore = 1;
    $scope.btnSolveCss = '{' + [
        "'btn': 1",
        "'btn-danger': !puzzleValid()",
        "'btn-success': puzzleValid()",
        "'btn-warning': solvingPuzzle()",
    ].join() + '}';

    $scope.solutionCss = function(solution, index) {
        if (_.contains(solution.indices, index)) {
            return 'solution-' + _.indexOf(solution.indices, index);
        }
        return '';
    }

    $scope.puzzleValid = function() {
        return $scope.puzzle.match(/[a-zA-z]{16}/);
    }

    $scope.solvingPuzzle = function() {
        return $scope.semaphore != 1;
    }

    $scope.keypressSolve = function($event) {
        // 13 keyCode `enter/return'
        if ($event.keyCode != 13) {
            return;
        }
        $scope.clickSolve();
    };

    $scope.clickSolve = function() {
        if (!$scope.puzzleValid()) {
            return;
        }
        $('#btn-solve').focus();
        $scope.solve();
    };

    $scope.solve = function() {
        // already computing solution
        if (!$scope.semaphore) {
            return;
        }
        var config = {
            method: 'GET',
            url: '/solve/' + $scope.puzzle
        };
        $scope.semaphore--;
        var res = $http(config)
        .success(function(data, status, headers, config) {
            $scope.semaphore++;
            $scope.solutions = data.solutions;
        })
        .error(function(data, status, headers, config) {
            $scope.semaphore++;
        });
    };

    $scope.randomPuzzle = function() {
        var alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        var letters = _.map(_.range(16), function(n) {
            return alphabet[_.random(0, alphabet.length - 1)];
        });
        $scope.puzzle = letters.join('');
    }

});

// display grid/solutions
app.filter('cell', function() {
    return function(input, index) {
        return input[index];
    };
});

// from: https://gist.github.com/cage1016/5729339
app.directive('capitalize', function () {
    return {
        require: 'ngModel',
        link: function (scope, element, attrs, modelCtrl) {
            var capitalize = function (inputValue) {
                if (angular.isUndefined(inputValue)) {
                    return
                };
                var capitalized = inputValue.toUpperCase();
                if (capitalized !== inputValue) {
                    modelCtrl.$setViewValue(capitalized);
                    modelCtrl.$render();
                }
                return capitalized;
            }
            modelCtrl.$parsers.push(capitalize);
            capitalize(scope[attrs.ngModel]);  // capitalize initial value
        }
    };
});

$(function() {
    $('#input-puzzle').focus();
});
