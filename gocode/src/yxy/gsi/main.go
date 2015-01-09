package main

import (
	"net/http"
	"flag"
	"fmt"
)

func main() {
	var port int
	var path string

	flag.IntVar(&port, "port", 7000, "listen port")
	flag.StringVar(&path, "path", ".", "path to serve")
	flag.Parse()
	fmt.Println("listen on port: ", port, path)
	panic(http.ListenAndServe(fmt.Sprintf(":%d", port),
							  http.FileServer(http.Dir(path))))

}
