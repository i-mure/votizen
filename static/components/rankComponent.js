// Register `rankList` component, along with its associated controller and template
const segmentColors = []
var randomColor = '#ffff'
angular.
  module('votizenApp').
  component('rankList', {
    template:
       `
     <div class="ui vertical stripe segment">
      <div class="ui middle aligned stackable grid container">
       <div class="ui celled list">
        <div class="ui red segment" ng-repeat="rank in ranks  | orderBy:'-payload.count' track by $index">
        <div id="cardcontent" class="ui content">
            <div class="labelholder"><a class="ui red circular label">{{rank.user.first_name}}</a></div>
            <div id="labelheader">{{rank.user.first_name}}</div>
        </div>
            <div class="stats"><span id="number">{{rank.payload.count}}</span>&nbsp;<span id="label">votes</span></div>
        </div>
        </div>
      </div>
    </div>
       `,
    controller:['fetchRank','$scope' ,function RankListController(fetchRank,$scope) {
          var $this =$scope;
          $this.ranks= fetchRank.query();
          console.log('Ranks:', $this.ranks);
    }]
  });