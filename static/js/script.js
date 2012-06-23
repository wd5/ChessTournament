$(function () {
    $('.chtour-tounrnament').live('click', function () {
        var tournamentId = $(this).data('tournament-id');
        window.location = '/tournaments/' + tournamentId;
    });

    $('.chtour-tounrnament-toss').live('click', function () {
        var tournamentId = $(this).data('tournament-id');
        $.ajax({
            cache: true,
            dataType: "html",
            url: '/tournaments/' + tournamentId + '/toss',
            type: 'POST',
            beforeSend: function (jqXHR) {
                jqXHR.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
            },
            success: function (content) {
                window.location.reload();
            }
        });
    });

    $('.chtour-tournament-game').live('click', function () {
        var tournamentId = $(this).data('tournament-id');
        var gameId = $(this).data('game-id');
        window.location = '/tournaments/' + tournamentId + '/' + gameId;
    });

    $('.chtour-game-result').live('click', function () {
        var currentButton = $(this);
        if (currentButton.hasClass('disabled') || currentButton.hasClass('btn-success')) {
            return;
        }
        var tournamentId = currentButton.data('tournament-id');
        var gameId = currentButton.data('game-id');
        var gameResult = currentButton.data('game-result');
        var buttons = currentButton.parent().children('.chtour-game-result');
        var previousButton = currentButton.parent().children('.chtour-game-result.btn-success');

        buttons.removeClass('btn-success').addClass('disabled');
        currentButton.addClass('btn-success');

        $.ajax({
            cache: false,
            dataType: 'html',
            url: '/tournaments/' + tournamentId + '/' + gameId + '/' + gameResult,
            type: 'POST',
            beforeSend: function (jqXHR) {
                jqXHR.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
            },
            success: function () {
                window.location.reload();
            },
            error: function () {
                buttons.removeClass('btn-success').removeClass('disabled');
                previousButton.addClass('btn-success');
            }
        });
    });

    function initAjaxForm (loginForm) {
        var form = $('form', loginForm).ajaxForm({
            success: function (content) {
                var responseContent = $(content);
                if (responseContent.hasClass('chtour-login-success')) {
                    window.location.reload();
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
                window.location.reload();
            }
        });
        return false;
    });
});