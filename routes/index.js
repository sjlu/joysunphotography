var express = require('express');
var router = express.Router();
var fs = require('fs');
var _ = require('lodash');
var async = require('async');
var easyimage = require('easyimage');
var path = './public/images/projects';
var util = require('util');

var createLayout = function(images) {
  var layouts = [];
  var nums = [2, 3, 4];
  while(images.length) {
    var layout = {
      width: 0,
      height: 0,
      images: [],
      cssClass: null
    }

    var num = images.length;
    if (images.length > 3) {
      num = nums.shift();
    }

    var dims = [];
    var dimSum = { // lol
      width: 0,
      height: 0
    };
    for (var n = 0; n < num; n++) {
      var image = images.shift();

      layout.images.push(image);

      dims.push({
        width: image.width,
        height: image.height
      });

      dimSum.width += image.width
      dimSum.height += image.height
    }

    var dimKey = 'width';
    if (dimSum.height > dimSum.width) {
      dimSum = 'height';
    }

    var minDim = _.min(dims, function(dim) {
      return dim[dimKey];
    });
    layout.width = minDim.width;
    layout.height = minDim.height;

    layout.cssClass = 'col-md-' + (12 / layout.images.length);

    layouts.push(layout);
    nums.push(num);
  }

  return layouts;
};

var listProjects = function(cb) {
  // lookup directories
  fs.readdir(path, function(err, dirs) {
    // lookup files in each dir
    async.map(dirs, function(dir, cb) {
      var dirPath = path + "/" + dir
      fs.readdir(dirPath, function(err, files) {
        // take each file and process them
        // through our image processor.
        async.map(files, function(file, cb) {
          // read each file
          var filePath = dirPath + '/' + file;
          easyimage.info(filePath, function(err, info) {
            if (err) return cb(err);

            info.path = filePath;
            return cb(null, info);
          });
        }, function(err, files) {
          // all files processed need to create
          // our layout for each project from here.
          if (err) return cb(err);

          // struct
          var project = {
            path: dirPath,
            images: files,
            name: null,
            canonical: dir,
            layouts: []
          };

          project.name = dir.replace(/_/g, ' ').replace(' and ', ' & ').replace(/\w\S*/g, function(txt) {
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
          });

          // sep vert and horiz
          var v = [];
          var h = [];

          _.each(project.images, function(image) {
            if (image.width > image.height) {
              h.push(image);
            } else {
              v.push(image);
            }
          })

          var vl = createLayout(v);
          var hl = createLayout(h);

          var whichLayout = false;
          while(vl.length && hl.length) {
            if (whichLayout) {
              project.layouts.push(vl.shift());
            } else {
              project.layouts.push(hl.shift());
            }

            whichLayout = !whichLayout;
          }
          project.layouts = project.layouts.concat(vl, hl);

          cb(null, project); // to file async
        });
      });
    }, function(err, projects) {
      cb(null, projects);
    });
  });
}

var cachedProjects = null;
var retrieveAndCacheProjects = function(cb) {
  if (cachedProjects) {
    return cb(null, cachedProjects);
  }

  listProjects(function(err, projects) {
    if (err) return cb(err);
    cachedProjects = projects;
    cb(null, projects);
  });
}

/* GET home page. */
router.get('/', function(req, res) {
  retrieveAndCacheProjects(function(err, projects) {
    res.render('index', { projects: projects });
  })
});

router.get('/project/:project', function(req, res) {
  retrieveAndCacheProjects(function(err, projects) {
    var project = _.find(projects, function(project) {
      return project.canonical === req.params.project;
    })
    console.log(project);
    res.render('project', { project: project });
  });
});

retrieveAndCacheProjects(function() {
  console.info('Projects cached.');
});

module.exports = router;
