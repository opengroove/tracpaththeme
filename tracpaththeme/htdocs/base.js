jQuery(document).ready(function($) {
    var mainnav = $('#mainnav');
    if (mainnav.children('ul').length === 0) {
        return;
    }
    var banner = $('#banner');
    var bannerHeight = banner.height();
    var threshold = mainnav.offset().top;
    var mainnavHeight = bannerHeight - threshold;
    var d = document;
    var w = $(window);
    var listener = function() {
        var scrollTop = w.scrollTop();
        var active = null;
        var fix = scrollTop >= threshold;
        var fixed = banner.css('position') === 'fixed';
        var loose = 3;
        var vals = {};
        var need = false;
        var tmp;
        if (fix) {
            var height = mainnavHeight;
            tmp = d.activeElement;
            switch (tmp && tmp.tagName.toLowerCase()) {
            case 'input': case 'textarea': case 'select': case 'button':
                active = $(tmp);
                height = active[0].offsetHeight || active.height() || height;
                break;
            default:
                tmp = location.hash.substring(1);
                active = $(tmp ? d.getElementById(tmp) : null);
                while (active.length !== 0 &&
                       active.css('display') === 'inline')
                {
                    active = active.parent();
                }
                break;
            }
            var top = null;
            if (active.length !== 0) {
                tmp = active.offset().top - scrollTop;
                if (tmp - loose <= mainnavHeight && tmp + height + loose >= 0)
                {
                    top = (tmp - bannerHeight - loose) + 'px'
                }
            }
            if (top === null) {
                top = -threshold + 'px';
            }
            if (banner.css('top') !== top) {
                vals.top = top;
                need = true;
            }
            var left = -w.scrollLeft() + 'px';
            if (banner.css('left') !== left) {
                vals.left = left;
                need = true;
            }
        }
        if (fix !== fixed) {
            vals.position = fix ? 'fixed' : 'static';
            need = true;
        }
        if (need === true) {
            banner.css(vals);
        }
    };
    $(d).delegate('input, textarea, select, button', 'focus blur', listener);
    w.bind('scroll resize', listener);
});
