import 'package:dartz/dartz.dart';
import 'package:flutter_enzo_english_test/core/errors/failures.dart';
import 'package:flutter_enzo_english_test/domain/entity/word_entity.dart';
import 'package:flutter_enzo_english_test/domain/repository/word_repository.dart';

class GetWordsByFolderUseCase {
  final WordRepository repository;

  GetWordsByFolderUseCase(this.repository);

  Future<Either<Failure, List<WordEntity>>> call({
    required String folderId,
    int? limit,
    int? skip,
  }) async {
    return await repository.getWordsByFolder(
      folderId: folderId,
      limit: limit,
      skip: skip,
    );
  }
}
