package main

import (
    "bytes"
    "fmt"
    "io"
    "net"
    // "os"
)

func main() {
    addr, _ := net.ResolveIPAddr("ip", "localhost")

    conn, _ := net.DialIP("ip4", addr, addr)

    var msg[512]byte

    msg[0] = 8 // echo
    msg[1] = 0 // code 0
    msg[2] = 0 // checksum, fix later
    msg[3] = 0 // checksum, fix later
    msg[4] = 0 // identifier[0]
    msg[5] = 13 // identifier[1]
    msg[6] = 0 // sequence[0]
    msg[7] = 37 // sequence[1]

    length := 8
    check := checkSum(msg[0:length])
    msg[2] = byte(check >> 8)
    msg[3] = byte(check & 255)
    conn.Write(msg[0:length])
    conn.Read(msg[0:])
    fmt.Println("Got reponse")
    if msg[5] == 13 {
        fmt.Println("identifier matches")
    }
    if msg[7] == 37 {
        fmt.Println("Sequence matches")
    }
}

func checkSum(msg []byte) uint16 {
    sum := 0
    // assume even for now
    for i := 1; i < len(msg) - 1; i += 2 {
        sum += int(msg[i])*256 + int(msg[i+1])
    }
    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)
    var answer uint16 = uint16(^sum)
    return answer
}

func readFully(conn net.Conn) ([]byte, error) {
    defer conn.Close()

    result := bytes.NewBuffer(nil)
    var buf [512]byte
    for  {
        n, err := conn.Read(buf[0:])
        result.Write(buf[0:n])
        if err != nil {
            if err == io.EOF {
                break
            }
            return nil, err
        }
    }
    return result.Bytes(), nil
}
