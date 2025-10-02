import 'package:equatable/equatable.dart';

sealed class WordsEvent extends Equatable {
  const WordsEvent();

  @override
  List<Object?> get props => [];
}

class LoadWordsByFolderEvent extends WordsEvent {
  final String userId;
  final String folderId;

  const LoadWordsByFolderEvent({required this.userId, required this.folderId});

  @override
  List<Object?> get props => [userId, folderId];
}

class RefreshWordsEvent extends WordsEvent {
  final String userId;
  final String folderId;

  const RefreshWordsEvent({required this.userId, required this.folderId});

  @override
  List<Object?> get props => [userId, folderId];
}
