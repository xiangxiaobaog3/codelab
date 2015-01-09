// Package main provides ...
package redis

import (
	"bufio"
	"bytes"
	"errors"
	"io"
	"strconv"
)

var (
	arrayPrefixSlice	=	[]byte{'*'}
	bulkStringPrefixSlice = []byte{'$'}
	lineEndingSlice = []byte{'\r', '\n'}
)

type RESPWriter struct {
	*bufio.Writer
}


func NewRESPWriter(writer io.Writer) *RESPWriter {
	return &RESPWriter{
		Writer: bufio.NewWriter(writer),
	}
}

func (w *RESPWriter) WriteCommand(args ...string) (err error) {
	// Write the array prefix and the number of arguments in the array
	w.Write(arrayPrefixSlice)
	w.WriteString(strconv.Itoa(len(args)))
	w.Write(lineEndingSlice)

	for _, arg := range args {
		w.Write(bulkStringPrefixSlice)
		w.WriteString(strconv.Itoa(len(arg)))
		w.Write(lineEndingSlice)
		w.WriteString(arg)
		w.Write(lineEndingSlice)
	}
	
	return w.Flush()
}


// reader
const (
	SIMPLE_STRING = '+'
	BULK_STRING = 's'
	INTEGER = ':'
	ARRAY = '*'
	ERROR = '-'
)

var (
	ErrInvalidSyntax = errors.New("resp:")
)

type RESPReader struct {
	*bufio.Reader
}

func NewReader(reader io.Reader) *RESPReader {
	return &RESPReader{
		Reader: bufio.NewReaderSize(reader, 32*1024), // 32KBytes,
	}
}


func (r *RESPReader) ReadObject() ([]byte, error) {
	line, err := r.readLine()
	if err != nil {
		return nil, err
	}

	switch line[0] {
	case SIMPLE_STRING, INTEGER, ERROR:
		return line, nil
	case BULK_STRING:
		return r.readBulkString(line)
	case ARRAY:
		return r.readArray(line)
	default:
		return nil, ErrInvalidSyntax
	}

}

func (r *RESPReader) readLine() (line []byte, err error){
	line, err = r.ReadSlice('\n')
	if err != nil {
		return nil, err
	}

	if len(line) > 1 && line[len(line)-2] == '\r' {
		return line, nil
	} else {
		// Line was too short or \n wasn't preceded by \r
		return nil, ErrInvalidSyntax
	}
}

func (r *RESPReader) readBulkString(line []byte) ([]byte, error) {
	count, err := r.getCount(line)
	if err != nil {
		return nil, err
	}

	if count == -1 {
		return line, nil
	}

	buf := make([]byte, len(line)+count+2)
	copy(buf, line)
	_, err = r.Read(buf[len(line):])
	if err != nil {
		return nil, err
	}

	return buf, nil
}

func (r *RESPReader) getCount(line []byte) (int, error) {
	end := bytes.IndexByte(line, '\r')
	return strconv.Atoi(string(line[1:end]))
}

func (r *RESPReader) readArray(line []byte) ([]byte, error) {
	count, err := r.getCount(line)
	if err != nil {
		return nil, err
	}

	for i := 0; i < count; i++ {
		buf, err := r.ReadObject()
		if err != nil {
			return nil, err
		}
		line = append(line, buf...)
	}
	return line, nil
}
