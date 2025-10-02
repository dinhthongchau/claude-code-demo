import 'package:flutter_enzo_english_test/domain/entity/folder_entity.dart';
import 'package:flutter_enzo_english_test/domain/entity/word_entity.dart';

/// Test fixtures for consistent test data

// Folders
final tFolderEntity1 = FolderEntity(
  id: '1',
  name: 'Test Folder 1',
  description: 'Test description 1',
  userId: 'test@example.com',
  createdAt: DateTime(2024, 1, 1),
  updatedAt: DateTime(2024, 1, 1),
  color: '#2196F3',
  icon: '📁',
);

final tFolderEntity2 = FolderEntity(
  id: '2',
  name: 'Test Folder 2',
  description: 'Test description 2',
  userId: 'test@example.com',
  createdAt: DateTime(2024, 1, 2),
  updatedAt: DateTime(2024, 1, 2),
  color: '#4CAF50',
  icon: '📚',
);

final List<FolderEntity> tFolderList = [tFolderEntity1, tFolderEntity2];

// Words
final tWordEntity1 = WordEntity(
  id: '1',
  word: 'apple',
  definition: 'A round fruit',
  examples: ['I ate an apple', 'Apple pie'],
  imageUrls: ['https://example.com/apple.jpg'],
  partOfSpeech: 'noun',
  pronunciation: '/ˈæp.əl/',
  notes: 'Common fruit',
  folderId: '1',
  userId: 'test@example.com',
  createdAt: DateTime(2024, 1, 1),
  updatedAt: DateTime(2024, 1, 1),
);

final tWordEntity2 = WordEntity(
  id: '2',
  word: 'book',
  definition: 'A written or printed work',
  examples: ['Read a book', 'Book club'],
  imageUrls: [],
  partOfSpeech: 'noun',
  pronunciation: '/bʊk/',
  notes: null,
  folderId: '1',
  userId: 'test@example.com',
  createdAt: DateTime(2024, 1, 2),
  updatedAt: DateTime(2024, 1, 2),
);

final List<WordEntity> tWordList = [tWordEntity1, tWordEntity2];

// JSON fixtures
final Map<String, dynamic> tFolderJson1 = {
  'id': '1',
  'name': 'Test Folder 1',
  'description': 'Test description 1',
  'user_id': 'test@example.com',
  'created_at': '2024-01-01T00:00:00.000',
  'updated_at': '2024-01-01T00:00:00.000',
  'color': '#2196F3',
  'icon': '📁',
};

final Map<String, dynamic> tWordJson1 = {
  'id': '1',
  'word': 'apple',
  'definition': 'A round fruit',
  'examples': ['I ate an apple', 'Apple pie'],
  'image_urls': ['https://example.com/apple.jpg'],
  'part_of_speech': 'noun',
  'pronunciation': '/ˈæp.əl/',
  'notes': 'Common fruit',
  'folder_id': '1',
  'user_id': 'test@example.com',
  'created_at': '2024-01-01T00:00:00.000',
  'updated_at': '2024-01-01T00:00:00.000',
};
