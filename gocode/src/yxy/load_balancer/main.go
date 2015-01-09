package main

import (
	"math/rand"
	"time"
)

type Request struct {
	fn func() int // the operation to perform
	c chan int    // the channel on which to return the result
}


func (w *Work)worke(done chan *Worker) {
	for {
		req := <-w.requests
		req.c <- req.fn()
		done <- w
	}
}

func requester(work chan Request) {
	c := make(chan int)
	nWorker := 3
	for {
		time.Sleep(rand.Int63n(nWorker * 2e9)) // spend
		work <- Request{workFn, c}
		result := <-c
		// futherProcess(result)
	}
}
