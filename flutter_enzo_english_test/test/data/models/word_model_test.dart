import 'package:flutter_enzo_english_test/data/models/word_model.dart';
import 'package:flutter_enzo_english_test/domain/entity/word_entity.dart';
import 'package:flutter_test/flutter_test.dart';

import '../../helpers/test_fixtures.dart';

void main() {
  final tWordModel = WordModel(
    id: '1',
    word: 'apple',
    definition: 'A round fruit',
    examples: const ['I ate an apple', 'Apple pie'],
    imageUrls: const ['https://example.com/apple.jpg'],
    partOfSpeech: 'noun',
    pronunciation: '/ˈæp.əl/',
    notes: 'Common fruit',
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
        expect(result.examples, []);
        expect(result.imageUrls, []);
        expect(result.partOfSpeech, null);
        expect(result.pronunciation, null);
        expect(result.notes, null);
      });

      test('should handle null arrays as empty lists', () {
        // arrange
        final json = {
          'id': '1',
          'word': 'test',
          'definition': 'A test word',
          'examples': null,
          'image_urls': null,
          'folder_id': '1',
          'user_id': 'test@example.com',
          'created_at': '2024-01-01T00:00:00.000',
          'updated_at': '2024-01-01T00:00:00.000',
        };

        // act
        final result = WordModel.fromJson(json);

        // assert
        expect(result.examples, []);
        expect(result.imageUrls, []);
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
        expect(result.word, tWordModel.word);
        expect(result.definition, tWordModel.definition);
        expect(result.examples, tWordModel.examples);
        expect(result.imageUrls, tWordModel.imageUrls);
        expect(result.partOfSpeech, tWordModel.partOfSpeech);
        expect(result.pronunciation, tWordModel.pronunciation);
        expect(result.notes, tWordModel.notes);
        expect(result.folderId, tWordModel.folderId);
        expect(result.userId, tWordModel.userId);
        expect(result.createdAt, tWordModel.createdAt);
        expect(result.updatedAt, tWordModel.updatedAt);
      });
    });
  });
}
