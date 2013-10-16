var Homepage;

Homepage = (function() {
  function Homepage() {
    var images = [];
    var viewport_height = $(window).height();

    var regen = function() {
      images = _.map($('.portfolio'), function(image) {
        var image_position = $(image).offset();
        var image_height = $(image).height();

        var image_top = image_position.top;
        var image_bottom = image_top + image_height;

        return {
          top: image_top,
          bottom: image_bottom,
          height: image_height,
          image: image
        }
      });

      viewport_height = $(window).height();
    };
    $(window).resize(_.debounce(regen, 250));
    $('.portfolio img').load(regen);

    var detect = function() {
      var window_top = $(window).scrollTop();
      var window_bottom = window_top + viewport_height;

      _.each(images, function(image) {
        var is_above = window_bottom < image.top && window_top < image.top;
        var is_below = image.bottom < window_top && image.bottom < window_bottom;
        if (is_above || is_below) {
          return $(image.image).removeClass('visible');
        }

        if (image.top > window_top && image.bottom < window_bottom) {
          return $(image.image).addClass('visible');
        }

        var top = window_top;
        var bottom = image.bottom;
        if (window_top < image.top) {
          top = image.top;
          bottom = window_bottom;
        }

        var viewed_height = bottom - top;
        if ((viewed_height / viewport_height) > 0.45) {
          return $(image.image).addClass('visible');
        }

        return $(image.image).removeClass('visible');
      });
    };
    $(window).scroll(_.throttle(detect, 100));
    $('.portfolio img').load(detect);
    detect();

  }

  return Homepage;
})();