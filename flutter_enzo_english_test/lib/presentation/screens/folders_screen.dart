import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_enzo_english_test/core/constants/constants.dart';
import 'package:flutter_enzo_english_test/core/get_it/injection_container.dart';
import 'package:flutter_enzo_english_test/presentation/blocs/folders/folders_bloc.dart';
import 'package:flutter_enzo_english_test/presentation/blocs/folders/folders_event.dart';
import 'package:flutter_enzo_english_test/presentation/blocs/folders/folders_state.dart';
import 'package:flutter_enzo_english_test/presentation/widgets/folder_card.dart';
import 'package:go_router/go_router.dart';

class FoldersScreen extends StatelessWidget {
  static const String routeName = '/';
  static const String routePath = '/';

  const FoldersScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) => getIt<FoldersBloc>()..add(const LoadFoldersEvent()),
      child: const _FoldersView(),
    );
  }
}

class _FoldersView extends StatelessWidget {
  const _FoldersView();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('My Folders')),
      body: BlocConsumer<FoldersBloc, FoldersState>(
        listener: (context, state) {
          if (state is FoldersError) {
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
          if (state is FoldersLoading && state.folders == null) {
            return _buildLoadingState();
          }

          if (state is FoldersSuccess ||
              (state.folders != null && state.folders!.isNotEmpty)) {
            final folders = state.folders!;
            return RefreshIndicator(
              onRefresh: () async {
                context.read<FoldersBloc>().add(const RefreshFoldersEvent());
                // Wait for state to update
                await Future.delayed(const Duration(milliseconds: 500));
              },
              child: ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: folders.length,
                itemBuilder: (context, index) {
                  final folder = folders[index];
                  return FolderCard(
                    folder: folder,
                    onTap: () {
                      context.push('/folder/${folder.id}', extra: folder);
                    },
                  );
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
          Icon(Icons.folder_open, size: 64, color: Colors.grey[400]),
          Text(
            AppConstants.emptyFoldersMessage,
            style: Theme.of(
              context,
            ).textTheme.titleMedium?.copyWith(color: Colors.grey[600]),
          ),
          TextButton.icon(
            onPressed: () {
              context.read<FoldersBloc>().add(const RefreshFoldersEvent());
            },
            icon: const Icon(Icons.refresh),
            label: const Text('Refresh'),
          ),
        ],
      ),
    );
  }
}
