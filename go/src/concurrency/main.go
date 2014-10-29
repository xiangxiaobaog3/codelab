// Package main provides ...
package main

import (
    "fmt"
    "math/rand"
    "time"
)

func f(n int) {
    for i := 0; i < 10; i++ {
        amt := time.Duration(rand.Intn(250))
        fmt.Println(n, ":", i)
        time.Sleep(time.Millisecond * amt)
    }
}

func ponger(c chan<- string) {
    for i := 0; ; i++ {
        c <- "pong"
    }
}

func pinger(c chan<- string) {
    for i := 0; ; i++ {
        c <- "ping"
    }
}

func printer(c <-chan string) {
    for {
        msg := <- c
        fmt.Println(msg)
        time.Sleep(time.Second * 1)
    }
}

func main() {
    // var c chan string = make(chan string)
    // go pinger(c)
    // go ponger(c)
    // go printer(c)

    // c1 := make(chan string)
    // c2 := make(chan string)

    // go func() {
    //     for {
    //         c1 <- "from 1"
    //         time.Sleep(time.Second * 2)
    //     }
    // }()

    // go func() {
    //     for {
    //         c2 <- "from 2"
    //         time.Sleep(time.Second * 2)
    //     }
    // }()

    // go func() {
    //     for  {
    //         select {
    //         case msg1 := <- c1:
    //             fmt.Println(msg1)
    //         case msg2 := <- c2:
    //             fmt.Println(msg2)
    //         case <- time.After(time.Second):
    //             fmt.Println("timeout")
    //         }
    //     }
    // }()

    c := make(chan int, 1)
    fmt.Println(<-c)
    c <- 10
    fmt.Println("Hello")

    var input string
    fmt.Scanln(&input)
}
