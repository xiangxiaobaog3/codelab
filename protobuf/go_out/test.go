package main

import (
	"os"
	"fmt"
)

type ByteSlice []byte
type ByteSize float64
type Sequence [] int

func (p *ByteSlice) Append(data []byte)(n int, err error) {
	return len(data), err
}

const (
	_ = iota // igonre first value by assaigning to blank identifier
	KB ByteSize = 1 << (10 * iota)
	MB
	GB
	TB
	PB
	EB
	ZB
	YB
)

func functionsOfSomeType() int {
	return 1
	
}

type T struct {
	a int
	b uint
}

func main() {
	var t interface{}
	t = functionsOfSomeType()
	switch t := t.(type) {
	default:
		fmt.Printf("unexpected type %T", t)
	case bool:
		fmt.Printf("boolean %t\n", t)
	case int:
		fmt.Printf("integer %d\n", t)
	}

	a := []int{1, 2, 3}
	a = append(a, 4, 5)
	print(cap(a))
	print(len(a))

	var timeZone = map[string] int {
		"UTC": 0*60*60,
		"EST": -5*60*60,
	}

	fmt.Println(timeZone)

	var b int = 2 << 31
	fmt.Println(b, " <<")

	_, t1 := timeZone["FFF"]
	fmt.Println(t1)
	ts := &T{10, 10}
	fmt.Println("a=", ts.a)
	fmt.Printf("  %+v\n", ts)
	fmt.Printf("  %+v\n", b)

	fmt.Println(KB, MB, GB, TB, PB)
	
	var (
		home = os.Getenv("HOME")
		// user = os.Getenv("USER")
	)
	fmt.Println(home)
	cc := ByteSlice{78, 99}
	fmt.Println(cc)
	// c := make([]ByteSlice{"AB"})
	// // c.Append(make([]byte{"C", "D"}))
	// fmt.Println(c)
	te := Sequence{1, 2, 3}
	fmt.Println(te)

}
