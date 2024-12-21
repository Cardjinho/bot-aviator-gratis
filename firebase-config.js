// Configuração do Firebase
const firebaseConfig = {
    apiKey: "AIzaSyBl6pScNvuB1_La_beozzFZZHK6mqvv96o",
    authDomain: "kirvano-mz.firebaseapp.com",
    databaseURL: "https://kirvano-mz-default-rtdb.firebaseio.com",
    projectId: "kirvano-mz",
    storageBucket: "kirvano-mz.appspot.com",
    messagingSenderId: "123456789012",
    appId: "1:123456789012:web:abcdefgh12345"
};

// Inicializar Firebase
const app = firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
