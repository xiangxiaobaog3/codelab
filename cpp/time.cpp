// time.cpp
// Description: A simple time class.
//
#include <iostream>

using namespace std;


class Time {
    private:
        int hours_;
        int minutes_;
        int seconds_;
    public:
        void set(int h, int m, int s) {
            hours_ = h;
            minutes_ = m;
            seconds_ = s;
        }
        void increment(void);
        void display(void);
};


void Time::increment(void) {
    seconds_ ++;
    minutes_ += seconds_/60;
    hours_ += minutes_/60;
    seconds_ %= 60;
    minutes_ %= 60;
    hours_ %= 60;
    return;
}


void Time::display() {
    cout << (hours_ % 12 ? hours_ % 12: 12) << ':' << 
        (minutes_ < 10 ? "0": "") << minutes_ << ':' <<
        (seconds_ < 10 ? "0" : "") << seconds_ << 
        (hours_ < 12 ? " AM" : " PM") << endl;
}


int main() {
    Time timer; 
    timer.set(23, 59, 58);
    timer.increment();
    timer.display();
    cout << endl;
    return 0;
}
