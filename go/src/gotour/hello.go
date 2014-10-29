package main

import (
    "strconv"
    "fmt"
)

type testInt func(int) bool // 声明一个函数类型

type Element interface{}
type List [] Element

type Person struct {
    name string
    age int
}

func (p Person) String() string {
    return "(name :" + p.name + "- age: " + strconv.Itoa(p.age) + "years)"
}

func isOdd(i int) bool {
    if i % 2 == 0 {
        return false
    }
    return true
}

func isEven(i int) bool {
    if i % 2 == 0 {
        return true
    }
    return false
}

func filter(slice []int, f testInt) [] int {
    var result [] int
    for _, value := range slice {
        if f(value) {
            result = append(result, value)
        }
    }
    return result
}

func fibonacci(c, quit chan int) {
    x, y := 1, 1
    for  {
        select {
        case c<-x:
            x, y = y, x+y
        case <-quit:
            fmt.Println("Quit")
            return
        }
    }
}

func main() {
    fmt.Println("Hello, world")
    // _, b := 34, 35
    for i := 0; i % 2 != 0; i++ {
        fmt.Println(i)
    }

    slice := []int {1, 2, 3, 4, 5, 6, 7}
    fmt.Println("slice = ", slice)
    odd := filter(slice, isOdd)
    fmt.Println("Odd elements of slice are: ", odd)
    even := filter(slice, isEven)
    fmt.Println("Even elements of slice are: ", even)

    list := make(List , 3)
    list[0] = 1
    list[1] = "Hello"
    list[2] = Person{"Dennis", 70}
    for index, element := range list {
        if value, ok := element.(int); ok {
            fmt.Println("int", index, value)
        } else if value, ok := element.(string); ok {
            fmt.Println("string", index, value)
        } else if value, ok := element.(Person); ok {
            fmt.Println("Person", index, value)
        }
        switch value := element.(type) {
        case int:
            fmt.Println("-int", value)
        }
    }

    c := make(chan int)
    quit := make(chan int)

    go func() {
        for i := 0; i < 10; i++ {
            fmt.Println(<-c)
        }
        quit <- 0
    }()

    fibonacci(c, quit)

}
