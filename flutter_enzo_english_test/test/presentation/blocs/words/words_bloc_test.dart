import 'package:bloc_test/bloc_test.dart';
import 'package:dartz/dartz.dart';
import 'package:flutter_enzo_english_test/core/constants/constants.dart';
import 'package:flutter_enzo_english_test/core/errors/failures.dart';
import 'package:flutter_enzo_english_test/domain/use_case/get_words_by_folder_use_case.dart';
import 'package:flutter_enzo_english_test/presentation/blocs/words/words_bloc.dart';
import 'package:flutter_enzo_english_test/presentation/blocs/words/words_event.dart';
import 'package:flutter_enzo_english_test/presentation/blocs/words/words_state.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

import '../../../helpers/test_fixtures.dart';

class MockGetWordsByFolderUseCase extends Mock
    implements GetWordsByFolderUseCase {}

void main() {
  late WordsBloc bloc;
  late MockGetWordsByFolderUseCase mockGetWordsByFolderUseCase;

  setUp(() {
    mockGetWordsByFolderUseCase = MockGetWordsByFolderUseCase();
    bloc = WordsBloc(getWordsByFolderUseCase: mockGetWordsByFolderUseCase);
  });

  tearDown(() {
    bloc.close();
  });

  const tFolderId = '1';

  test('initial state should be WordsInitial with empty list', () {
    expect(bloc.state, const WordsInitial(words: []));
  });

  group('LoadWordsByFolderEvent', () {
    blocTest<WordsBloc, WordsState>(
      'should emit [WordsLoading, WordsSuccess] when data is fetched successfully',
      build: () {
        when(
          () => mockGetWordsByFolderUseCase(
            folderId: any(named: 'folderId'),
            limit: any(named: 'limit'),
            skip: any(named: 'skip'),
          ),
        ).thenAnswer((_) async => Right(tWordList));
        return bloc;
      },
      act: (bloc) => bloc.add(const LoadWordsByFolderEvent(tFolderId)),
      expect: () => [isA<WordsLoading>(), WordsSuccess(words: tWordList)],
      verify: (_) {
        verify(
          () => mockGetWordsByFolderUseCase(
            folderId: tFolderId,
            limit: AppConstants.defaultPageLimit,
            skip: AppConstants.defaultPageSkip,
          ),
        ).called(1);
      },
    );

    blocTest<WordsBloc, WordsState>(
      'should emit [WordsLoading, WordsError] when fetching fails with ServerFailure',
      build: () {
        when(
          () => mockGetWordsByFolderUseCase(
            folderId: any(named: 'folderId'),
            limit: any(named: 'limit'),
            skip: any(named: 'skip'),
          ),
        ).thenAnswer((_) async => const Left(ServerFailure('Server error')));
        return bloc;
      },
      act: (bloc) => bloc.add(const LoadWordsByFolderEvent(tFolderId)),
      expect: () => [
        isA<WordsLoading>(),
        const WordsError(words: [], errorMessage: 'Server error'),
      ],
      verify: (_) {
        verify(
          () => mockGetWordsByFolderUseCase(
            folderId: tFolderId,
            limit: AppConstants.defaultPageLimit,
            skip: AppConstants.defaultPageSkip,
          ),
        ).called(1);
      },
    );

    blocTest<WordsBloc, WordsState>(
      'should emit [WordsLoading, WordsError] when fetching fails with NetworkFailure',
      build: () {
        when(
          () => mockGetWordsByFolderUseCase(
            folderId: any(named: 'folderId'),
            limit: any(named: 'limit'),
            skip: any(named: 'skip'),
          ),
        ).thenAnswer(
          (_) async => const Left(NetworkFailure('No internet connection')),
        );
        return bloc;
      },
      act: (bloc) => bloc.add(const LoadWordsByFolderEvent(tFolderId)),
      expect: () => [
        isA<WordsLoading>(),
        const WordsError(words: [], errorMessage: 'No internet connection'),
      ],
      verify: (_) {
        verify(
          () => mockGetWordsByFolderUseCase(
            folderId: tFolderId,
            limit: AppConstants.defaultPageLimit,
            skip: AppConstants.defaultPageSkip,
          ),
        ).called(1);
      },
    );

    blocTest<WordsBloc, WordsState>(
      'should preserve previous words in loading state',
      build: () {
        when(
          () => mockGetWordsByFolderUseCase(
            folderId: any(named: 'folderId'),
            limit: any(named: 'limit'),
            skip: any(named: 'skip'),
          ),
        ).thenAnswer((_) async => Right(tWordList));
        return bloc;
      },
      seed: () => WordsSuccess(words: tWordList),
      act: (bloc) => bloc.add(const LoadWordsByFolderEvent(tFolderId)),
      expect: () => [
        WordsLoading.fromState(state: WordsSuccess(words: tWordList)),
        WordsSuccess(words: tWordList),
      ],
    );

    blocTest<WordsBloc, WordsState>(
      'should emit [WordsLoading, WordsSuccess] with empty list when folder has no words',
      build: () {
        when(
          () => mockGetWordsByFolderUseCase(
            folderId: any(named: 'folderId'),
            limit: any(named: 'limit'),
            skip: any(named: 'skip'),
          ),
        ).thenAnswer((_) async => const Right([]));
        return bloc;
      },
      act: (bloc) => bloc.add(const LoadWordsByFolderEvent(tFolderId)),
      expect: () => [isA<WordsLoading>(), const WordsSuccess(words: [])],
    );
  });

  group('RefreshWordsEvent', () {
    blocTest<WordsBloc, WordsState>(
      'should emit [WordsSuccess] when refresh is successful (no loading state)',
      build: () {
        when(
          () => mockGetWordsByFolderUseCase(
            folderId: any(named: 'folderId'),
            limit: any(named: 'limit'),
            skip: any(named: 'skip'),
          ),
        ).thenAnswer((_) async => Right(tWordList));
        return bloc;
      },
      act: (bloc) => bloc.add(const RefreshWordsEvent(tFolderId)),
      expect: () => [WordsSuccess(words: tWordList)],
      verify: (_) {
        verify(
          () => mockGetWordsByFolderUseCase(
            folderId: tFolderId,
            limit: AppConstants.defaultPageLimit,
            skip: AppConstants.defaultPageSkip,
          ),
        ).called(1);
      },
    );

    blocTest<WordsBloc, WordsState>(
      'should emit [WordsError] when refresh fails',
      build: () {
        when(
          () => mockGetWordsByFolderUseCase(
            folderId: any(named: 'folderId'),
            limit: any(named: 'limit'),
            skip: any(named: 'skip'),
          ),
        ).thenAnswer((_) async => const Left(ServerFailure('Server error')));
        return bloc;
      },
      act: (bloc) => bloc.add(const RefreshWordsEvent(tFolderId)),
      expect: () => [const WordsError(words: [], errorMessage: 'Server error')],
      verify: (_) {
        verify(
          () => mockGetWordsByFolderUseCase(
            folderId: tFolderId,
            limit: AppConstants.defaultPageLimit,
            skip: AppConstants.defaultPageSkip,
          ),
        ).called(1);
      },
    );
  });
}
