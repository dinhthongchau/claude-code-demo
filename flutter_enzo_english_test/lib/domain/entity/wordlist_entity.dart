import 'package:flutter_enzo_english_test/domain/entity/word_entity.dart';

/// WordList entity for domain layer
/// 
/// Represents a collection of words associated with a user and folder.
/// This is the core business object that contains no external dependencies.
class WordListEntity {
  /// Unique identifier for the WordList (generated from user_id + folder_id)
  final String wordListId;
  
  /// User identifier (email or ID)
  final String userId;
  
  /// Folder identifier
  final String folderId;
  
  /// List of words in this WordList
  final List<WordEntity> words;
  
  /// When the WordList was created
  final DateTime createdAt;
  
  /// When the WordList was last updated
  final DateTime updatedAt;

  const WordListEntity({
    required this.wordListId,
    required this.userId,
    required this.folderId,
    required this.words,
    required this.createdAt,
    required this.updatedAt,
  });

  /// Create a copy with updated fields
  WordListEntity copyWith({
    String? wordListId,
    String? userId,
    String? folderId,
    List<WordEntity>? words,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return WordListEntity(
      wordListId: wordListId ?? this.wordListId,
      userId: userId ?? this.userId,
      folderId: folderId ?? this.folderId,
      words: words ?? this.words,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }

  /// Get the number of words in this WordList
  int get wordCount => words.length;

  /// Check if the WordList is empty
  bool get isEmpty => words.isEmpty;

  /// Check if the WordList has words
  bool get isNotEmpty => words.isNotEmpty;

  /// Get words that have images
  List<WordEntity> get wordsWithImages => 
      words.where((word) => word.imageUrl != null && word.imageUrl!.isNotEmpty).toList();

  /// Get words that have examples
  List<WordEntity> get wordsWithExamples => 
      words.where((word) => word.example != null && word.example!.isNotEmpty).toList();

  /// Get count of words with images
  int get wordsWithImagesCount => wordsWithImages.length;

  /// Get count of words with examples  
  int get wordsWithExamplesCount => wordsWithExamples.length;

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is WordListEntity &&
        other.wordListId == wordListId &&
        other.userId == userId &&
        other.folderId == folderId &&
        other.words.length == words.length &&
        other.createdAt == createdAt &&
        other.updatedAt == updatedAt;
  }

  @override
  int get hashCode {
    return Object.hash(
      wordListId,
      userId,
      folderId,
      words.length,
      createdAt,
      updatedAt,
    );
  }

  @override
  String toString() {
    return 'WordListEntity('
        'wordListId: $wordListId, '
        'userId: $userId, '
        'folderId: $folderId, '
        'words: ${words.length} items, '
        'createdAt: $createdAt, '
        'updatedAt: $updatedAt'
        ')';
  }
}
