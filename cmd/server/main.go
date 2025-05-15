// cmd/server/main.go

package main

import (
	"log"
	"net/http"

	"github.com/jedi-knights/test-insights/internal/handlers"
)

func main() {
	mux := http.NewServeMux()

	// App routes
	mux.HandleFunc("/", handlers.Home)
	mux.HandleFunc("/testcases", handlers.ListTestCases)

	// Kubernetes probes
	mux.HandleFunc("/healthz", handlers.LivenessProbe)
	mux.HandleFunc("/readyz", handlers.ReadinessProbe)
	mux.HandleFunc("/startupz", handlers.StartupProbe)

	log.Println("Starting server on :8080")
	err := http.ListenAndServe(":8080", mux)
	if err != nil {
		log.Fatalf("Server failed: %s", err)
	}
}
