import 'package:dartz/dartz.dart';
import 'package:flutter_enzo_english_test/core/errors/failures.dart';
import 'package:flutter_enzo_english_test/domain/entity/folder_entity.dart';

abstract class FolderRepository {
  Future<Either<Failure, List<FolderEntity>>> getFolders({
    int? limit,
    int? skip,
  });
}
