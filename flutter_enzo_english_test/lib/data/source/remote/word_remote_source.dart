import 'package:flutter_enzo_english_test/core/api/api_config.dart';
import 'package:flutter_enzo_english_test/core/errors/exceptions.dart';
import 'package:flutter_enzo_english_test/core/network/dio_client.dart';
import 'package:flutter_enzo_english_test/data/models/word_model.dart';
import 'package:flutter_enzo_english_test/data/models/wordlist_model.dart';

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

      // Use new WordList endpoint instead of old words endpoint
      final response = await dioClient.get(
        ApiConfig.userFolderWordListEndpoint(userId, folderId),
        queryParameters: queryParameters,
      );

      if (response.data == null) {
        throw ServerException('Response data is null');
      }

      final responseData = response.data as Map<String, dynamic>;

      if (responseData['success'] != true) {
        throw ServerException(
          responseData['message'] ?? 'Failed to fetch WordList',
        );
      }

      // The response now contains a WordList object with a words array
      final wordListData = responseData['data'] as Map<String, dynamic>;
      final wordListModel = WordListModel.fromJson(wordListData);

      // Extract the words from the WordList and return as List<WordModel>
      // This maintains compatibility with existing code that expects List<WordModel>
      return wordListModel.words.cast<WordModel>();
    } catch (e) {
      rethrow;
    }
  }
}
