package conn

import (
	"net"
)

type conn struct {
	conn net.Conn
	br          *bufio.Reader
	bw           *bufio.Writer
}
