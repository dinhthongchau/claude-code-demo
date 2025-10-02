import 'package:dartz/dartz.dart';
import 'package:flutter_enzo_english_test/core/errors/exceptions.dart';
import 'package:flutter_enzo_english_test/core/errors/failures.dart';
import 'package:flutter_enzo_english_test/data/source/remote/folder_remote_source.dart';
import 'package:flutter_enzo_english_test/domain/entity/folder_entity.dart';
import 'package:flutter_enzo_english_test/domain/repository/folder_repository.dart';

class FolderRepositoryImpl implements FolderRepository {
  final FolderRemoteSource remoteSource;

  FolderRepositoryImpl(this.remoteSource);

  @override
  Future<Either<Failure, List<FolderEntity>>> getFolders({
    int? limit,
    int? skip,
  }) async {
    try {
      final folders = await remoteSource.getFolders(limit: limit, skip: skip);
      final entities = folders.map((model) => model.toEntity()).toList();
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
