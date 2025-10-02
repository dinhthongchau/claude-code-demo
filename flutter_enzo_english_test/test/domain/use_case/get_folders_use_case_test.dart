import 'package:dartz/dartz.dart';
import 'package:flutter_enzo_english_test/core/errors/failures.dart';
import 'package:flutter_enzo_english_test/domain/repository/folder_repository.dart';
import 'package:flutter_enzo_english_test/domain/use_case/get_folders_use_case.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import '../../helpers/test_fixtures.dart';

class MockFolderRepository extends Mock implements FolderRepository {}

void main() {
  late GetFoldersUseCase useCase;
  late MockFolderRepository mockRepository;

  setUp(() {
    mockRepository = MockFolderRepository();
    useCase = GetFoldersUseCase(mockRepository);
  });

  group('GetFoldersUseCase', () {
    test('should get folders from the repository', () async {
      // arrange
      when(
        () => mockRepository.getFolders(
          limit: any(named: 'limit'),
          skip: any(named: 'skip'),
        ),
      ).thenAnswer((_) async => Right(tFolderList));

      // act
      final result = await useCase(limit: 100, skip: 0);

      // assert
      expect(result, Right(tFolderList));
      verify(() => mockRepository.getFolders(limit: 100, skip: 0)).called(1);
      verifyNoMoreInteractions(mockRepository);
    });

    test('should return ServerFailure when repository fails', () async {
      // arrange
      const tFailure = ServerFailure('Server error');
      when(
        () => mockRepository.getFolders(
          limit: any(named: 'limit'),
          skip: any(named: 'skip'),
        ),
      ).thenAnswer((_) async => const Left(tFailure));

      // act
      final result = await useCase(limit: 100, skip: 0);

      // assert
      expect(result, const Left(tFailure));
      verify(() => mockRepository.getFolders(limit: 100, skip: 0)).called(1);
      verifyNoMoreInteractions(mockRepository);
    });

    test(
      'should return NetworkFailure when repository has network error',
      () async {
        // arrange
        const tFailure = NetworkFailure('No internet connection');
        when(
          () => mockRepository.getFolders(
            limit: any(named: 'limit'),
            skip: any(named: 'skip'),
          ),
        ).thenAnswer((_) async => const Left(tFailure));

        // act
        final result = await useCase(limit: 100, skip: 0);

        // assert
        expect(result, const Left(tFailure));
        verify(() => mockRepository.getFolders(limit: 100, skip: 0)).called(1);
        verifyNoMoreInteractions(mockRepository);
      },
    );

    test('should work with null limit and skip parameters', () async {
      // arrange
      when(
        () => mockRepository.getFolders(
          limit: any(named: 'limit'),
          skip: any(named: 'skip'),
        ),
      ).thenAnswer((_) async => Right(tFolderList));

      // act
      final result = await useCase();

      // assert
      expect(result, Right(tFolderList));
      verify(
        () => mockRepository.getFolders(limit: null, skip: null),
      ).called(1);
      verifyNoMoreInteractions(mockRepository);
    });
  });
}
