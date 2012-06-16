$(function () {
    var homeData = $('#main').html();

    $('.chtour-home').live('click', function () {
        $('#main').empty().append(homeData);
        $('header .chtour-home').parent().siblings().removeClass('active');
        $('header .chtour-home').parent().addClass('active');
    });

    $('.chtour-tounrnaments').live('click', function () {
        $.ajax({
            cache: true,
            dataType: "html",
            url: '/tournaments',
            success: function (content) {
                $('#main').empty().append(content);
                $('header .chtour-tounrnaments').parent().siblings().removeClass('active');
                $('header .chtour-tounrnaments').parent().addClass('active');
            }
        });
    });


    $('.chtour-tounrnament').live('click', function () {
        var tournamentId = $(this).data('tournament-id');
        $.ajax({
            cache: true,
            dataType: "html",
            url: '/tournaments/' + tournamentId,
            success: function (content) {
                $('#main').empty().append(content);
                $('header .chtour-tounrnaments').parent().siblings().removeClass('active');
                $('header .chtour-tounrnaments').parent().addClass('active');
            }
        });
    });

    $('.chtour-players').live('click', function () {
        $.ajax({
            cache: true,
            dataType: "html",
            url: '/players',
            success: function (content) {
                $('#main').empty().append(content);
                $('header .chtour-players').parent().siblings().removeClass('active');
                $('header .chtour-players').parent().addClass('active');
            }
        });
    });
});