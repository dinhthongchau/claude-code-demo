import 'package:flutter_enzo_english_test/core/api/api_config.dart';
import 'package:flutter_enzo_english_test/core/errors/exceptions.dart';
import 'package:flutter_enzo_english_test/core/network/dio_client.dart';
import 'package:flutter_enzo_english_test/data/models/word_model.dart';

class WordRemoteSource {
  final DioClient dioClient;

  WordRemoteSource(this.dioClient);

  Future<List<WordModel>> getWordsByFolder({
    required String userId,
    required String folderId,
    int? limit,
    int? skip,
  }) async {
    try {
      final queryParameters = <String, dynamic>{};
      if (limit != null) queryParameters['limit'] = limit;
      if (skip != null) queryParameters['skip'] = skip;

      final response = await dioClient.get(
        ApiConfig.userFolderWordsEndpoint(userId, folderId),
        queryParameters: queryParameters,
      );

      if (response.data == null) {
        throw ServerException('Response data is null');
      }

      final responseData = response.data as Map<String, dynamic>;

      if (responseData['success'] != true) {
        throw ServerException(
          responseData['message'] ?? 'Failed to fetch words',
        );
      }

      final data = responseData['data'] as List<dynamic>;

      return data
          .map((json) => WordModel.fromJson(json as Map<String, dynamic>))
          .toList();
    } catch (e) {
      rethrow;
    }
  }
}
