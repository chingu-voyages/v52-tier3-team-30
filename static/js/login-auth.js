import {auth, githubProvider, provider} from "./firebase-config.js";

import { signInWithPopup } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-auth.js";



/* == UI - Elements == */
const signInWithGitHubButton = document.getElementById("sign-in-with-github-btn")
const signUpWithGitHubButton = document.getElementById("sign-up-with-github-btn")

const signInWithGoogleButtonEl = document.getElementById("sign-in-with-google-btn")
const signUpWithGoogleButtonEl = document.getElementById("sign-up-with-google-btn")

const errorMsgGoogleSignIn = document.getElementById("google-signin-error-message")
const errorMsgGitHubSignIn = document.getElementById("github-signin-error-message")



/* == UI - Event Listeners == */
if (signInWithGitHubButton) {
    signInWithGitHubButton.addEventListener("click", authSignInWithGitHub)
}

if (signInWithGoogleButtonEl) {
    signInWithGoogleButtonEl.addEventListener("click", authSignInWithGoogle)
}


if (signUpWithGoogleButtonEl) {
    signUpWithGoogleButtonEl.addEventListener("click", authSignUpWithGoogle)
}


if (signUpWithGitHubButton) {
    signUpWithGitHubButton.addEventListener("click", authSignUpWithGitHub)
}


/* === Main Code === */

/* = Functions - Firebase - Authentication = */
async function authSignInWithGitHub() {
    // Configure GitHub Auth provider with custom parameters
    provider.setCustomParameters({
        'prompt': 'select_account'
    });

    try {
        // Attempt to sign in with a popup and retrieve user data
        const result = await signInWithPopup(auth, githubProvider);

        // Check if the result or user object is undefined or null
        if (!result || !result.user) {
            throw new Error('Authentication failed: No user data returned.');
        }

        const user = result.user;
        const email = user.email;

        // Ensure the email is available in the user data
        if (!email) {
            throw new Error('Authentication failed: No email address returned.');
        }

        // Retrieve ID token for the user
        const idToken = await user.getIdToken();

        // Log in the user using the obtained ID token
        loginUser(user, idToken);

    } catch (error) {
        // Handle errors by logging and potentially updating the UI
        console.log(error, 'Error during sign-in with GitHub');
        errorMsgGoogleSignIn.style.display = 'none';
        errorMsgGitHubSignIn.style.display = 'block';
        errorMsgGitHubSignIn.innerHTML = error;
    }
}



// Function to create new account with Google auth - will also sign in existing users
async function authSignUpWithGitHub() {
    provider.setCustomParameters({
        'prompt': 'select_account'
    });

    try {
        const result = await signInWithPopup(auth, githubProvider);
        const user = result.user;
        const email = user.email;

        // Sign in user
        const idToken = await user.getIdToken();
        loginUser(user, idToken);
    } catch (error) {
        // The AuthCredential type that was used or other errors.
        console.log("Error during GitHub signup: ", error.message);
        // Handle error appropriately here, e.g., updating UI to show an error message
    }
}



// Function to sign in with Google authentication
async function authSignInWithGoogle() {
    // Configure Google Auth provider with custom parameters
    provider.setCustomParameters({
        'prompt': 'select_account'
    });

    try {
        // Attempt to sign in with a popup and retrieve user data
        const result = await signInWithPopup(auth, provider);

        // Check if the result or user object is undefined or null
        if (!result || !result.user) {
            throw new Error('Authentication failed: No user data returned.');
        }

        const user = result.user;
        const email = user.email;

        // Ensure the email is available in the user data
        if (!email) {
            throw new Error('Authentication failed: No email address returned.');
        }

        // Retrieve ID token for the user
        const idToken = await user.getIdToken();

        // Log in the user using the obtained ID token
        loginUser(user, idToken);

    } catch (error) {
        // Handle errors by logging and potentially updating the UI
        console.log(error, 'Error during sign-in with Google');
        errorMsgGoogleSignIn.style.display = 'block';
        errorMsgGitHubSignIn.style.display = 'none';
        errorMsgGoogleSignIn.innerHTML = error;
    }
}



// Function to create new account with Google auth - will also sign in existing users
async function authSignUpWithGoogle() {
    provider.setCustomParameters({
        'prompt': 'select_account'
    });

    try {
        const result = await signInWithPopup(auth, provider);
        const user = result.user;
        const email = user.email;

        // Sign in user
        const idToken = await user.getIdToken();
        loginUser(user, idToken);
    } catch (error) {
        // The AuthCredential type that was used or other errors.
        console.log("Error during Google signup: ", error.message);
        // Handle error appropriately here, e.g., updating UI to show an error message
    }
}


function loginUser(user, idToken) {
    fetch('/auth', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${idToken}`
        },
        credentials: 'same-origin'  // Ensures cookies are sent with the request
    }).then(response => {
        if (response.ok) {
            window.location.href = '/dashboard';
        } else {
            console.error('Failed to login');
            // Handle errors here
        }
    }).catch(error => {
        console.error('Error with Fetch operation: ', error);
    });
}

