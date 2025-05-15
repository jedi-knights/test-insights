# syntax=docker/dockerfile:1

# --- Stage 1: Build ---
FROM golang:1.22 as builder

WORKDIR /app

# Copy go mod and sum files
COPY go.mod ./
COPY go.sum ./
RUN go mod download

# Copy the source code
COPY . .

# Build the application
RUN CGO_ENABLED=0 GOOS=linux go build -o test-insights ./cmd/server

# --- Stage 2: Run ---
FROM alpine:3.19

WORKDIR /app

# Copy the binary from the builder stage
COPY --from=builder /app/test-insights .

# Copy static assets and templates (if needed)
COPY internal/templates ./templates
COPY static ./static

# Expose the default HTTP port
EXPOSE 8080

# Run the binary
ENTRYPOINT ["./test-insights"]
