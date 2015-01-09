#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <errno.h>
#include <netinet/in.h>
#include <string.h>

#include <ev.h>


#define PORT 8333
#define BUFFER_SIZE 1024

void accept_cb(struct ev_loop *loop, struct ev_io *watcher, int revents);
void read_cb(struct ev_loop *loop, struct ev_io *watcher, int revents);
static void timeout_cb(EV_P_ ev_timer *w, int revents);

int main(int argc, char *argv[])
{
    struct ev_loop *loop = ev_default_loop(0);
    int sd;
    struct sockaddr_in addr;
    int addr_len = sizeof(addr);
    struct ev_io socket_watcher;
    ev_timer timeout_watcher;

    if ( (sd = socket(PF_INET, SOCK_STREAM, 0)) < 0)
    {
        printf("sock error. errno: %d\n", errno);
        return -1;
    }

    bzero(&addr, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(PORT);
    addr.sin_addr.s_addr =INADDR_ANY;

    if (bind(sd, (struct sockaddr *) &addr, sizeof(addr)) != 0)
    {
        printf("listen error\n");
        return -1;
    }

    printf("ev_loop begin\n");

    // 设置回调函数， 字段等
    ev_io_init(&socket_watcher, accept_cb, sd, EV_READ);
    ev_io_start(loop, &socket_watcher);

    ev_timer_init(&timeout_watcher, timeout_cb, 2, 1);
    ev_timer_start(loop, &timeout_watcher);

    while(1) {
        printf("ev_loop\n");
        ev_loop(loop, 0);
    }

    return 0;
}


void accept_cb(struct ev_loop *loop, struct ev_io *watcher, int revents) 
{
    struct sockaddr_in client_addr;
    socklen_t client_len = sizeof(client_addr);
    int client_sd;

    struct ev_io *w_client = (struct ev_io*) malloc(sizeof(struct ev_io));

    if (EV_ERROR & revents) {
        printf("error event in accept\n");
        return;
    }

    client_sd = accept(watcher->fd, (struct sockaddr *)&client_addr, &client_len);
    if (client_sd < 0) {
        printf("accept error\n");
        return;
    }

    printf("someone connected.\n");
    ev_io_init(w_client, read_cb, client_sd, EV_READ);
    ev_io_start(loop, w_client);
}

void read_cb(struct ev_loop *loop, struct ev_io *watcher, int revents)
{
    char buffer[BUFFER_SIZE];
    ssize_t read;

    if (EV_ERROR & revents) {
        printf("error event in read");
        return;
    }

    read = recv(watcher->fd, buffer, BUFFER_SIZE, 0);
    if (read < 0) {
        printf("read error, errno:%d\n", errno);
        return;
    }

    if (read == 0) {
        printf("someone disconnnected. errno:%d\n", errno);
        ev_io_stop(loop, watcher);
        free(watcher);
        return;
    } else {
        printf("get the message: %s\n", buffer);
    }

    send(watcher->fd, buffer, read, 0);
    bzero(buffer, read);
}

static void timeout_cb(EV_P_ ev_timer *w, int revents) 
{
    puts("timeout");
}
