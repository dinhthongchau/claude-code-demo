class Word {
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

  Word({
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

  factory Word.fromJson(Map<String, dynamic> json) {
    return Word(
      id: json['id'],
      word: json['word'],
      definition: json['definition'],
      examples: List<String>.from(json['examples'] ?? []),
      imageUrls: List<String>.from(json['image_urls'] ?? []),
      partOfSpeech: json['part_of_speech'],
      pronunciation: json['pronunciation'],
      notes: json['notes'],
      folderId: json['folder_id'],
      userId: json['user_id'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
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
}
