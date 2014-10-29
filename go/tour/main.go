// Package main provides ...
package main

import (
    "fmt"
    "net/http"
    "strings"
    "log"
)

func sayHelloName(w http.ResponseWriter, r *http.Request) {
    r.ParseForm() // 解析参数
    fmt.Println(r.Form)
    fmt.Println("path", r.URL.Path)
    fmt.Println("schema", r.URL.Scheme)
    fmt.Println(r.Form["url_long"])
    for k, v := range r.Form {
        fmt.Println("Key: ", k)
        fmt.Println("Val: ", strings.Join(v, " "))
    }
    
    fmt.Fprintf(w, "Hello abcdefg")
}

func main() {
    http.HandleFunc("/", sayHelloName)
    err := http.ListenAndServe(":9090", nil)
    if err != nil {
        log.Fatal("ListenAndServe: ", err)
    }
}
