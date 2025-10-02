import 'package:flutter/material.dart';
import '../../data/models/folder_model.dart';
import '../../data/api_client.dart';

class FolderCard extends StatefulWidget {
  final Folder folder;

  const FolderCard({
    super.key,
    required this.folder,
  });

  @override
  State<FolderCard> createState() => _FolderCardState();
}

class _FolderCardState extends State<FolderCard> {
  int? wordCount;
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadWordCount();
  }

  Future<void> _loadWordCount() async {
    try {
      final count = await ApiClient.fetchWordCount(widget.folder.id);
      if (mounted) {
        setState(() {
          wordCount = count;
          isLoading = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          wordCount = 0;
          isLoading = false;
        });
      }
    }
  }

  Color _parseColor(String? colorHex) {
    if (colorHex == null || colorHex.isEmpty) {
      return Colors.blue;
    }
    try {
      return Color(int.parse(colorHex.replaceFirst('#', '0xFF')));
    } catch (e) {
      return Colors.blue;
    }
  }

  @override
  Widget build(BuildContext context) {
    final folderColor = _parseColor(widget.folder.color);

    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      elevation: 2,
      child: InkWell(
        onTap: () {
          // Future: Navigate to word list screen
        },
        borderRadius: BorderRadius.circular(4),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              // Folder icon with color
              Container(
                width: 48,
                height: 48,
                decoration: BoxDecoration(
                  color: folderColor.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Center(
                  child: Text(
                    widget.folder.icon ?? '📁',
                    style: const TextStyle(fontSize: 24),
                  ),
                ),
              ),
              const SizedBox(width: 16),

              // Folder details
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      widget.folder.name,
                      style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 4),
                    if (widget.folder.description != null &&
                        widget.folder.description!.isNotEmpty)
                      Text(
                        widget.folder.description!,
                        style: TextStyle(
                          fontSize: 14,
                          color: Colors.grey[600],
                        ),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                    const SizedBox(height: 4),

                    // Word count
                    isLoading
                        ? const SizedBox(
                            width: 80,
                            height: 16,
                            child: LinearProgressIndicator(),
                          )
                        : Text(
                            '$wordCount ${wordCount == 1 ? 'word' : 'words'}',
                            style: TextStyle(
                              fontSize: 14,
                              color: folderColor,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                  ],
                ),
              ),

              // Chevron icon
              Icon(
                Icons.chevron_right,
                color: Colors.grey[400],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
