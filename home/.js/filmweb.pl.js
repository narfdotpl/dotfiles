// skip welcome screen
$('.welcomeScreenButton').click()

// facebook autologin
if ($('.userName').length == 0) {
    $('.btn-fb').click()
}
