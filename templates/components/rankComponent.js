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
<div class="ui red segment" ng-repeat="rank in ranks  | orderBy:'-total' track by $index">
    <div id="cardcontent" class="ui content">
        <div class="labelholder"><a class="ui red circular label">{{rank.initials}}</a></div>
        <div id="labelheader">{{rank.teamname}}</div>
    </div>
        <div class="stats"><span id="number">{{rank.total}}</span>&nbsp;<span id="label">votes</span></div>
</div>
    </div>
  </div>
  </div>
       `,
    controller:['fetchRank','$scope' ,function RankListController(fetchRank,$scope) {
        // this.ranks= fetchRank.query()  --use it when api in ready
          var $this =$scope;
    //sample use case when fetched data arrives
        $this.ranks = [
    {   
        "email":"mfarm@gmail.com",
        "teamname":"Mfarm",
        "initials":"M",
        "total":9
    },
    {   
        "email":"votizen@gmail.com",
        "teamname":"Votizen",
        "initials":"V",
        "total":10
    }
     
]


    }]
  });