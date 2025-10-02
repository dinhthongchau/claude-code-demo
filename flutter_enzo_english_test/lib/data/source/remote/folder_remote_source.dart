import 'package:flutter_enzo_english_test/core/api/api_config.dart';
import 'package:flutter_enzo_english_test/core/errors/exceptions.dart';
import 'package:flutter_enzo_english_test/core/network/dio_client.dart';
import 'package:flutter_enzo_english_test/data/models/folder_model.dart';

class FolderRemoteSource {
  final DioClient dioClient;

  FolderRemoteSource(this.dioClient);

  Future<List<FolderModel>> getFolders({int? limit, int? skip}) async {
    try {
      final queryParameters = <String, dynamic>{};
      if (limit != null) queryParameters['limit'] = limit;
      if (skip != null) queryParameters['skip'] = skip;

      final response = await dioClient.get(
        ApiConfig.foldersEndpoint,
        queryParameters: queryParameters,
      );

      if (response.data == null) {
        throw ServerException('Response data is null');
      }

      final responseData = response.data as Map<String, dynamic>;

      if (responseData['success'] != true) {
        throw ServerException(
          responseData['message'] ?? 'Failed to fetch folders',
        );
      }

      final data = responseData['data'] as List<dynamic>;

      return data
          .map((json) => FolderModel.fromJson(json as Map<String, dynamic>))
          .toList();
    } catch (e) {
      rethrow;
    }
  }
}
