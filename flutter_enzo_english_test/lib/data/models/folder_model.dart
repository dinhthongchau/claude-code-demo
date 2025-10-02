class Folder {
  final String id;
  final String name;
  final String? description;
  final String userId;
  final DateTime createdAt;
  final DateTime updatedAt;
  final String? color;
  final String? icon;

  Folder({
    required this.id,
    required this.name,
    this.description,
    required this.userId,
    required this.createdAt,
    required this.updatedAt,
    this.color,
    this.icon,
  });

  factory Folder.fromJson(Map<String, dynamic> json) {
    return Folder(
      id: json['id'],
      name: json['name'],
      description: json['description'],
      userId: json['user_id'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
      color: json['color'],
      icon: json['icon'],
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
}
