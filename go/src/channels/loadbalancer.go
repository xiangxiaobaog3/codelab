package main

import (
    "time"
)

type Work struct {
    x, y, z int
}

func worker(in <- chan *Work, out chan <- *Work) {
    for w := range in {
        w.z = w.x * w.y
        time.Sleep(w.z * 100 * time.Millisecond)
        out <- w
    }
}

// channels are first-class values
type Request struct {
    fn func() int // The operation to perform.
    c chan int // The channel to return the result.
}

func requester(work chan<- Request) {
    c := make(chan int)
    for {
        // Kill some time (fake load).
        Sleep(rand.Int63n(nWorker * 2 * Second))
        work <- Request{workFn, c} // send request
    }
}

func Run() {
    in, out := make(chan *Work), make(chan *Work)
    for i:=0; i<NumberWorkers; i++ {
        go worker(in, out)
    }
    go SendLotsOfWork(in)
    receiveLotsOfResults(out)
}
