import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import 'a_i_agents_model.dart';
export 'a_i_agents_model.dart';

class AIAgentsWidget extends StatefulWidget {
  const AIAgentsWidget({
    super.key,
    required this.apiData,
  });

  final dynamic apiData;

  @override
  State<AIAgentsWidget> createState() => _AIAgentsWidgetState();
}

class _AIAgentsWidgetState extends State<AIAgentsWidget> {
  late AIAgentsModel _model;

  @override
  void setState(VoidCallback callback) {
    super.setState(callback);
    _model.onUpdate();
  }

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => AIAgentsModel());

    WidgetsBinding.instance.addPostFrameCallback((_) => safeSetState(() {}));
  }

  @override
  void dispose() {
    _model.maybeDispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Container();
  }
}
