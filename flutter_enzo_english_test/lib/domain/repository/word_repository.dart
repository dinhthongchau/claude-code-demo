import 'package:dartz/dartz.dart';
import 'package:flutter_enzo_english_test/core/errors/failures.dart';
import 'package:flutter_enzo_english_test/domain/entity/word_entity.dart';

abstract class WordRepository {
  Future<Either<Failure, List<WordEntity>>> getWordsByFolder({
    required String userId,
    required String folderId,
    int? limit,
    int? skip,
  });
}
