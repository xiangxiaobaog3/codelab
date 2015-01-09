package main

import (
	"io"
	"fmt"
	"log"
	"bytes"
	"net/http"
	"encoding/binary"
)

type Gopher struct {
	Name string
	AgeYears int
}

type binWriter struct {
	w	io.Writer
	buf	bytes.Buffer
	err		error
}

func (w *binWriter) Flush() (int64, error) {
	if w.err != nil {
		return 0, w.err
	}
	return w.buf.WriteTo(w.w)
}

func (w *binWriter) Write(v interface{}) {
	if w.err != nil {
		return
	}

	switch x := v.(type) {
	case string:
		w.Write(int32(len(x))) // 4 byte to store string length
		w.Write([]byte(x))
	case int:
		w.Write(int64(x))
	default:
		w.err = binary.Write(&w.buf, binary.LittleEndian, v)
	}
}

func (g *Gopher) WriteTo(w io.Writer) (int64, error) {
	bw := &binWriter{w: w}
	bw.Write(g.Name)
	bw.Write(g.AgeYears)
	return bw.Flush()
}

func main() {
	buf := bytes.NewBuffer(nil)
	g := Gopher{"abcdefg", 12000010101}
	size, err := g.WriteTo(buf)
	fmt.Println(size, err, buf.Bytes())
}


func init() {
	http.HandleFunc("/", errorHandler(betterHandler))
}

func errorHandler(f func(w http.ResponseWriter, r *http.Request) error) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		err := f(w, r)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			log.Printf("Handling %q: %v", r.RequestURI, err)
		}
	}
}

func betterHandler(w http.ResponseWriter, r *http.Request) error {
	if err := doThis(); err != nil {
		return fmt.Errorf("doing this: %v", err)
	}

	if err := doThat(); err != nil {
		return fmt.Errorf("doing that: %v", err)
	}
	return nil
}

func doThis() error {
	return nil
}

func doThat() error {
	return nil
}
