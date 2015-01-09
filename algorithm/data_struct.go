package data_struct

type Stack struct {
	data [] int;
}

func (s *Stack) Pop() int {
	x, s := s[len(s)-1], s[:len(s)-1]
	return x
}

func (s *Stack) Push(d int)  {
	append(data, d)
}
