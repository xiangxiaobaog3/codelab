// Package main provides ...
package main

import (
    "fmt"
    "net/http"
    "text/template"
)

type MyMux struct {
    
}

func (p *MyMux) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    if r.URL.Path == "/" {
        sayHelloName(w, r)
        return
    }
    http.NotFound(w, r)
    return
}

func sayHelloName(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hello myroute!")
}

func main() {
    // mux := &MyMux{}
    // http.ListenAndServe(":9090", mux)

    t, err := template.New("foo").Parse(`{{ define "T" }}Hello, {{.}}!{{end}}`)
    fmt.Println(t, err)
    // err = t.ExecuteTemplate(out, "T", "<script>alert</script>")
}

