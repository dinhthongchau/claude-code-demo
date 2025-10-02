import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:flutter_enzo_english_test/domain/entity/word_entity.dart';
import 'package:flutter_enzo_english_test/presentation/widgets/word_card.dart';
import 'package:flutter_test/flutter_test.dart';

import '../../helpers/test_fixtures.dart';

void main() {
  setUpAll(() async {
    // Initialize dotenv with a test value
    dotenv.testLoad(fileInput: '''
BASE_URL=http://localhost:8829
''');
  });

  group('WordCard', () {
    testWidgets('should display word and definition', (tester) async {
      // arrange & act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(body: WordCard(word: tWordEntity1)),
        ),
      );

      // assert
      expect(find.text('apple'), findsOneWidget);
      expect(find.text('A round fruit'), findsOneWidget);
    });

    testWidgets('should display example when provided', (tester) async {
      // arrange & act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(body: WordCard(word: tWordEntity1)),
        ),
      );

      // assert
      expect(find.text('Example:'), findsOneWidget);
      expect(find.text('I ate an apple'), findsOneWidget);
    });

    testWidgets('should not display example section when example is null', (
      tester,
    ) async {
      // arrange
      final wordWithoutExample = WordEntity(
        id: '3',
        wordId: 'test_003',
        word: 'test',
        definition: 'A test word',
        example: null,
        imageUrl: null,
        folderId: '1',
        userId: 'test@example.com',
        createdAt: DateTime(2024, 1, 1),
        updatedAt: DateTime(2024, 1, 1),
      );

      // act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(body: WordCard(word: wordWithoutExample)),
        ),
      );

      // assert
      expect(find.text('Example:'), findsNothing);
    });

    testWidgets('should display image when imageUrl is provided', (
      tester,
    ) async {
      // arrange & act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(body: WordCard(word: tWordEntity1)),
        ),
      );

      // assert
      // Should find an Image widget
      expect(find.byType(Image), findsOneWidget);
    });

    testWidgets('should display placeholder when imageUrl is null', (
      tester,
    ) async {
      // arrange & act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(body: WordCard(word: tWordEntity2)),
        ),
      );

      // assert
      // Should find a placeholder icon
      expect(find.byIcon(Icons.image_outlined), findsOneWidget);
    });
  });
}
