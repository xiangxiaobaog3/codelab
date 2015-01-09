package main

import (
	"fmt"
	"time"
	"sync"
)


type Job struct {
	i int
	max int
	text string
}

func outputText(j *Job, goGroup *sync.WaitGroup) {
	for j.i < j.max {
		time.Sleep(1 * time.Millisecond)
		fmt.Println(j.text)
		j.i++
	}
	goGroup.Done()
}


func main() {
	goGroup := new(sync.WaitGroup)

	fmt.Println("Starting")

	hello := Job{0, 3, "hello"}
	world := Job{0, 5, "world"}

	go outputText(&hello, goGroup)
	go outputText(&world, goGroup)

	goGroup.Add(2)
	goGroup.Wait()
}
