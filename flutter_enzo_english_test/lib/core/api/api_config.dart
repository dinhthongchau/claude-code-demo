import 'package:flutter_dotenv/flutter_dotenv.dart';

class ApiConfig {
  /// Get base URL from environment variables
  static String getBaseUrl() {
    final baseUrl = dotenv.env['BASE_URL'];
    if (baseUrl == null || baseUrl.isEmpty) {
      throw Exception('BASE_URL not found in .env file');
    }
    return baseUrl;
  }

  /// API endpoints
  static const String authEndpoint = '/api/v1/auth/current-user';
  static const String foldersEndpoint = '/api/v1/folders';

  /// User folder words endpoint (simplified structure) - DEPRECATED
  static String userFolderWordsEndpoint(String userId, String folderId) =>
      '/api/v1/users/$userId/folders/$folderId/words';

  /// User folder WordList endpoint (NEW - WordLists system)
  static String userFolderWordListEndpoint(String userId, String folderId) =>
      '/api/v1/users/$userId/folders/$folderId/wordlist';

  static String wordEndpoint(String wordId) => '/api/v1/words/$wordId';
  static const String wordsEndpoint = '/api/v1/words';

  /// Request timeouts
  static const Duration connectTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(seconds: 30);
  static const Duration sendTimeout = Duration(seconds: 30);
}
