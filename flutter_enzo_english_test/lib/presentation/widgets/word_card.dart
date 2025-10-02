import 'package:flutter/material.dart';
import 'package:flutter_enzo_english_test/core/api/api_config.dart';
import 'package:flutter_enzo_english_test/domain/entity/word_entity.dart';

/// Simplified word card for displaying essential word information
/// Shows: word title, definition, single example, and optional image
class WordCard extends StatelessWidget {
  final WordEntity word;

  const WordCard({super.key, required this.word});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surface,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: Theme.of(context).colorScheme.outline.withValues(alpha: 0.2),
          width: 1,
        ),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          spacing: 8,
          children: [
            // Word title
            Row(
              children: [
                Expanded(
                  child: Text(
                    word.word,
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(
                          fontWeight: FontWeight.bold,
                          color: Theme.of(context).colorScheme.primary,
                        ),
                  ),
                ),
                // Image thumbnail
                if (word.imageUrl != null)
                  ClipRRect(
                    borderRadius: BorderRadius.circular(8),
                    child: Image.network(
                      '${ApiConfig.getBaseUrl()}/api/v1/global/words/${word.wordId}/image',
                      width: 60,
                      height: 60,
                      fit: BoxFit.cover,
                      errorBuilder: (context, error, stackTrace) {
                        return Container(
                          width: 60,
                          height: 60,
                          decoration: BoxDecoration(
                            color: Colors.grey[200],
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Icon(
                            Icons.image_outlined,
                            color: Colors.grey[400],
                            size: 30,
                          ),
                        );
                      },
                    ),
                  )
                else
                  Container(
                    width: 60,
                    height: 60,
                    decoration: BoxDecoration(
                      color: Colors.grey[200],
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Icon(
                      Icons.image_outlined,
                      color: Colors.grey[400],
                      size: 30,
                    ),
                  ),
              ],
            ),
            // Divider
            const Divider(),
            // Definition
            Text(
              word.definition,
              style: Theme.of(context).textTheme.bodyMedium,
            ),
            // Example
            if (word.example != null && word.example!.isNotEmpty) ...[
              const SizedBox(height: 8),
              Text(
                'Example:',
                style: Theme.of(context).textTheme.bodySmall?.copyWith(
                      fontWeight: FontWeight.bold,
                      color: Colors.grey[700],
                    ),
              ),
              const SizedBox(height: 4),
              Padding(
                padding: const EdgeInsets.only(left: 8),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  spacing: 8,
                  children: [
                    Text(
                      '•',
                      style: Theme.of(context).textTheme.bodySmall,
                    ),
                    Expanded(
                      child: Text(
                        word.example!,
                        style: Theme.of(context).textTheme.bodySmall?.copyWith(
                              fontStyle: FontStyle.italic,
                              color: Colors.grey[700],
                            ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
