package examples

import (
	"context"
	"errors"
	"io"
	"strings"
	"testing"
)

func TestCompteur(t *testing.T) {
	if got := exemple(); got != 1 {
		t.Fatalf("got %d", got)
	}
}
func TestCharge(t *testing.T) {
	got, err := charge(strings.NewReader("Go"))
	if err != nil || string(got) != "Go" {
		t.Fatalf("%q %v", got, err)
	}
	_, err = charge(failureReader{})
	if !errors.Is(err, io.ErrUnexpectedEOF) {
		t.Fatalf("%v", err)
	}
}

type failureReader struct{}

func (failureReader) Read([]byte) (int, error) { return 0, io.ErrUnexpectedEOF }
func TestAttendre(t *testing.T) {
	c := make(chan string, 1)
	c <- "go"
	got, err := attendre(context.Background(), c)
	if got != "go" || err != nil {
		t.Fatalf("%q %v", got, err)
	}
	close(c)
	_, err = attendre(context.Background(), c)
	if !errors.Is(err, io.EOF) {
		t.Fatalf("%v", err)
	}
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	_, err = attendre(ctx, make(chan string))
	if !errors.Is(err, context.Canceled) {
		t.Fatalf("%v", err)
	}
}
