// Package main provides ...
package main

import (
    "encoding/asn1"
    "fmt"
    "net"
    // "os"
    "time"
    "bytes"
    "encoding/base64"
)

type Person struct {
    Name Name
    Email []Email
}

type Name struct {
    Family  string
    Personal string
}

type Email struct {
    Kind string
    Address string
}


func main() {
    service := ":1200"
    tcpAddr, _ := net.ResolveTCPAddr("tcp", service)
    listener, _ := net.ListenTCP("tcp", tcpAddr)

    eightBitData := []byte{1, 2, 3, 4, 5, 6, 7, 8}
    bb := &bytes.Buffer{}
    encoder := base64.NewEncoder(base64.StdEncoding, bb)
    encoder.Write(eightBitData)
    encoder.Close()
    fmt.Println(bb)


    for  {
        conn, err := listener.Accept()
        if err != nil {
            continue
        }
        daytime := time.Now()
        mdata, _ := asn1.Marshal(daytime)
        conn.Write(mdata)
        conn.Close()
    }
}
