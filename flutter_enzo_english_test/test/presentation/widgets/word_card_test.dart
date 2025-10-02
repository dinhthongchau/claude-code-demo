import 'package:flutter/material.dart';
import 'package:flutter_enzo_english_test/domain/entity/word_entity.dart';
import 'package:flutter_enzo_english_test/presentation/widgets/word_card.dart';
import 'package:flutter_test/flutter_test.dart';

import '../../helpers/test_fixtures.dart';

void main() {
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

    testWidgets('should display part of speech when provided', (tester) async {
      // arrange & act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(body: WordCard(word: tWordEntity1)),
        ),
      );

      // assert
      expect(find.text('noun'), findsOneWidget);
    });

    testWidgets('should display pronunciation when provided', (tester) async {
      // arrange & act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(body: WordCard(word: tWordEntity1)),
        ),
      );

      // assert
      expect(find.text('/ˈæp.əl/'), findsOneWidget);
    });

    testWidgets('should display examples when provided', (tester) async {
      // arrange & act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(body: WordCard(word: tWordEntity1)),
        ),
      );

      // assert
      expect(find.text('Examples:'), findsOneWidget);
      expect(find.text('I ate an apple'), findsOneWidget);
      expect(find.text('Apple pie'), findsOneWidget);
    });

    testWidgets('should display notes when provided', (tester) async {
      // arrange & act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(body: WordCard(word: tWordEntity1)),
        ),
      );

      // assert
      expect(find.text('Common fruit'), findsOneWidget);
      expect(find.byIcon(Icons.note), findsOneWidget);
    });

    testWidgets('should not display notes section when notes is null', (
      tester,
    ) async {
      // arrange & act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(body: WordCard(word: tWordEntity2)),
        ),
      );

      // assert
      expect(find.byIcon(Icons.note), findsNothing);
    });

    testWidgets('should limit examples to first 3', (tester) async {
      // arrange
      final wordWithManyExamples = WordEntity(
        id: tWordEntity1.id,
        word: tWordEntity1.word,
        definition: tWordEntity1.definition,
        examples: const ['Ex 1', 'Ex 2', 'Ex 3', 'Ex 4', 'Ex 5'],
        imageUrls: tWordEntity1.imageUrls,
        partOfSpeech: tWordEntity1.partOfSpeech,
        pronunciation: tWordEntity1.pronunciation,
        notes: tWordEntity1.notes,
        folderId: tWordEntity1.folderId,
        userId: tWordEntity1.userId,
        createdAt: tWordEntity1.createdAt,
        updatedAt: tWordEntity1.updatedAt,
      );

      // act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(body: WordCard(word: wordWithManyExamples)),
        ),
      );

      // assert
      expect(find.text('Ex 1'), findsOneWidget);
      expect(find.text('Ex 2'), findsOneWidget);
      expect(find.text('Ex 3'), findsOneWidget);
      expect(find.text('Ex 4'), findsNothing);
      expect(find.text('Ex 5'), findsNothing);
    });
  });
}
