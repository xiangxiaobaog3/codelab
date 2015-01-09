#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>


int main(int argc, char *argv[])
{
    int sock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);

    struct sockaddr_in addr;

    addr.sin_family = AF_INET;
    addr.sin_port = htons(1100);
    addr.sin_addr.s_addr = htonl(INADDR_ANY);

    bind(sock, (struct sockaddr *)&addr, sizeof(addr));
    listen(sock, 10);

    for (;;) {
        int new_sock = accept(sock, NULL, NULL);

        char buf[100];
        size_t size = read(new_sock, buf, 100);
        if (size == 0) {
            close(new_sock);
        } else {
            write(new_sock, buf, size);
        }
    }
    return 0;
}
