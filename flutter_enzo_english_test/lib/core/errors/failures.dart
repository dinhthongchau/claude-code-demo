import 'package:equatable/equatable.dart';

/// Base class for all failures in the application
abstract class Failure extends Equatable {
  final String message;

  const Failure(this.message);

  @override
  List<Object?> get props => [message];
}

/// Server-side failure (4xx, 5xx errors)
class ServerFailure extends Failure {
  const ServerFailure(super.message);
}

/// Network connectivity failure
class NetworkFailure extends Failure {
  const NetworkFailure(super.message);
}

/// Cache/local storage failure
class CacheFailure extends Failure {
  const CacheFailure(super.message);
}

/// Generic failure for unexpected errors
class UnexpectedFailure extends Failure {
  const UnexpectedFailure(super.message);
}
