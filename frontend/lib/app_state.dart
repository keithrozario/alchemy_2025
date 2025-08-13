import 'package:flutter/material.dart';
import '/backend/api_requests/api_manager.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'flutter_flow/flutter_flow_util.dart';

class FFAppState extends ChangeNotifier {
  static FFAppState _instance = FFAppState._internal();

  factory FFAppState() {
    return _instance;
  }

  FFAppState._internal();

  static void reset() {
    _instance = FFAppState._internal();
  }

  Future initializePersistedState() async {}

  void update(VoidCallback callback) {
    callback();
    notifyListeners();
  }

  bool _panValidation = false;
  bool get panValidation => _panValidation;
  set panValidation(bool value) {
    _panValidation = value;
  }

  bool _adharValidation = false;
  bool get adharValidation => _adharValidation;
  set adharValidation(bool value) {
    _adharValidation = value;
  }

  bool _isDocument = false;
  bool get isDocument => _isDocument;
  set isDocument(bool value) {
    _isDocument = value;
  }

  bool _dataExtraction = false;
  bool get dataExtraction => _dataExtraction;
  set dataExtraction(bool value) {
    _dataExtraction = value;
  }

  bool _mapsValidation = false;
  bool get mapsValidation => _mapsValidation;
  set mapsValidation(bool value) {
    _mapsValidation = value;
  }

  bool _prilimnaryAssessment = false;
  bool get prilimnaryAssessment => _prilimnaryAssessment;
  set prilimnaryAssessment(bool value) {
    _prilimnaryAssessment = value;
  }

  bool _adharCheckbox = false;
  bool get adharCheckbox => _adharCheckbox;
  set adharCheckbox(bool value) {
    _adharCheckbox = value;
  }

  bool _documentCheckbox = false;
  bool get documentCheckbox => _documentCheckbox;
  set documentCheckbox(bool value) {
    _documentCheckbox = value;
  }

  bool _dataCheckbox = false;
  bool get dataCheckbox => _dataCheckbox;
  set dataCheckbox(bool value) {
    _dataCheckbox = value;
  }

  bool _mapsCheckbox = false;
  bool get mapsCheckbox => _mapsCheckbox;
  set mapsCheckbox(bool value) {
    _mapsCheckbox = value;
  }

  bool _prelliminaryCheckbox = false;
  bool get prelliminaryCheckbox => _prelliminaryCheckbox;
  set prelliminaryCheckbox(bool value) {
    _prelliminaryCheckbox = value;
  }

  bool _aiAgentscomp = false;
  bool get aiAgentscomp => _aiAgentscomp;
  set aiAgentscomp(bool value) {
    _aiAgentscomp = value;
  }

  bool _showExtractedData = false;
  bool get showExtractedData => _showExtractedData;
  set showExtractedData(bool value) {
    _showExtractedData = value;
  }

  bool _documentIssues = false;
  bool get documentIssues => _documentIssues;
  set documentIssues(bool value) {
    _documentIssues = value;
  }

  bool _prelliminarycontainer = false;
  bool get prelliminarycontainer => _prelliminarycontainer;
  set prelliminarycontainer(bool value) {
    _prelliminarycontainer = value;
  }

  List<String> _errorMessages = [];
  List<String> get errorMessages => _errorMessages;
  set errorMessages(List<String> value) {
    _errorMessages = value;
  }

  void addToErrorMessages(String value) {
    errorMessages.add(value);
  }

  void removeFromErrorMessages(String value) {
    errorMessages.remove(value);
  }

  void removeAtIndexFromErrorMessages(int index) {
    errorMessages.removeAt(index);
  }

  void updateErrorMessagesAtIndex(
    int index,
    String Function(String) updateFn,
  ) {
    errorMessages[index] = updateFn(_errorMessages[index]);
  }

  void insertAtIndexInErrorMessages(int index, String value) {
    errorMessages.insert(index, value);
  }
}
