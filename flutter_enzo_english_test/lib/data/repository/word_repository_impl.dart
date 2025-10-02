import 'package:dartz/dartz.dart';
import 'package:flutter_enzo_english_test/core/errors/exceptions.dart';
import 'package:flutter_enzo_english_test/core/errors/failures.dart';
import 'package:flutter_enzo_english_test/data/source/remote/word_remote_source.dart';
import 'package:flutter_enzo_english_test/domain/entity/word_entity.dart';
import 'package:flutter_enzo_english_test/domain/repository/word_repository.dart';

class WordRepositoryImpl implements WordRepository {
  final WordRemoteSource remoteSource;

  WordRepositoryImpl(this.remoteSource);

  @override
  Future<Either<Failure, List<WordEntity>>> getWordsByFolder({
    required String folderId,
    int? limit,
    int? skip,
  }) async {
    try {
      final words = await remoteSource.getWordsByFolder(
        folderId: folderId,
        limit: limit,
        skip: skip,
      );
      final entities = words.map((model) => model.toEntity()).toList();
      return Right(entities);
    } on ServerException catch (e) {
      return Left(ServerFailure(e.message));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(e.message));
    } catch (e) {
      return Left(UnexpectedFailure(e.toString()));
    }
  }
}
