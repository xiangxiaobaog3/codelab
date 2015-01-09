#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <stdio.h>

int main(int argc, char *argv[])
{
    int sock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);
    struct sockaddr_in addr;

    addr.sin_family = AF_INET;
    addr.sin_port = htons(1100);
    addr.sin_addr.s_addr = htonl(INADDR_ANY);

    connect(sock, (struct sockaddr *) &addr, sizeof(addr));

    for (;;) { 
        write(sock, "ping", sizeof("ping"));
        char buf[100];
        read(sock, buf, 100);
        fwrite(buf, 100, 1, stdout);
    }
    return 0;
}
