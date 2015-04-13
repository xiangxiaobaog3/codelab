// 
// Task ventilator
// Binds PUSH socket to tcp://localhost:5557
// Sends batch of tasks to workers via that socket
//

#include <unistd.h>

#include "zhelpers.h"

int main(int argc, char *argv[])
{
    void *context = zmq_ctx_new();

    // Socket to send messages on
    void *sender = zmq_socket(context, ZMQ_PUSH);
    zmq_bind(sender, "tcp://*:5557");

    // Socket to send start of batch message on
    void *sink = zmq_socket(context, ZMQ_PUSH);
    zmq_bind(sink, "tcp://localhost:5558");

    printf("Press Enter when the workers are ready: ");
    getchar();
    printf("Sending tasks to workers ...\n");

    // The first message is "0" and signals start of batch
    s_send(sink, "0");

    srandom((unsigned) time(NULL));

    // Send 100 tasks
    int task_nbr;
    int total_msec = 0; // Total expected cost in msec

    int workload;
    for (task_nbr=0; task_nbr<100; task_nbr++) {
        workload = randof(100) + 1;
        total_msec += workload;
        char string[10];
        sprintf(string, "%d", workload);
        s_send(sender, string);
    }

    printf("Total expected cost: %d msec\n", total_msec);
    sleep(1);

    zmq_close(sink);
    zmq_close(sender);
    zmq_ctx_destroy(context);

    return 0;
}
