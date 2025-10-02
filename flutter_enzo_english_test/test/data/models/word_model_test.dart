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
