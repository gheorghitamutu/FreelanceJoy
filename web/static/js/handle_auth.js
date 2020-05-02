'use strict';

// Your web app's Firebase configuration
var firebaseConfig = {
    apiKey: "AIzaSyBGSIJAtDKQWCW0_5CF1sf1xdVxPE_qwlY",
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
window.addEventListener('load', function () {
  document.getElementById('sign-out').onclick = function () {
    firebase.auth().signOut();
  };

  // FirebaseUI config.
  var uiConfig = {
    signInSuccessUrl: '/',
    signInOptions: [
      // Comment out any lines corresponding to providers you did not check in
      // the Firebase console.
      firebase.auth.GoogleAuthProvider.PROVIDER_ID,
      firebase.auth.EmailAuthProvider.PROVIDER_ID,
      //firebase.auth.FacebookAuthProvider.PROVIDER_ID,
      //firebase.auth.TwitterAuthProvider.PROVIDER_ID,
      //firebase.auth.GithubAuthProvider.PROVIDER_ID,
      //firebase.auth.PhoneAuthProvider.PROVIDER_ID

    ],
    // Terms of service url.
    tosUrl: '<your-tos-url>'
  };

  firebase.auth().onAuthStateChanged(function (user) {
    if (user) {
      // User is signed in, so display the "sign out" button and login info.
      document.getElementById('sign-out').style.display = 'block';
      document.getElementById('user-data').style.display = 'block';
      document.getElementById('sign-in-status').textContent = 'Signed in';
      document.getElementById('account-details').textContent = JSON.stringify(user, null, '  ');
      console.log(`Signed in as ${user.displayName} (${user.email})`);

      user.getIdToken().then(function (token) {
        // Add the token to the browser's cookies. The server will then be
        // able to verify the token against the API.
        // SECURITY NOTE: As cookies can easily be modified, only put the
        // token (which is verified server-side) in a cookie; do not add other
        // user information.
        document.cookie = "token=" + token;
      });

    } else {
      // User is signed out.
      // Initialize the FirebaseUI Widget using Firebase.
      var ui = new firebaseui.auth.AuthUI(firebase.auth());
      // Show the Firebase login button.
      ui.start('#firebaseui-auth-container', uiConfig);
      // Update the login state indicators.
      document.getElementById('sign-out').style.display = 'none';
      document.getElementById('user-data').style.display = 'none';
      document.getElementById('sign-in-status').textContent = 'Signed out';
      document.getElementById('account-details').textContent = '';
      // Clear the token cookie.
      document.cookie = "token=";
    }
  }, function (error) {
    console.log(error);
    alert('Unable to log in: ' + error)
  });
});
// [END gae_python37_auth_javascript]