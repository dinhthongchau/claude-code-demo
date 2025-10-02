import 'package:bloc_test/bloc_test.dart';
import 'package:dartz/dartz.dart';
import 'package:flutter_enzo_english_test/core/constants/constants.dart';
import 'package:flutter_enzo_english_test/core/errors/failures.dart';
import 'package:flutter_enzo_english_test/domain/use_case/get_folders_use_case.dart';
import 'package:flutter_enzo_english_test/presentation/blocs/folders/folders_bloc.dart';
import 'package:flutter_enzo_english_test/presentation/blocs/folders/folders_event.dart';
import 'package:flutter_enzo_english_test/presentation/blocs/folders/folders_state.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import '../../../helpers/test_fixtures.dart';

class MockGetFoldersUseCase extends Mock implements GetFoldersUseCase {}

void main() {
  late FoldersBloc bloc;
  late MockGetFoldersUseCase mockGetFoldersUseCase;

  setUp(() {
    mockGetFoldersUseCase = MockGetFoldersUseCase();
    bloc = FoldersBloc(getFoldersUseCase: mockGetFoldersUseCase);
  });

  tearDown(() {
    bloc.close();
  });

  test('initial state should be FoldersInitial with empty list', () {
    expect(bloc.state, const FoldersInitial(folders: []));
  });

  group('LoadFoldersEvent', () {
    blocTest<FoldersBloc, FoldersState>(
      'should emit [FoldersLoading, FoldersSuccess] when data is fetched successfully',
      build: () {
        when(
          () => mockGetFoldersUseCase(
            limit: any(named: 'limit'),
            skip: any(named: 'skip'),
          ),
        ).thenAnswer((_) async => Right(tFolderList));
        return bloc;
      },
      act: (bloc) => bloc.add(const LoadFoldersEvent()),
      expect: () => [
        isA<FoldersLoading>(),
        FoldersSuccess(folders: tFolderList),
      ],
      verify: (_) {
        verify(
          () => mockGetFoldersUseCase(
            limit: AppConstants.defaultPageLimit,
            skip: AppConstants.defaultPageSkip,
          ),
        ).called(1);
      },
    );

    blocTest<FoldersBloc, FoldersState>(
      'should emit [FoldersLoading, FoldersError] when fetching fails with ServerFailure',
      build: () {
        when(
          () => mockGetFoldersUseCase(
            limit: any(named: 'limit'),
            skip: any(named: 'skip'),
          ),
        ).thenAnswer((_) async => const Left(ServerFailure('Server error')));
        return bloc;
      },
      act: (bloc) => bloc.add(const LoadFoldersEvent()),
      expect: () => [
        isA<FoldersLoading>(),
        const FoldersError(folders: [], errorMessage: 'Server error'),
      ],
      verify: (_) {
        verify(
          () => mockGetFoldersUseCase(
            limit: AppConstants.defaultPageLimit,
            skip: AppConstants.defaultPageSkip,
          ),
        ).called(1);
      },
    );

    blocTest<FoldersBloc, FoldersState>(
      'should emit [FoldersLoading, FoldersError] when fetching fails with NetworkFailure',
      build: () {
        when(
          () => mockGetFoldersUseCase(
            limit: any(named: 'limit'),
            skip: any(named: 'skip'),
          ),
        ).thenAnswer(
          (_) async => const Left(NetworkFailure('No internet connection')),
        );
        return bloc;
      },
      act: (bloc) => bloc.add(const LoadFoldersEvent()),
      expect: () => [
        isA<FoldersLoading>(),
        const FoldersError(folders: [], errorMessage: 'No internet connection'),
      ],
      verify: (_) {
        verify(
          () => mockGetFoldersUseCase(
            limit: AppConstants.defaultPageLimit,
            skip: AppConstants.defaultPageSkip,
          ),
        ).called(1);
      },
    );

    blocTest<FoldersBloc, FoldersState>(
      'should preserve previous folders in loading state',
      build: () {
        when(
          () => mockGetFoldersUseCase(
            limit: any(named: 'limit'),
            skip: any(named: 'skip'),
          ),
        ).thenAnswer((_) async => Right(tFolderList));
        return bloc;
      },
      seed: () => FoldersSuccess(folders: tFolderList),
      act: (bloc) => bloc.add(const LoadFoldersEvent()),
      expect: () => [
        FoldersLoading.fromState(state: FoldersSuccess(folders: tFolderList)),
        FoldersSuccess(folders: tFolderList),
      ],
    );
  });

  group('RefreshFoldersEvent', () {
    blocTest<FoldersBloc, FoldersState>(
      'should emit [FoldersSuccess] when refresh is successful (no loading state)',
      build: () {
        when(
          () => mockGetFoldersUseCase(
            limit: any(named: 'limit'),
            skip: any(named: 'skip'),
          ),
        ).thenAnswer((_) async => Right(tFolderList));
        return bloc;
      },
      act: (bloc) => bloc.add(const RefreshFoldersEvent()),
      expect: () => [FoldersSuccess(folders: tFolderList)],
      verify: (_) {
        verify(
          () => mockGetFoldersUseCase(
            limit: AppConstants.defaultPageLimit,
            skip: AppConstants.defaultPageSkip,
          ),
        ).called(1);
      },
    );

    blocTest<FoldersBloc, FoldersState>(
      'should emit [FoldersError] when refresh fails',
      build: () {
        when(
          () => mockGetFoldersUseCase(
            limit: any(named: 'limit'),
            skip: any(named: 'skip'),
          ),
        ).thenAnswer((_) async => const Left(ServerFailure('Server error')));
        return bloc;
      },
      act: (bloc) => bloc.add(const RefreshFoldersEvent()),
      expect: () => [
        const FoldersError(folders: [], errorMessage: 'Server error'),
      ],
      verify: (_) {
        verify(
          () => mockGetFoldersUseCase(
            limit: AppConstants.defaultPageLimit,
            skip: AppConstants.defaultPageSkip,
          ),
        ).called(1);
      },
    );
  });
}
