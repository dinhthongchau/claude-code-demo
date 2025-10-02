import 'package:flutter/material.dart';
import 'package:flutter_enzo_english_test/domain/entity/folder_entity.dart';
import 'package:flutter_enzo_english_test/presentation/screens/folders_screen.dart';
import 'package:flutter_enzo_english_test/presentation/screens/words_screen.dart';
import 'package:go_router/go_router.dart';

class AppRouter {
  static final GoRouter router = GoRouter(
    initialLocation: FoldersScreen.routePath,
    routes: [
      GoRoute(
        path: FoldersScreen.routePath,
        name: FoldersScreen.routeName,
        builder: (context, state) => const FoldersScreen(),
      ),
      GoRoute(
        path: '/folder/:folderId',
        name: 'folder',
        builder: (context, state) {
          final folderId = state.pathParameters['folderId']!;
          final folder = state.extra as FolderEntity?;
          return WordsScreen(folderId: folderId, folder: folder);
        },
      ),
    ],
    errorBuilder: (context, state) => Scaffold(
      appBar: AppBar(title: const Text('Error')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          spacing: 16,
          children: [
            const Icon(Icons.error_outline, size: 64, color: Colors.red),
            Text('Page not found: ${state.matchedLocation}'),
            ElevatedButton(
              onPressed: () => context.go(FoldersScreen.routePath),
              child: const Text('Go to Home'),
            ),
          ],
        ),
      ),
    ),
  );
}
