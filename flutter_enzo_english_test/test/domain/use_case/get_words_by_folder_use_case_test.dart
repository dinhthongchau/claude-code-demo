import 'package:dartz/dartz.dart';
import 'package:flutter_enzo_english_test/core/errors/failures.dart';
import 'package:flutter_enzo_english_test/domain/repository/word_repository.dart';
import 'package:flutter_enzo_english_test/domain/use_case/get_words_by_folder_use_case.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import '../../helpers/test_fixtures.dart';

class MockWordRepository extends Mock implements WordRepository {}

void main() {
  late GetWordsByFolderUseCase useCase;
  late MockWordRepository mockRepository;

  setUp(() {
    mockRepository = MockWordRepository();
    useCase = GetWordsByFolderUseCase(mockRepository);
  });

  const tFolderId = '1';

  group('GetWordsByFolderUseCase', () {
    test(
      'should get words from the repository for a specific folder',
      () async {
        // arrange
        when(
          () => mockRepository.getWordsByFolder(
            folderId: any(named: 'folderId'),
            limit: any(named: 'limit'),
            skip: any(named: 'skip'),
          ),
        ).thenAnswer((_) async => Right(tWordList));

        // act
        final result = await useCase(folderId: tFolderId, limit: 100, skip: 0);

        // assert
        expect(result, Right(tWordList));
        verify(
          () => mockRepository.getWordsByFolder(
            folderId: tFolderId,
            limit: 100,
            skip: 0,
          ),
        ).called(1);
        verifyNoMoreInteractions(mockRepository);
      },
    );

    test('should return ServerFailure when repository fails', () async {
      // arrange
      const tFailure = ServerFailure('Server error');
      when(
        () => mockRepository.getWordsByFolder(
          folderId: any(named: 'folderId'),
          limit: any(named: 'limit'),
          skip: any(named: 'skip'),
        ),
      ).thenAnswer((_) async => const Left(tFailure));

      // act
      final result = await useCase(folderId: tFolderId, limit: 100, skip: 0);

      // assert
      expect(result, const Left(tFailure));
      verify(
        () => mockRepository.getWordsByFolder(
          folderId: tFolderId,
          limit: 100,
          skip: 0,
        ),
      ).called(1);
      verifyNoMoreInteractions(mockRepository);
    });

    test(
      'should return NetworkFailure when repository has network error',
      () async {
        // arrange
        const tFailure = NetworkFailure('No internet connection');
        when(
          () => mockRepository.getWordsByFolder(
            folderId: any(named: 'folderId'),
            limit: any(named: 'limit'),
            skip: any(named: 'skip'),
          ),
        ).thenAnswer((_) async => const Left(tFailure));

        // act
        final result = await useCase(folderId: tFolderId, limit: 100, skip: 0);

        // assert
        expect(result, const Left(tFailure));
        verify(
          () => mockRepository.getWordsByFolder(
            folderId: tFolderId,
            limit: 100,
            skip: 0,
          ),
        ).called(1);
        verifyNoMoreInteractions(mockRepository);
      },
    );

    test('should work with null limit and skip parameters', () async {
      // arrange
      when(
        () => mockRepository.getWordsByFolder(
          folderId: any(named: 'folderId'),
          limit: any(named: 'limit'),
          skip: any(named: 'skip'),
        ),
      ).thenAnswer((_) async => Right(tWordList));

      // act
      final result = await useCase(folderId: tFolderId);

      // assert
      expect(result, Right(tWordList));
      verify(
        () => mockRepository.getWordsByFolder(
          folderId: tFolderId,
          limit: null,
          skip: null,
        ),
      ).called(1);
      verifyNoMoreInteractions(mockRepository);
    });

    test('should return empty list when folder has no words', () async {
      // arrange
      when(
        () => mockRepository.getWordsByFolder(
          folderId: any(named: 'folderId'),
          limit: any(named: 'limit'),
          skip: any(named: 'skip'),
        ),
      ).thenAnswer((_) async => const Right([]));

      // act
      final result = await useCase(folderId: tFolderId, limit: 100, skip: 0);

      // assert
      expect(result, isA<Right>());
      result.fold(
        (failure) => fail('Expected Right but got Left'),
        (words) => expect(words, []),
      );
      verify(
        () => mockRepository.getWordsByFolder(
          folderId: tFolderId,
          limit: 100,
          skip: 0,
        ),
      ).called(1);
      verifyNoMoreInteractions(mockRepository);
    });
  });
}
