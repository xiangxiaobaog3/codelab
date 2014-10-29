// Package main provides ...
package main

import (
    "fmt"
    "os"
    "time"
    "math"
    "math/rand"
)

type Shape interface {
    area() float64
}

type Android struct {
    Person
    Model string
}

type Person struct {
    Name string
}

func (p  *Person) Talk() {
    fmt.Println("Hi, my name is", p.Name)
}

type Circle struct {
    x, y, r float64
}

// interfaces can also be used as fields
type MultiShape struct {
    shapes []Shape
}

func (m *MultiShape) area() float64 {
    var area float64
    for _, s := range m.shapes {
        area += s.area()
    }
    return area
}


func swap(x *int, y *int) {
    n := *x
    *x = *y
    *y = n
}

func one(xPtr *int) {
    *xPtr = 1
}

func zero(x *int) {
    *x = 0
}

func fib(n int) int {
    if n == 0 {
        return 0
    }
    if n == 1 {
        return 1
    }
    return fib(n - 1) + fib(n - 2)
}

func makeOddGenerator() func() uint {
    i := uint(0)
    return func() uint {
        i += 1
        if i % 2 == 0 {
            i += 1
        }
        return i
    }
}

func half(n int) (int, bool) {
    if x := n % 2; x == 0 {
        return n/2, true
    }
    return 0, false
}

func first() {
    print("1st")
}

func second() {
    print("2st")
}

func factorial(x uint) uint {
    if x == 0 {
        return 1
    }
    return x * factorial(x-1)
}

func makeEvenGenerator() func() uint {
    i := uint(0)
    return func() (ret uint) {
        ret = i
        i += 2
        return
    }
}

func add(args ...int) int {
    total := 0
    for _, v := range args {
        total += v
    }
    return total
}

func findSmallest(li []int) int {
    s := li[0]
    for _, v := range li[1:] {
        if v < s {
            s = v
        }
    }
    return s
}

func boring(msg string, c chan string) {
    for i := 0; ; i++ {
        fmt.Printf("%s %d", msg, i)
        time.Sleep(time.Duration(rand.Intn(1e3)) * time.Millisecond)
    }
}

func main() {

    slice1 := []int{1, 2, 3}
    slice2 := make([]int, 2, 4)

    copy(slice2, slice1)
    fmt.Println(slice1, slice2)

    elements := map[string]string {
        "H": "Hydrogen",
        "He": "Helium",
        "Li": "Lithum",
    }

    fmt.Println(elements)
    fmt.Println(findSmallest([]int{10, 0, 1, 2, 3,}))
    fmt.Println(add(1, 2, 3))
    xs := []int{1, 2, 3}
    fmt.Println(add(xs...))
    x := 0
    increment := func() int {
        x += 1
        return x
    }
    increment()
    increment()
    increment()
    fmt.Println(x)

    nextEven := makeEvenGenerator()
    fmt.Println(nextEven())
    fmt.Println(nextEven())
    fmt.Println(nextEven())
    fmt.Println(factorial(5))
    // fmt.Println(add([]int{1, 2, 3}))
    // c := make(chan string)
    // go boring("boring!", c)
    // for i := 0; i < 5; i++ {
    //     fmt.Printf("You say: %q\n", <-c) // Receive expression is just a value
    // }
    // fmt.Println("Your're boring. I'm leaving.")

    f, _ := os.Open("main.go")
    defer f.Close()

    // fmt.Println(half(1))
    // fmt.Println(half(2))
    // oddNext := makeOddGenerator()
    // fmt.Println(oddNext())
    // fmt.Println(oddNext())
    // print(fib(6))
    print("***")

    xx := 5
    zero(&xx)
    fmt.Println(xx)

    xPtr := new(int) // new takes 
    // fmt.Printf("%T %v", xPtr, xPtr)
    one(xPtr)
    n1, n2 := 1, 2
    swap(&n1, &n2)
    fmt.Println(n1, n2)

    c := Circle{x:0, y:0, r:5}
    fmt.Println(circleArea(&c))
    fmt.Println(c.area())

    a := new(Android)
    a.Person.Talk()

    a.Talk()
}

func totalArea(shapes ...Shape) float64 {
    var area float64
    for _, s := range shapes {
        area += s.area()
    }
    return area
}

func circleArea(c *Circle) float64 {
    return math.Pi * c.r*c.r
}

func (c *Circle) area() float64 {
    return math.Pi * c.r*c.r
}
