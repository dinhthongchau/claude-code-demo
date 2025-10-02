import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_enzo_english_test/data/models/wordlist_model.dart';
import 'package:flutter_enzo_english_test/domain/entity/wordlist_entity.dart';
import '../../helpers/test_fixtures.dart';

void main() {
  group('WordListModel', () {
    test('should be a subclass of WordListEntity', () {
      // arrange
      final wordListModel = WordListModel.fromJson(tWordListJson1);
      
      // assert
      expect(wordListModel, isA<WordListEntity>());
    });

    group('fromJson', () {
      test('should return a valid model from JSON with words array', () {
        // act
        final result = WordListModel.fromJson(tWordListJson1);

        // assert
        expect(result.wordListId, 'list_test_example_com_1');
        expect(result.userId, 'test@example.com');
        expect(result.folderId, '1');
        expect(result.words.length, 2);
        expect(result.words[0].wordId, 'apple_001');
        expect(result.words[0].word, 'apple');
        expect(result.words[1].wordId, 'book_002');
        expect(result.words[1].word, 'book');
        expect(result.createdAt, DateTime(2024, 1, 1));
        expect(result.updatedAt, DateTime(2024, 1, 1));
      });

      test('should return a valid model from JSON with empty words array', () {
        // act
        final result = WordListModel.fromJson(tWordListJson2);

        // assert
        expect(result.wordListId, 'list_test_example_com_2');
        expect(result.userId, 'test@example.com');
        expect(result.folderId, '2');
        expect(result.words.length, 0);
        expect(result.createdAt, DateTime(2024, 1, 2));
        expect(result.updatedAt, DateTime(2024, 1, 2));
      });

      test('should handle missing words field with empty array', () {
        // arrange
        final json = {
          'word_list_id': 'test_id',
          'user_id': 'test@example.com',
          'folder_id': '1',
          'created_at': '2024-01-01T00:00:00.000',
          'updated_at': '2024-01-01T00:00:00.000',
        };

        // act
        final result = WordListModel.fromJson(json);

        // assert
        expect(result.words.length, 0);
      });

      test('should handle words as string IDs (graceful degradation)', () {
        // arrange
        final json = {
          'word_list_id': 'test_id',
          'user_id': 'test@example.com',
          'folder_id': '1',
          'words': ['APPLE_001', 'BANANA_002'], // String IDs instead of objects
          'created_at': '2024-01-01T00:00:00.000',
          'updated_at': '2024-01-01T00:00:00.000',
        };

        // act
        final result = WordListModel.fromJson(json);

        // assert
        expect(result.words.length, 2);
        expect(result.words[0].wordId, 'APPLE_001');
        expect(result.words[1].wordId, 'BANANA_002');
        // Other fields should be empty for graceful degradation
        expect(result.words[0].word, '');
        expect(result.words[0].definition, '');
      });
    });

    group('toJson', () {
      test('should return a JSON map containing proper data', () {
        // arrange
        final wordListModel = WordListModel.fromJson(tWordListJson1);

        // act
        final result = wordListModel.toJson();

        // assert
        expect(result['word_list_id'], 'list_test_example_com_1');
        expect(result['user_id'], 'test@example.com');
        expect(result['folder_id'], '1');
        expect(result['words'], isA<List>());
        expect((result['words'] as List).length, 2);
        expect(result['created_at'], '2024-01-01T00:00:00.000');
        expect(result['updated_at'], '2024-01-01T00:00:00.000');
      });

      test('should return a JSON map with empty words array', () {
        // arrange
        final wordListModel = WordListModel.fromJson(tWordListJson2);

        // act
        final result = wordListModel.toJson();

        // assert
        expect(result['words'], isA<List>());
        expect((result['words'] as List).length, 0);
      });
    });

    group('toEntity', () {
      test('should return a WordListEntity with same properties', () {
        // arrange
        final wordListModel = WordListModel.fromJson(tWordListJson1);

        // act
        final result = wordListModel.toEntity();

        // assert
        expect(result, isA<WordListEntity>());
        expect(result.wordListId, wordListModel.wordListId);
        expect(result.userId, wordListModel.userId);
        expect(result.folderId, wordListModel.folderId);
        expect(result.words.length, wordListModel.words.length);
        expect(result.createdAt, wordListModel.createdAt);
        expect(result.updatedAt, wordListModel.updatedAt);
      });
    });

    group('copyWith', () {
      test('should return a new instance with updated properties', () {
        // arrange
        final wordListModel = WordListModel.fromJson(tWordListJson1);
        final newWords = wordListModel.words.take(1).toList();

        // act
        final result = wordListModel.copyWith(
          folderId: 'new_folder_id',
          words: newWords,
        );

        // assert
        expect(result.folderId, 'new_folder_id');
        expect(result.words.length, 1);
        // Other properties should remain the same
        expect(result.wordListId, wordListModel.wordListId);
        expect(result.userId, wordListModel.userId);
        expect(result.createdAt, wordListModel.createdAt);
      });

      test('should return same instance when no properties changed', () {
        // arrange
        final wordListModel = WordListModel.fromJson(tWordListJson1);

        // act
        final result = wordListModel.copyWith();

        // assert
        expect(result.wordListId, wordListModel.wordListId);
        expect(result.userId, wordListModel.userId);
        expect(result.folderId, wordListModel.folderId);
        expect(result.words.length, wordListModel.words.length);
      });
    });

    group('equality', () {
      test('should be equal when all properties are the same', () {
        // arrange
        final wordListModel1 = WordListModel.fromJson(tWordListJson1);
        final wordListModel2 = WordListModel.fromJson(tWordListJson1);

        // assert
        expect(wordListModel1, equals(wordListModel2));
        expect(wordListModel1.hashCode, equals(wordListModel2.hashCode));
      });

      test('should not be equal when properties differ', () {
        // arrange
        final wordListModel1 = WordListModel.fromJson(tWordListJson1);
        final wordListModel2 = WordListModel.fromJson(tWordListJson2);

        // assert
        expect(wordListModel1, isNot(equals(wordListModel2)));
      });
    });

    group('toString', () {
      test('should return a string representation', () {
        // arrange
        final wordListModel = WordListModel.fromJson(tWordListJson1);

        // act
        final result = wordListModel.toString();

        // assert
        expect(result, contains('WordListModel'));
        expect(result, contains('list_test_example_com_1'));
        expect(result, contains('test@example.com'));
        expect(result, contains('2 items'));
      });
    });

    group('WordListEntity properties', () {
      test('should provide correct word count', () {
        // arrange
        final wordListModel = WordListModel.fromJson(tWordListJson1);

        // assert
        expect(wordListModel.wordCount, 2);
        expect(wordListModel.isNotEmpty, true);
        expect(wordListModel.isEmpty, false);
      });

      test('should provide correct empty state', () {
        // arrange
        final wordListModel = WordListModel.fromJson(tWordListJson2);

        // assert
        expect(wordListModel.wordCount, 0);
        expect(wordListModel.isEmpty, true);
        expect(wordListModel.isNotEmpty, false);
      });

      test('should provide words with images count', () {
        // arrange
        final wordListModel = WordListModel.fromJson(tWordListJson1);

        // assert
        expect(wordListModel.wordsWithImagesCount, 1); // Only apple has image
        expect(wordListModel.wordsWithExamplesCount, 2); // Both have examples
      });
    });
  });
}
