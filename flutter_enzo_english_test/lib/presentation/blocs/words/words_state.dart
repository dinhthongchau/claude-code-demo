import 'package:equatable/equatable.dart';
import 'package:flutter_enzo_english_test/domain/entity/word_entity.dart';

sealed class WordsState extends Equatable {
  final List<WordEntity>? words;

  const WordsState({this.words});

  @override
  List<Object?> get props => [words];
}

class WordsInitial extends WordsState {
  const WordsInitial({super.words});
}

class WordsLoading extends WordsState {
  WordsLoading.fromState({required WordsState state})
    : super(words: state.words);
}

class WordsSuccess extends WordsState {
  const WordsSuccess({super.words});
}

class WordsError extends WordsState {
  final String? errorMessage;

  const WordsError({super.words, required this.errorMessage});

  @override
  List<Object?> get props => [...super.props, errorMessage];
}
