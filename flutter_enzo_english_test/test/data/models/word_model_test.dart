import 'package:flutter_enzo_english_test/data/models/word_model.dart';
import 'package:flutter_enzo_english_test/domain/entity/word_entity.dart';
import 'package:flutter_test/flutter_test.dart';

import '../../helpers/test_fixtures.dart';

void main() {
  final tWordModel = WordModel(
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

  group('WordModel', () {
    test('should be a subclass of WordEntity', () {
      // assert
      expect(tWordModel, isA<WordEntity>());
    });

    group('fromJson', () {
      test('should return a valid model from JSON', () {
        // act
        final result = WordModel.fromJson(tWordJson1);

        // assert
        expect(result, tWordModel);
      });

      test('should handle missing optional fields with defaults', () {
        // arrange
        final json = {
          'id': '1',
          'word_id': 'test_001',
          'word': 'test',
          'definition': 'A test word',
          'folder_id': '1',
          'user_id': 'test@example.com',
          'created_at': '2024-01-01T00:00:00.000',
          'updated_at': '2024-01-01T00:00:00.000',
        };

        // act
        final result = WordModel.fromJson(json);

        // assert
        expect(result.example, null);
        expect(result.imageUrl, null);
      });

      test('should handle null optional fields', () {
        // arrange
        final json = {
          'id': '1',
          'word_id': 'test_002',
          'word': 'test',
          'definition': 'A test word',
          'example': null,
          'image_url': null,
          'folder_id': '1',
          'user_id': 'test@example.com',
          'created_at': '2024-01-01T00:00:00.000',
          'updated_at': '2024-01-01T00:00:00.000',
        };

        // act
        final result = WordModel.fromJson(json);

        // assert
        expect(result.example, null);
        expect(result.imageUrl, null);
      });

      test('should handle WordList response format (missing id, folder_id, user_id)', () {
        // arrange - This is the format from WordList endpoint
        final json = {
          'word_id': 'APPLE_001',
          'word': 'apple',
          'definition': 'A round red or green fruit that grows on trees',
          'example': 'I ate a delicious apple for breakfast',
          'image_url': 'image_users/APPLE_001.jpg',
          'created_at': '2025-10-02T05:30:28.878000',
          'updated_at': '2025-10-02T05:30:31.250000',
          // Note: id, folder_id, user_id are missing (from global dictionary)
        };

        // act
        final result = WordModel.fromJson(json);

        // assert
        expect(result.wordId, 'APPLE_001');
        expect(result.word, 'apple');
        expect(result.definition, 'A round red or green fruit that grows on trees');
        expect(result.example, 'I ate a delicious apple for breakfast');
        expect(result.imageUrl, 'image_users/APPLE_001.jpg');
        // Missing fields should default to empty string
        expect(result.id, '');
        expect(result.folderId, '');
        expect(result.userId, '');
      });
    });

    group('toJson', () {
      test('should return a JSON map containing proper data', () {
        // act
        final result = tWordModel.toJson();

        // assert
        expect(result, tWordJson1);
      });
    });

    group('toEntity', () {
      test('should return a WordEntity with same properties', () {
        // act
        final result = tWordModel.toEntity();

        // assert
        expect(result, isA<WordEntity>());
        expect(result.id, tWordModel.id);
        expect(result.wordId, tWordModel.wordId);
        expect(result.word, tWordModel.word);
        expect(result.definition, tWordModel.definition);
        expect(result.example, tWordModel.example);
        expect(result.imageUrl, tWordModel.imageUrl);
        expect(result.folderId, tWordModel.folderId);
        expect(result.userId, tWordModel.userId);
        expect(result.createdAt, tWordModel.createdAt);
        expect(result.updatedAt, tWordModel.updatedAt);
      });
    });
  });
}
