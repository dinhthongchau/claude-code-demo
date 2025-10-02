import 'package:flutter/material.dart';
import '../data/models/folder_model.dart';
import '../data/api_client.dart';
import 'widgets/folder_card.dart';

class FoldersScreen extends StatefulWidget {
  const FoldersScreen({super.key});

  @override
  State<FoldersScreen> createState() => _FoldersScreenState();
}

class _FoldersScreenState extends State<FoldersScreen> {
  late Future<List<Folder>> _foldersFuture;

  @override
  void initState() {
    super.initState();
    _foldersFuture = ApiClient.fetchFolders();
  }

  Future<void> _refreshFolders() async {
    setState(() {
      _foldersFuture = ApiClient.fetchFolders();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: FutureBuilder<List<Folder>>(
          future: _foldersFuture,
          builder: (context, snapshot) {
            if (snapshot.hasData) {
              final folderCount = snapshot.data!.length;
              return Text(
                'My Folders ($folderCount ${folderCount == 1 ? 'folder' : 'folders'})',
              );
            }
            return const Text('My Folders');
          },
        ),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: RefreshIndicator(
        onRefresh: _refreshFolders,
        child: FutureBuilder<List<Folder>>(
          future: _foldersFuture,
          builder: (context, snapshot) {
            // Loading state
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(
                child: CircularProgressIndicator(),
              );
            }

            // Error state
            if (snapshot.hasError) {
              return Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(
                      Icons.error_outline,
                      color: Colors.red,
                      size: 64,
                    ),
                    const SizedBox(height: 16),
                    Text(
                      'Error loading folders',
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                    const SizedBox(height: 8),
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 32),
                      child: Text(
                        snapshot.error.toString(),
                        textAlign: TextAlign.center,
                        style: TextStyle(color: Colors.grey[600]),
                      ),
                    ),
                    const SizedBox(height: 16),
                    ElevatedButton.icon(
                      onPressed: _refreshFolders,
                      icon: const Icon(Icons.refresh),
                      label: const Text('Retry'),
                    ),
                  ],
                ),
              );
            }

            // Empty state
            if (!snapshot.hasData || snapshot.data!.isEmpty) {
              return Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(
                      Icons.folder_outlined,
                      size: 64,
                      color: Colors.grey,
                    ),
                    const SizedBox(height: 16),
                    Text(
                      'No folders yet',
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'Pull down to refresh',
                      style: TextStyle(color: Colors.grey[600]),
                    ),
                  ],
                ),
              );
            }

            // Success state - display folders
            final folders = snapshot.data!;
            return ListView.builder(
              itemCount: folders.length,
              itemBuilder: (context, index) {
                return FolderCard(folder: folders[index]);
              },
            );
          },
        ),
      ),
    );
  }
}
