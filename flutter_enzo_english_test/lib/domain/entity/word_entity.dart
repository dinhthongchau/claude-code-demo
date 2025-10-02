import 'package:equatable/equatable.dart';

/// Simplified word entity for AI bubble feature preparation
/// Uses single example and image instead of arrays
class WordEntity extends Equatable {
  final String id;
  final String wordId;
  final String word;
  final String definition;
  final String? example;
  final String? imageUrl;
  final String folderId;
  final String userId;
  final DateTime createdAt;
  final DateTime updatedAt;

  const WordEntity({
    required this.id,
    required this.wordId,
    required this.word,
    required this.definition,
    this.example,
    this.imageUrl,
    required this.folderId,
    required this.userId,
    required this.createdAt,
    required this.updatedAt,
  });

  @override
  List<Object?> get props => [
    id,
    wordId,
    word,
    definition,
    example,
    imageUrl,
    folderId,
    userId,
    createdAt,
    updatedAt,
  ];
}
