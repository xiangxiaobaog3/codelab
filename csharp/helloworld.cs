using System;
using System.IO;

enum AccountState { Normal, Freeze };

class HashBank : IBank
{
		Hashtable bankHashtable = new Hashtable();

}

interface IAccount
{
		int GetAccountNumber();
}

struct Account
{
		public AccountState State;
		public string Name;
		public string Address;
		public int AccountNumber;
		public int Balance;
		public int Overdraft;
}

enum TrafficLight 
{
		Red,
		Green
}

public class CustomerAccount: IAccount
{
		private decimal balance = 0;
		public virtual bool WithDrawFunds (decimal amount)
		{
				if (balance < amount)
						return false;
				return true;
		}

		public int GetAccountNumber() 
		{
				return 321;
		}

}

public class AAAAcount: CustomerAccount
{
		public override bool WithDrawFunds (decimal amount)
		{
				return true;
		}
}

class AccountBalance: IAccount
{
		private decimal balance = 0;

		public bool WithDrawFunds( decimal amount )
		{
				if ( balance < amount )
						return false;
				balance -= amount;
				return true;
		}

		public int GetAccountNumber()
		{
				return 123;
		}
}

class HelloWorld
{
		public static void Main()
		{
				AAAAcount a = new AAAAcount();
				Console.WriteLine(a.WithDrawFunds((decimal)10.0));
				Account account;
				account = new Account();
				account.Name = "HEE";
				Console.WriteLine(account.Name);
				TrafficLight light;
				light = TrafficLight.Red;
				Console.WriteLine(light);
		}
}
