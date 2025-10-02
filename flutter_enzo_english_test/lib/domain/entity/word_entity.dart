import 'package:equatable/equatable.dart';

class WordEntity extends Equatable {
  final String id;
  final String word;
  final String definition;
  final List<String> examples;
  final List<String> imageUrls;
  final String? partOfSpeech;
  final String? pronunciation;
  final String? notes;
  final String folderId;
  final String userId;
  final DateTime createdAt;
  final DateTime updatedAt;

  const WordEntity({
    required this.id,
    required this.word,
    required this.definition,
    required this.examples,
    required this.imageUrls,
    this.partOfSpeech,
    this.pronunciation,
    this.notes,
    required this.folderId,
    required this.userId,
    required this.createdAt,
    required this.updatedAt,
  });

  @override
  List<Object?> get props => [
    id,
    word,
    definition,
    examples,
    imageUrls,
    partOfSpeech,
    pronunciation,
    notes,
    folderId,
    userId,
    createdAt,
    updatedAt,
  ];
}
