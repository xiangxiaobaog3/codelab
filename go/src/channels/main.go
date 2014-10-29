package main

import (
    "time"
    "fmt"
    "math"
)

func Compose(f, g func(x float64) float64) func(x float64) float64 {
    return func(x float64) float64 {
        return f(g(x))
    }
}

func main() {
    timerChan := make(chan time.Time)
    ch1 := make(chan int)
    ch2 := make(chan int)

    deltaT := 1000 * time.Millisecond

    go func() {
        time.Sleep(deltaT)
        timerChan <- time.Now() // send time on timerChan
        ch1 <- 1
        ch2 <- 2
    }()

    // Do something else; when ready, receive.
    // Receive will block until timerChan delivers.
    // Value sent is other goroutine's completion time.

    fmt.Println("executing ...")

    completedAt := <- timerChan
    fmt.Printf("completedAt %T %v", completedAt, completedAt)

    select {
    case v := <-ch1:
        fmt.Println("channel 1 sends", v)
    case v:= <-ch2:
        fmt.Println("channel 2 sends", v)
    default: // optional
        fmt.Println("neither channel was ready")
    }

    fmt.Println(Compose(math.Sin, math.Cos)(0.5))

}
