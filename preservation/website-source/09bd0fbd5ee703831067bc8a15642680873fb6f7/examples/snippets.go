package examples

import ("context"; "fmt"; "io"; "net/http")

type Compteur struct { N int }

func (c *Compteur) Incr() { c.N++ }

func exemple() int {
    c := Compteur{} // valeur zéro utilisable
    c.Incr()
    return c.N
}

func charge(r io.Reader) ([]byte, error) {
    data, err := io.ReadAll(r)
    if err != nil {
        return nil, fmt.Errorf("lire la réponse : %w", err)
    }
    return data, nil
}

func bonjour(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodGet {
        http.Error(w, "méthode non autorisée", http.StatusMethodNotAllowed)
        return
    }
    w.Header().Set("Content-Type", "text/plain; charset=utf-8")
    fmt.Fprint(w, "bonjour")
}

func attendre(ctx context.Context, travail <-chan string) (string, error) {
    select {
    case v, ok := <-travail:
        if !ok { return "", io.EOF }
        return v, nil
    case <-ctx.Done():
        return "", ctx.Err()
    }
}
