import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'models/api_response.dart';
import 'models/folder_model.dart';
import 'models/word_model.dart';

class ApiClient {
  static String get baseUrl => dotenv.env['BASE_URL'] ?? 'http://localhost:8829';

  /// Fetch all folders from the API
  static Future<List<Folder>> fetchFolders() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/v1/folders'),
      );

      if (response.statusCode == 200) {
        final jsonResponse = json.decode(response.body);
        final apiResponse = ApiResponse<List<dynamic>>.fromJson(
          jsonResponse,
          (data) => data as List<dynamic>,
        );

        if (apiResponse.success && apiResponse.data != null) {
          return apiResponse.data!
              .map((folderJson) => Folder.fromJson(folderJson))
              .toList();
        } else {
          throw Exception('Failed to load folders: ${apiResponse.message}');
        }
      } else {
        throw Exception('Failed to load folders: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching folders: $e');
    }
  }

  /// Fetch word count for a specific folder
  static Future<int> fetchWordCount(String folderId) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/v1/folders/$folderId/words'),
      );

      if (response.statusCode == 200) {
        final jsonResponse = json.decode(response.body);
        final apiResponse = ApiResponse<List<dynamic>>.fromJson(
          jsonResponse,
          (data) => data as List<dynamic>,
        );

        if (apiResponse.success && apiResponse.data != null) {
          return apiResponse.data!.length;
        } else {
          return 0;
        }
      } else {
        return 0;
      }
    } catch (e) {
      return 0;
    }
  }

  /// Fetch all words in a folder (optional, for future use)
  static Future<List<Word>> fetchWordsInFolder(String folderId) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/v1/folders/$folderId/words'),
      );

      if (response.statusCode == 200) {
        final jsonResponse = json.decode(response.body);
        final apiResponse = ApiResponse<List<dynamic>>.fromJson(
          jsonResponse,
          (data) => data as List<dynamic>,
        );

        if (apiResponse.success && apiResponse.data != null) {
          return apiResponse.data!
              .map((wordJson) => Word.fromJson(wordJson))
              .toList();
        } else {
          throw Exception('Failed to load words: ${apiResponse.message}');
        }
      } else {
        throw Exception('Failed to load words: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching words: $e');
    }
  }
}
