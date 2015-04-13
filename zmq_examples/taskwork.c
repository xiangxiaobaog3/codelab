// 
// Task worker
// Connects PULL socket to tcp://localhost:5557
// Connects workloads from ventilator via that socket
// Connects PUSH socket to tcp://localhost:5558
// Sends results to sink via that socket
//

#include "zhelpers.h"


int main(int argc, char *argv[])
{
    void *context = zmq_ctx_new();
    
    // Socket to receive messages on
    void *receiver = zmq_socket(context, ZMQ_PULL);
    zmq_connect(receiver, "tcp://localhost:5557");

    // socket to send messages to
    void *sender = zmq_socket(context, ZMQ_PUSH);
    zmq_connect(sender, "tcp://localhost:5558");

    // Process tasks forever
    while (1) {
        char *string = s_recv(receiver);
        // Simple progress indicator for the viewer
        fflush(stdout);
        printf("%s.", string);

        // Do the work
        s_sleep(atoi(string));
        free(string);

        // Send results to sink.
        s_send(sender, "-");
    }
    zmq_close(receiver);
    zmq_close(sender);
    zmq_ctx_destroy(context);

    return 0;
}
