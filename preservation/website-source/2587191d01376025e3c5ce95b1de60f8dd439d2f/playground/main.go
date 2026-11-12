//go:build js && wasm

package main

import "syscall/js"

func main() {
	js.Global().Set("runGo", js.FuncOf(func(_ js.Value, args []js.Value) any {
		if len(args) != 1 {
			return "Erreur : programme manquant."
		}
		return run(args[0].String())
	}))
	select {}
}
