var app = angular.module('myApp',['zingchart-angularjs']);

app.controller('MainController', function($scope, $http)
{
   url="/rest/getAllData"
   $http.get(url).success( function(response)
   {
   var excangeName = ['BITSTAMP', 'CEXIO', 'Arbitrag']
   var exchnage1 = [];
   var exchnage2 = [];
   var arbitrag = [];
   var startDate = response[0]['timestamp'];
        for (i=0; i< response.length; i++)
        {
          if (response[i]['exchange'] == excangeName[0])
             exchnage1.push(response[i]['last']);
          else if (response[i]['exchange'] == excangeName[1])
              exchnage2.push(response[i]['last']);
           if (i%2 && i>=2)
           {
                var value1 = response[i-2]['last'];
                var value2 = response[i-1]['last'];
                var arbitragValue = value1 - value2;
                arbitrag.push(arbitragValue);
           }

        }
        //$scope.myData = [exchnage1, exchnage2];

        $scope.myData = {
            type : 'line',

            title: {
                text: 'Compare prices Between Exchnages'
            },

           scaleY: {
                label: {
                    text: 'Price'
                  }
           },

           scaleX:{
            minValue: startDate,
            step: 60000,
            transform:{
              type: 'date',
              all: '%D, %d %M %Y<br>%h:%i %A',
              itemsOverlap: true,

              item: {
                backgroundColor: '#ffe6e6',
                fontColor: 'red'
              },
              guide: {
                alpha: 1,
                lineColor: 'red',
                lineWidth: 2,
                visible: true
              }
            },
            item: {
              fontSize: 10
            }
          },

            legend: {
                 'margin-right' : '150px',
                  'margin-top' : '200px',
                header : {
                    text: 'Exchanges',
                    'background-color': 'silver'
                }
            },

            series : [
               {
                    text: excangeName[0],
                    backgroundColor : 'navy',
                    values: exchnage1
                },
                {
                    text: excangeName[1],
                    values: exchnage2
                },

                {
                    text: excangeName[2],
                    values: arbitrag
                }

            ]
         }

   });
});