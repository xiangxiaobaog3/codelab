// Package main provides ...
package main

import (
    "os"
    "io"
    "sync"
    "fmt"
    "log"
    "strconv"
    "net/http"
    "encoding/json"
)

var store = NewURLStore("store.json")
const AddForm = `
<form method="POST" action="/add">
URL: <input type="text" name="url" />
<input type="submit" value="Add" />
</form>
`

type Record struct {
    Key, URL string
}

type URLStore struct {
    urls map[string]string
    mu sync.RWMutex
    // file *os.File
    save chan Record
}

func (s *URLStore) saveLoop(filename string) {
}

func (s *URLStore) load() error {
    if _, err := s.file.Seek(0, 0); err != nil {
        return nil
    }
    d := json.NewDecoder(s.file)
    var err error
    for err == nil {
        var r Record
        if err = d.Decode(&r); err == nil {
            s.Set(r.Key, r.URL)
        }
    }
    if err == io.EOF {
        return nil
    }
    return err
}

// Setter and Getter methods
func (s *URLStore) Get(key string) string {
    s.mu.RLock()
    defer s.mu.RUnlock()
    return s.urls[key]
}

func (s *URLStore) Set(key string, url string) bool{
    // if the key is already present, `Set` returns a boolean `false` value 
    // and the map is not updated
    s.mu.Lock()
    defer s.mu.Unlock()
    _, present := s.urls[key]
    if present {
        return false
    }
    s.urls[key] = url
    // s.save(key, url)
    return true
}

func NewURLStore(filename string) *URLStore {
    s := &URLStore{
        urls: make(map[string]string),
        save: make(chan Record),
    }
    f, _ := os.OpenFile(filename, os.O_RDWR|os.O_CREATE|os.O_APPEND, 0644)
    s.file = f
    if err := s.load(); err != nil {
        log.Println("URLStore: ", err)
    }
    return s
}

func (s *URLStore) Put(url string) string {
    for {
        key := genKey(s.Count())
        if s.Set(key, url) {
            return key
        }
        panic("shouldn't get here")
    }
}

func (s *URLStore) Count() int {
    s.mu.RLock()
    defer s.mu.RUnlock()
    return len(s.urls)
}

func genKey(n int) string {
    return strconv.Itoa(n)
}

func Hello(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hello, world!")
}

func Add(w http.ResponseWriter, r *http.Request) {
    url := r.FormValue("url")
    if url == "" {
        fmt.Fprint(w, AddForm)
        return
    }
    key := store.Put(url)
    fmt.Fprintf(w, "<a href=\"http://localhost:8080/%s>%s</a>\"", key, key)
}

func Redirect(w http.ResponseWriter, r *http.Request) {
    key := r.URL.Path[1:]
    url := store.Get(key)
    // print(url)
    if url == "" {
        http.NotFound(w, r)
        return
    }
    http.Redirect(w, r, url, http.StatusFound)
}


func main() {
    store.Set("a", "http://g.cn")
    store.Set("b", "http://baidu.cn")
    http.HandleFunc("/add", Add)
    http.HandleFunc("/", Redirect)
    http.ListenAndServe(":8080", nil)
}

func shouldEscape(c byte) bool {
    switch c {
    case ' ', '?', '&', '=', '#', '+', '%':
        return true
    }
    return false
}
