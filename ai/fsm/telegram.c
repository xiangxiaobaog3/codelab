struct Telegram
{
    int Sender;
    int Receiver;
    int Msg; // Enumerated in the MessageTypes.h
    double DispatchedTime;
    void* ExtraInfo;
};
