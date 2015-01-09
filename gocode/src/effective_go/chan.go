package main

import (
	"fmt"
)

const MaxOutstanding = 100

type Request struct { 
	args []int
	f func([]int) int
	resultChan chan int
}

var sem = make(chan int, MaxOutstanding)

func process(r *Request) {
	fmt.Println("process request")
}

func handle(r *Request) {
	sem <- 1 // wait for active queue to drain
	process(r) // May take a long time.
	<-sem     // Done; enable next request to run.
}

func Serve(queue chan *Request) {
	for {
		req := <-queue
		go handle(req) // Don't wait for handle to finish
	}
}

func Server1(queue chan *Request) {
	for req := range queue {
		sem <- 1
		go func(req *Request) {
			handle(req)
			<-sem
		}(req)
	}
}

func server(workChan <- chan *Work) {
	for work := range workChan {
		go safelyDo(work)
	}
}

func safelyDo(work *Work) {
	defer func() {
		if err := recover(); err != nil {
			log.Println("Work failed: ", err)
		}
	}()
	process(work)
}
