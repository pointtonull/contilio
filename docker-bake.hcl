group "default" {
  targets = ["application"]
}

target "application" {
  context    = "."
  dockerfile = "./Dockerfile"

  tags = [
    "transport:latest"
  ]

  args = {
    SERVICE_DEBUG        = "true"
    SERVICE_ENVIRONMENT  = "ci"
    DB_DSN               = "sqlite+aiosqlite:///./transport_data/transport.db"
  }

  output = ["type=docker"]
}
