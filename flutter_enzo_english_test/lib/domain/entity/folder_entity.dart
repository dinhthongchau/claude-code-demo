import 'package:equatable/equatable.dart';

class FolderEntity extends Equatable {
  final String id;
  final String name;
  final String description;
  final String userId;
  final DateTime createdAt;
  final DateTime updatedAt;
  final String color;
  final String icon;

  const FolderEntity({
    required this.id,
    required this.name,
    required this.description,
    required this.userId,
    required this.createdAt,
    required this.updatedAt,
    required this.color,
    required this.icon,
  });

  @override
  List<Object?> get props => [
    id,
    name,
    description,
    userId,
    createdAt,
    updatedAt,
    color,
    icon,
  ];
}
