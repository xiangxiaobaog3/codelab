// Package main provides ...
package main

import (
	"fmt"
	"io"
	"net"
	"runtime"
)

type Client struct {
	Incoming chan []byte
	Outgoing chan []byte
	Quit chan bool
	Conn net.Conn
}

func NewClient(conn net.Conn) *Client {
	return &Client{
		Incoming: make(chan []byte),
		Outgoing: make(chan []byte),
		Quit: make(chan bool),
		Conn: conn,
	}
}

func (c *Client) clean() {
	for {
		select {
		case <- c.Quit:
			c.Conn.Close()
		}
	}
}

func (c *Client) Sender(){
	for {
		bytes := <- c.Incoming
		_, err := c.Conn.Write(bytes)
		if err != nil {
			c.Quit <- true
			return
		}
	}
}


func (c *Client) Reader() {
	buf := make([]byte, 8)

	for {
		bytes, err := c.Conn.Read(buf)
		if err != nil {
			if err == io.EOF {
				fmt.Println("client offline")
			} else {
				fmt.Println("read error: ", err)
			}
			c.Quit <- true
			return
		}
		// fmt.Println(buf[0:bytes])
		if bytes > 0 {
			c.Incoming <- buf[0:bytes]
		}
	}

}

func handleClient(conn net.Conn) {
	client := NewClient(conn)

	go client.clean()
	go client.Sender()
	go client.Reader()

}

func main() {
	runtime.GOMAXPROCS(2)
	tcpAddr, _ := net.ResolveTCPAddr("tcp", ":9999")
	listener, _ := net.Listen(tcpAddr.Network(), tcpAddr.String())

	defer listener.Close()

	for {
		conn, _ := listener.Accept()
		go handleClient(conn)
	}

}
