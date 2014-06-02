var express = require('express');
var router = express.Router();
var fs = require('fs');
var _ = require('lodash');

var projects = JSON.parse(fs.readFileSync('./build/projects.json', {
  encoding: 'utf-8'
}));

/* GET home page. */
router.get('/', function(req, res) {
  res.render('index', { projects: projects });
  console.log(projects);
});

router.get('/project/:project', function(req, res) {
  var project = _.find(projects, function(project) {
    return project.canonical === req.params.project;
  });
  res.render('project', { project: project });
});

module.exports = router;
