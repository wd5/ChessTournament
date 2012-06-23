(function( $ ) {
    var menu = {};
    var defaults = {
        breadcrumb: '',
        content: '',
        getActiveStateItem: function (item) {
            return item;
        }
    };

    function switchMenuItem () {
        var item = menu[$(this).attr('href')];

        $.each(menu, function (index, item) {
            item.options.getActiveStateItem(item.menuItem).removeClass('active');
        });
        item.options.getActiveStateItem(item.menuItem).addClass('active');

        $.ajax({
            dataType: "html",
            type: 'POST',
            url: item.url,
            success: function (content) {
                item.contentItem.empty().append(content);
            }
        });

        return false;
    }

    $.fn.chtourNavigation = function(options) {
        var options = $.extend({}, defaults, options);
        this.each(function (index, item) {
            var url = $(item).attr('href');
            menu[url] = {
                options: options,
                menuItem: $(item),
                breadcrumbItem: $(options.breadcrumb),
                breadcrumbStack: [],
                contentItem: $(options.content),
                url: url
            };

            item = menu[url];
            item.menuItem.click(switchMenuItem).filter(function () {
                return item.options.getActiveStateItem(item.menuItem).hasClass('active');
            }).click();
        })


    };
})( jQuery );