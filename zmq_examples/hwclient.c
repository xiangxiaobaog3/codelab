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
    // socket to talk to server
    //
    printf("connecting to hello world server ...\n");
    void *requester = zmq_socket(context, ZMQ_REQ);
    zmq_connect(requester, "tcp://localhost:5555");

    zmq_close(requester);
    zmq_ctx_destroy(context);

    return 0;
}

