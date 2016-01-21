var API_URL = 'https://api.buildnumber.io'

$().ready( function(){

    var $emailField = $('#email-field')
    var $signupButton = $('#signup-button')
    var $form = $('#signup-form')
    var $errorContainer = $('#signup-result .result-error')
    var $successContainer = $('#signup-result .result-success')

    $signupButton.ladda()

    $form.submit(function(ev) {
        ev.preventDefault()
        var email = $emailField.val()

        $emailField.prop('disabled', true)
        $signupButton.ladda('start')
        $errorContainer.slideUp(300)
        $successContainer.slideUp(300)

        $.post(API_URL + '/accounts', {
            email: email
        }).success(function(data) {
            var msg = "Your API token has been sent to " + email + ".<br>" +
                "Check your emails!"
            $successContainer.html(msg)
            $successContainer.slideDown(300)
        }).error(function(err) {
            $errorContainer.text(err)
            $errorContainer.slideDown(300)
        }).always(function() {
            $emailField.prop('disabled', false)
            $signupButton.ladda('stop')
        })
    })
});
