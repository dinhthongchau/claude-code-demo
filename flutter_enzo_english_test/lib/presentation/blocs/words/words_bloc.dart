import 'package:flutter/foundation.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_enzo_english_test/core/constants/constants.dart';
import 'package:flutter_enzo_english_test/domain/use_case/get_words_by_folder_use_case.dart';
import 'package:flutter_enzo_english_test/presentation/blocs/words/words_event.dart';
import 'package:flutter_enzo_english_test/presentation/blocs/words/words_state.dart';

class WordsBloc extends Bloc<WordsEvent, WordsState> {
  final GetWordsByFolderUseCase getWordsByFolderUseCase;

  WordsBloc({required this.getWordsByFolderUseCase})
    : super(const WordsInitial(words: [])) {
    on<LoadWordsByFolderEvent>(_onLoadWordsByFolder);
    on<RefreshWordsEvent>(_onRefreshWords);
  }

  Future<void> _onLoadWordsByFolder(
    LoadWordsByFolderEvent event,
    Emitter<WordsState> emit,
  ) async {
    emit(WordsLoading.fromState(state: state));

    try {
      final result = await getWordsByFolderUseCase(
        folderId: event.folderId,
        limit: AppConstants.defaultPageLimit,
        skip: AppConstants.defaultPageSkip,
      );

      result.fold(
        (failure) {
          debugPrint('Failed to load words: ${failure.message}');
          emit(WordsError(words: state.words, errorMessage: failure.message));
        },
        (words) {
          emit(WordsSuccess(words: words));
        },
      );
    } catch (e, stackTrace) {
      debugPrint('Unexpected error loading words: $e');
      debugPrint('Stack trace: $stackTrace');
      emit(
        WordsError(
          words: state.words,
          errorMessage: AppConstants.genericErrorMessage,
        ),
      );
    }
  }

  Future<void> _onRefreshWords(
    RefreshWordsEvent event,
    Emitter<WordsState> emit,
  ) async {
    // Don't show loading state for refresh (pull-to-refresh handles it)
    try {
      final result = await getWordsByFolderUseCase(
        folderId: event.folderId,
        limit: AppConstants.defaultPageLimit,
        skip: AppConstants.defaultPageSkip,
      );

      result.fold(
        (failure) {
          debugPrint('Failed to refresh words: ${failure.message}');
          emit(WordsError(words: state.words, errorMessage: failure.message));
        },
        (words) {
          emit(WordsSuccess(words: words));
        },
      );
    } catch (e, stackTrace) {
      debugPrint('Unexpected error refreshing words: $e');
      debugPrint('Stack trace: $stackTrace');
      emit(
        WordsError(
          words: state.words,
          errorMessage: AppConstants.genericErrorMessage,
        ),
      );
    }
  }
}
