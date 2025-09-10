import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js";
import { getFirestore, collection, addDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-firestore.js";
import { getAuth, signInAnonymously, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-auth.js";

// Your web app's Firebase configuration
// Paste your firebaseConfig object here from the Firebase console
const firebaseConfig = {
  // Your API Key
  apiKey: "AIzaSyCtNOFajQsqUM6gnXoJRuMjhKNLd3cuqs0",
  // Your Auth Domain
  authDomain: "kangalert-8cb1d.firebaseapp.com",
  // Your Project ID
  projectId: "kangalert-8cb1d",
  // Your Storage Bucket
  storageBucket: "kangalert-8cb1d.firebasestorage.app",
  // Your Messaging Sender ID
  messagingSenderId: "287396440261",
  // Your App ID
  appId: "1:287396440261:web:59f47b5041cf1caaeca8ac"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const auth = getAuth(app);

let user;

// We will sign in the user anonymously to handle submissions
signInAnonymously(auth).then(() => {
    console.log("Signed in anonymously.");
}).catch((error) => {
    console.error("Anonymous sign-in failed:", error);
});

onAuthStateChanged(auth, (currentUser) => {
    if (currentUser) {
        user = currentUser;
        console.log("Current user:", user.uid);
    } else {
        console.log("No user is signed in.");
    }
});

// --- MAP AND GEOLOCATION ---
let map = L.map('map').setView([-25.2744, 133.7751], 5); // Australia center
let currentMarker;
let currentLocation;

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Get current location
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(position => {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;
        currentLocation = { lat, lng };
        map.setView([lat, lng], 14);

        currentMarker = L.marker([lat, lng]).addTo(map)
            .bindPopup("Your current location").openPopup();

        // Allow marker to be dragged to fine-tune location
        currentMarker.dragging.enable();
        currentMarker.on('dragend', function(e) {
            const markerLatLng = e.target.getLatLng();
            currentLocation = { lat: markerLatLng.lat, lng: markerLatLng.lng };
            console.log("Marker dragged to:", currentLocation);
        });
    }, () => {
        alert("Geolocation failed or was denied. You can manually drag the pin on the map.");
    });
}

// --- FORM SUBMISSION ---
const showFormBtn = document.getElementById('showFormBtn');
const reportForm = document.getElementById('reportForm');
const submitReportBtn = document.getElementById('submitReportBtn');

showFormBtn.addEventListener('click', () => {
    reportForm.style.display = 'block';
    showFormBtn.style.display = 'none';
});

reportForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Check if a location is set
    if (!currentLocation) {
        alert("Please allow geolocation or drag the pin on the map to your location.");
        return;
    }

    const reportData = {
        animalType: document.getElementById('animalType').value,
        location: 'on road', // We'll assume this for now, can be an input later
        condition: document.getElementById('condition').value,
        size: document.getElementById('size').value,
        joeyPresent: document.getElementById('joeyPresent').value,
        notes: document.getElementById('notes').value,
        anonymous: document.getElementById('anonymous').checked,
        submissionTime: serverTimestamp(),
        geoPoint: new firebase.firestore.GeoPoint(currentLocation.lat, currentLocation.lng),
        status: 'New',
        joinedUsers: []
    };

    // Add the report to Firestore
    try {
        const docRef = await addDoc(collection(db, "reports"), reportData);
        console.log("Document written with ID: ", docRef.id);
        alert("Report submitted successfully!");
        reportForm.reset();
        reportForm.style.display = 'none';
        showFormBtn.style.display = 'block';
    } catch (error) {
        console.error("Error adding document: ", error);
        alert("Failed to submit report. Please try again.");
    }
});
