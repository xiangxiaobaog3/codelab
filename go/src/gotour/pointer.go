// Package main provides ...
package main1

import (
    "fmt"
)

func zero(x int) {
    x = 0
}

func main() {
    x := 5
    zero(x)
    fmt.Println(x)
}
