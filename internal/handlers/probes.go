// internal/handlers/probes.go

package handlers

import (
	"net/http"
)

func LivenessProbe(w http.ResponseWriter, r *http.Request) {
	// Add internal health checks here if needed
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("alive"))
}

func ReadinessProbe(w http.ResponseWriter, r *http.Request) {
	// In real cases, check DB connection or cache readiness here
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("ready"))
}

func StartupProbe(w http.ResponseWriter, r *http.Request) {
	// Optional: used for long init processes (e.g., migrations)
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("started"))
}

