import 'package:flutter_enzo_english_test/domain/entity/folder_entity.dart';

class FolderModel extends FolderEntity {
  const FolderModel({
    required super.id,
    required super.name,
    required super.description,
    required super.userId,
    required super.createdAt,
    required super.updatedAt,
    required super.color,
    required super.icon,
  });

  factory FolderModel.fromJson(Map<String, dynamic> json) {
    return FolderModel(
      id: json['id'] as String,
      name: json['name'] as String,
      description: json['description'] as String? ?? '',
      userId: json['user_id'] as String,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
      color: json['color'] as String? ?? '#2196F3',
      icon: json['icon'] as String? ?? '📁',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'description': description,
      'user_id': userId,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
      'color': color,
      'icon': icon,
    };
  }

  FolderEntity toEntity() {
    return FolderEntity(
      id: id,
      name: name,
      description: description,
      userId: userId,
      createdAt: createdAt,
      updatedAt: updatedAt,
      color: color,
      icon: icon,
    );
  }
}
