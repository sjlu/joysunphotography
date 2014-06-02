var express = require('express');
var router = express.Router();

var projects = fs.readFileSync('./build/projects.json');

/* GET home page. */
router.get('/', function(req, res) {
  res.render('index', { projects: projects });
});

router.get('/project/:project', function(req, res) {
  var project = _.find(projects, function(project) {
    return project.canonical === req.params.project;
  });
  res.render('project', { project: project });
});

module.exports = router;
