import 'package:flutter_enzo_english_test/domain/entity/word_entity.dart';

class WordModel extends WordEntity {
  const WordModel({
    required super.id,
    required super.wordId,
    required super.word,
    required super.definition,
    super.example,
    super.imageUrl,
    required super.folderId,
    required super.userId,
    required super.createdAt,
    required super.updatedAt,
  });

  factory WordModel.fromJson(Map<String, dynamic> json) {
    return WordModel(
      id: json['id'] as String? ?? '', // Handle missing id from WordList response
      wordId: json['word_id'] as String,
      word: json['word'] as String,
      definition: json['definition'] as String,
      example: json['example'] as String?,
      imageUrl: json['image_url'] as String?,
      folderId: json['folder_id'] as String? ?? '', // Handle missing folder_id from WordList response
      userId: json['user_id'] as String? ?? '', // Handle missing user_id from WordList response
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'word_id': wordId,
      'word': word,
      'definition': definition,
      'example': example,
      'image_url': imageUrl,
      'folder_id': folderId,
      'user_id': userId,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }

  WordEntity toEntity() {
    return WordEntity(
      id: id,
      wordId: wordId,
      word: word,
      definition: definition,
      example: example,
      imageUrl: imageUrl,
      folderId: folderId,
      userId: userId,
      createdAt: createdAt,
      updatedAt: updatedAt,
    );
  }
}
