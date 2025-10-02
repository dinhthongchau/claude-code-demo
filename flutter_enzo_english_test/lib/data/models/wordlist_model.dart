import 'package:flutter_enzo_english_test/data/models/word_model.dart';
import 'package:flutter_enzo_english_test/domain/entity/word_entity.dart';
import 'package:flutter_enzo_english_test/domain/entity/wordlist_entity.dart';

/// WordList model for data layer
/// 
/// Represents a collection of words associated with a user and folder.
/// Maps between JSON API responses and domain entities.
class WordListModel extends WordListEntity {
  const WordListModel({
    required super.wordListId,
    required super.userId,
    required super.folderId,
    required super.words,
    required super.createdAt,
    required super.updatedAt,
  });

  /// Create WordListModel from JSON response
  factory WordListModel.fromJson(Map<String, dynamic> json) {
    // Handle words array - can be either word IDs (strings) or full word objects
    final wordsData = json['words'] as List<dynamic>? ?? [];
    final List<WordModel> words = [];

    for (final wordData in wordsData) {
      if (wordData is String) {
        // If it's just a word ID, create a minimal WordModel
        // This shouldn't happen with the /wordlist endpoint, but handle it gracefully
        words.add(WordModel(
          id: '', // No MongoDB ID available
          wordId: wordData,
          word: '', // Will need to be resolved
          definition: '',
          example: null,
          imageUrl: null,
          folderId: '', // Required field
          userId: '', // Required field
          createdAt: DateTime.now(),
          updatedAt: DateTime.now(),
        ));
      } else if (wordData is Map<String, dynamic>) {
        // Full word object from resolved WordList
        words.add(WordModel.fromJson(wordData));
      }
    }

    return WordListModel(
      wordListId: json['word_list_id'] as String,
      userId: json['user_id'] as String,
      folderId: json['folder_id'] as String,
      words: words,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );
  }

  /// Convert WordListModel to JSON
  Map<String, dynamic> toJson() {
    return {
      'word_list_id': wordListId,
      'user_id': userId,
      'folder_id': folderId,
      'words': words.map((word) => (word as WordModel).toJson()).toList(),
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }

  /// Convert to domain entity
  WordListEntity toEntity() {
    return WordListEntity(
      wordListId: wordListId,
      userId: userId,
      folderId: folderId,
      words: words.map((word) => (word as WordModel).toEntity()).toList(),
      createdAt: createdAt,
      updatedAt: updatedAt,
    );
  }

  /// Create a copy with updated fields
  @override
  WordListModel copyWith({
    String? wordListId,
    String? userId,
    String? folderId,
    List<WordEntity>? words,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return WordListModel(
      wordListId: wordListId ?? this.wordListId,
      userId: userId ?? this.userId,
      folderId: folderId ?? this.folderId,
      words: words?.cast<WordModel>() ?? this.words.cast<WordModel>(),
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is WordListModel &&
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
    return 'WordListModel('
        'wordListId: $wordListId, '
        'userId: $userId, '
        'folderId: $folderId, '
        'words: ${words.length} items, '
        'createdAt: $createdAt, '
        'updatedAt: $updatedAt'
        ')';
  }
}
