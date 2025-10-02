import 'package:dartz/dartz.dart';
import 'package:flutter_enzo_english_test/core/errors/failures.dart';
import 'package:flutter_enzo_english_test/domain/entity/folder_entity.dart';
import 'package:flutter_enzo_english_test/domain/repository/folder_repository.dart';

class GetFoldersUseCase {
  final FolderRepository repository;

  GetFoldersUseCase(this.repository);

  Future<Either<Failure, List<FolderEntity>>> call({
    int? limit,
    int? skip,
  }) async {
    return await repository.getFolders(limit: limit, skip: skip);
  }
}
