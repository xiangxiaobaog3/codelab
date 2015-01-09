// Package main provides ...
package main

import (
    "net/rpc"
    "fmt"
)

type Args struct {
    A, B int
}

type Quotient struct {
    Quo, Rem int
}

func main() {
    serverAddress := "127.0.0.1:1234"

    client, err := rpc.DialHTTP("tcp", serverAddress)
    fmt.Println(err)

    var reply int
    args := Args{17, 8}
    client.Call("Arith.Multiply", args, &reply)
    client.Call("Arith.XX", args, &reply)
    fmt.Println(reply)
    fmt.Printf("Arith: %d*%d=%d\n", args.A, args.B, reply)

    var quot Quotient
    client.Call("Arith.Divide", args, &quot)

    fmt.Printf("Arith: %d/%d=%d remainder %d\n", args.A, args.B, quot.Quo, quot.Rem)
}
