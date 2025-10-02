import 'package:flutter/foundation.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_enzo_english_test/core/constants/constants.dart';
import 'package:flutter_enzo_english_test/domain/use_case/get_folders_use_case.dart';
import 'package:flutter_enzo_english_test/presentation/blocs/folders/folders_event.dart';
import 'package:flutter_enzo_english_test/presentation/blocs/folders/folders_state.dart';

class FoldersBloc extends Bloc<FoldersEvent, FoldersState> {
  final GetFoldersUseCase getFoldersUseCase;

  FoldersBloc({required this.getFoldersUseCase})
    : super(const FoldersInitial(folders: [])) {
    on<LoadFoldersEvent>(_onLoadFolders);
    on<RefreshFoldersEvent>(_onRefreshFolders);
  }

  Future<void> _onLoadFolders(
    LoadFoldersEvent event,
    Emitter<FoldersState> emit,
  ) async {
    emit(FoldersLoading.fromState(state: state));

    try {
      final result = await getFoldersUseCase(
        limit: AppConstants.defaultPageLimit,
        skip: AppConstants.defaultPageSkip,
      );

      result.fold(
        (failure) {
          debugPrint('Failed to load folders: ${failure.message}');
          emit(
            FoldersError(folders: state.folders, errorMessage: failure.message),
          );
        },
        (folders) {
          emit(FoldersSuccess(folders: folders));
        },
      );
    } catch (e, stackTrace) {
      debugPrint('Unexpected error loading folders: $e');
      debugPrint('Stack trace: $stackTrace');
      emit(
        FoldersError(
          folders: state.folders,
          errorMessage: AppConstants.genericErrorMessage,
        ),
      );
    }
  }

  Future<void> _onRefreshFolders(
    RefreshFoldersEvent event,
    Emitter<FoldersState> emit,
  ) async {
    // Don't show loading state for refresh (pull-to-refresh handles it)
    try {
      final result = await getFoldersUseCase(
        limit: AppConstants.defaultPageLimit,
        skip: AppConstants.defaultPageSkip,
      );

      result.fold(
        (failure) {
          debugPrint('Failed to refresh folders: ${failure.message}');
          emit(
            FoldersError(folders: state.folders, errorMessage: failure.message),
          );
        },
        (folders) {
          emit(FoldersSuccess(folders: folders));
        },
      );
    } catch (e, stackTrace) {
      debugPrint('Unexpected error refreshing folders: $e');
      debugPrint('Stack trace: $stackTrace');
      emit(
        FoldersError(
          folders: state.folders,
          errorMessage: AppConstants.genericErrorMessage,
        ),
      );
    }
  }
}
