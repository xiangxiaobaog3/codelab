using System;
using System.Windows.Forms;

delegate void DisplayMessage(string message);

public class TestCustomDelegate
{
		public static void Main()
		{
				DisplayMessage messageTarget;

				if (Enviroment.GetCommandLineArgs().Length > 1)
				{
						messageTarget = ShowWindowsMessage;
				} else 
				{
						messageTarget = Console.WriteLine;
				}

				messageTarget ("Hello word!");
		}

		private static void ShowWindowsMessage(string message)
		{
				MessageBox.Show(message);
		}
}


public class Delegates
{
		delegate void RobotAction();

		RobotAction myRobotAction;


		void Start()
		{
				myRobotAction = RobotWalk;
		}

		void Update()
		{
				myRobotAction();
		}

		public void DoRobotWalk()
		{
				myRobotAction = RobotWalk;
		}

		void RobotWalk()
		{
				Debug.Log("Robot walking");
		}
}
