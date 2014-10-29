package main1

import (
    "fmt"
    "time"
)

func fibonacci(n int, c chan int) {
    x, y := 0, 1
    for i :=0; i<n; i++ {
        c <- x
        x, y = y, x+y
    }
    close(c)
}

func fib1(c, quit chan int) {
    x, y := 0, 1
    for {
        select {
        case c <- x:
            x, y = y, x+y
        case <-quit:
            fmt.Println("quit")
            return
        }
    }
}

func main() {
    c := make(chan int, 2)
    c <- 1
    c <- 2
    fmt.Println(<-c)
    fmt.Println(<-c)

    ch := make(chan int, 2)
    // go fibonacci(cap(ch), ch)
    fmt.Println("ch", cap(ch))
    go fibonacci(5, ch) // use goroutines

    for i := range ch {
        fmt.Println(i)
    }
    quit := make(chan int)

    go func() {
        for i := 0; i < 10; i++ {
            fmt.Println(<-c)
        }
        quit <- 0
    }()
    fib1(c, quit)

    tick := time.Tick(100 * time.Millisecond)
    boom := time.After(500 * time.Millisecond)
    for {
        select {
        case <- tick:
            fmt.Println("tick.")
        case <- boom:
            fmt.Println("BOOM!")
            return
        default:
            fmt.Println("    .")
            time.Sleep(50 * time.Millisecond)
        }
    }
}
