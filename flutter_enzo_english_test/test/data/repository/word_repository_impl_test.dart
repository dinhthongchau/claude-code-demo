import 'package:dartz/dartz.dart';
import 'package:flutter_enzo_english_test/core/errors/exceptions.dart';
import 'package:flutter_enzo_english_test/core/errors/failures.dart';
import 'package:flutter_enzo_english_test/data/models/word_model.dart';
import 'package:flutter_enzo_english_test/data/repository/word_repository_impl.dart';
import 'package:flutter_enzo_english_test/data/source/remote/word_remote_source.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import '../../helpers/test_fixtures.dart';

class MockWordRemoteSource extends Mock implements WordRemoteSource {}

void main() {
  late WordRepositoryImpl repository;
  late MockWordRemoteSource mockRemoteSource;

  setUp(() {
    mockRemoteSource = MockWordRemoteSource();
    repository = WordRepositoryImpl(mockRemoteSource);
  });

  const tUserId = 'test@example.com';
  const tFolderId = '1';

  final tWordModelList = [
    WordModel(
      id: tWordEntity1.id,
      wordId: tWordEntity1.wordId,
      word: tWordEntity1.word,
      definition: tWordEntity1.definition,
      example: tWordEntity1.example,
      imageUrl: tWordEntity1.imageUrl,
      folderId: tWordEntity1.folderId,
      userId: tWordEntity1.userId,
      createdAt: tWordEntity1.createdAt,
      updatedAt: tWordEntity1.updatedAt,
    ),
    WordModel(
      id: tWordEntity2.id,
      wordId: tWordEntity2.wordId,
      word: tWordEntity2.word,
      definition: tWordEntity2.definition,
      example: tWordEntity2.example,
      imageUrl: tWordEntity2.imageUrl,
      folderId: tWordEntity2.folderId,
      userId: tWordEntity2.userId,
      createdAt: tWordEntity2.createdAt,
      updatedAt: tWordEntity2.updatedAt,
    ),
  ];

  group('getWordsByFolder', () {
    test('should return word entities when remote source succeeds', () async {
      // arrange
      when(
        () => mockRemoteSource.getWordsByFolder(
          userId: any(named: 'userId'),
          folderId: any(named: 'folderId'),
          limit: any(named: 'limit'),
          skip: any(named: 'skip'),
        ),
      ).thenAnswer((_) async => tWordModelList);

      // act
      final result = await repository.getWordsByFolder(
        userId: tUserId,
        folderId: tFolderId,
        limit: 100,
        skip: 0,
      );

      // assert
      expect(result, isA<Right>());
      result.fold((failure) => fail('Expected Right but got Left'), (words) {
        expect(words.length, 2);
        expect(words[0].id, tWordEntity1.id);
        expect(words[1].id, tWordEntity2.id);
      });
      verify(
        () => mockRemoteSource.getWordsByFolder(
          userId: tUserId,
          folderId: tFolderId,
          limit: 100,
          skip: 0,
        ),
      ).called(1);
      verifyNoMoreInteractions(mockRemoteSource);
    });

    test(
      'should return ServerFailure when remote source throws ServerException',
      () async {
        // arrange
        when(
          () => mockRemoteSource.getWordsByFolder(
            userId: any(named: 'userId'),
            folderId: any(named: 'folderId'),
            limit: any(named: 'limit'),
            skip: any(named: 'skip'),
          ),
        ).thenThrow(ServerException('Server error', statusCode: 500));

        // act
        final result = await repository.getWordsByFolder(
          userId: tUserId,
          folderId: tFolderId,
          limit: 100,
          skip: 0,
        );

        // assert
        expect(result, isA<Left>());
        result.fold((failure) {
          expect(failure, isA<ServerFailure>());
          expect(failure.message, 'Server error');
        }, (_) => fail('Expected Left but got Right'));
        verify(
          () => mockRemoteSource.getWordsByFolder(
            userId: tUserId,
            folderId: tFolderId,
            limit: 100,
            skip: 0,
          ),
        ).called(1);
        verifyNoMoreInteractions(mockRemoteSource);
      },
    );

    test(
      'should return NetworkFailure when remote source throws NetworkException',
      () async {
        // arrange
        when(
          () => mockRemoteSource.getWordsByFolder(
            userId: any(named: 'userId'),
            folderId: any(named: 'folderId'),
            limit: any(named: 'limit'),
            skip: any(named: 'skip'),
          ),
        ).thenThrow(NetworkException('No internet connection'));

        // act
        final result = await repository.getWordsByFolder(
          userId: tUserId,
          folderId: tFolderId,
          limit: 100,
          skip: 0,
        );

        // assert
        expect(result, isA<Left>());
        result.fold((failure) {
          expect(failure, isA<NetworkFailure>());
          expect(failure.message, 'No internet connection');
        }, (_) => fail('Expected Left but got Right'));
        verify(
          () => mockRemoteSource.getWordsByFolder(
            userId: tUserId,
            folderId: tFolderId,
            limit: 100,
            skip: 0,
          ),
        ).called(1);
        verifyNoMoreInteractions(mockRemoteSource);
      },
    );

    test(
      'should return UnexpectedFailure when remote source throws unexpected exception',
      () async {
        // arrange
        when(
          () => mockRemoteSource.getWordsByFolder(
            userId: any(named: 'userId'),
            folderId: any(named: 'folderId'),
            limit: any(named: 'limit'),
            skip: any(named: 'skip'),
          ),
        ).thenThrow(Exception('Unexpected error'));

        // act
        final result = await repository.getWordsByFolder(
          userId: tUserId,
          folderId: tFolderId,
          limit: 100,
          skip: 0,
        );

        // assert
        expect(result, isA<Left>());
        result.fold((failure) {
          expect(failure, isA<UnexpectedFailure>());
          expect(failure.message, contains('Unexpected error'));
        }, (_) => fail('Expected Left but got Right'));
        verify(
          () => mockRemoteSource.getWordsByFolder(
            userId: tUserId,
            folderId: tFolderId,
            limit: 100,
            skip: 0,
          ),
        ).called(1);
        verifyNoMoreInteractions(mockRemoteSource);
      },
    );

    test('should return empty list when folder has no words', () async {
      // arrange
      when(
        () => mockRemoteSource.getWordsByFolder(
          userId: any(named: 'userId'),
          folderId: any(named: 'folderId'),
          limit: any(named: 'limit'),
          skip: any(named: 'skip'),
        ),
      ).thenAnswer((_) async => []);

      // act
      final result = await repository.getWordsByFolder(
        userId: tUserId,
        folderId: tFolderId,
        limit: 100,
        skip: 0,
      );

      // assert
      expect(result, isA<Right>());
      result.fold(
        (failure) => fail('Expected Right but got Left'),
        (words) => expect(words, []),
      );
      verify(
        () => mockRemoteSource.getWordsByFolder(
          userId: tUserId,
          folderId: tFolderId,
          limit: 100,
          skip: 0,
        ),
      ).called(1);
      verifyNoMoreInteractions(mockRemoteSource);
    });
  });
}
