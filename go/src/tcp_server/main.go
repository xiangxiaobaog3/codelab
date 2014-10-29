package main

import (
	"net"
	"os"
	"sync"
	"bufio"
	"fmt"
	"errors"
)

func main() {
	port := "6666"
	tcpAddr, err := net.ResolveTCPAddr("tcp4", ":" + port)
	checkError(err)

	listener, err := net.ListenTCP("tcp", tcpAddr)
	checkError(err)

	for {
		conn, err := listener.Accept()
		if err != nil {
			continue
		}
		go handleClient(conn)
	}

}

type Client struct {
	mu	sync.Mutex
	conn	net.Conn
	bw           *bufio.Writer
	br           *bufio.Reader
}

func (c *Client) Close() {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.conn.Close()
	// unlock
}

func (c *Client) Flush() error {
	return c.bw.Flush()
}

func (c *Client) ReadLine() ([]byte, error) {
	return c.br.ReadSlice('\n')
}

func (c *Client) Write(bytes []byte) (int, error) {
	if n, err := c.bw.Write(bytes); err == nil {
		c.Flush()
		return n, err
	}
	return 0, errors.New("Write failed")
}

func NewClient(conn net.Conn) *Client {
	return &Client{
		conn: conn,
		bw: bufio.NewWriter(conn),
		br: bufio.NewReader(conn),
	}
}

func handleClient(conn net.Conn) {
	client := NewClient(conn)
	defer client.Close()
	for {
		bytes, _ := client.ReadLine()
		client.Write(bytes[0:len(bytes)])
	}
}

func checkError(err error) {
	if err != nil {
		fmt.Fprintf(os.Stderr, "Fata error: %s", err.Error())
		os.Exit(1)
	}
}
