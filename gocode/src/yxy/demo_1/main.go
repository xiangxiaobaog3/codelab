// Package main provides ...
package main

import (
    "fmt"
    "bytes"
    "sort"
    "errors"
    "container/list"
)

type Person struct {
    Name string
    Age int
}

type ByName []Person

func (this ByName) Len() int {
    return len(this)
}

func (this ByName) Less(i, j int) bool {
    return this[i].Name < this[j].Name
}

func (this ByName) Swap(i, j int) {
    this[i], this[j] = this[j], this[i]
}


func main() {
    var buf bytes.Buffer
    // test_file()
    buf.Write([]byte("test"))
    err := errors.New("error message")
    fmt.Println(err)

    var x list.List
    x.PushBack(1)
    x.PushBack(2)
    x.PushBack(3)

    for e := x.Front(); e != nil; e=e.Next() {
        // fmt.Println(e.Value())
        fmt.Println(e.Value.(int))
    }

    kids := []Person{
        {"Jill", 9},
        {"Jack", 10},
    }
    sort.Sort(ByName(kids))
    fmt.Println(kids)
}
