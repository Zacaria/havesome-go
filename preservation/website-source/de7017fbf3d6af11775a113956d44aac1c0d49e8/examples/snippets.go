package examples

import ("context"; "fmt"; "io")

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

func attendre(ctx context.Context, travail <-chan string) (string, error) {
    select {
    case v, ok := <-travail:
        if !ok { return "", io.EOF }
        return v, nil
    case <-ctx.Done():
        return "", ctx.Err()
    }
}
