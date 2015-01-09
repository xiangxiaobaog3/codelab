package main

import (
    "fmt"
    "net"
    "os"
    "io/ioutil"
)

func main() {
    dotAddr := "192.168.1.1"
    addr := net.ParseIP(dotAddr)

    if addr == nil {
        fmt.Println("Invalid address")
        os.Exit(1)
    }

    mask := addr.DefaultMask()
    network := addr.Mask(mask)
    ones, bits := mask.Size()
    fmt.Println("Address is ", addr.String(),
      " Default mask length is ", bits,
      " Leading ones count is ", ones,
      " Mask is (hex) ", mask.String(),
      " Network is ", network.String())

    // ResolveIP
    // addr1, _ := net.ResolveIPAddr("ip", "g.cn")
    tcpAddr, _ := net.ResolveTCPAddr("tcp4", "baidu.com:80")
    fmt.Println("Resolved address is ", tcpAddr.String())

    addrs, _ := net.LookupHost("web.4399.com")
    for _, s := range addrs {
        fmt.Println(s)
    }

    conn, err := net.DialTCP("tcp", nil, tcpAddr)
    checkError(err)

    _, err = conn.Write([]byte("HEAD / HTTP/1.0\r\n\r\n"))
    checkError(err)

    result, err := ioutil.ReadAll(conn)
    checkError(err)

    fmt.Println(string(result))

    // bind a port and listen at it.
    // w
}

func checkError(err error) {
    if err != nil {
        fmt.Fprintf(os.Stderr, "Fatal error: %s", err.Error())
        os.Exit(1)
    }
}
