var API_URL = 'https://api.buildnumber.io'

$().ready( function(){

    var token = $.url().param('token') || "6f2ee720c648ba30e36c43a5da8b95ac"
    $('.api-key').text(token)

    var $emailField = $('#email-field')
    var $signupButton = $('#signup-button')
    var $form = $('#signup-form')
    var $errorContainer = $('#signup-result .result-error')
    var $successContainer = $('#signup-result .result-success')

    $signupButton.ladda()

    $form.submit(function(ev) {
        ev.preventDefault()
        var email = $emailField.val()

        var regex = /^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/
        if (!regex.test(email)) {
            $errorContainer.text("Please enter a valid email address")
            $errorContainer.slideDown(300)
            return
        }

        $emailField.prop('disabled', true)
        $signupButton.ladda('start')
        $errorContainer.slideUp(300)
        $successContainer.slideUp(300)

        $.post({
            url: API_URL + '/accounts',
            contentType: 'application/json',
            data: JSON.stringify({ email: email })
        }).success(function(data) {
            var msg = "Your API token has been sent to " + email + ".<br>" +
                "Check your emails!"
            $successContainer.html(msg)
            $successContainer.slideDown(300)
        }).error(function(err) {
            var errorText = _.get(err, 'responseJSON.error', 'Something went wrong, please try again!')
            $errorContainer.text(errorText)
            $errorContainer.slideDown(300)
        }).always(function() {
            $emailField.prop('disabled', false)
            $signupButton.ladda('stop')
        })
    })
});
