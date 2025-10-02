import 'package:equatable/equatable.dart';
import 'package:flutter_enzo_english_test/domain/entity/folder_entity.dart';

sealed class FoldersState extends Equatable {
  final List<FolderEntity>? folders;

  const FoldersState({this.folders});

  @override
  List<Object?> get props => [folders];
}

class FoldersInitial extends FoldersState {
  const FoldersInitial({super.folders});
}

class FoldersLoading extends FoldersState {
  FoldersLoading.fromState({required FoldersState state})
    : super(folders: state.folders);
}

class FoldersSuccess extends FoldersState {
  const FoldersSuccess({super.folders});
}

class FoldersError extends FoldersState {
  final String? errorMessage;

  const FoldersError({super.folders, required this.errorMessage});

  @override
  List<Object?> get props => [...super.props, errorMessage];
}
