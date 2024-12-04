import { initializeApp } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-app.js";
import { getAuth,
         GoogleAuthProvider,
         GithubAuthProvider } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-firestore.js";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBNmcyBXqUO8ZFFG_G1hsu8NEV11a5e2Jc",
  authDomain: "v52-tier3-team-30.firebaseapp.com",
  projectId: "v52-tier3-team-30",
  storageBucket: "v52-tier3-team-30.firebasestorage.app",
  messagingSenderId: "443358892905",
  appId: "1:443358892905:web:d3cf51373e3300290423f8"
};

  // Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();
const githubProvider = new GithubAuthProvider();

const db = getFirestore(app);

export { auth, provider, githubProvider, db };