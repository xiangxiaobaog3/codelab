// 
// Hello world server
// Expects "Hello" from client, repllies with "World"
//


#include <stdio.h>
#include <unistd.h>
#include <string.h>

#include "zmq.h"


int main (void)
{
    void *context = zmq_ctx_new();

    // socket to talk to clients
    void *responder = zmq_socket(context, ZMQ_REP);
    zmq_bind(responder, "tcp://*:5555");

    while (1) {
        // Wait for next request from client
        zmq_msg_t request;
        zmq_msg_init (&request);
        zmq_msg_recv (&request, responder, 0);
        printf("Received Hello\n");
        zmq_msg_close (&request);

        // Do some work
        sleep(1);

        // Send reply back to clients
        zmq_msg_t reply;
        zmq_msg_init_size (&reply, 5);
        memcpy(zmq_msg_data (&reply), "World", 5);
        zmq_msg_send(&reply, responder, 0);
        zmq_msg_close(&reply);
    }

    // We never get here but if we did, this would be show we end
    zmq_close(responder);
    zmq_ctx_destroy(context);
    return 0;
}