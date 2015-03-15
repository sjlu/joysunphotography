var projectsGenerator = require('./lib/projects');
var fs = require('fs');
var _ = require('lodash');

projectsGenerator(function(err, projects) {
  projects = _.filter(projects, function(p) {
    return !_.contains(['black_and_white'], p.canonical);
  })

  fs.writeFileSync('./build/projects.json', JSON.stringify(projects));
});