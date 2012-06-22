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

    $('.chtour-tounrnament-toss').live('click', function () {
        var tournamentId = $(this).data('tournament-id');
        $.ajax({
            cache: true,
            dataType: "html",
            url: '/tournaments/' + tournamentId + '/toss',
            success: function (content) {
                $('#main').empty().append(content);
                $('header .chtour-tounrnaments').parent().siblings().removeClass('active');
                $('header .chtour-tounrnaments').parent().addClass('active');
            }
        });
    });

    $('.chtour-tournament-game').live('click', function () {
        var gameId = $(this).data('game-id');
        $.ajax({
            cache: true,
            dataType: "html",
            url: '/games/' + gameId,
            success: function (content) {
                $('#main').empty().append(content);
            }
        });
    });

    $('.chtour-game-result').live('click', function () {
        var currentButton = $(this);
        if (currentButton.hasClass('disabled') || currentButton.hasClass('btn-success')) {
            return;
        }
        var gameId = currentButton.data('game-id');
        var gameResult = currentButton.data('game-result');
        var buttons = currentButton.parent().children('.chtour-game-result');
        var previousButton = currentButton.parent().children('.chtour-game-result.btn-success');

        buttons.removeClass('btn-success').addClass('disabled');
        currentButton.addClass('btn-success');

        $.ajax({
            cache: false,
            dataType: 'html',
            url: '/games/' + gameId + '/set-result/' + gameResult,
            success: function () {
                buttons.removeClass('disabled');
            },
            error: function () {
                buttons.removeClass('btn-success').removeClass('disabled');
                previousButton.addClass('btn-success');
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

    function initAjaxForm (loginForm) {
        var form = $('form', loginForm).ajaxForm({
            success: function (content) {
                var responseContent = $(content);
                if (responseContent.hasClass('chtour-login-success')) {
                    $('.chtour-permission').addClass('chtour-logged');
                    if (responseContent.hasClass('chtour-login-stuff')) {
                        $('.chtour-permission').addClass('chtour-logged-staff');
                    }
                    loginForm.modal('hide');
                } else {
                    loginForm.children().replaceWith(responseContent.children());
                    initAjaxForm(loginForm);
                }
            }
        });
        $('.chtour-login-button', loginForm).click(function () {
            form.submit();
        });
    }

    function initLoginForm (content) {
        $('.chtour-login-form').remove();
        var loginForm = $(content);
        initAjaxForm(loginForm);
        loginForm.modal();
    }

    $('.chtour-login').click(function () {
        $.ajax({
            cache: true,
            dataType: "html",
            url: '/accounts/login/',
            success: initLoginForm
        });
        return false;
    });

    $('.chtour-logout').click(function () {
        $.ajax({
            cache: true,
            dataType: "html",
            url: '/accounts/logout/',
            success: function () {
                $('.chtour-permission').removeClass('chtour-logged').removeClass('chtour-logged-staff');
            }
        });
        return false;
    });
});