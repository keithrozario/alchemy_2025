// Automatic FlutterFlow imports
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'index.dart'; // Imports other custom widgets
import '/custom_code/actions/index.dart'; // Imports custom actions
import '/flutter_flow/custom_functions.dart'; // Imports custom functions
import 'package:flutter/material.dart';
// Begin custom widget code
// DO NOT REMOVE OR MODIFY THE CODE ABOVE!

import 'package:cymbal_bank_l_o_a_n_a_p_p/custom_code/file_upload_service.dart';

import 'dart:html' as html;
import 'dart:typed_data';
import 'package:http/http.dart' as http;

class DragAndDropFileSelection extends StatefulWidget {
  const DragAndDropFileSelection({
    super.key,
    this.width,
    this.height,
  });

  final double? width;
  final double? height;

  @override
  State<DragAndDropFileSelection> createState() =>
      _DragAndDropFileSelectionState();
}

class _DragAndDropFileSelectionState extends State<DragAndDropFileSelection> {
  List<html.File> selectedFiles = [];
  List<Uint8List> fileBytesList = [];
  bool isDragging = false;

  final List<String> allowedMimeTypes = ['application/pdf', 'image/png'];

  void _handleFiles(List<html.File> files) {
    for (final file in files) {
      if (!allowedMimeTypes.contains(file.type)) continue;
      if (fileUploadService.selectedFiles.any((f) => f.name == file.name))
        continue;

      final reader = html.FileReader();
      reader.readAsArrayBuffer(file);

      reader.onLoadEnd.listen((event) {
        final bytes = reader.result as Uint8List?;
        if (bytes != null) {
          setState(() {
            selectedFiles.add(file);
            fileBytesList.add(bytes);

            fileUploadService.selectedFiles.add(file);
            fileUploadService.fileBytesList.add(bytes);
          });
        }
      });
    }
  }

  void _pickFiles() {
    final input = html.FileUploadInputElement()
      ..multiple = true
      ..accept = '*/*';
    input.click();

    input.onChange.listen((event) {
      final files = input.files;
      if (files != null && files.isNotEmpty) {
        _handleFiles(files);
      }
    });
  }

  void _uploadFiles() async {
    if (selectedFiles.isEmpty || fileBytesList.isEmpty) return;

    final uri = Uri.parse('https://your-api-endpoint.com/upload');

    for (int i = 0; i < selectedFiles.length; i++) {
      final request = http.MultipartRequest('POST', uri)
        ..files.add(
          http.MultipartFile.fromBytes(
            'file',
            fileBytesList[i],
            filename: selectedFiles[i].name,
          ),
        );

      final response = await request.send();

      if (response.statusCode == 200) {
        print('✅ Uploaded: ${selectedFiles[i].name}');
      } else {
        print('❌ Failed: ${selectedFiles[i].name}');
      }
    }
  }

  void _cancel() async {
    setState(() {
      selectedFiles.clear();
      fileBytesList.clear();
    });
    fileUploadService.clear();
  }

  void removeAtIndex(int index) {
    selectedFiles.removeAt(index);
    fileBytesList.removeAt(index);
    setState(() {});
  }

  @override
  void initState() {
    super.initState();

    html.document.body!.addEventListener('drop', (event) {
      event.preventDefault();
      setState(() => isDragging = false);

      final dataTransfer = (event as dynamic).dataTransfer;
      if (dataTransfer != null &&
          dataTransfer.files != null &&
          dataTransfer.files!.isNotEmpty) {
        final pdfFiles = dataTransfer.files!
            .where((f) => f.type == 'application/pdf')
            .toList();
        _handleFiles(pdfFiles);
      }
    });

    html.document.body!.addEventListener('dragover', (event) {
      event.preventDefault();
      setState(() => isDragging = true);
    });

    html.document.body!.addEventListener('dragleave', (event) {
      event.preventDefault();
      setState(() => isDragging = false);
    });
  }

  @override
  Widget build(BuildContext context) {
    double wrapWidth = MediaQuery.of(context).size.width * 0.9;
    double spacing = 8;
    return selectedFiles.isNotEmpty
        ? Container(
            width: wrapWidth,
            child: Wrap(
              spacing: spacing,
              runSpacing: spacing,
              children: [
                ...selectedFiles.asMap().entries.map((entry) {
                  int index = entry.key;
                  var file = entry.value;
                  return Stack(
                    children: [
                      Container(
                        width: MediaQuery.of(context).size.width * 0.198,
                        padding: EdgeInsets.all(8),
                        decoration: BoxDecoration(
                          border: Border.all(color: Colors.grey),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Row(
                          crossAxisAlignment: CrossAxisAlignment.center,
                          children: [
                            Icon(
                              Icons.picture_as_pdf_rounded,
                              color: Colors.red,
                              size: 24,
                            ),
                            SizedBox(width: 4),
                            Text(
                              file.name,
                              overflow: TextOverflow.ellipsis,
                              maxLines: 1,
                            ),
                          ],
                        ),
                      ),
                      Positioned(
                        top: 4,
                        right: 4,
                        child: GestureDetector(
                          onTap: () => removeAtIndex(index),
                          child: Icon(
                            Icons.close,
                            size: 16,
                            color: Colors.black,
                          ),
                        ),
                      ),
                    ],
                  );
                }),
                InkWell(
                  onTap: () {
                    _pickFiles();
                  },
                  child: Text(
                    "Upload",
                    style: TextStyle(
                      color: Colors.green,
                      decoration: TextDecoration.underline,
                    ),
                  ),
                ),
              ],
            ),
          )
        : Center(
            child: Column(
              children: [
                MouseRegion(
                  onEnter: (_) => setState(() => isDragging = true),
                  onExit: (_) => setState(() => isDragging = false),
                  child: Container(
                    width: 1000,
                    height: 127,
                    alignment: Alignment.center,
                    decoration: BoxDecoration(
                      // color: isDragging ? Colors.blue[100] : Colors.grey[200],
                      // border: Border.all(
                      //   color: Colors.grey,
                      //   width: 1,
                      // ),
                      borderRadius: BorderRadius.circular(4),
                    ),
                    child: Column(
                      mainAxisAlignment:
                          MainAxisAlignment.center, // Center vertically
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: [
                        // Icon(
                        //   Icons.cloud_upload_outlined,
                        //   weight: 100,
                        // ),
                        Container(
                          padding: EdgeInsets.all(8),
                          // width: MediaQuery.of(context).size.width * 0.7,
                          // height: MediaQuery.of(context).size.height * 0.15,
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              InkWell(
                                onTap: () {
                                  _pickFiles();
                                },
                                child: Text(
                                  "Upload",
                                  style: TextStyle(
                                      color: Colors.green,
                                      decoration: TextDecoration.underline),
                                ),
                              ),
                              SizedBox(
                                width: 8,
                              ),
                              Text("or Drag and Drop your files")
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          );
  }
}
