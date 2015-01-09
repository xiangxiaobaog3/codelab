using System;
using System.Collection;

public interface IAccount
{
		void PayInFunds ( decimal amount );
		bool WithdrawFunds ( decimal amount );
		decimal GetBalance ();
		string GetName();
}

public class CustomerAccount : IAccount
{
		private decimal balance = 0;
		private string name;

		public CustomerAccount ( string name, decimal balance )
		{
				name = name;
				balance = balance;
		}

		public virtual bool WithdrawFunds ( decimal amount )
		{
				if (balance < amount)
				{
						return false;
				}
				balance -= amount;
				return true;
		}

		public void PayInFunds ( decimal amount )
		{
				balance += amount;
		}

		public decimal GetBalance()
		{
				return balance;
		}

		public string GetName()
		{
				return name;
		}

}

