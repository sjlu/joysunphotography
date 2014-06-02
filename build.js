var projectsGenerator = require('./lib/projects');
var fs = require('fs');

projectsGenerator(function(err, projects) {
  fs.writeFileSync('./build/projects.json', JSON.stringify(projects));
});