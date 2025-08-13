import '/components/final_response_tab_widget.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import 'final_page_model.dart';
export 'final_page_model.dart';

class FinalPageWidget extends StatefulWidget {
  const FinalPageWidget({super.key});

  static String routeName = 'finalPage';
  static String routePath = '/finalPage';

  @override
  State<FinalPageWidget> createState() => _FinalPageWidgetState();
}

class _FinalPageWidgetState extends State<FinalPageWidget> {
  late FinalPageModel _model;

  final scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => FinalPageModel());

    WidgetsBinding.instance.addPostFrameCallback((_) => safeSetState(() {}));
  }

  @override
  void dispose() {
    _model.dispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        FocusScope.of(context).unfocus();
        FocusManager.instance.primaryFocus?.unfocus();
      },
      child: Scaffold(
        key: scaffoldKey,
        backgroundColor: FlutterFlowTheme.of(context).primaryBackground,
        body: SafeArea(
          top: true,
          child: Container(
            decoration: BoxDecoration(
              color: Color(0xFF009E25),
              image: DecorationImage(
                fit: BoxFit.contain,
                alignment: AlignmentDirectional(-1.0, -1.0),
                image: Image.asset(
                  'assets/images/Screenshot_2025-06-12_4.44.34_PM.png',
                ).image,
              ),
            ),
            child: Align(
              alignment: AlignmentDirectional(1.0, -1.0),
              child: Padding(
                padding: EdgeInsetsDirectional.fromSTEB(0.0, 20.0, 50.0, 0.0),
                child: Container(
                  width: MediaQuery.sizeOf(context).width * 0.73,
                  height: MediaQuery.sizeOf(context).height * 0.95,
                  decoration: BoxDecoration(
                    color: FlutterFlowTheme.of(context).secondaryBackground,
                    borderRadius: BorderRadius.circular(20.0),
                    border: Border.all(
                      color: FlutterFlowTheme.of(context).alternate,
                      width: 1.0,
                    ),
                  ),
                  child: Column(
                    mainAxisSize: MainAxisSize.max,
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      wrapWithModel(
                        model: _model.finalResponseTabModel,
                        updateCallback: () => safeSetState(() {}),
                        child: FinalResponseTabWidget(),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
