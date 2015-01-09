using System;

public class Stack<T>
{
	readonly int m_Size;
	int m_StackPointer = 0;
	T[] m_Items;

	public Stack(): this(100) {}

	public Stack(int size)
	{
		m_Size = size;
		m_Items = new T[m_Size];
	}

	public void Push(T item)
	{
		if (m_StackPointer >= m_Size)
			throw new StackOverflowException();
		m_Items[m_StackPointer] = item;
		m_StackPointer++; 
	}

	public T Pop()
	{
		m_StackPointer--;
		if (m_StackPointer >= 0)
		{
			return m_Items[m_StackPointer];
		} else {
			m_StackPointer = 0;
			throw new InvalidOperationException("Cannot pop an empty stack.");
		}
	}
}


public class Node<K,T>
{
		public K Key;
		public T Item;
		public Node<K,T> NextNode;
		public Node()
		{
				Key = default(K);
				Item = default(T);
				NextNode = null;
		}

		public Node(K key, T item, Node<K,T> nextNode)
		{
				Key = key;
				Item = item;
				nextNode = nextNode;
		}
}


public class LinkedList<K,T>
{
		Node<T,K> m_Head;
		public LinkedList()
		{
				m_Head = new Node<K,T>();
		}

		public void AddHead(K key, T item)
		{
				Node<K,T> newNode = new Node<K,T>(key, item, m_Head.NextNode);
				m_Head.NextNode = newNode;
		}
}

public static class HelloGeneric {
		public static void Main()
		{
				Stack<int> stack = new Stack<int>();
				stack.Push(1);

				Stack<string> stacks = new Stack<string>();
				stacks.Push("x");
				// string number = (string)stack.Pop();
		}
}
