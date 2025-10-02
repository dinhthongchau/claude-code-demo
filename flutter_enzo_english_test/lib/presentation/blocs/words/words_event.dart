import 'package:equatable/equatable.dart';

sealed class WordsEvent extends Equatable {
  const WordsEvent();

  @override
  List<Object?> get props => [];
}

class LoadWordsByFolderEvent extends WordsEvent {
  final String folderId;

  const LoadWordsByFolderEvent(this.folderId);

  @override
  List<Object?> get props => [folderId];
}

class RefreshWordsEvent extends WordsEvent {
  final String folderId;

  const RefreshWordsEvent(this.folderId);

  @override
  List<Object?> get props => [folderId];
}
