import 'package:flutter_enzo_english_test/data/models/folder_model.dart';
import 'package:flutter_enzo_english_test/domain/entity/folder_entity.dart';
import 'package:flutter_test/flutter_test.dart';

import '../../helpers/test_fixtures.dart';

void main() {
  final tFolderModel = FolderModel(
    id: '1',
    name: 'Test Folder 1',
    description: 'Test description 1',
    userId: 'test@example.com',
    createdAt: DateTime(2024, 1, 1),
    updatedAt: DateTime(2024, 1, 1),
    color: '#2196F3',
    icon: '📁',
  );

  group('FolderModel', () {
    test('should be a subclass of FolderEntity', () {
      // assert
      expect(tFolderModel, isA<FolderEntity>());
    });

    group('fromJson', () {
      test('should return a valid model from JSON', () {
        // act
        final result = FolderModel.fromJson(tFolderJson1);

        // assert
        expect(result, tFolderModel);
      });

      test('should handle missing optional fields with defaults', () {
        // arrange
        final json = {
          'id': '1',
          'name': 'Test Folder',
          'user_id': 'test@example.com',
          'created_at': '2024-01-01T00:00:00.000',
          'updated_at': '2024-01-01T00:00:00.000',
        };

        // act
        final result = FolderModel.fromJson(json);

        // assert
        expect(result.description, '');
        expect(result.color, '#2196F3');
        expect(result.icon, '📁');
      });
    });

    group('toJson', () {
      test('should return a JSON map containing proper data', () {
        // act
        final result = tFolderModel.toJson();

        // assert
        expect(result, tFolderJson1);
      });
    });

    group('toEntity', () {
      test('should return a FolderEntity with same properties', () {
        // act
        final result = tFolderModel.toEntity();

        // assert
        expect(result, isA<FolderEntity>());
        expect(result.id, tFolderModel.id);
        expect(result.name, tFolderModel.name);
        expect(result.description, tFolderModel.description);
        expect(result.userId, tFolderModel.userId);
        expect(result.createdAt, tFolderModel.createdAt);
        expect(result.updatedAt, tFolderModel.updatedAt);
        expect(result.color, tFolderModel.color);
        expect(result.icon, tFolderModel.icon);
      });
    });
  });
}
