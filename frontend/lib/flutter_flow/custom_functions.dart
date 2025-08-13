import 'dart:convert';
import 'dart:math' as math;

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:intl/intl.dart';
import 'package:timeago/timeago.dart' as timeago;
import 'lat_lng.dart';
import 'place.dart';
import 'uploaded_file.dart';


dynamic dummyData() {
  return {
    "form_data": {
      "full_name": "swathi",
      "aadhar_number": "2324235345",
      "pan_number": "23435435",
      "loan_tenure": "60",
      "loan_amount": "6700000",
      "type_of_property": "under construction",
      "loan_type": "constant EMI"
    },
    "document_data": {
      "payslip.pdf": {
        "full_name": "Rahul Sharma",
        "employer_name": "Cymbal Corporation",
        "total_salary": "260583.00",
        "salary_month": "05-2025",
        "pan": "ABCDE1234F",
        "document_type": "salary_slip"
      }
    },
    "status": "FAILED",
    "messages": [
      "AoC NOA no avaialble",
      "Signature missing on page 4 of property deed"
    ],
    "preliminary_assessment": "Some string to describe preliminary assessment"
  };
}
