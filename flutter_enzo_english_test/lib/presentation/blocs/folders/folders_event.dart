import 'package:equatable/equatable.dart';

sealed class FoldersEvent extends Equatable {
  const FoldersEvent();

  @override
  List<Object?> get props => [];
}

class LoadFoldersEvent extends FoldersEvent {
  const LoadFoldersEvent();
}

class RefreshFoldersEvent extends FoldersEvent {
  const RefreshFoldersEvent();
}
