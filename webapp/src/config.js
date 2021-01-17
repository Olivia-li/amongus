import firebase from 'firebase'

const config = {
    apiKey: "AIzaSyAN9aAPlFsbECyyxBcELLTBlgQXmKzHCY8",
    authDomain: "amongus-htn.firebaseapp.com",
    databaseURL: "https://amongus-htn-default-rtdb.firebaseio.com",
    projectId: "amongus-htn",
    storageBucket: "amongus-htn.appspot.com",
    messagingSenderId: "690456555474",
    appId: "1:690456555474:web:19dfa6912e35387dd4a20b"
  };

var fire = firebase.initializeApp(config);
export default fire;