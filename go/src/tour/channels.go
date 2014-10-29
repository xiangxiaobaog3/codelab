package main

import (
    "fmt"
    "time"
)

func sum(a []int, c chan int) {
    sum := 0
    for _, v := range a {
        sum += v
        time.Sleep(100 * time.Millisecond)
    }
    c <- sum // send sum to c
}

func main() {
    a := [] int { 7, 2, 8, -9, 4, 0 }
    c := make(chan int)

    go sum(a[:len(a)/2], c)
    // go sum(a[len(a)/2:], c)
    // x, y := <-c, <-c // receive from c
    x := <-c

    fmt.Println(x)
}
