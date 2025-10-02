import 'package:get_it/get_it.dart';
import 'package:flutter_enzo_english_test/core/api/api_config.dart';
import 'package:flutter_enzo_english_test/core/network/dio_client.dart';
import 'package:flutter_enzo_english_test/data/repository/folder_repository_impl.dart';
import 'package:flutter_enzo_english_test/data/repository/word_repository_impl.dart';
import 'package:flutter_enzo_english_test/data/source/remote/folder_remote_source.dart';
import 'package:flutter_enzo_english_test/data/source/remote/word_remote_source.dart';
import 'package:flutter_enzo_english_test/domain/repository/folder_repository.dart';
import 'package:flutter_enzo_english_test/domain/repository/word_repository.dart';
import 'package:flutter_enzo_english_test/domain/use_case/get_folders_use_case.dart';
import 'package:flutter_enzo_english_test/domain/use_case/get_words_by_folder_use_case.dart';
import 'package:flutter_enzo_english_test/presentation/blocs/folders/folders_bloc.dart';
import 'package:flutter_enzo_english_test/presentation/blocs/words/words_bloc.dart';

final getIt = GetIt.instance;

Future<void> setupDependencies() async {
  // External - Dio Client
  getIt.registerLazySingleton<DioClient>(
    () => DioClient(baseUrl: ApiConfig.getBaseUrl()),
  );

  // Data Sources
  getIt.registerLazySingleton<FolderRemoteSource>(
    () => FolderRemoteSource(getIt<DioClient>()),
  );
  getIt.registerLazySingleton<WordRemoteSource>(
    () => WordRemoteSource(getIt<DioClient>()),
  );

  // Repositories
  getIt.registerLazySingleton<FolderRepository>(
    () => FolderRepositoryImpl(getIt<FolderRemoteSource>()),
  );
  getIt.registerLazySingleton<WordRepository>(
    () => WordRepositoryImpl(getIt<WordRemoteSource>()),
  );

  // Use Cases
  getIt.registerLazySingleton<GetFoldersUseCase>(
    () => GetFoldersUseCase(getIt<FolderRepository>()),
  );
  getIt.registerLazySingleton<GetWordsByFolderUseCase>(
    () => GetWordsByFolderUseCase(getIt<WordRepository>()),
  );

  // BLoCs
  getIt.registerFactory<FoldersBloc>(
    () => FoldersBloc(getFoldersUseCase: getIt<GetFoldersUseCase>()),
  );
  getIt.registerFactory<WordsBloc>(
    () => WordsBloc(getWordsByFolderUseCase: getIt<GetWordsByFolderUseCase>()),
  );
}
