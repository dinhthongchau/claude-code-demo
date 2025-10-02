import 'package:flutter/material.dart';
import 'package:flutter_enzo_english_test/presentation/widgets/folder_card.dart';
import 'package:flutter_test/flutter_test.dart';

import '../../helpers/test_fixtures.dart';

void main() {
  group('FolderCard', () {
    testWidgets('should display folder name and description', (tester) async {
      // act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: FolderCard(
              folder: tFolderEntity1,
              onTap: () {},
            ),
          ),
        ),
      );

      // assert
      expect(find.text('Test Folder 1'), findsOneWidget);
      expect(find.text('Test description 1'), findsOneWidget);
      expect(find.text('📁'), findsOneWidget);
    });

    testWidgets('should handle tap events', (tester) async {
      // arrange
      var tapped = false;

      // act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: FolderCard(
              folder: tFolderEntity1,
              onTap: () => tapped = true,
            ),
          ),
        ),
      );

      await tester.tap(find.byType(InkWell));
      await tester.pump();

      // assert
      expect(tapped, true);
    });

    testWidgets('should display icon from folder entity', (tester) async {
      // arrange & act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: FolderCard(folder: tFolderEntity2, onTap: () {}),
          ),
        ),
      );

      // assert
      expect(find.text('📚'), findsOneWidget);
    });

    testWidgets('should show chevron icon', (tester) async {
      // arrange & act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: FolderCard(folder: tFolderEntity1, onTap: () {}),
          ),
        ),
      );

      // assert
      expect(find.byIcon(Icons.chevron_right), findsOneWidget);
    });
  });
}
