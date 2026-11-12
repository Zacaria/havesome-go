package examples

import ("net/http"; "net/http/httptest"; "testing")

func TestBonjour(t *testing.T) {
    for _, tc := range []struct{ method string; status int; body string }{
        {http.MethodGet, http.StatusOK, "bonjour"},
        {http.MethodPost, http.StatusMethodNotAllowed, "méthode non autorisée\n"},
    } {
        t.Run(tc.method, func(t *testing.T) {
            w := httptest.NewRecorder()
            http.HandlerFunc(bonjour).ServeHTTP(w, httptest.NewRequest(tc.method, "/", nil))
            if w.Code != tc.status || w.Body.String() != tc.body {
                t.Fatalf("got %d %q", w.Code, w.Body.String())
            }
        })
    }
}
