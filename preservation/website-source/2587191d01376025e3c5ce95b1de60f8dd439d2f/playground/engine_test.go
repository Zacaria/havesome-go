package main

import (
	"strings"
	"testing"
)

func TestRun(t *testing.T) {
	tests := []struct{ name, source, want string }{
		{"sortie", `package main
import "fmt"
func main() { fmt.Println("bonjour") }`, "bonjour\n"},
		{"erreur", `package main
func main() { x := }`, "Erreur :"},
		{"reseau interdit", `package main
import "net/http"
func main() { _, _ = http.Get("https://example.com") }`, "Erreur :"},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := run(tt.source); !strings.Contains(got, tt.want) {
				t.Fatalf("run() = %q, veut %q", got, tt.want)
			}
		})
	}
}
func TestOutputBound(t *testing.T) {
	var w limitedOutput
	s := strings.Repeat("x", 20000)
	n, err := w.Write([]byte(s))
	if n != len(s) || err != nil || w.Len() != 16384 {
		t.Fatal(n, err, w.Len())
	}
}
