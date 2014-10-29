package main1

import (
    "fmt"
    "math"
    "time"
    "runtime"
    "net/http"
)

// closures
// a closures is a function value that references variable from outside body.
func adder() func(int) int {
    sum := 0
    return func(x int) int {
        sum += x
        return sum
    }
}

type Vertex struct {
    X, Y float64
}

type MyFloat float64

func (f MyFloat) Abs() float64 {
    if f < 0 {
        return float64(-f)
    }
    return float64(f)
}

func (v *Vertex) Abs() float64 {
    return math.Sqrt(v.X*v.X + v.Y*v.Y)
}

func fibonacci() func() int {
    i := 0
    j := 1
    s := i + j

    return func() int {
        s = i + j
        i = j
        j = s
        return s
    }
}

type Hello struct {}

func (h Hello) ServeHTTP(
    w http.ResponseWriter,
    r *http.Request) {
        fmt.Fprint(w, "Hello!")
}

// goroutines

func say(s string) {
    for i := 0; i < 5; i ++ {
        time.Sleep(100 * time.Millisecond)
        fmt.Println(s, i)
    }
}



func main() {
    pos, neg := adder(), adder()

    for i := 0; i < 10; i++ {
        fmt.Println(pos(i), neg(-2*i))
    }

    f := fibonacci()

    for i:=0; i<10; i ++ {
        fmt.Println(f())
    }

    fmt.Print("Go runs on ")
    switch os := runtime.GOOS; os {
    case "darwin":
        fmt.Println("OS X.")
    case "linux":
        fmt.Println("Linux.")
    default:
        fmt.Printf("%s.", os)
    }

    v := &Vertex{3, 4}
    fmt.Println(v.Abs())

    f1 := MyFloat(-math.Sqrt2)
    fmt.Println(f1.Abs())

    // say("ABC")
    go say("world")
    say("")
    fmt.Println(f1.Abs())
    time.Sleep(1)
}
