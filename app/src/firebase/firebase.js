// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from 'firebase/auth'; // Correct import for auth in Firebase 9+ version

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDN8yJU0zt8WyoqBIy1AwprtuXi7tbcnBk",
  authDomain: "ml-llm-280c9.firebaseapp.com",
  projectId: "ml-llm-280c9",
  storageBucket: "ml-llm-280c9.firebasestorage.app",
  messagingSenderId: "288547872180",
  appId: "1:288547872180:web:cb3394d8dc8610709fe6e1",
  measurementId: "G-989TYH9038"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
export {auth}