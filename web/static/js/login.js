'use strict';

// Your web app's Firebase configuration
var firebaseConfig = {
    apiKey: "AIzaSyDSrNzYnq4QWK8aijewDLptmC06LdA0V8Q",
    authDomain: "freelancejoy.firebaseapp.com",
    databaseURL: "https://freelancejoy.firebaseio.com",
    projectId: "freelancejoy",
    storageBucket: "freelancejoy.appspot.com",
    messagingSenderId: "927858267242",
    appId: "1:927858267242:web:7e0e0e8251af5d80ef2613",
    measurementId: "G-GZE64K9308"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);
firebase.analytics();

// [START gae_python37_auth_javascript]
window.addEventListener('load', function() {
    let sign_out = document.getElementById('sign-out');
    let sign_out_sidebar = document.getElementById('sign-out-sidebar');
    let user_data = document.getElementById('user-data');
    let sign_in_status = document.getElementById('sign-in-status');
    let account_details = document.getElementById('account-details');

    let logout = function() {
        firebase.auth().signOut();
        document.cookie = "token=";
        window.location.href = '/logout';
    }

    if (sign_out !== null) {
        sign_out.onclick = logout;
    }

    if (sign_out_sidebar !== null) {
        sign_out_sidebar.onclick = logout;
    }

    // FirebaseUI config.
    var uiConfig = {
        signInSuccessUrl: '/dashboard',
        signInOptions: [
            // Comment out any lines corresponding to providers you did not check in
            // the Firebase console.
            firebase.auth.GoogleAuthProvider.PROVIDER_ID,
            firebase.auth.EmailAuthProvider.PROVIDER_ID,
            // firebase.auth.FacebookAuthProvider.PROVIDER_ID,
            // firebase.auth.TwitterAuthProvider.PROVIDER_ID,
            // firebase.auth.GithubAuthProvider.PROVIDER_ID,
            firebase.auth.PhoneAuthProvider.PROVIDER_ID

        ],
        // Terms of service url.
        tosUrl: '<your-tos-url>'
    };

    firebase.auth().onAuthStateChanged(function(user) {

        console.log(`Cookie: ${document.cookie}`);
        console.log(`User: ${user}`);

        if (user) {
            if (user_data !== null) {
                user_data.style.display = 'block';
            }
            if (sign_in_status !== null) {
                sign_in_status.textContent = 'Signed in';
            }
            if (account_details !== null) {
                account_details.textContent = JSON.stringify(user, null, '  ');
            }

            console.log(`Signed in as ${user.displayName} (${user.email})`);

            user.getIdToken().then(function(token) {
                // Add the token to the browser's cookies. The server will then be
                // able to verify the token against the API.
                // SECURITY NOTE: As cookies can easily be modified, only put the
                // token (which is verified server-side) in a cookie; do not add other
                // user information.
                document.cookie = "token=" + token;
            });

        }
        else {
            try {
            // Initialize the FirebaseUI Widget using Firebase.
            var ui = new firebaseui.auth.AuthUI(firebase.auth());
            // Show the Firebase login button.
            ui.start('#firebaseui-auth-container', uiConfig);
            }
            catch(error) {
                console.log(error);
            }
            // Update the login state indicators.
            if (user_data !== null) {
                user_data.style.display = 'none';
            }
            if (sign_in_status !== null) {
                sign_in_status.textContent = 'Signed out';
            }
            if (account_details !== null) {
                account_details.textContent = '';
            }
            // Clear the token cookie.
            document.cookie = "token=";
        }
    }, function(error) {
        console.log(error);
        alert('Unable to log in: ' + error)
    });
});
// [END gae_python37_auth_javascript]