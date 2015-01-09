package tcpserver

type Server interface {
	Bind(port int, address string) error
	Listen(port int, address string) error
	Start() error
	Stop() error
}

type TCPServer struct {
}

func (t *TCPServer) Start()  {
}
