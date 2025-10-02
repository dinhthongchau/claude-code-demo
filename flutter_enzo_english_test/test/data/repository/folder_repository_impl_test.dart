import 'package:dartz/dartz.dart';
import 'package:flutter_enzo_english_test/core/errors/exceptions.dart';
import 'package:flutter_enzo_english_test/core/errors/failures.dart';
import 'package:flutter_enzo_english_test/data/models/folder_model.dart';
import 'package:flutter_enzo_english_test/data/repository/folder_repository_impl.dart';
import 'package:flutter_enzo_english_test/data/source/remote/folder_remote_source.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import '../../helpers/test_fixtures.dart';

class MockFolderRemoteSource extends Mock implements FolderRemoteSource {}

void main() {
  late FolderRepositoryImpl repository;
  late MockFolderRemoteSource mockRemoteSource;

  setUp(() {
    mockRemoteSource = MockFolderRemoteSource();
    repository = FolderRepositoryImpl(mockRemoteSource);
  });

  final tFolderModelList = [
    FolderModel(
      id: tFolderEntity1.id,
      name: tFolderEntity1.name,
      description: tFolderEntity1.description,
      userId: tFolderEntity1.userId,
      createdAt: tFolderEntity1.createdAt,
      updatedAt: tFolderEntity1.updatedAt,
      color: tFolderEntity1.color,
      icon: tFolderEntity1.icon,
    ),
    FolderModel(
      id: tFolderEntity2.id,
      name: tFolderEntity2.name,
      description: tFolderEntity2.description,
      userId: tFolderEntity2.userId,
      createdAt: tFolderEntity2.createdAt,
      updatedAt: tFolderEntity2.updatedAt,
      color: tFolderEntity2.color,
      icon: tFolderEntity2.icon,
    ),
  ];

  group('getFolders', () {
    test('should return folder entities when remote source succeeds', () async {
      // arrange
      when(
        () => mockRemoteSource.getFolders(
          limit: any(named: 'limit'),
          skip: any(named: 'skip'),
        ),
      ).thenAnswer((_) async => tFolderModelList);

      // act
      final result = await repository.getFolders(limit: 100, skip: 0);

      // assert
      expect(result, isA<Right>());
      result.fold((failure) => fail('Expected Right but got Left'), (folders) {
        expect(folders.length, 2);
        expect(folders[0].id, tFolderEntity1.id);
        expect(folders[1].id, tFolderEntity2.id);
      });
      verify(() => mockRemoteSource.getFolders(limit: 100, skip: 0)).called(1);
      verifyNoMoreInteractions(mockRemoteSource);
    });

    test(
      'should return ServerFailure when remote source throws ServerException',
      () async {
        // arrange
        when(
          () => mockRemoteSource.getFolders(
            limit: any(named: 'limit'),
            skip: any(named: 'skip'),
          ),
        ).thenThrow(ServerException('Server error', statusCode: 500));

        // act
        final result = await repository.getFolders(limit: 100, skip: 0);

        // assert
        expect(result, isA<Left>());
        result.fold((failure) {
          expect(failure, isA<ServerFailure>());
          expect(failure.message, 'Server error');
        }, (_) => fail('Expected Left but got Right'));
        verify(
          () => mockRemoteSource.getFolders(limit: 100, skip: 0),
        ).called(1);
        verifyNoMoreInteractions(mockRemoteSource);
      },
    );

    test(
      'should return NetworkFailure when remote source throws NetworkException',
      () async {
        // arrange
        when(
          () => mockRemoteSource.getFolders(
            limit: any(named: 'limit'),
            skip: any(named: 'skip'),
          ),
        ).thenThrow(NetworkException('No internet connection'));

        // act
        final result = await repository.getFolders(limit: 100, skip: 0);

        // assert
        expect(result, isA<Left>());
        result.fold((failure) {
          expect(failure, isA<NetworkFailure>());
          expect(failure.message, 'No internet connection');
        }, (_) => fail('Expected Left but got Right'));
        verify(
          () => mockRemoteSource.getFolders(limit: 100, skip: 0),
        ).called(1);
        verifyNoMoreInteractions(mockRemoteSource);
      },
    );

    test(
      'should return UnexpectedFailure when remote source throws unexpected exception',
      () async {
        // arrange
        when(
          () => mockRemoteSource.getFolders(
            limit: any(named: 'limit'),
            skip: any(named: 'skip'),
          ),
        ).thenThrow(Exception('Unexpected error'));

        // act
        final result = await repository.getFolders(limit: 100, skip: 0);

        // assert
        expect(result, isA<Left>());
        result.fold((failure) {
          expect(failure, isA<UnexpectedFailure>());
          expect(failure.message, contains('Unexpected error'));
        }, (_) => fail('Expected Left but got Right'));
        verify(
          () => mockRemoteSource.getFolders(limit: 100, skip: 0),
        ).called(1);
        verifyNoMoreInteractions(mockRemoteSource);
      },
    );

    test(
      'should return empty list when remote source returns empty list',
      () async {
        // arrange
        when(
          () => mockRemoteSource.getFolders(
            limit: any(named: 'limit'),
            skip: any(named: 'skip'),
          ),
        ).thenAnswer((_) async => []);

        // act
        final result = await repository.getFolders(limit: 100, skip: 0);

        // assert
        expect(result, isA<Right>());
        result.fold(
          (failure) => fail('Expected Right but got Left'),
          (folders) => expect(folders, []),
        );
        verify(
          () => mockRemoteSource.getFolders(limit: 100, skip: 0),
        ).called(1);
        verifyNoMoreInteractions(mockRemoteSource);
      },
    );
  });
}
