import '/components/final_response_tab_widget.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'dart:ui';
import 'final_page_widget.dart' show FinalPageWidget;
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';

class FinalPageModel extends FlutterFlowModel<FinalPageWidget> {
  ///  State fields for stateful widgets in this page.

  // Model for finalResponseTab component.
  late FinalResponseTabModel finalResponseTabModel;

  @override
  void initState(BuildContext context) {
    finalResponseTabModel = createModel(context, () => FinalResponseTabModel());
  }

  @override
  void dispose() {
    finalResponseTabModel.dispose();
  }
}
