package main

import (
    "net"
    // "fmt"
    "bufio"
)


// 这是一个聊天室
// 熟悉goroutine是用chan来通讯的

type Client struct {
    incoming chan string
    outgoing chan string
    writer *bufio.Writer
    reader *bufio.Reader
}

func (c *Client) Read() {
    // 从socket读内容
    for {
        line, _ := c.reader.ReadString('\n')
        c.incoming <- line
    }
}

func (c *Client) Write() {
    for data := range c.outgoing {
        c.writer.WriteString(data)
        c.writer.Flush()
    }
}

func (c *Client) Listen() {
    go c.Read()
    go c.Write()
}

func NewClient(conn net.Conn) *Client {
    client := &Client{
        make(chan string),
        make(chan string),
        bufio.NewWriter(conn),
        bufio.NewReader(conn),
    }
    client.Listen()
    return client
}


type ChatRoom struct {
    clients []*Client
    joins chan net.Conn
    incoming chan string
    outgoing chan string
}


func (chatRoom *ChatRoom) Broadcast(data string) {
    // 广播所有的消息
    for _, client := range chatRoom.clients {
        client.outgoing <- data
    }
}

func (chatRoom *ChatRoom) Join(conn net.Conn) {
    // 新连接一个客户端
    client := NewClient(conn)
    chatRoom.clients = append(chatRoom.clients, client)
    go func() {
        for {
            chatRoom.outgoing <- <- client.incoming
        }
    }()
}

func (chatRoom *ChatRoom) Listen() {
    go func() {
        for {
            select {
            case data := <- chatRoom.outgoing:
                chatRoom.Broadcast(data)
            case conn := <- chatRoom.joins:
                chatRoom.Join(conn)
            }
        }
    }()
}

func NewChatRoom() *ChatRoom {
    chatRoom := &ChatRoom{
        make([]*Client, 0),
        make(chan net.Conn),
        make(chan string),
        make(chan string),
    }
    chatRoom.Listen()
    return chatRoom
}

func main() {
    chatRoom := NewChatRoom()

    ln, _ := net.Listen("tcp", ":6666")
    for {
        conn, _ := ln.Accept()
        chatRoom.joins <- conn
    }
}
