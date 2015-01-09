package main

import (
	"fmt"
)

type Queue struct {
	data [100]int;
	head int;
	tail int;
}

func qsort(data []int) {
	if len(data) <= 1 {
		return
	}
	mid, i := data[0], 1
	head, tail := 0, len(data)-1
	for head < tail {
		if data[i] > mid {
			data[i], data[tail] = data[tail], data[i]
			tail--
		} else {
			data[i], data[head] = data[head], data[i]
			head++
			i++
		}
	}
	data[head] = mid
	qsort(data[:head])
	qsort(data[head+1:])
}

func main() {
	li := []int{5, 4, 3, 2, 1}
	qsort(li)
	fmt.Println(li)

	q := new(Queue)
	fmt.Println(q)

}
