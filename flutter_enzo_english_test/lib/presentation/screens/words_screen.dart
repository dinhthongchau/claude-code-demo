import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_enzo_english_test/core/constants/constants.dart';
import 'package:flutter_enzo_english_test/core/get_it/injection_container.dart';
import 'package:flutter_enzo_english_test/domain/entity/folder_entity.dart';
import 'package:flutter_enzo_english_test/presentation/blocs/words/words_bloc.dart';
import 'package:flutter_enzo_english_test/presentation/blocs/words/words_event.dart';
import 'package:flutter_enzo_english_test/presentation/blocs/words/words_state.dart';
import 'package:flutter_enzo_english_test/presentation/widgets/word_card.dart';

class WordsScreen extends StatelessWidget {
  static const String routeName = 'words';
  static const String routePath = 'words';

  final String folderId;
  final FolderEntity? folder;

  const WordsScreen({super.key, required this.folderId, this.folder});

  @override
  Widget build(BuildContext context) {
    // TODO: Get user ID from auth state instead of hardcoding
    const userId = 'dinhthongchau@gmail.com';

    return BlocProvider(
      create: (context) =>
          getIt<WordsBloc>()
            ..add(LoadWordsByFolderEvent(userId: userId, folderId: folderId)),
      child: _WordsView(folder: folder, folderId: folderId),
    );
  }
}

class _WordsView extends StatelessWidget {
  final FolderEntity? folder;
  final String folderId;

  const _WordsView({required this.folder, required this.folderId});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(folder?.name ?? 'Words')),
      body: BlocConsumer<WordsBloc, WordsState>(
        listener: (context, state) {
          if (state is WordsError) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text(
                  state.errorMessage ?? AppConstants.genericErrorMessage,
                ),
                backgroundColor: Colors.red,
              ),
            );
          }
        },
        builder: (context, state) {
          if (state is WordsLoading && state.words == null) {
            return _buildLoadingState();
          }

          if (state is WordsSuccess ||
              (state.words != null && state.words!.isNotEmpty)) {
            final words = state.words!;
            return RefreshIndicator(
              onRefresh: () async {
                // TODO: Get user ID from auth state
                const userId = 'dinhthongchau@gmail.com';
                context.read<WordsBloc>().add(
                  RefreshWordsEvent(userId: userId, folderId: folderId),
                );
                await Future.delayed(const Duration(milliseconds: 500));
              },
              child: ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: words.length,
                itemBuilder: (context, index) {
                  final word = words[index];
                  return WordCard(word: word);
                },
              ),
            );
          }

          // Empty state
          return _buildEmptyState(context);
        },
      ),
    );
  }

  Widget _buildLoadingState() {
    return const Center(child: CircularProgressIndicator());
  }

  Widget _buildEmptyState(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        spacing: 16,
        children: [
          Icon(Icons.library_books_outlined, size: 64, color: Colors.grey[400]),
          Text(
            AppConstants.emptyWordsMessage,
            style: Theme.of(
              context,
            ).textTheme.titleMedium?.copyWith(color: Colors.grey[600]),
          ),
          TextButton.icon(
            onPressed: () {
              // TODO: Get user ID from auth state
              const userId = 'dinhthongchau@gmail.com';
              context.read<WordsBloc>().add(
                RefreshWordsEvent(userId: userId, folderId: folderId),
              );
            },
            icon: const Icon(Icons.refresh),
            label: const Text('Refresh'),
          ),
        ],
      ),
    );
  }
}
