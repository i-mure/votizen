const  apiEndpoint = ' ./rank.json'

angular.
  module('votizenApp').
  factory('fetchRank', ['$resource',
    function($resource) {
      return $resource(apiEndpoint, {}, {
        query: {
          method: 'GET',
          isArray: true
        }
      });
    }
  ]);

 