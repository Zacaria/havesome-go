package main

//go:generate sh -c "GOOS=js GOARCH=wasm go build -trimpath -o ../engine.wasm . && cp $(go env GOROOT)/lib/wasm/wasm_exec.js ../wasm_exec.js"

import (
	"bytes"
	"fmt"

	"github.com/traefik/yaegi/interp"
	"github.com/traefik/yaegi/stdlib"
)

// The worker, not this writer, bounds execution time. Keep output bounded too.
type limitedOutput struct {
	bytes.Buffer
	truncated bool
}

func (w *limitedOutput) Write(p []byte) (int, error) {
	n := len(p)
	if n > 16384-w.Len() {
		w.truncated = true
	}
	if left := 16384 - w.Len(); left > 0 {
		if len(p) > left {
			p = p[:left]
		}
		_, _ = w.Buffer.Write(p)
	}
	return n, nil
}

func run(source string) (result string) {
	defer func() {
		if r := recover(); r != nil {
			result = fmt.Sprint("Erreur de l’interpréteur : ", r)
		}
	}()
	var out limitedOutput
	i := interp.New(interp.Options{Stdout: &out, Stderr: &out})
	// No OS, network, syscall or JavaScript packages are exposed to programs.
	allowed := interp.Exports{}
	for _, name := range []string{"fmt/fmt", "errors/errors", "strings/strings", "strconv/strconv", "math/math"} {
		allowed[name] = stdlib.Symbols[name]
	}
	if err := i.Use(allowed); err != nil {
		return "Erreur : " + err.Error()
	}
	_, err := i.Eval(source)
	result = out.String()
	if out.truncated {
		result += "\n[Sortie tronquée à 16 Kio]\n"
	}
	if err != nil {
		result += "Erreur : " + err.Error()
	}
	return result
}
