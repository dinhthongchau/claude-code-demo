import 'package:flutter_enzo_english_test/domain/entity/folder_entity.dart';
import 'package:flutter_enzo_english_test/domain/entity/word_entity.dart';
import 'package:flutter_enzo_english_test/domain/entity/wordlist_entity.dart';

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

// Words (Simplified structure for AI bubble feature)
final tWordEntity1 = WordEntity(
  id: '1',
  wordId: 'apple_001',
  word: 'apple',
  definition: 'A round fruit',
  example: 'I ate an apple',
  imageUrl: 'image_users/apple_001.jpg',
  folderId: '1',
  userId: 'test@example.com',
  createdAt: DateTime(2024, 1, 1),
  updatedAt: DateTime(2024, 1, 1),
);

final tWordEntity2 = WordEntity(
  id: '2',
  wordId: 'book_002',
  word: 'book',
  definition: 'A written or printed work',
  example: 'Read a book',
  imageUrl: null,
  folderId: '1',
  userId: 'test@example.com',
  createdAt: DateTime(2024, 1, 2),
  updatedAt: DateTime(2024, 1, 2),
);

final List<WordEntity> tWordList = [tWordEntity1, tWordEntity2];

// WordLists (NEW - WordLists system)
final tWordListEntity1 = WordListEntity(
  wordListId: 'list_test_example_com_1',
  userId: 'test@example.com',
  folderId: '1',
  words: [tWordEntity1, tWordEntity2],
  createdAt: DateTime(2024, 1, 1),
  updatedAt: DateTime(2024, 1, 1),
);

final tWordListEntity2 = WordListEntity(
  wordListId: 'list_test_example_com_2',
  userId: 'test@example.com',
  folderId: '2',
  words: [],
  createdAt: DateTime(2024, 1, 2),
  updatedAt: DateTime(2024, 1, 2),
);

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
  'word_id': 'apple_001',
  'word': 'apple',
  'definition': 'A round fruit',
  'example': 'I ate an apple',
  'image_url': 'image_users/apple_001.jpg',
  'folder_id': '1',
  'user_id': 'test@example.com',
  'created_at': '2024-01-01T00:00:00.000',
  'updated_at': '2024-01-01T00:00:00.000',
};

// WordList JSON fixtures (NEW - WordLists system)
final Map<String, dynamic> tWordListJson1 = {
  'word_list_id': 'list_test_example_com_1',
  'user_id': 'test@example.com',
  'folder_id': '1',
  'words': [
    {
      'id': '1',
      'word_id': 'apple_001',
      'word': 'apple',
      'definition': 'A round fruit',
      'example': 'I ate an apple',
      'image_url': 'image_users/apple_001.jpg',
      'folder_id': '1',
      'user_id': 'test@example.com',
      'created_at': '2024-01-01T00:00:00.000',
      'updated_at': '2024-01-01T00:00:00.000',
    },
    {
      'id': '2',
      'word_id': 'book_002',
      'word': 'book',
      'definition': 'A written or printed work',
      'example': 'Read a book',
      'image_url': null,
      'folder_id': '1',
      'user_id': 'test@example.com',
      'created_at': '2024-01-02T00:00:00.000',
      'updated_at': '2024-01-02T00:00:00.000',
    }
  ],
  'created_at': '2024-01-01T00:00:00.000',
  'updated_at': '2024-01-01T00:00:00.000',
};

final Map<String, dynamic> tWordListJson2 = {
  'word_list_id': 'list_test_example_com_2',
  'user_id': 'test@example.com',
  'folder_id': '2',
  'words': [],
  'created_at': '2024-01-02T00:00:00.000',
  'updated_at': '2024-01-02T00:00:00.000',
};
