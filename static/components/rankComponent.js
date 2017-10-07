// Register `rankList` component, along with its associated controller and template

angular.
  module('votizenApp').
  component('rankList', {
    template:
       `
     <div class="ui vertical stripe segment">
      <h1 style="text-align:center;padding-bottom:10px;">Bithub Results</h1>
      <br />
      <div class="ui middle aligned stackable grid container">
       <div class="ui celled list">
        <div class="ui red segment" ng-repeat="rank in ranks  | orderBy:'-payload.count' track by $index">
        <div id="cardcontent" class="ui content">
            <div class="labelholder"><a class="ui {{randomColor()}} circular label">{{rank.user.first_name | limitTo:2}}</a></div>
            <div id="labelheader">{{rank.user.first_name}}</div>
        </div>
            <div class="stats"><span id="number">{{rank.payload.count}}</span>&nbsp;<span id="label">votes</span>
                <span class="index header <red></red>"># - {{ $index+1 }}</span>
            </div>
        </div>
        </div>
      </div>
    </div>
       `,
    controller:['fetchRank','$scope' ,function RankListController(fetchRank,$scope) {
          $scope.colors = ['red', 'teal', 'purple', 'green', 'yellow', 'gray', 'pink', 'orange', 'olive', 'violet', 'gray', 'black'];
          $scope.randomColor = () => {
            return $scope.colors[Math.floor(Math.random() * $scope.colors.length)];
          };


          var $this =$scope;
          $this.ranks= fetchRank.query();
          console.log('Ranks:', $this.ranks);
    }]
  });