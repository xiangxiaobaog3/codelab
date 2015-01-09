package sort_algor

import (
	"fmt"
)


func GenerateRandomList() []int {
	list := []int{1, 4, 5, 7}
	return list
}


func swap(array []int, i int, j int) {
	array[j], array[i] = array[i], array[j]
}


func BubbleSort(array []int)  {
	length := len(array)
	for i := 0; i < length; i++ {
		for j := i+1; j < length; j ++ {
			if array[i] > array[j] {
				swap(array, i, j)
			}
		}
	}
}

func InsertionSort(array []int) {
	for i := 1; i < len(array); i++ {
		t := array[i]
		j := i - 1
		for (j > -1) {
			if array[j] > t {
				break
			} 
			array[j+1] = array[j]
			j--
		}
		array[j+1] = t
	}
}


func main() {
	list := GenerateRandomList()
	// BubbleSort(list)
	InsertionSort(list)
	fmt.Println(list)
}
