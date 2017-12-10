var app = angular.module('myApp',['zingchart-angularjs']);

app.controller('MainController', function($scope, $interval){
    $scope.myData=[0,1,1];

    $interval(function(){
        $scope.myData.push(Math.random() * 10);
    }, 1000);
});