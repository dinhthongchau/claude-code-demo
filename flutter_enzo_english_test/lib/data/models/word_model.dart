import 'package:flutter_enzo_english_test/domain/entity/word_entity.dart';

class WordModel extends WordEntity {
  const WordModel({
    required super.id,
    required super.word,
    required super.definition,
    required super.examples,
    required super.imageUrls,
    super.partOfSpeech,
    super.pronunciation,
    super.notes,
    required super.folderId,
    required super.userId,
    required super.createdAt,
    required super.updatedAt,
  });

  factory WordModel.fromJson(Map<String, dynamic> json) {
    return WordModel(
      id: json['id'] as String,
      word: json['word'] as String,
      definition: json['definition'] as String,
      examples:
          (json['examples'] as List<dynamic>?)
              ?.map((e) => e as String)
              .toList() ??
          [],
      imageUrls:
          (json['image_urls'] as List<dynamic>?)
              ?.map((e) => e as String)
              .toList() ??
          [],
      partOfSpeech: json['part_of_speech'] as String?,
      pronunciation: json['pronunciation'] as String?,
      notes: json['notes'] as String?,
      folderId: json['folder_id'] as String,
      userId: json['user_id'] as String,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'word': word,
      'definition': definition,
      'examples': examples,
      'image_urls': imageUrls,
      'part_of_speech': partOfSpeech,
      'pronunciation': pronunciation,
      'notes': notes,
      'folder_id': folderId,
      'user_id': userId,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }

  WordEntity toEntity() {
    return WordEntity(
      id: id,
      word: word,
      definition: definition,
      examples: examples,
      imageUrls: imageUrls,
      partOfSpeech: partOfSpeech,
      pronunciation: pronunciation,
      notes: notes,
      folderId: folderId,
      userId: userId,
      createdAt: createdAt,
      updatedAt: updatedAt,
    );
  }
}
