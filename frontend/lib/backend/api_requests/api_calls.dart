import 'dart:convert';
import 'dart:typed_data';
import 'package:flutter/foundation.dart';

import '/flutter_flow/flutter_flow_util.dart';
import 'api_manager.dart';

export 'api_manager.dart' show ApiCallResponse;

const _kPrivateApiFunctionName = 'ffPrivateApiCall';

class LoanAPICall {
  static Future<ApiCallResponse> call({
    String? fullName = '',
    String? address = '',
    String? aadharNumber = '',
    String? panNumber = '',
    String? loanTenure = '',
    String? loanAmount = '',
    String? typeOfProperty = '',
    List<FFUploadedFile>? filesList,
  }) async {
    final files = filesList ?? [];

    return ApiManager.instance.makeApiCall(
      callName: 'loanAPI',
      apiUrl:
          'https://alchemy-backend-v2-209692124655.us-central1.run.app/submit',
      callType: ApiCallType.POST,
      headers: {},
      params: {
        'full_name': fullName,
        'address': address,
        'aadhar_number': aadharNumber,
        'pan_number': panNumber,
        'loan_tenure': loanTenure,
        'loan_amount': loanAmount,
        'type_of_property': typeOfProperty,
        'files': files,
      },
      bodyType: BodyType.MULTIPART,
      returnBody: true,
      encodeBodyUtf8: false,
      decodeUtf8: false,
      cache: false,
      isStreamingApi: false,
      alwaysAllowBody: false,
    );
  }
}

class ApiPagingParams {
  int nextPageNumber = 0;
  int numItems = 0;
  dynamic lastResponse;

  ApiPagingParams({
    required this.nextPageNumber,
    required this.numItems,
    required this.lastResponse,
  });

  @override
  String toString() =>
      'PagingParams(nextPageNumber: $nextPageNumber, numItems: $numItems, lastResponse: $lastResponse,)';
}

String _toEncodable(dynamic item) {
  return item;
}

String _serializeList(List? list) {
  list ??= <String>[];
  try {
    return json.encode(list, toEncodable: _toEncodable);
  } catch (_) {
    if (kDebugMode) {
      print("List serialization failed. Returning empty list.");
    }
    return '[]';
  }
}

String _serializeJson(dynamic jsonVar, [bool isList = false]) {
  jsonVar ??= (isList ? [] : {});
  try {
    return json.encode(jsonVar, toEncodable: _toEncodable);
  } catch (_) {
    if (kDebugMode) {
      print("Json serialization failed. Returning empty json.");
    }
    return isList ? '[]' : '{}';
  }
}
