package main

import (
    "fmt"
    "net"
    "os"
    "time"
)

func main() {
    service := ":2200"
    tcpAddr, err := net.ResolveTCPAddr("tcp4", service)
    checkError(err)

    listener, err := net.ListenTCP("tcp", tcpAddr)
    checkError(err)

    for  {
        conn, err := listener.Accept()
        if err != nil {
            continue
        }

        showTime(conn)
        conn.SetTimeout(10)
        go echo(conn)

        // conn.Close()
    }
}

func showTime(conn net.Conn) {
    daytime := time.Now().String()
    conn.Write([]byte(daytime))
}

func echo(conn net.Conn) {
    var buf [512]byte
    defer conn.Close()

    for  {
        n, err := conn.Read(buf[0:])
        if err != nil {
            return
        }
        fmt.Println(string(buf[0:]))
        _, err2 := conn.Write([]byte("> " + string(buf[0:n])))
        if err2 != nil {
            return
        }
    }

}

func checkError(err error){
    if err != nil {
        fmt.Fprintf(os.Stderr, "Fatal error: %s\n", err.Error())
        os.Exit(1)
    }
}
