var GoogleAuth;
var SCOPE = "https://www.googleapis.com/auth/youtube.readonly https://www.googleapis.com/auth/yt-analytics.readonly"
function handleClientLoad() {
    // Load the API's client and auth2 modules.
    // Call the initClient function after the modules load.
    gapi.load('client:auth2', initClient);
}

function initClient() {
    // In practice, your app can retrieve one or more discovery documents.
    var discoveryUrl = 'https://www.googleapis.com/discovery/v1/apis/youtubeAnalytics/v1/rest';

    // Initialize the gapi.client object, which app uses to make API requests.
    // Get API key and client ID from API Console.
    // 'scope' field specifies space-delimited list of access scopes.
    gapi.client.init({
        'apiKey': 'AIzaSyC7xh_rhfgg2i41NUCz9q-uBvKZr05ITVc',
        'clientId': '76722557587-o7cb6jusf0ucadvfbb4g2vk5chn6nf3b.apps.googleusercontent.com',
        'discoveryDocs': [discoveryUrl],
        'scope': SCOPE,
}).then(function () {
    GoogleAuth = gapi.auth2.getAuthInstance();

    // Listen for sign-in state changes.
    GoogleAuth.isSignedIn.listen(updateSigninStatus);

    // Call handleAuthClick function when user clicks on
    //      "Sign In/Authorize" button.
    $('#google-sign-in-or-out-button').click(function() {
        handleAuthClick();
    });
    // $('#revoke-access-button').click(function() {
    //     revokeAccess();
    // });
});
}

function handleAuthClick() {
if (GoogleAuth.isSignedIn.get()) {
    // User is authorized and has clicked "Sign out" button.
    GoogleAuth.signOut();
} else {
    // User is not signed in. Start Google auth flow.
    GoogleAuth.grantOfflineAccess().then((res) => {
        googleAuthCode = res.code
     });
}
}

function revokeAccess() {
    GoogleAuth.disconnect();
}

function setSigninStatus() {
    var user = GoogleAuth.currentUser.get();
    var isAuthorized = user.hasGrantedScopes(SCOPE);
    
    googleBtn = document.querySelector("#google-sign-in-or-out-button")
    googleBtnDelete = document.querySelector("#youtube-delete")
    youtubeIcon = document.querySelector("#youtube-icon")
    youtubeCancel = document.querySelector("#youtube-cancel")
    if (isAuthorized) {
        if (!googleBtn.classList.contains("activated")){
            googleBtn.classList.add("activated")
        }
        if (googleBtnDelete.classList.contains("d-none")){
            googleBtnDelete.classList.remove("d-none")
        }
        if (!youtubeIcon.classList.contains("activated-icon")){
            youtubeIcon.classList.add("activated-icon")
        }
        if (!youtubeCancel.classList.contains("activated-icon")){
            youtubeCancel.classList.add("activated-icon")
        }
        $('#youtube-button-text').html(user.getBasicProfile().getName());
        saveUserData(user)
    } else {
        if (googleBtn.classList.contains("activated")){
            googleBtn.classList.remove("activated")
        }
        if (!googleBtnDelete.classList.contains("d-none")){
            googleBtnDelete.classList.add("d-none")
        }
        if (youtubeIcon.classList.contains("activated-icon")){
            youtubeIcon.classList.remove("activated-icon")
        }
        if (youtubeCancel.classList.contains("activated-icon")){
            youtubeCancel.classList.remove("activated-icon")
        }
        $('#youtube-button-text').html("Connect YouTube");
        removeUserData()
    }
}

function updateSigninStatus() {
    setSigninStatus();
}

var googleConnected = false
var googleUser = null
var googleAuthCode = null

function saveUserData(user){
    googleConnected = true
    googleUser = user
}

function removeUserData(){
    googleConnected = false
    googleUser = null
}
