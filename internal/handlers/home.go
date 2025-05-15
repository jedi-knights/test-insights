// internal/handlers/home.go

package handlers

import (
	"fmt"
	"net/http"
)

func Home(w http.ResponseWriter, r *http.Request) {
	// Temporary content for initial setup
	fmt.Fprintln(w, "Welcome to Test Insights!")
}
