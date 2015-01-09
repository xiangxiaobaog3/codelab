package main

import (
	"fmt"
	"bufio"
	"strings"
)

type Locker interface {
	Lock()
	Unlock()
}

type Mutex int

func (m Mutex) Lock()  {
	fmt.Println("Locking ...")
}

func (m Mutex) Unlock()  {
	fmt.Println("UnLocking ...")
}

type LockedBufferedWriter struct {
	Locker
	bufio.Writer
}

func (l *LockedBufferedWriter) Write(p []byte) (size int, err error) {
	l.Lock()
	defer l.Unlock()
	return l.Writer.Write(p) // inner write
}


func main() {
	// l := Mutex(1)
    //
	// writer := bufio.NewWriter(os.Stdout)
	// lw := LockedBufferedWriter{l, os.Stdout}
	s := bufio.NewScanner(strings.NewReader("(foo 1 'bar')\n(baz 2 'quux')"))
	for s.Scan() {
		tok := s.Bytes()
		fmt.Println("Found token ", tok)
	}

}
