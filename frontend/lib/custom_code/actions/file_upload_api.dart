// Automatic FlutterFlow imports
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'index.dart'; // Imports other custom actions
import '/flutter_flow/custom_functions.dart'; // Imports custom functions
import 'package:flutter/material.dart';
// Begin custom action code
// DO NOT REMOVE OR MODIFY THE CODE ABOVE!

import 'package:cymbal_bank_l_o_a_n_a_p_p/custom_code/file_upload_service.dart';

import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';

Future<dynamic> fileUploadApi(
  String? fullname,
  String? address,
  String? aadharnumber,
  String? pannumber,
  String? loantenure,
  String? loanamount,
  String? typeofproperty,
) async {
  final uri = Uri.parse(
      '/submit');

  final selectedFiles = fileUploadService.selectedFiles;
  final fileBytesList = fileUploadService.fileBytesList;

  if (selectedFiles.isEmpty || fileBytesList.isEmpty) {
    print('⚠️ No files selected.');
    return;
  }

  final request = http.MultipartRequest('POST', uri);

  // Attach all files with the same key 'files'
  for (int i = 0; i < selectedFiles.length; i++) {
    request.files.add(
      http.MultipartFile.fromBytes(
        'files',
        fileBytesList[i],
        filename: selectedFiles[i].name,
        contentType: MediaType('application', 'pdf'),
      ),
    );
  }

  // Add form fields
  request.fields['full_name'] = fullname ?? '';
  request.fields['loan_type'] = address ?? '';
  request.fields['aadhar_number'] = aadharnumber ?? '';
  request.fields['pan_number'] = pannumber ?? '';
  request.fields['loan_tenure'] = loantenure ?? '';
  request.fields['loan_amount'] = loanamount ?? '';
  request.fields['type_of_property'] = typeofproperty ?? '';

  try {
    final response = await request.send();
    final responseBody = await response.stream.bytesToString();

    if (response.statusCode == 200) {
      print('✅ Success: $responseBody');
      return jsonDecode(responseBody);
    } else {
      print('❌ Failed: $responseBody');
      return {
        'error': true,
        'status': response.statusCode,
        'message': responseBody,
      };
    }
  } catch (e) {
    print('❌ Upload error: $e');
  }

  // Optional: clear file storage
  fileUploadService.clear();
}
