import 'dart:typed_data';
import 'dart:html';

class FileUploadService {
  static final FileUploadService _instance = FileUploadService._internal();
  factory FileUploadService() => _instance;
  FileUploadService._internal();

  List<File> selectedFiles = [];
  List<Uint8List> fileBytesList = [];

  void clear() {
    selectedFiles.clear();
    fileBytesList.clear();
  }
}

final fileUploadService = FileUploadService();
