import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/foundation.dart';

Future initFirebase() async {
  if (kIsWeb) {
    await Firebase.initializeApp(
        options: FirebaseOptions(
            apiKey: "AIzaSyAgQ5MzVf_mJoRj0hkqsCzN_WhqAlmIgE4",
            authDomain: "pitchhubsmes.firebaseapp.com",
            projectId: "pitchhubsmes",
            storageBucket: "pitchhubsmes.firebasestorage.app",
            messagingSenderId: "893379612030",
            appId: "1:893379612030:web:94d218adfed2c422baf72f",
            measurementId: "G-F0PCXYMK1Q"));
  } else {
    await Firebase.initializeApp();
  }
}
